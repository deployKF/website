# User Authentication and External Identity Providers

This guide explains how to __configure user authentication__ and connect with __external identity providers__ in deployKF.

---

## Overview

deployKF uses [Dex](https://github.com/dexidp/dex) and [Oauth2 Proxy](https://github.com/oauth2-proxy/oauth2-proxy) via [our Istio `EnvoyFilters`](https://github.com/deployKF/deployKF/tree/v0.1.1/generator/templates/manifests/deploykf-core/deploykf-istio-gateway/templates/gateway) for user authentication.

Dex allows multiple authentication methods to be used at the same time, including:

- Connecting External Identity Providers
- Defining Static User/Password Combinations

## External Identity Providers

Dex provides [connectors](https://dexidp.io/docs/connectors/) for many external identity providers including [LDAP (Active Directory)](https://dexidp.io/docs/connectors/ldap/), [GitHub](https://dexidp.io/docs/connectors/github/), [Google](https://dexidp.io/docs/connectors/google/), [Microsoft](https://dexidp.io/docs/connectors/microsoft/) and [OpenID Connect (Azure, Okta, Salesforce, etc)](https://dexidp.io/docs/connectors/oidc/).

The [`deploykf_core.deploykf_auth.dex.connectors`](https://github.com/deployKF/deployKF/blob/v0.1.1/generator/default_values.yaml#L403-L414) value configures the list of connectors which are available for user authentication.

For example, to connect with Google, you might use the following values:

```yaml
deploykf_core:
  deploykf_auth:
    dex:
      connectors:
        ## NOTE:
        ##  - this element is formatted the same as described in: 
        ##    https://dexidp.io/docs/connectors/google/
        ##  - in addition to `type`, `id`, `name`, and `config`, 
        ##    which are the same as upstream dex, we provide the
        ##    `configExistingSecret` and `configExistingSecretKey`
        ##    fields, to set the `config` from a kubernetes secret
        - type: google
          id: google
          name: Google

          ## NOTE: 
          ##  - the full `config` must come from a single source, 
          ##     you can NOT mix `config` and `configExistingSecret`
          config:
           clientID : "kubeflow"
           clientSecret : "XXXXXXXXXXXXXXXXXXXXXXXXX"
           redirectURI : "https://XXXXXXXX/dex/callback"

          ## NOTE: 
          ##  - the `configExistingSecretKey` key in the secret must 
          ##    contain a string of YAML that is formatted the same 
          ##    as the CONTENTS of the `config` map key above
          #configExistingSecret: "my-dex-connector-secret"
          #configExistingSecretKey: "google-config"
```


!!! warning "SAML 2.0 Connector"

    You should __NOT__ use the [SAML 2.0 connector](https://dexidp.io/docs/connectors/saml/), as it does not support refreshing tokens, so users would be forced to re-login every 60 minutes.

## Static User/Password Combinations

The [`deploykf_core.deploykf_auth.dex.staticPasswords`](https://github.com/deployKF/deployKF/blob/v0.1.1/generator/default_values.yaml#L378-L401) value defines a list of static user/password combinations.

For example, you might use the following values to define three users:

```yaml
deploykf_core:
  deploykf_auth:
    dex:
      staticPasswords:
        ## a user with password defined as a plaintext value
        - email: "plaintext@example.com"
          password:
            value: "password"

        ## a user with password defined as a bcrypt hash
        ##  - a bcrypt hash for "PASSWORD_STRING" can be generated with one of the following:
        ##     - echo "PASSWORD_STRING" | htpasswd -BinC 10 NULL | cut -d: -f2
        ##     - python -c 'import bcrypt; print(bcrypt.hashpw(b"password", bcrypt.gensalt(10)).decode())'
        - email: "bcrypt@example.com"
          password:
            ## the bcrypt hash of the password "password"
            value: "$2y$10$z22lKMtSyC65VhMfTROkGesiS2ofrVQQdkGu.vjhIH2HM5Epmhil2"
            type: "hash"

        ## a user with password defined from a kubernetes secret
        - email: "kubernetes-secret@example.com"
          existingSecret: "my-secret"
          existingSecretKey: "password-key"
```

!!! note "Password Secret Rotation"

    If a user's password is defined from a Kubernetes Secret, the password will be automatically rotated when the Secret is updated.

!!! note "Service Accounts"

    The static accounts are commonly used as "service accounts" for things like [Accessing the Kubeflow Pipelines API](../../user-guides/access-kubeflow-pipelines-api.md), but may also be used for regular users if you do not have an external identity provider.
