---
icon: material/developer-board
description: >-
  Learn how to access the Kubeflow Pipelines API with the Kubeflow Pipelines Python SDK and authenticate with deployKF.
---

# Access Kubeflow Pipelines API

Learn how to __access the Kubeflow Pipelines API__ with the __Kubeflow Pipelines Python SDK__ and authenticate with deployKF.

---

## __Overview__

The [Kubeflow Pipelines SDK](https://kubeflow-pipelines.readthedocs.io/) is the Python client for [Kubeflow Pipelines](../reference/tools.md#kubeflow-pipelines).
This SDK is used to author, compile, and then submit workflows to the Kubeflow Pipelines API.

This table outlines the SDK authentication methods available in deployKF:

Authentication Method<br><small>(Click for Details)</small> | In Cluster | Outside Cluster | No User Interaction
--- | :---: | :---: | :---:
[Browser Login Flow](#browser-login-flow) | :octicons-check-16: | :octicons-check-16: | :octicons-x-16:
[Dex Static Credentials](#dex-static-credentials) | :octicons-check-16: | :octicons-check-16: | :octicons-check-16:
[Kubernetes ServiceAccount Token](#kubernetes-serviceaccount-token) | :octicons-check-16: | :octicons-x-16: | :octicons-check-16:

!!! warning "Kubeflow Pipelines SDK Versions"

    You MUST use the correct version of the [Kubeflow Pipelines Python SDK](https://pypi.org/project/kfp/), using the wrong version of the SDK will result in errors.
    The following table shows the correct SDK version to use with each version of deployKF:

    deployKF Version | Kubeflow Pipelines | SDK Version
    --- | --- | ---
    `0.1.4` and earlier | v1 | `pip install kfp==1.18.22`
    `0.1.5` and later | v2 | `pip install kfp>=2.0.0,<3`

    To check the version of the `kfp` SDK, run the following Python code:

    ```python
    import kfp
    print(kfp.__version__)
    ```

---

## __Browser Login Flow__

The browser login flow (also known as "out-of-band" OIDC login) allows users to authenticate their local SDK using a web browser.
This flow is suitable for interactive workflows, such as Jupyter Notebooks, or other situations that have access to a web browser.

A significant benefit of this flow is that it allows users to act as themselves, rather than a service account, and supports all [external identity providers](../guides/platform/deploykf-authentication.md#external-identity-providers) that may be configured in deployKF.

!!! warning "Minimum deployKF Version"

    The "out-of-band" OIDC login flow requires [deployKF v0.1.3](../releases/changelog-deploykf.md), or later.

### __Authentication Flow__

The flow to authenticate the SDK using an "out-of-band" OIDC login is:

1. The credential provider attempts to read a cached token, from the user's home directory:
    - If an unexpired token is found, it is returned to the SDK.
    - If an expired token is found, the credential provider attempts to refresh the token.
2. Otherwise, the credential provider starts a new "out-of-band" OIDC login flow:
    - The user is prompted to open a URL in their browser.
    - Once the user has authenticated, a code is provided to the user.
    - The user copies the code from the browser and pastes it into the terminal.
    - The token is persisted to the user's home directory, and returned to the SDK.

### __Reference Implementation__

The following reference implementation shows how to authenticate the _Kubeflow Pipelines SDK_ using an "out-of-band" OIDC login flow.

The `DeployKFCredentialsOutOfBand()` class extends `TokenCredentialsBase()` to create a custom credential provider that implements the "out-of-band" OIDC login flow.

??? code "Python Code - _Define Credentials Provider_"

    ```python
    import base64
    import hashlib
    import json
    import logging
    import os
    import sys
    import time
    from typing import Optional
    
    import requests
    import urllib3
    from kubernetes.client import configuration
    from requests_oauthlib import OAuth2Session
    
    try:
        # for kubeflow pipelines v2
        from kfp.client.token_credentials_base import TokenCredentialsBase
    except ImportError:
        # for kubeflow pipelines v1
        from kfp.auth import TokenCredentialsBase
    
    
    class DeployKFCredentialsOutOfBand(TokenCredentialsBase):
        """
        A Kubeflow Pipelines credential provider which uses an "out-of-band" OIDC login flow.
    
        WARNING: intended for deployKF clusters only, unlikely to work with other Kubeflow clusters.
    
        Key features:
         - uses the OIDC client named 'kubeflow-pipelines-sdk', which is pre-configured in deployKF
         - stores tokens in the user's home directory '~/.config/kfp/dkf_credentials.json'
           (this file is indexed by issuer URL, so multiple clusters can be used concurrently)
         - attempts to use the "refresh_token" grant before prompting the user to login again
           (in deployKF, refresh tokens are valid if used at least once every 7 days, and not longer than 90 days in total)
        """
    
        def __init__(self, issuer_url: str, skip_tls_verify: bool = False):
            """
            Initialize a DeployKFTokenCredentials instance.
    
            :param issuer_url: the OIDC issuer URL (e.g. 'https://deploykf.example.com:8443/dex')
            :param skip_tls_verify: if True, skip TLS verification
            """
            # oidc configuration
            self.oidc_issuer_url = issuer_url
            self.oidc_client_id = "kubeflow-pipelines-sdk"
            self.oidc_redirect_uri = "urn:ietf:wg:oauth:2.0:oob"
            self.oidc_scope = ["openid", "email", "groups", "profile", "offline_access"]
    
            # other configuration
            self.http_timeout = 15
            self.local_credentials_path = os.path.join(
                os.path.expanduser("~"), ".config", "kfp", "dkf_credentials.json"
            )
    
            # setup logging
            self.log = logging.getLogger(__name__)
            self._setup_logging()
    
            # disable SSL verification, if requested
            self.skip_tls_verify = skip_tls_verify
            if self.skip_tls_verify:
                self.log.warning("TLS verification is disabled")
                urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
                os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    
            # discover the OIDC issuer configuration
            self._discover_oidc()
    
            # perform the initial login, if necessary
            self.get_token()
    
        def _setup_logging(self):
            self.log.propagate = False
            self.log.setLevel(logging.INFO)
            if not self.log.hasHandlers():
                handler = logging.StreamHandler()
                formatter = logging.Formatter(
                    fmt="%(asctime)s %(levelname)-8s %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S",
                )
                handler.setFormatter(formatter)
                self.log.addHandler(handler)
    
        def _discover_oidc(self):
            """
            Discover the OIDC issuer configuration.
            https://openid.net/specs/openid-connect-discovery-1_0.html
            """
            oidc_discovery_url = f"{self.oidc_issuer_url}/.well-known/openid-configuration"
            self.log.info("Discovering OIDC configuration from: %s", oidc_discovery_url)
            response = requests.get(
                url=oidc_discovery_url,
                timeout=self.http_timeout,
                verify=not self.skip_tls_verify,
            )
            response.raise_for_status()
            oidc_issuer_config = response.json()
            self.oidc_issuer = oidc_issuer_config["issuer"]
            self.oidc_auth_endpoint = oidc_issuer_config["authorization_endpoint"]
            self.oidc_token_endpoint = oidc_issuer_config["token_endpoint"]
    
        def _read_credentials(self) -> dict:
            """
            Read credentials from the JSON file for the current issuer.
            """
            self.log.debug(
                "Checking for existing credentials in: %s", self.local_credentials_path
            )
            if os.path.exists(self.local_credentials_path):
                with open(self.local_credentials_path, "r") as file:
                    data = json.load(file)
                    return data.get(self.oidc_issuer, {})
            return {}
    
        def _write_credentials(self, token: str):
            """
            Write the provided token to the local credentials file (under the current issuer).
            """
            # Create the directory, if it doesn't exist
            credential_dir = os.path.dirname(self.local_credentials_path)
            if not os.path.exists(credential_dir):
                os.makedirs(credential_dir, exist_ok=True)
    
            # Read all existing credentials from the JSON file
            credentials_data = {}
            if os.path.exists(self.local_credentials_path):
                with open(self.local_credentials_path, "r") as f:
                    data = json.load(f)
    
            # Update the credentials for the given issuer
            credentials_data[self.oidc_issuer] = token
            self.log.info("Writing credentials to: %s", self.local_credentials_path)
            with open(self.local_credentials_path, "w") as f:
                json.dump(credentials_data, f)
    
        def _generate_pkce_verifier(self) -> (str, str):
            """
            Generate a PKCE code verifier and its derived challenge.
            https://tools.ietf.org/html/rfc7636#section-4.1
            """
            # Generate a code_verifier of length between 43 and 128 characters
            code_verifier = base64.urlsafe_b64encode(os.urandom(96)).decode("utf-8")
            code_verifier = code_verifier.rstrip("=")
            code_verifier = code_verifier[:128]
    
            # Generate the code_challenge using the S256 method
            sha256_digest = hashlib.sha256(code_verifier.encode("utf-8")).digest()
            code_challenge = (
                base64.urlsafe_b64encode(sha256_digest).decode("utf-8").rstrip("=")
            )
    
            return code_verifier, code_challenge
    
        def _refresh_token(self, oauth_session: OAuth2Session) -> Optional[dict]:
            """
            Attempt to refresh the provided token.
            https://requests-oauthlib.readthedocs.io/en/latest/oauth2_workflow.html#refreshing-tokens
            """
            if not oauth_session.token.get("refresh_token", None):
                return None
    
            self.log.warning("Attempting to refresh token...")
            try:
                new_token = oauth_session.refresh_token(
                    self.oidc_token_endpoint,
                    client_id=self.oidc_client_id,
                    timeout=self.http_timeout,
                    verify=not self.skip_tls_verify,
                )
                self.log.info("Successfully refreshed token!")
                self._write_credentials(new_token)
                return new_token
            except Exception as ex:
                self.log.error("Failed to refresh token!", exc_info=ex)
    
        def _login(self, oauth_session: OAuth2Session) -> dict:
            """
            Start a new "out-of-band" login flow.
            """
            self.log.info("Starting new 'out-of-band' login flow...")
    
            verifier, challenge = self._generate_pkce_verifier()
            authorization_url, state = oauth_session.authorization_url(
                self.oidc_auth_endpoint,
                code_challenge_method="S256",
                code_challenge=challenge,
            )
    
            # ensure everything is printed to the console before continuing
            sys.stderr.flush()
            time.sleep(0.5)
    
            # Get the authorization code from the user
            print(
                f"\nPlease open this URL in a browser to continue:\n > {authorization_url}\n",
                flush=True,
            )
            user_input = input("Enter the authorization code:\n > ")
            authorization_code = user_input.strip()
    
            # Exchange the authorization code for a token
            new_token = oauth_session.fetch_token(
                self.oidc_token_endpoint,
                code=authorization_code,
                code_verifier=verifier,
                include_client_id=True,
                state=state,
                timeout=self.http_timeout,
                verify=not self.skip_tls_verify,
            )
            self.log.info("Successfully fetched new token!")
            self._write_credentials(new_token)
            return new_token
    
        def get_token(self) -> str:
            """
            Get the current auth token.
            Will attempt to use "refresh_token" before prompting the user to login again.
            """
            # return the existing token, if it's valid for at least 5 minutes
            stored_token = self._read_credentials()
            if stored_token:
                expires_at = stored_token.get("expires_at", 0)
                expires_in = expires_at - time.time()
                if expires_in > 300:
                    self.log.info(
                        "Using cached auth token (expires in %d seconds)", expires_in
                    )
                    return stored_token["id_token"]
                elif expires_in > 0:
                    self.log.warning(
                        "Existing auth token expires in %d seconds",
                        expires_in,
                    )
                else:
                    self.log.warning("Existing auth token has expired!")
    
            oauth_session = OAuth2Session(
                self.oidc_client_id,
                redirect_uri=self.oidc_redirect_uri,
                scope=self.oidc_scope,
                token=stored_token,
            )
    
            # try to refresh the token, or start a new login flow
            new_token = self._refresh_token(oauth_session)
            if not new_token:
                new_token = self._login(oauth_session)
    
            return new_token["id_token"]
    
        def refresh_api_key_hook(self, config: configuration.Configuration):
            config.verify_ssl = not self.skip_tls_verify
            config.api_key["authorization"] = self.get_token()
    ```

The following examples demonstrate using the `DeployKFCredentialsOutOfBand()` class to create an authenticated `kfp.Client()`:

??? code "Python Code - _Use Credentials Provider_ - _KFP v1_"

    ```python
    import kfp

    # initialize a credentials instance 
    credentials = DeployKFCredentialsOutOfBand(
        issuer_url="https://deploykf.example.com:8443/dex", 
        skip_tls_verify=True,
    )

    # creates a patched client that supports disabling SSL verification
    # required before kfp v2: https://github.com/kubeflow/pipelines/pull/7174
    def patched_kfp_client(verify_ssl=True):
        _original_load_config = kfp.Client._load_config
    
        def _patched_load_config(client_self, *args, **kwargs):
            config = _original_load_config(client_self, *args, **kwargs)
            config.verify_ssl = verify_ssl
            return config
    
        _patched_client = kfp.Client
        _patched_client._load_config = _patched_load_config
    
        return _patched_client
    
    # initialize a client instance
    kfp_client = patched_kfp_client(verify_ssl=not credentials.skip_tls_verify)(
        host="https://deploykf.example.com:8443/pipeline",
        credentials=credentials,
    )

    # test the client by listing experiments
    experiments = kfp_client.list_experiments(namespace="my-profile")
    print(experiments)
    ```

??? code "Python Code - _Use Credentials Provider_ - _KFP v2_"

    ```python
    import kfp

    # initialize a credentials instance 
    credentials = DeployKFCredentialsOutOfBand(
        issuer_url="https://deploykf.example.com:8443/dex", 
        skip_tls_verify=True,
    )

    # initialize a client instance
    kfp_client = kfp.Client(
        host="https://deploykf.example.com:8443/pipeline",
        verify_ssl=not credentials.skip_tls_verify,
        credentials=credentials,
    )

    # test the client by listing experiments
    experiments = kfp_client.list_experiments(namespace="my-profile")
    print(experiments)
    ```

!!! info "Refresh Token Expiry"

    By default, deployKF allows refresh tokens to be used for __90 days in total__, as long as they are used at least __once every 7 days__.
    While these defaults are usually sufficient, the following values control the refresh token expiry:

    - [`deploykf_core.deploykf_auth.dex.expiry.refreshToken.idle`](https://github.com/deployKF/deployKF/blob/v0.1.4/generator/default_values.yaml#L519)
    - [`deploykf_core.deploykf_auth.dex.expiry.refreshToken.total`](https://github.com/deployKF/deployKF/blob/v0.1.4/generator/default_values.yaml#L522)

---

## __Dex Static Credentials__

Dex static credentials work from both __inside__ and __outside__ the cluster without needing __user interaction__ during authentication.
This makes them suitable for use in CI/CD pipelines, or other privileged automated workflows that need to access Kubeflow Pipelines.

!!! info "Provision Static Credentials"

    Dex static credentials are managed by config values and are provisioned by the cluster administrator.
    The _user authentication guide_ provides information about [managing static credentials in deployKF](../guides/platform/deploykf-authentication.md#static-userpassword-combinations).

### __Authentication Flow__

The flow to authenticate the SDK using Dex static credentials is:

1. The client sends an unauthenticated request to the Kubeflow Pipelines API.
2. The request is redirected to Dex for authentication.
3. The client authenticates with Dex using the static credentials.
4. The client is issued a session cookie by OAuth2 Proxy.
5. The client uses the session cookie with all subsequent requests.

### __Reference Implementation__

The following reference implementation shows how to authenticate the _Kubeflow Pipelines SDK_ using Dex static credentials.

The `KFPClientManager()` class creates authenticated `kfp.Client()` instances that use Dex static credentials for authentication.

??? code "Python Code - _Define Client Manager_"

    ```python
    import re
    from urllib.parse import urlsplit, urlencode
    
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
    
            # disable SSL verification, if requested
            if self._skip_tls_verify:
                urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
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
    
            # GET the api_url, which should redirect to Dex
            resp = s.get(
                self._api_url, allow_redirects=True, verify=not self._skip_tls_verify
            )
            if resp.status_code == 200:
                pass
            elif resp.status_code == 403:
                # if we get 403, we might be at the oauth2-proxy sign-in page
                # the default path to start the sign-in flow is `/oauth2/start?rd=<url>`
                url_obj = urlsplit(resp.url)
                url_obj = url_obj._replace(
                    path="/oauth2/start", query=urlencode({"rd": url_obj.path})
                )
                resp = s.get(
                    url_obj.geturl(), allow_redirects=True, verify=not self._skip_tls_verify
                )
            else:
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
                resp = s.get(
                    url_obj.geturl(), allow_redirects=True, verify=not self._skip_tls_verify
                )
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
                verify=not self._skip_tls_verify,
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

The following example demonstrates using the `KFPClientManager()` class to create an authenticated `kfp.Client()`:

??? code "Python Code - _Use Client Manager_"

    ```python
    # initialize a KFPClientManager
    kfp_client_manager = KFPClientManager(
        api_url="https://deploykf.example.com:8443/pipeline",
        skip_tls_verify=True,
        
        dex_username="user1@example.com",
        dex_password="user1",
        
        dex_auth_type="local",
    )
    
    # get a newly authenticated KFP client
    # TIP: long-lived sessions might need to get a new client when their session expires
    kfp_client = kfp_client_manager.create_kfp_client()
    
    # test the client by listing experiments
    experiments = kfp_client.list_experiments(namespace="my-profile")
    print(experiments)
    ```

!!! info "Supported Authentication Methods"

    The `KFPClientManager` class ONLY supports authentication with [__static__](../guides/platform/deploykf-authentication.md#static-userpassword-combinations) (`local`) or [__LDAP__](../guides/platform/deploykf-authentication.md#external-identity-providers) (`ldap`) credentials, as determined by the `dex_auth_type` class parameter.
    Due to the nature of other authentication methods, it is not likely that they could be supported by this class in the future.

---

## __Kubernetes ServiceAccount Token__

The Kubeflow Pipelines backend has a trust relationship with the Kubernetes ServiceAccount system.
This means that if a request is made to the Kubeflow Pipelines API (internal service) that presents a Kubernetes ServiceAccount bearer token, the request will be authenticated as that ServiceAccount.

This authentication method provides a reliable way to authenticate with the Kubeflow Pipelines API from __inside__ the cluster, without needing __user interaction__ during authentication.

!!! warning "RBAC Access"

    The level of Kubeflow Pipelines access which a Kubernetes ServiceAccount has, is defined by [Kubernetes RBAC](https://kubernetes.io/docs/reference/access-authn-authz/rbac/), rather than deployKF [profile definitions](../guides/platform/deploykf-profiles.md).

    By default, the ServiceAccount used by _Kubeflow Pipelines_ and _Kubeflow Notebooks_ (called `default-editor`), will have read/write access to all Kubeflow Pipelines resources in the __same namespace__ as the Pod.

### __Authentication Flow__

The flow to authenticate the SDK using a Kubernetes ServiceAccount token is:

1. The Pod where the client is running, has a ServiceAccount token volume mounted.
2. The client uses the bearer token to authenticate with the Kubeflow Pipelines API.
3. Kubernetes itself manages the token's expiry and rotation.

### __Reference Implementation__

Kubernetes has a feature called [ServiceAccount token volume projection](https://kubernetes.io/docs/concepts/storage/projected-volumes/#serviceaccounttoken) which mounts and automatically manages ServiceAccount tokens for Pods.
The following reference implementations show how to authenticate the _Kubeflow Pipelines SDK_ using these Kubernetes ServiceAccount tokens.

#### Manually Mount a Token Volume

You may adjust the definition of any Pod to mount a ServiceAccount token volume that can be used to authenticate with the Kubeflow Pipelines API.

For example, the following Pod has a ServiceAccount token volume mounted at the `/var/run/secrets/kubeflow/pipelines/token` path:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: access-kfp-example
spec:
  ## NOTE: the token will be for the service account of the Pod
  serviceAccountName: default-editor
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

#### Automatically Mount a Token Volume with PodDefaults

Kubeflow includes a special CRD called [PodDefault](../guides/tools/kubeflow-poddefaults.md) which will mutate Pods at admission time based on the presence of certain labels.
You may use a PodDefault to automatically inject a token volume into a Pod when it is created.

??? code "Example - _PodDefault for ServiceAccount Token Volume_"

    If you wish to define your own PodDefault, you may do so by creating one in a Profile Namespace.

    For example, the following PodDefault will inject a ServiceAccount token volume into any Pod with the label `my-kfp-api-token=true`:
 
    ```yaml
    apiVersion: kubeflow.org/v1alpha1
    kind: PodDefault
    metadata:
      name: my-kfp-api-token
      namespace: "<YOUR_USER_PROFILE_NAMESPACE>"
    spec:
      desc: "Mount a serviceAccountToken to authenticate with Kubeflow Pipelines API"
      selector:
        matchLabels:
          my-kfp-api-token: "true"
      env:
        - name: KF_PIPELINES_SA_TOKEN_PATH
          value: /var/run/secrets/kubeflow/pipelines/token
      volumes:
        - name: volume-kf-pipeline-token
          projected:
            sources:
              - serviceAccountToken:
                  path: token
                  expirationSeconds: 7200
                  audience: pipelines.kubeflow.org
      volumeMounts:
        - mountPath: /var/run/secrets/kubeflow/pipelines
          name: volume-kf-pipeline-token
          readOnly: true
    ```

When the [`kubeflow_tools.pipelines.profileResourceGeneration.kfpApiTokenPodDefault`](https://github.com/deployKF/deployKF/blob/v0.1.4/generator/default_values.yaml#L1972-L1980) value is `true`, such a PodDefault is automatically provisioned in each Profile Namespace:

```yaml
kubeflow_tools:
  pipelines:
    profileResourceGeneration:
      kfpApiTokenPodDefault: true
```

The PodDefault is called `"kubeflow-pipelines-api-token"`, selects Pods with the `kubeflow-pipelines-api-token=true` label, and injects KFP ServiceAccount token volumes into them.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: access-kfp-example
  labels:
    kubeflow-pipelines-api-token: "true"
spec:
  ## NOTE: the token will be for the service account of the Pod
  serviceAccountName: default-editor
  containers:
    - image: hello-world:latest
      name: hello-world
```

!!! info "Kubeflow Notebooks Integration"

    [Kubeflow Notebooks](../reference/tools.md#kubeflow-notebooks) detects any [PodDefaults](../guides/tools/kubeflow-poddefaults.md) which are in a Profile Namespace.
    Users may tick a checkbox under `"Advanced Options"` → `"Configurations"` to apply a PodDefault when spawning a new Notebook.
    
    If you wish to apply a PodDefault to ALL new Notebooks, see the "advanced pod options" section of [Configure Kubeflow Notebooks](../guides/tools/kubeflow-notebooks.md#advanced-pod-options).

#### Example Python Code

When run inside a Pod that has a ServiceAccount token volume mounted, the following Python code creates a `kfp.Client()` using the token for authentication:

```python
import kfp

# by default, when run from inside a Kubernetes cluster:
#  - the token is read from the `KF_PIPELINES_SA_TOKEN_PATH` path
#  - the host is set to `http://ml-pipeline-ui.kubeflow.svc.cluster.local`
kfp_client = kfp.Client()

# test the client by listing experiments
experiments = kfp_client.list_experiments(namespace="my-profile")
print(experiments)
```

??? question_secondary "Can I specify a different token path or host?"

    By default, when `kfp.Client()` is run from inside a Kubernetes Pod, the token is read from `/var/run/secrets/kubeflow/pipelines/token` (or the value of the `KF_PIPELINES_SA_TOKEN_PATH` environment variable),
    and `http://ml-pipeline-ui.kubeflow.svc.cluster.local` is used for the host.

    You may also explicitly initialize a `ServiceAccountTokenVolumeCredentials` instance and pass it to the `kfp.Client()` constructor as the `credentials` parameter.

    For example to read the token from `/var/run/secrets/kubeflow/pipelines/token2`:

    ```python
    import kfp

    try:
        # for kubeflow pipelines v2
        from kfp.client.set_volume_credentials import ServiceAccountTokenVolumeCredentials
    except ImportError:
        # for kubeflow pipelines v1
        from kfp.auth import ServiceAccountTokenVolumeCredentials
    
    # initialize a credentials instance
    credentials = ServiceAccountTokenVolumeCredentials(
        path="/var/run/secrets/kubeflow/pipelines/token2"
    )

    # initialize a client instance
    # NOTE: we must use the `Service/ml-pipeline-ui` service, NOT the public gateway
    kfp_client = kfp.Client(
        host="http://ml-pipeline-ui.kubeflow.svc.cluster.local",
        credentials=credentials,
    )
    
    # test the client by listing experiments
    experiments = kfp_client.list_experiments(namespace="my-profile")
    print(experiments)
    ```