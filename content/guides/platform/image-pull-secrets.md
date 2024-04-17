---
icon: material/cloud-download
description: >-
  Learn how to configure image pull secrets and private container registries in deployKF.

# TODO: remove status, after a while
status: new
---

# Image Pull Secrets and Private Registries

Learn how to configure __image pull secrets__ and __private container registries__ in deployKF.

---

## Overview

You may need to configure image pull secrets in deployKF.
For example, you may want to avoid Docker Hub [rate limits](https://www.docker.com/increase-rate-limits/) on public images, or use a private container registry that requires authentication.

Image pull secrets tell Kubernetes how to authenticate with a container registry when pulling images.

## Image Pull Secrets

deployKF provides a built-in [:custom-kyverno-color: __Kyverno__](../dependencies/kyverno.md#what-is-kyverno) policy to clone image-pull-secrets into every namespace, and automatically add them to the `spec.imagePullSecrets` field of every Pod in the cluster.
See [the `ClusterPolicy`](https://github.com/deployKF/deployKF/blob/v0.1.4/generator/templates/manifests/deploykf-dependencies/kyverno/templates/ClusterPolicy-image-pull-secrets.yaml) for more details.

These steps will guide you through creating and using an image pull secret in deployKF.

??? step "Step 1 - Authenticate with your Container Registry"

    You will need to use `docker login` to authenticate with your container registry.

    For example, to authenticate with Docker Hub:

    ```bash
    # login to your container registry
    docker login
    
    # review the docker config file
    cat ~/.docker/config.json
    ```

    For information on using `docker login` with other container registries, see the following documentation:
    
    - [Google Container Registry](https://cloud.google.com/artifact-registry/docs/docker/authentication#json-key)
    - [GitHub Container Registry](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry#authenticating-with-a-personal-access-token-classic) 
    - [Quay](https://docs.quay.io/guides/login.html)

    ---

    !!! warning "Credentials Store"

        If `~/.docker/config.json` contains a `credsStore` field, you won't be able to create the secret from the file directly.
        See the [upstream Kubernetes documentation](https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/#create-a-secret-by-providing-credentials-on-the-command-line) for more details.

??? step "Step 2 - Create a Kubernetes Secret"

    Next, you will need to create a Kubernetes secret from your `~/.docker/config.json` file.

    For example, to create a secret called `my-docker-config` in the `argocd` namespace:

    ```shell
    kubectl create secret generic "my-docker-config" \
      --from-file=.dockerconfigjson=~/.docker/config.json \
      --type=kubernetes.io/dockerconfigjson \
      --namespace "argocd"
    ```

??? step "Step 3 - Configure deployKF to use the Secret"

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

## Private Registries

In some situations, like when your cluster is not connected to the internet, you may need to use a private container registry for all container images.

!!! warning "Advanced Topic"
    
    Using a private container registry is an advanced scenario, and is NOT recommended for most users (because of the number of images in deployKF).
    If at all possible, we recommend using the default image locations.

    For your reference, the default image locations are spread across multiple container registries:

    - [Docker Hub](https://hub.docker.com/) (`docker.io`)
    - [Google Container Registry](https://gcr.io/) (`gcr.io`)
    - [GitHub Container Registry](https://ghcr.io/) (`ghcr.io`)
    - [Quay](https://quay.io/) (`quay.io`)

Currently, we don't have an out-of-the-box solution to mirror all the images to a private registry.

However, we have created values to override the default image locations for all images in deployKF.
Almost all image values are under the `<path_to_tool>.images` key of each component, with the rest ending with an `image` suffix.

For example, the images for Kubeflow Pipelines are under [`kubeflow_tools.pipelines.images`](https://github.com/deployKF/deployKF/blob/v0.1.4/generator/default_values.yaml#L1772-L1814):

```yaml
kubeflow_tools:
  pipelines:
    images:
      kfpCacheServer:
        repository: gcr.io/ml-pipeline/cache-server
        tag: ~

      kfpMetadataEnvoy:
        repository: gcr.io/ml-pipeline/metadata-envoy
        tag: ~

      kfpMetadataWriter:
        repository: gcr.io/ml-pipeline/metadata-writer
        tag: ~

      kfpApiServer:
        repository: gcr.io/ml-pipeline/api-server
        tag: ~

      kfpPersistenceagent:
        repository: gcr.io/ml-pipeline/persistenceagent
        tag: ~

      kfpScheduledworkflow:
        repository: gcr.io/ml-pipeline/scheduledworkflow
        tag: ~

      kfpFrontend:
        repository: gcr.io/ml-pipeline/frontend
        tag: ~

      kfpViewerCrdController:
        repository: gcr.io/ml-pipeline/viewer-crd-controller
        tag: ~

      kfpVisualizationServer:
        repository: gcr.io/ml-pipeline/visualization-server
        tag: ~

      tfxMlMetadataStoreServer:
        repository: gcr.io/tfx-oss-public/ml_metadata_store_server
        ## NOTE: this tag is not aligned to the other KFP images
        tag: ~
```

You will notice that the `tag` is not specified for some images.
This is because Helm/Kustomize will automatically set this at deploy time based on the version of the component.

This makes determining the correct tag to mirror a bit more difficult.
The only way to determine the correct tag is to render the manifests for each component and extract the tag from the rendered manifests.

For example, to print the images for Kubeflow Pipelines (which is a Kustomize app), you might run the following commands:

```shell
# Render the manifests
deploykf generate ... --output-dir ./GENERATOR_OUTPUT

# Go to the component directory
cd ./GENERATOR_OUTPUT/manifests/kubeflow-tools/pipelines

# Print the images
kustomize build . \
  | perl -nle $'print $1 if /image: ["\']?([^ {"\']+)["\']?/'
```

For example, to print the images for Istio (which is a Helm chart), you might run the following commands:

```shell
# Render the manifests
deploykf generate ... --output-dir ./GENERATOR_OUTPUT

# Go to the component directory
cd ./GENERATOR_OUTPUT/manifests/deploykf-dependencies/istio

# Update the Helm dependencies
helm dependency update .

# Print the images
# NOTE: the istio chart needs the namespace to be set
helm template . --namespace istio-system \
  | perl -nle $'print $1 if /image: ["\']?([^ {"\']+)["\']?/'
```

!!! info "Regex"

    The above commands are using the `/image: ["']?([^ {"']+)["']?/` regex.
    We are not sure if this regex is sufficent for all cases to extract the image string.

!!! warning "Non-Manifest Images"

    Some images are not technically "part of the manifests" of a component.
    That is, they are not used in the `image` field of a `Deployment` or `StatefulSet`.

    For example, Istio injects a sidecar into every Pod, and this sidecar is a separate image.
    We have tried to expose all these images in the `<path_to_tool>.images` values, but we may have missed some.

Once you have the images and tags, you can use the `docker` command to pull the images and push them to your private registry.
Finally, you will need to update all corresponding deployKF image values to point to your private registry.

!!! contribute "Help Us Improve"

    If you have a better idea, or have created a script to automate this process, please let us know!