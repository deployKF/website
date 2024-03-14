---
icon: material/shield-account
description: >-
  Learn about user authentication and connecting with external identity providers in deployKF.
  Active Directory, Okta, GitHub, Google, AWS Cognito, and more.

# disable the mkdocs-macros-plugin for this page
render_macros: false
---

# User Authentication and External Identity Providers

Learn about __user authentication__ and connecting with __external identity providers__ in deployKF.

!!! tip "Related Guides"

    In addition to configuring how users are __authenticated__, you will likely want to __authorize__ them by [assigning to profiles](deploykf-profiles.md).
    Note, the level of access a user has is directly determined by which profiles they are a member of.

---

## Introduction

deployKF provides a very flexible approach to user authentication.

All user-facing components that require authentication are connected with the embedded [Dex](https://github.com/dexidp/dex) instance.
Most components connect to Dex via [OAuth2 Proxy](https://github.com/oauth2-proxy/oauth2-proxy) with [Istio `EnvoyFilters`](https://github.com/deployKF/deployKF/tree/v0.1.4/generator/templates/manifests/deploykf-core/deploykf-istio-gateway/templates/gateway) (e.g. Kubeflow), but some components connect with Dex directly (e.g. MinIO, Argo Server). 

When a user needs to be authenticated, they will be redirected to Dex, which then authenticates them using one (or more) of the following methods:

Authentication Method<br><small>(Click for Details)</small> | Description
--- | ---
[External Identity Providers](#external-identity-providers) | Connect with external identity providers like Active Directory, Okta, GitHub, Google.
[Static User/Password Combinations](#static-userpassword-combinations) | Define a list of static user/password combinations that are local to deployKF.<br><br>These credentials are commonly used as "service accounts" for things like [Accessing the Kubeflow Pipelines API](../../user-guides/access-kubeflow-pipelines-api.md), but may also be used for regular users if you don't have an external identity provider.

## External Identity Providers

Typically, organizations will have an existing identity provider like Okta, GitHub, or Google.

Dex provides [connectors](https://dexidp.io/docs/connectors/) for many external identity providers.
The following table lists some common identity providers and the Dex connector you should use to connect with them:

Provider Name<br><small>(Click for Example)</small> | Dex Connector Type
--- | ---
[Active Directory (LDAP)](#active-directory-ldap) | [`ldap`](https://dexidp.io/docs/connectors/ldap/)
[AWS Cognito](#aws-cognito) | [`oidc`](https://dexidp.io/docs/connectors/oidc/)
[GitHub](#github) | [`github`](https://dexidp.io/docs/connectors/github/)
[Google Workspace](#google-workspace) | [`google`](https://dexidp.io/docs/connectors/google/)
[Microsoft Identity Platform](#microsoft-identity-platform) | [`microsoft`](https://dexidp.io/docs/connectors/microsoft/)
[Okta](#okta) | [`oidc`](https://dexidp.io/docs/connectors/oidc/)
[OneLogin](#onelogin) | [`oidc`](https://dexidp.io/docs/connectors/oidc/)
[Keycloak](#keycloak) | [`oidc`](https://dexidp.io/docs/connectors/oidc/)
[Generic (OpenID Connect)](#generic-openid-connect) | [`oidc`](https://dexidp.io/docs/connectors/oidc/)

!!! warning "SAML 2.0"

    You should NOT use the [`saml`](https://dexidp.io/docs/connectors/saml/) connector, as it does not support refresh tokens, so users would be forced to re-login every 60 minutes.
    Most identity providers with _SAML 2.0_ also have _OpenID Connect (OIDC)_, which supports refresh tokens.

!!! warning "Groups"

    Currently, deployKF does not use the `groups` claim from providers.
    Within deployKF, groups are virtual constructs which are defined with the [profile values](deploykf-profiles.md#group-entities).

### Connector Values

The [`deploykf_core.deploykf_auth.dex.connectors`](https://github.com/deployKF/deployKF/blob/v0.1.3/generator/default_values.yaml#L449-L460) value configures the list of Dex connectors which are available for user authentication.
You may define multiple connectors, users will be prompted to choose one when they login.

The generic structure of a `connector` list element is as follows:

```yaml
deploykf_core:
  deploykf_auth:
    dex:
      connectors:
        - ## the connector type (ldap, github, oidc, etc.)
          type: <connector-type>
          
          ## identifier for the connector (any string)
          id: <connector-id>
          
          ## human-readable name for the connector (any string)
          name: <connector-name>
          
          ## (OPTION 1):
          ##  - set the config with values (NOT RECOMMENDED)
          ##  - see provider guides for examples
          config:
            config-key-1: config-value-1
            config-key-2: config-value-2
            config-key-3: config-value-3
          
          ## (OPTION 2):
          ##  - read a kubernetes secret from the 'deploykf-auth' namespace
          ##  - using this completely overrides the `config` map above
          #configExistingSecret: "my-secret-name"
          #configExistingSecretKey: "key-in-secret-with-config-yaml-string"
```

??? question_secondary "How do I use `configExistingSecret`?"

    To use the `configExistingSecret` option, you must create a Kubernetes secret with the `config` values.

    The secret must be created in the `deploykf-auth` namespace, and the `configExistingSecretKey` key in the secret must contain a string of YAML which is formatted the same as the `config` map key above.

    Note, the `type`, `id`, and `name` fields are defined in the `connector` list element, NOT in the secret.

    For example, you may create a secret like this:
    
    ```yaml
    kind: Secret
    apiVersion: v1
    metadata:
      name: my-secret-name
      namespace: deploykf-auth
    ## NOTE: you may also use `data` if you base64 encode the string
    stringData:
      key-in-secret-with-config-yaml-string: |
        config-key-1: config-value-1
        config-key-2: config-value-2
        config-key-3: config-value-3
    ```

    The following values will then make use of the secret:
    
    ```yaml
    deploykf_core:
      deploykf_auth:
        dex:
          connectors:
            - type: <connector-type>
              id: <connector-id>
              name: <connector-name>
              configExistingSecret: "my-secret-name"
              configExistingSecretKey: "key-in-secret-with-config-yaml-string"
    ```

??? question_secondary "Can I use External Secrets Operator?"

    If you are using [External Secrets Operator](https://github.com/external-secrets/external-secrets), you can easily include the `ExternalSecret` manifest in your deployKF values.
    The [`deploykf_core.deploykf_auth.extraManifests`](https://github.com/deployKF/deployKF/blob/v0.1.3/generator/default_values.yaml#L396-L400) value will include additional manifests in the `deploykf-auth` namespace.

    For example, the following values will create an `ExternalSecret` named `my-secret-name`:

    ```yaml
    deploykf_core:
      deploykf_auth:
        extraManifests:
          - |
            apiVersion: external-secrets.io/v1beta1
            kind: ExternalSecret
            metadata:
              name: my-secret-name
              namespace: deploykf-auth
            spec:
              refreshInterval: "60s"

              ## the secret store to read from
              secretStoreRef:
                name: my-secret-store
                kind: SecretStore
            
              ## the secret to be created
              target:
                ## the `configExistingSecret` would be this secret
                name: my-secret-name

                ## NOTE: we wrap templates in {{ `...` }} to stop helm from parsing them
                template:
                  data:
                    ## the `configExistingSecretKey` would be this key
                    google-config: |
                      clientID: {{ `{{ .clientID | quote }}` }}
                      clientSecret: {{ `{{ .clientSecret | quote }}` }}
                      redirectURI: "https://deploykf.example.com/dex/callback"

              ## data to read from the secret store
              ##  - key: the secret to read from the secret store
              ##  - property: usually a GJSON expression to extract the value from the secret
              data:
                - secretKey: clientID
                  remoteRef:
                    key: /deploykf/auth/google-oidc
                    property: clientID

                - secretKey: clientSecret
                  remoteRef:
                    key: /deploykf/auth/google-oidc
                    property: clientSecret
    ```

### Provider Examples

The following guides show provider-specific instructions for configuring Dex [connectors](https://dexidp.io/docs/connectors/):

??? steps "Active Directory (LDAP)"

    ###### Active Directory (LDAP)

    How to connect deployKF with Active Directory will depend on the structure of your Active Directory:

    - [Dex: Docs for `ldap` connector](https://dexidp.io/docs/connectors/ldap/)

    The following values act as a good starting point for connecting deployKF with LDAP:

    ```yaml
    deploykf_core:
      deploykf_auth:
        dex:
          connectors:
            - type: ldap
              id: ldap
              name: LDAP
              config:
                ## the LDAP server URL and port
                host: ldap.example.com:636

                ## if we should skip TLS certificate verification
                ## WARNING: this is insecure, prefer to use `rootCAData`
                insecureSkipVerify: false

                ## a base64 encoded PEM file with your root CA certificate
                #rootCAData: ""

                ## the credentials to use for searching the directory
                ## NOTE: not required if anonymous bind is allowed
                #bindDN: uid=Administrator,cn=Users,dc=example,dc=com
                #bindPW: password

                ## text used in password-prompt box
                usernamePrompt: "Username"

                ## how users are searched for, based on the provided username
                userSearch:

                  ## base search from
                  baseDN: cn=Users,dc=example,dc=com

                  ## an additional search filter to apply
                  filter: "(objectClass=person)"

                  ## how to map user attributes
                  username: uid
                  idAttr: uid
                  emailAttr: mail
                  nameAttr: name

                ## how groups are searched for, based on the found user
                groupSearch:
                  ## base search from
                  baseDN: cn=Groups,dc=example,dc=com
    
                  ## an additional search filter to apply
                  ## NOTE: you may need to limit the search to prevent a large number of results
                  filter: "(objectClass=group)"

                  ## list of user-attribute to group-attribute pairs
                  ## the value of the found user's `userAttr` must be one of the group's `groupAttr`
                  userMatchers:
                    - userAttr: uid
                      groupAttr: member

                  ## how to map group attributes
                  nameAttr: cn
    ```

    !!! info "Restricting Access to Members of Specific Group"
        
        deployKF does not currently use `groups` from providers.
        If you need to restrict deployKF to members of specific group, you must extend the `userSearch.filter` to include a group membership check.

        For example, if users are in the `cn=Users,dc=example,dc=com` OU, and you want to restrict access to members of the `cn=deploykf,ou=Groups,dc=example,dc=com` group, you could use the following:

        ```yaml
        userSearch:
          baseDN: cn=Users,dc=example,dc=com
          filter: "(&(objectClass=person)(memberOf=cn=deploykf,ou=Groups,dc=example,dc=com))"
        ```

        This pattern could be extended to support multiple groups by using `(|(memberOf=...)(memberOf=...))`.

    !!! warning "Use Kubernetes Secrets"

        Consider using `configExistingSecret` instead of `config` to avoid storing secrets in your values,
        see the [Connector Values](#connector-values) section for more details.

??? steps "AWS Cognito"

    ###### AWS Cognito

    To connect deployKF with AWS Cognito, you must first create an "App Client" in AWS Cognito:

    - [AWS: Create user pool app clients](https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-client-apps.html)    
    - [Dex: Docs for `oidc` connector](https://dexidp.io/docs/connectors/oidc/)

    The following values will connect deployKF with your AWS Cognito application:

    ```yaml
    deploykf_core:
      deploykf_auth:
        dex:
          connectors:
            - type: oidc
              id: aws-cognito
              name: AWS Cognito
              config:
                issuer: https://cognito-idp.<AWS_REGION>.amazonaws.com/<USER_POOL_ID>

                clientID: "XXXXXXXXXXXXXXXXXXXX"
                clientSecret: "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

                ## replace with your deploykf domain
                ## NOTE: this must be an allowed redirect URI in the AWS Cognito app
                redirectURI: https://deploykf.example.com/dex/callback

                ## openid scopes to request
                scopes:
                  - openid
                  - email
                  - profile

                ## cognito does not send the `name` claim
                userNameKey: cognito:username

                ## cognito does not always send the `email_verified` claim
                insecureSkipEmailVerified: true
    ```

    !!! warning "Use Kubernetes Secrets"

        Consider using `configExistingSecret` instead of `config` to avoid storing secrets in your values,
        see the [Connector Values](#connector-values) section for more details.

??? steps "GitHub"

    ###### GitHub

    To connect deployKF with GitHub, you must create an OAuth application in GitHub:

    - [GitHub: Creating an OAuth app](https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/creating-an-oauth-app)
    - [Dex: Docs for `github` connector](https://dexidp.io/docs/connectors/github/)

    The following values will connect deployKF with your GitHub application:

    ```yaml
    deploykf_core:
      deploykf_auth:
        dex:
          connectors:
            - type: github
              id: github
              name: GitHub
              config:
                clientID: "XXXXXXXXXXXXXXXXXXXX"
                clientSecret: "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

                ## replace with your deploykf domain
                ## NOTE: this must be an allowed redirect URI in the GitHub app
                redirectURI: https://deploykf.example.com/dex/callback

                ## a list of GitHub organizations to allow users from
                orgs:
                  - my-org

                ## only required for GitHub Enterprise
                #hostName: github.example.com
    ```

    !!! warning "Use Kubernetes Secrets"

        Consider using `configExistingSecret` instead of `config` to avoid storing secrets in your values,
        see the [Connector Values](#connector-values) section for more details.

??? steps "Google Workspace"

    ###### Google Workspace

    To connect deployKF with Google Workspace, you must register an application in the Google API Console:

    - [Google: Setting up OAuth 2.0](https://developers.google.com/identity/openid-connect/openid-connect)
    - [Dex: Docs for `google` connector](https://dexidp.io/docs/connectors/google/)

    The following values will connect deployKF with your Google Workspace:

    ```yaml
    deploykf_core:
      deploykf_auth:
        dex:
          connectors:
            - type: google
              id: google
              name: Google
              config:
                clientID: "XXXXXXXXXXXXXXXXXXXX"
                clientSecret: "XXXXXXXXXXXXXXXXXXXXXXXXX"

                ## replace with your deploykf domain
                ## NOTE: this must be an allowed redirect URI in the Google app
                redirectURI: https://deploykf.example.com/dex/callback
    ```

    !!! warning "Use Kubernetes Secrets"

        Consider using `configExistingSecret` instead of `config` to avoid storing secrets in your values,
        see the [Connector Values](#connector-values) section for more details.

??? steps "Microsoft Identity Platform"

    ###### Microsoft Identity Platform

    To connect deployKF with Microsoft Identity Platform, register an application in Azure:

    - [Azure: Register app with Microsoft identity platform](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app)
    - [Dex: Docs for `microsoft` connector](https://dexidp.io/docs/connectors/microsoft/)

    The following values will connect deployKF with your Microsoft Identity Platform application:

    ```yaml
    deploykf_core:
      deploykf_auth:
        dex:
          connectors:
            - type: microsoft
              id: microsoft
              name: Microsoft
              config:
                clientID: "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX"
                clientSecret: "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

                ## replace with your deploykf domain
                ## NOTE: this must be an allowed redirect URI in the Okta app
                redirectURI: "https://deploykf.example.com/dex/callback"
    ```

    !!! warning "Use Kubernetes Secrets"

        Consider using `configExistingSecret` instead of `config` to avoid storing secrets in your values,
        see the [Connector Values](#connector-values) section for more details.

??? steps "Okta"

    ###### Okta

    To connect deployKF with Okta, you must first create a "OIDC - Web Application" application in Okta:

    - [Okta: Create OIDC app integrations](https://help.okta.com/en-us/content/topics/apps/apps_app_integration_wizard_oidc.htm)
    - [Dex: Docs for `oidc` connector](https://dexidp.io/docs/connectors/oidc/)

    The following values will connect deployKF with your Okta application:

    ```yaml
    deploykf_core:
      deploykf_auth:
        dex:
          connectors:
            - type: oidc
              id: okta
              name: Okta
              config:
                issuer: https://MY_COMPANY.okta.com

                clientID: "XXXXXXXXXXXXXXXXXXXX"
                clientSecret: "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

                ## replace with your deploykf domain
                ## NOTE: this must be an allowed redirect URI in the Okta app
                redirectURI: https://deploykf.example.com/dex/callback

                ## openid scopes to request
                scopes:
                  - openid
                  - email
                  - profile
                  ## NOTE: offline_access is required for refresh tokens
                  ##  - ensure the Okta app has "Refresh Token" grant type enabled
                  ##  - set the "Refresh Token Behavior" to "Rotate token after every use"
                  - offline_access

                ## okta does not always send the `email_verified` claim
                insecureSkipEmailVerified: true
    ```

    !!! warning "Use Kubernetes Secrets"

        Consider using `configExistingSecret` instead of `config` to avoid storing secrets in your values,
        see the [Connector Values](#connector-values) section for more details.

??? steps "OneLogin"

    ###### OneLogin

    To connect deployKF with OneLogin, you must first create an "OpenID Connect" application in OneLogin:

    - [OneLogin: Create OpenID Connect app](https://onelogin.service-now.com/support?id=kb_article&sys_id=2fd988e697b72150c90c3b0e6253af7f&kb_category=de885d2187372d10695f0f66cebb351f)
    - [Dex: Docs for `oidc` connector](https://dexidp.io/docs/connectors/oidc/)

    The following values will connect deployKF with your OneLogin application:

    ```yaml
    deploykf_core:
      deploykf_auth:
        dex:
          connectors:
            - type: oidc
              id: onelogin
              name: OneLogin
              config:
                issuer: https://openid-connect.onelogin.com/oidc

                clientID: "XXXXXXXXXXXXXXXXXXXX"
                clientSecret: "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

                ## replace with your deploykf domain
                ## NOTE: this must be an allowed redirect URI in the OneLogin app
                redirectURI: https://deploykf.example.com/dex/callback

                ## openid scopes to request
                scopes:
                  - openid
                  - email
                  - profile
                  ## NOTE: offline_access is required for refresh tokens
                  - offline_access

                ## onelogin does not always send the `email_verified` claim
                insecureSkipEmailVerified: true
    ```

??? steps "Keycloak"

    ###### Keycloak

    To connect deployKF with Keycloak, you must first create an "OpenID Connect" client in Keycloak:

    - [Keycloak: Managing OpenID Connect clients](https://www.keycloak.org/docs/latest/server_admin/index.html#_oidc_clients)
    - [Keycloak: Using OpenID Connect to secure apps](https://www.keycloak.org/docs/latest/securing_apps/#_oidc)
    - [Dex: Docs for `oidc` connector](https://dexidp.io/docs/connectors/oidc/)

    The following values will connect deployKF with your Keycloak application:

    ```yaml
    deploykf_core:
      deploykf_auth:
        dex:
          connectors:
            - type: oidc
              id: keycloak
              name: Keycloak
              config:
                issuer: https://keycloak.example.com/realms/<REALM_NAME>

                clientID: "XXXXXXXXXXXXXXXXXXXX"
                clientSecret: "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

                ## replace with your deploykf domain
                ## NOTE: this must be an allowed redirect URI in the Keycloak app
                redirectURI: https://deploykf.example.com/dex/callback

                ## openid scopes to request
                scopes:
                  - openid
                  - email
                  - profile
                  ## NOTE: offline_access is required for refresh tokens
                  - offline_access

                ## keycloak does not always send the `email_verified` claim
                insecureSkipEmailVerified: true

                ## if your Keycloak uses a self-signed certificate
                #insecureSkipVerify: true
    ```

??? steps "Generic (OpenID Connect)"

    ###### Generic (OpenID Connect)

    Many identity providers support the [OpenID Connect (OIDC)](https://openid.net/connect/) protocol, which is an extension of OAuth2.

    Dex provides an [`oidc`](https://dexidp.io/docs/connectors/oidc/) connector which can be used to connect with any OIDC provider.
    
    For example, here are generic values for connecting with an OIDC provider:

    ```yaml
    deploykf_core:
      deploykf_auth:
        dex:
          connectors:
            - type: oidc
              id: oidc
              name: Generic OIDC
              config:
                ## replace with your OIDC provider's issuer URL
                ## NOTE: the URL must expose the `.well-known/openid-configuration` endpoint 
                issuer: https://oidc.example.com

                ## credentials for the OIDC client
                clientID: "XXXXXXXXXXXXXXXXXXXX"
                clientSecret: "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

                ## replace with your deploykf domain
                ## NOTE: this must be an allowed redirect URI in the OIDC app
                redirectURI: https://deploykf.example.com/dex/callback

                ## openid scopes to request
                scopes:
                  - openid
                  - email
                  - profile
                  ## NOTE: offline_access is typically required for refresh tokens
                  ##       if possible, configure your provider to only allow each
                  ##       refresh token to be used once
                  - offline_access

                ## set to true, if provider does not always send `email_verified` claim
                insecureSkipEmailVerified: true
    ```

## Static User/Password Combinations

deployKF supports defining static user/password combinations which are local to itself.

These static credentials are commonly used as "service accounts" for things like [Accessing the Kubeflow Pipelines API](../../user-guides/access-kubeflow-pipelines-api.md), but may also be used for regular users if you don't have an external identity provider.

!!! info "Password Secret Rotation"

    If a user's password is defined from a Kubernetes Secret (with `existingSecret`), the password will be automatically rotated when the Secret is updated.

The [`deploykf_core.deploykf_auth.dex.staticPasswords`](https://github.com/deployKF/deployKF/blob/v0.1.1/generator/default_values.yaml#L378-L401) value defines the list of credentials which are available for user authentication.

The following values show three different ways to define static credentials:

```yaml
deploykf_core:
  deploykf_auth:
    dex:
      staticPasswords:
        ## (OPTION 1):
        ##  - a user with password defined as a plaintext value
        - email: "plaintext@example.com"
          password:
            value: "password"

        ## (OPTION 2):
        ##  - a user with password defined as a bcrypt hash
        ##  - a bcrypt hash for "password" can be generated with one of the following:
        ##     - echo "password" | htpasswd -BinC 10 NULL | cut -d: -f2
        ##     - python -c 'import bcrypt; print(bcrypt.hashpw(b"password", bcrypt.gensalt(10)).decode())'
        - email: "bcrypt@example.com"
          password:
            ## the bcrypt hash of the password "password"
            value: "$2y$10$z22lKMtSyC65VhMfTROkGesiS2ofrVQQdkGu.vjhIH2HM5Epmhil2"
            type: "hash"

        ## (OPTION 3):
        ##  - a user with password defined from a kubernetes secret
        - email: "kubernetes-secret@example.com"
          existingSecret: "my-secret"
          existingSecretKey: "password-key"
```