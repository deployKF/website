# Access Kubeflow Pipelines API

This guide explains how to access the _Kubeflow Pipelines API_ with the _Kubeflow Pipelines Python SDK_ and __authenticate with deployKF__.

---

## Overview

As described in the [User Authentication Admin Guide](../guides/platform/deploykf-authentication.md), deployKF uses [Dex](https://github.com/dexidp/dex) and [Oauth2 Proxy](https://github.com/oauth2-proxy/oauth2-proxy) for user authentication.

To use the [Kubeflow Pipelines Python SDK](https://kubeflow-pipelines.readthedocs.io/), you will need to authenticate with Dex to obtain an Oauth2 Proxy session cookie, and then use that cookie to access the Kubeflow Pipelines API.

Depending on where you are running the Kubeflow Pipelines Python SDK, different authentication methods are available.

Authentication Method | In Cluster | Outside Cluster
--- | :---: | :---:
[Dex Credentials](#authenticate-with-dex-credentials) | :octicons-check-16: | :octicons-check-16:
[Kubernetes Service Account Token](#authenticate-with-kubernetes-serviceaccount-token) | :octicons-check-16: | :octicons-x-16:

## Authenticate with Dex Credentials

To authenticate the Kubeflow Pipelines Python SDK with Dex credentials, you may use the following Python code.

First, we define a `KFPClientManager()` class that creates authenticated `kfp.Client()` instances when `create_kfp_client()` is called:

```python
import re
from urllib.parse import urlsplit

import kfp
import requests
import urllib3


class KFPClientManager:
    """
    A class that creates `kfp.Client` instances with Dex authentication.
    """

    def __init__(
        self,
        api_url: str,
        dex_username: str,
        dex_password: str,
        dex_auth_type: str = "local",
        skip_tls_verify: bool = False,
    ):
        """
        Initialize the KfpClient

        :param api_url: the Kubeflow Pipelines API URL
        :param skip_tls_verify: if True, skip TLS verification
        :param dex_username: the Dex username
        :param dex_password: the Dex password
        :param dex_auth_type: the auth type to use if Dex has multiple enabled, one of: ['ldap', 'local']
        """
        self._api_url = api_url
        self._skip_tls_verify = skip_tls_verify
        self._dex_username = dex_username
        self._dex_password = dex_password
        self._dex_auth_type = dex_auth_type
        self._client = None

        # ensure `dex_default_auth_type` is valid
        if self._dex_auth_type not in ["ldap", "local"]:
            raise ValueError(
                f"Invalid `dex_auth_type` '{self._dex_auth_type}', must be one of: ['ldap', 'local']"
            )

    def _get_session_cookies(self) -> str:
        """
        Get the session cookies by authenticating against Dex
        :return: a string of session cookies in the form "key1=value1; key2=value2"
        """

        # use a persistent session (for cookies)
        s = requests.Session()

        # disable SSL verification, if requested
        if self._skip_tls_verify:
            s.verify = False
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        # GET the api_url, which should redirect to Dex
        resp = s.get(self._api_url, allow_redirects=True)
        if resp.status_code != 200:
            raise RuntimeError(
                f"HTTP status code '{resp.status_code}' for GET against: {self._api_url}"
            )

        # if we were NOT redirected, then the endpoint is unsecured
        if len(resp.history) == 0:
            # no cookies are needed
            return ""

        # if we are at `/auth?=xxxx` path, we need to select an auth type
        url_obj = urlsplit(resp.url)
        if re.search(r"/auth$", url_obj.path):
            url_obj = url_obj._replace(
                path=re.sub(r"/auth$", f"/auth/{self._dex_auth_type}", url_obj.path)
            )

        # if we are at `/auth/xxxx/login` path, then we are at the login page
        if re.search(r"/auth/.*/login$", url_obj.path):
            dex_login_url = url_obj.geturl()
        else:
            # otherwise, we need to follow a redirect to the login page
            resp = s.get(url_obj.geturl(), allow_redirects=True)
            if resp.status_code != 200:
                raise RuntimeError(
                    f"HTTP status code '{resp.status_code}' for GET against: {url_obj.geturl()}"
                )
            dex_login_url = resp.url

        # attempt Dex login
        resp = s.post(
            dex_login_url,
            data={"login": self._dex_username, "password": self._dex_password},
            allow_redirects=True,
        )
        if resp.status_code != 200:
            raise RuntimeError(
                f"HTTP status code '{resp.status_code}' for POST against: {dex_login_url}"
            )

        # if we were NOT redirected, then the login credentials were probably invalid
        if len(resp.history) == 0:
            raise RuntimeError(
                f"Login credentials are probably invalid - "
                f"No redirect after POST to: {dex_login_url}"
            )

        return "; ".join([f"{c.name}={c.value}" for c in s.cookies])

    def _create_kfp_client(self) -> kfp.Client:
        try:
            session_cookies = self._get_session_cookies()
        except Exception as ex:
            raise RuntimeError(f"Failed to get Dex session cookies") from ex

        # monkey patch the kfp.Client to support disabling SSL verification
        # kfp only added support in v2: https://github.com/kubeflow/pipelines/pull/7174
        original_load_config = kfp.Client._load_config

        def patched_load_config(client_self, *args, **kwargs):
            config = original_load_config(client_self, *args, **kwargs)
            config.verify_ssl = not self._skip_tls_verify
            return config

        patched_kfp_client = kfp.Client
        patched_kfp_client._load_config = patched_load_config

        return patched_kfp_client(
            host=self._api_url,
            cookies=session_cookies,
        )

    def create_kfp_client(self) -> kfp.Client:
        """Get a newly authenticated Kubeflow Pipelines client."""
        return self._create_kfp_client()
```

Next, we use the `KFPClientManager()` class to create an authenticated `kfp.Client()`:

```python
# initialize a KFPClientManager
kfp_client_manager = KFPClientManager(
    api_url="https://deploykf.example.com/pipeline",
    
    dex_username="user-1@example.com",
    dex_password="user-1",
    dex_auth_type="local",
    
    skip_tls_verify=True,
)

# get a newly authenticated KFP client
# TIP: long-lived sessions might need to get a new client when their session expires
kfp_client = kfp_client_manager.create_kfp_client()

# test the client by listing experiments
kfp_client.list_experiments(namespace="my-profile-namespace")
```

!!! warning "Static and LDAP Credentials Only"

    The `KFPClientManager()` class ONLY supports authentication with __Static__ or __LDAP__ credentials.
    Due to the nature of other authentication methods, it is not likely that they could be supported by this class in the future.


## Authenticate with Kubernetes ServiceAccount Token

When running the Pipelines SDK inside a Pod on the cluster, a [ServiceAccount token volume](https://kubernetes.io/docs/tasks/configure-pod-container/configure-service-account/#service-account-token-volume-projection) 
can be mounted to the Pod, the Kubeflow Pipelines SDK can use this token to authenticate itself with the Kubeflow Pipelines API.

The following Pod demonstrates mounting a ServiceAccount token volume:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: access-kfp-example
spec:
  containers:
    - image: hello-world:latest
      name: hello-world
      env:
        - name: KF_PIPELINES_SA_TOKEN_PATH
          value: /var/run/secrets/kubeflow/pipelines/token
      volumeMounts:
        - mountPath: /var/run/secrets/kubeflow/pipelines
          name: volume-kf-pipeline-token
          readOnly: true
  volumes:
    - name: volume-kf-pipeline-token
      projected:
        sources:
          - serviceAccountToken:
              path: token
              expirationSeconds: 7200
              audience: pipelines.kubeflow.org      
```

The following Python code creates a `kfp.Client()` using a ServiceAccount token for authentication:

```python
import kfp

# the value of KF_PIPELINES_SA_TOKEN_PATH is used when no `path` is set
# otherwise, "/var/run/secrets/kubeflow/pipelines/token" is the default
credentials = kfp.auth.ServiceAccountTokenVolumeCredentials(path=None)

# note, we point at the internal `Service/ml-pipeline` service,
# rather than the external deployKF gateway
client = kfp.Client(host="http://ml-pipeline-ui.kubeflow.svc.cluster.local", credentials=credentials)

# check that we can list experiments
experiments = client.list_experiments(namespace="my-profile")
print(experiments)
```

!!! warning "RBAC Access"

    By default, this token will only have access to Kubeflow Pipelines resources in the __same namespace__ as the Pod.

!!! info "PodDefault for ServiceAccount Token Volume"

    The [`kubeflow_tools.pipelines.profileResourceGeneration.kfpApiTokenPodDefault`](https://github.com/deployKF/deployKF/blob/v0.1.1/generator/default_values.yaml#L1803-L1811) value 
    configures if a `PodDefault` named `"kubeflow-pipelines-api-token"` is automatically generated in each profile namespace.

    If this value is set to `true`, then any Pod in a profile namespace having a `kubeflow-pipelines-api-token` label with value `"true"` will automatically have a ServiceAccount token volume mounted to the Pod.