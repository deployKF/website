---
icon: material/cloud-download
description: >-
  Learn how to configure image pull secrets in deployKF.
---

# Image Pull Secrets

Learn how to configure __image pull secrets__ in deployKF.

---

## Overview

You may need to configure image pull secrets in deployKF.
Image pull secrets tell Kubernetes how to authenticate with a container registry when pulling images.

For example, you may want to avoid Docker Hub [rate limits](https://www.docker.com/increase-rate-limits/) on public images, or use a [private container registry](./offline.md#private-container-registries) that requires authentication.

## Configure Image Pull Secrets

deployKF provides a built-in [:custom-kyverno-color: __Kyverno__](../dependencies/kyverno.md#what-is-kyverno) policy to clone image-pull-secrets into every namespace, and automatically add them to the `spec.imagePullSecrets` field of every Pod in the cluster.
See [the `ClusterPolicy`](https://github.com/deployKF/deployKF/blob/v0.1.4/generator/templates/manifests/deploykf-dependencies/kyverno/templates/ClusterPolicy-image-pull-secrets.yaml) for more details.

These steps will guide you through creating and using an image pull secret in deployKF.

??? step "Step 1 - Authenticate with Container Registry"

    You will need to use `docker login` to authenticate with your container registry.

    For example, to authenticate with Docker Hub:

    ```bash
    # login to your container registry
    docker login
    
    # review the docker config file
    cat ~/.docker/config.json
    ```

    ---

    !!! info "Other Container Registries"

        For information on using `docker login` with other container registries, see the following documentation:
        
        - [Google Container Registry](https://cloud.google.com/artifact-registry/docs/docker/authentication#json-key)
        - [GitHub Container Registry](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry#authenticating-with-a-personal-access-token-classic) 
        - [Quay](https://docs.quay.io/guides/login.html)

??? step "Step 2 - Create Kubernetes Secret"

    Next, you will need to create a Kubernetes secret from your `~/.docker/config.json` file.

    For example, to create a secret called `my-docker-config` in the `argocd` namespace:

    ```shell
    kubectl create secret generic "my-docker-config" \
      --namespace "argocd" \
      --type=kubernetes.io/dockerconfigjson \
      --from-file=.dockerconfigjson=~/.docker/config.json
    ```

    ---

    !!! warning "Credentials Store"

        If `~/.docker/config.json` contains a `credsStore` field, you won't be able to create the secret from the file directly, see the [upstream Kubernetes documentation](https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/#create-a-secret-by-providing-credentials-on-the-command-line) for more details.

        For example, to create a secret for `docker.io` with an [Access Token](https://docs.docker.com/security/for-developers/access-tokens/):

        ```shell
        kubectl create secret docker-registry "my-docker-config" \
          --namespace "argocd" \
          --docker-server="https://index.docker.io/v1/" \
          --docker-username="MY_DOCKER_USERNAME" \
          --docker-password="MY_DOCKER_ACCESS_TOKEN"
        ```

        For example, to create a secret for `ghcr.io` with a [Personal Access Token (PAT)](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens):

        ```shell
        kubectl create secret docker-registry "my-ghcr-config" \
          --namespace "argocd" \
          --docker-server="https://ghcr.io/v2/" \
          --docker-username="MY_GITHUB_USERNAME" \
          --docker-password="MY_GITHUB_PAT"
        ```

        For example, to create a secret for `<region>-docker.pkg.dev` (GCP) with a [Service Account Key](https://cloud.google.com/artifact-registry/docs/docker/authentication#json-key):

        ```shell
        kubectl create secret docker-registry "my-gcr-config" \
          --namespace "argocd" \
          --docker-server="https://<region>-docker.pkg.dev" \
          --docker-username="_json_key" \
          --docker-password="$(cat ~/path/to/service-account-key.json)"
        ```

??? step "Step 3 - Configure deployKF"

    Finally, you will need to configure deployKF to use the new secret.

    The [`deploykf_dependencies.kyverno.clusterPolicies.imagePullSecrets`](https://github.com/deployKF/deployKF/blob/v0.1.4/generator/default_values.yaml#L396-L417) values are used to configure [our Kyverno ClusterPolicy](https://github.com/deployKF/deployKF/blob/v0.1.4/generator/templates/manifests/deploykf-dependencies/kyverno/templates/ClusterPolicy-image-pull-secrets.yaml).

    The following values will enable the policy and use the `my-docker-config` secret (from the `argocd` namespace):

    ```yaml
    deploykf_dependencies:
      kyverno:
        clusterPolicies:
    
          imagePullSecrets:
            ## if the policy is enabled
            enabled: true
    
            ## a list of namespaces to exclude from this policy
            #excludeNamespaces:
            #  - "argocd"
            #  - "kube-system"
    
            ## a list of registry credentials
            registryCredentials:
              - existingSecret: "my-docker-config"
                existingSecretNamespace: "argocd"
    ```

    ---

    !!! info "Exclude Namespaces"

        The `imagePullSecrets.excludeNamespaces` value will exclude namespaces from the policy.

        By default, the `argocd` and `kube-system` namespaces are excluded 
        _(**WARNING:** if you set this key, make sure you list them, as the default values will be overridden)_.
        The `kyverno` namespace is always excluded, so you don't need to list it.

        This value supports the following wildcards:

        - `*` - matches zero or many characters
        - `?` - matches at least one character