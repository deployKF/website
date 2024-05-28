---
icon: material/wall
description: >-
  Learn how to use deployKF in offline and air-gapped clusters.
  Use private container registries and Helm repositories.

# TODO: remove status, after a while
status: new
---

# Air-Gapped Clusters and Private Registries

Learn how to use deployKF in offline and air-gapped clusters.
Use private container registries and Helm repositories.

---

## Overview

In some situations, you may need to use deployKF in an offline or air-gapped cluster.
This guide will help you understand how to use deployKF in these scenarios.

The main topics covered in this guide are:

- [ArgoCD Plugin Mode](#argocd-plugin-mode)
- [Private Container Registries](#private-container-registries)
- [Private Helm Repositories](#private-helm-repositories)

---

## ArgoCD Plugin Mode

If you are using [_ArgoCD Plugin Mode_](../modes.md) in an offline or air-gapped cluster, the plugin will be unable to download the generator package from the [`deployKF/deployKF` GitHub releases page](https://github.com/deployKF/deployKF/releases).

If you still want the convenience of using the plugin (as opposed to [_Manifests Repo Mode_](../modes.md)), you can download the _generator package_ manually and host it on an internal git repo.

??? step "Step 1 - Install the Plugin"

    When you [install the plugin](https://github.com/deployKF/deployKF/tree/main/argocd-plugin), you will likely need to mirror the container images used by the plugin to a private registry.

    See the [manifests of the plugin](https://github.com/deployKF/deployKF/tree/main/argocd-plugin/argocd-install) for the list of images to update and mirror.

??? step "Step 2 - Download the Generator Package"

    For the [version of deployKF](../../releases/changelog-deploykf.md) that you want to use, download the `deploykf-<version>-generator.zip` generator package from the [`deployKF/deployKF` GitHub releases page](https://github.com/deployKF/deployKF/releases).

    For example, to download the generator package for version `{{ latest_deploykf_version }}`, you might run the following command:

    ```shell
    curl -fL -o "deploykf-{{ latest_deploykf_version }}-generator.zip" \
      "https://github.com/deployKF/deployKF/releases/download/v{{ latest_deploykf_version }}/deploykf-{{ latest_deploykf_version }}-generator.zip"
    ```

??? step "Step 3 - Update App-of-Apps"

    After pushing the `deploykf-{{ latest_deploykf_version }}-generator.zip` file to your internal git repository, replace the `source_version` parameter with `source_path` in your app-of-apps `Application`.

    For example, your app-of-apps `Application` might look like this:

    ```yaml
    apiVersion: argoproj.io/v1alpha1
    kind: Application
    metadata:
      name: deploykf-app-of-apps
      namespace: argocd
      labels:
        app.kubernetes.io/name: deploykf-app-of-apps
        app.kubernetes.io/part-of: deploykf
    spec:
      project: ...
    
      source:

        ## the git repository containing the generator package
        ##
        repoURL: "https://git.example.com/deploykf.git"
        targetRevision: "main"
        path: "."
    
        ## plugin configuration
        ##
        plugin:
          name: "deploykf"
          parameters:
    
            ## the path to the generator package within the `repoURL` repository
            - name: "source_path"
              string: "./deploykf-{{ latest_deploykf_version }}-generator.zip"
    
            ## paths to values files within the `repoURL` repository
            - name: "values_files"
              array:
                - ...
    
            ## a string containing the contents of a values file
            - name: "values"
              string: |
                ...
    
      destination:
        ...
    ```

---

## Private Container Registries

In some situations, like when your cluster is not connected to the internet, you may need to use a private container registry for all container images.

!!! warning "Advanced Topic"
    
    Using a private container registry is an advanced scenario, and is NOT recommended for most users (because of the number of images in deployKF).
    If at all possible, we recommend using the default image locations.

    For your reference, the default image locations are spread across multiple container registries:

    - [Docker Hub](https://hub.docker.com/) (`docker.io`)
    - [Google Container Registry](https://gcr.io/) (`gcr.io`)
    - [GitHub Container Registry](https://ghcr.io/) (`ghcr.io`)
    - [Quay](https://quay.io/) (`quay.io`)

??? step "Step 1 - Get list of Images"

    The first step is to determine which images and tags need to be mirrored to your private registry.
    Currently, we don't have an out-of-the-box solution for this.
    
    However, we have created values to override all images in deployKF.
    Almost all image values are under the `<path_to_tool>.images` key of each component, but some are in a different location (these end in an `image` suffix, to make them easier to find).
    For example, the images for Kubeflow Pipelines are under [`kubeflow_tools.pipelines.images`](https://github.com/deployKF/deployKF/blob/v0.1.5/generator/default_values.yaml#L1785-L1825) and [`kubeflow_tools.pipelines.kfpV2.xxxxImage`](https://github.com/deployKF/deployKF/blob/v0.1.5/generator/default_values.yaml#L1926-L1938).

    !!! tip

        Search for `images:` and `image:` in the [`default_values.yaml`](https://github.com/deployKF/deployKF/blob/v{{ latest_deploykf_version }}/generator/default_values.yaml) to find all current image values.

    You will notice that the `tag` is not specified for some images.
    This is because Helm/Kustomize will automatically set this at deploy time based on the version of the component.
    This makes determining the correct tag to mirror a bit more difficult.
    The only way to determine the correct tag is to __render the manifests for each component__ and extract the images which are actually used.

    For example, to print the images for __Kubeflow Pipelines__ (which is a Kustomize app), you might run the following commands:
    
    ```shell
    # Render the manifests
    deploykf generate ... --output-dir ./GENERATOR_OUTPUT
    
    # Go to the component directory
    cd ./GENERATOR_OUTPUT/manifests/kubeflow-tools/pipelines
    
    # Print the images
    kustomize build . \
      | perl -nle $'print $1 if /image: ["\']?([^ {"\']+)["\']?/'
    ```

    For example, to print the images for __Istio__ (which is a Helm chart), you might run the following commands:
    
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

    !!! warning "Not all Images are in the Manifests"
    
        Some images are not technically "part of the manifests", that is, not used in the `image` field of a PodSpec.
        This means they will NOT show up with the above commands.
        However, all such images should have an associated deployKF value, so you can find them in the [`default_values.yaml`](https://github.com/deployKF/deployKF/blob/v{{ latest_deploykf_version }}/generator/default_values.yaml).

        For example, [Istio](../dependencies/istio.md) injects sidecar containers into Pod definitions at runtime (and the image used is configured by a ConfigMap).
        Its associated image value is [`deploykf_dependencies.istio.images.istioProxy`](https://github.com/deployKF/deployKF/blob/v0.1.5/generator/default_values.yaml#L250-L252).

    !!! info "Regex"
    
        The above commands are using the regex `/image: ["']?([^ {"']+)["']?/` to extract parts of the manifest which look like `image: "xxxx"`, `image: 'xxxx'`, or `image: xxxx`.

        We are not sure if this regex is sufficient for all cases, please let us know if you find a better one!

??? step "Step 2 - Mirror the Images"

    Once you have the list of images and tags, you will need to mirror them to your private container registry.
    You may use the `docker` command to pull and push the images.

    For example, you might create a script which loops through each image and does the following:

    ```shell
    # set the source image
    SOURCE_REGISTRY="ghcr.io" # depending on image: "docker.io", "grc.io", "ghcr.io", "quay.io"
    SOURCE_IMAGE="deploykf/kubeflow-pipelines/cache-server:X.Y.Z"

    # set the destination image
    DEST_REGISTRY="docker.example.com"
    DEST_IMAGE="${SOURCE_IMAGE}"

    # pull the images
    docker pull "${SOURCE_REGISTRY}/${SOURCE_IMAGE}"

    # tag the images
    docker tag "${SOURCE_REGISTRY}/${SOURCE_IMAGE}" "${DEST_REGISTRY}/${DEST_IMAGE}"

    # push the images
    # NOTE: you may need to login first with `docker login ...`
    docker push "${DEST_REGISTRY}/${DEST_IMAGE}"
    ```

    !!! tip "Image Names"

        We recommend using the same image name as the source image, as this will make it easier to update the deployKF values.

??? step "Step 3 - Set Image Values"

    Finally, you will need to update all the deployKF image values to use the mirrored images.

    Almost all image values are under the `<path_to_tool>.images` key of each component, but some are in a different location (these end in an `image` suffix, to make them easier to find).

    !!! tip

        Search for `images:` and `image:` in the [`default_values.yaml`](https://github.com/deployKF/deployKF/blob/v{{ latest_deploykf_version }}/generator/default_values.yaml) to find all current image values.

    For example, the images for Kubeflow Pipelines are under [`kubeflow_tools.pipelines.images`](https://github.com/deployKF/deployKF/blob/v0.1.5/generator/default_values.yaml#L1785-L1825) and [`kubeflow_tools.pipelines.kfpV2.xxxxImage`](https://github.com/deployKF/deployKF/blob/v0.1.5/generator/default_values.yaml#L1926-L1938):
    
    ```yaml
    kubeflow_tools:
      pipelines:
        images:
          kfpCacheServer:
            repository: docker.example.com/deploykf/kubeflow-pipelines/cache-server
            tag: X.Y.Z
    
          kfpMetadataEnvoy:
            repository: docker.example.com/deploykf/kubeflow-pipelines/metadata-envoy
            tag: X.Y.Z
    
          kfpMetadataWriter:
            repository: docker.example.com/deploykf/kubeflow-pipelines/metadata-writer
            tag: X.Y.Z
    
          kfpApiServer:
            repository: docker.example.com/deploykf/kubeflow-pipelines/api-server
            tag: X.Y.Z
    
          kfpPersistenceagent:
            repository: docker.example.com/deploykf/kubeflow-pipelines/persistenceagent
            tag: X.Y.Z
    
          kfpScheduledworkflow:
            repository: docker.example.com/deploykf/kubeflow-pipelines/scheduledworkflow
            tag: X.Y.Z
    
          kfpFrontend:
            repository: docker.example.com/deploykf/kubeflow-pipelines/frontend
            tag: X.Y.Z
    
          kfpViewerCrdController:
            repository: docker.example.com/deploykf/kubeflow-pipelines/viewer-crd-controller
            tag: X.Y.Z
    
          kfpVisualizationServer:
            repository: docker.example.com/deploykf/kubeflow-pipelines/visualization-server
            tag: X.Y.Z
    
          tfxMlMetadataStoreServer:
            repository: docker.example.com/deploykf/ml_metadata_store_server
            ## NOTE: this tag is not aligned to the other KFP images
            tag: X.Y.Z

        kfpV2:
          driverImage: "docker.example.com/deploykf/kubeflow-pipelines/kfp-driver:X.Y.Z"
          launcherImage: "docker.example.com/deploykf/kubeflow-pipelines/kfp-launcher:X.Y.Z"

          ## NOTE: this tag is not aligned to the other KFP images
          v2CompatibleLauncherImage: "docker.example.com/deploykf/kubeflow-pipelines/kfp-launcher:1.8.22-deploykf.0"
    ```

!!! contribute "Help Us Improve"

    If you have a better idea, or have created a script to automate this process, please let us know!

---

## Private Helm Repositories

A small number of deployKF components use an upstream Helm repository.
If your cluster does not have internet access, you may need to mirror these Helm charts to a private repository, or install these components manually.

=== ":star: Mirror the Helm Charts :star:"

    If you are able to mirror Helm charts to a private repository, you can tell deployKF to use this repository instead of the default ones.

    ??? step "Step 1 - Get list of Helm Charts"

        The first step is to determine which Helm charts need to be mirrored to your private repository.
        Currently, we don't have an out-of-the-box solution for this.
        
        However, we have created values to override all Helm charts in deployKF.
        All Helm repository URLs can be overridden with the `<path_to_tool>.charts.<chart_name>.repository` values.

        !!! tip
    
            Search for `charts:` in the [`default_values.yaml`](https://github.com/deployKF/deployKF/blob/v{{ latest_deploykf_version }}/generator/default_values.yaml) to find all current chart values.

    ??? step "Step 2 - Mirror the Helm Charts"

        Once you have the list of Helm charts, you will need to mirror them to a private repository.

        Unless you already have a [traditional Helm repository](https://helm.sh/docs/topics/chart_repository/), you will likely want to use the new [OCI-based registries](https://helm.sh/docs/topics/registries/) to push the charts to a container registry that you already have.

        For example, you might create a script which loops through each chart and does the following:

        ```shell
        # set the source chart
        SOURCE_REPO="https://charts.jetstack.io"
        SOURCE_CHART="cert-manager"
        SOURCE_VERSION="X.Y.Z"

        # set the destination repository
        DEST_REPO="oci://ghcr.io/MY_GITHUB_USER/helm-charts" # or another OCI registry

        # we untar the chart because some charts have a "v" in their version (cert-manager)
        # but OCI registries don't ignore the "v" like traditional Helm registries, 
        # so we need to remove it
        UNTAR_DIR="./${SOURCE_CHART}-${SOURCE_VERSION}"
        rm -rf "${UNTAR_DIR}"

        # pull the chart
        helm pull \
          --repo "${SOURCE_REPO}" \
          --version "${SOURCE_VERSION}" \
          --untar \
          --untardir "${UNTAR_DIR}" \
          "${SOURCE_CHART}"

        # repackage the chart
        helm package \
          "${SOURCE_CHART}-${SOURCE_VERSION}/${SOURCE_CHART}" \
          --version "${SOURCE_VERSION}"

        # push the chart
        # NOTE: you may need to login first with `docker login ...`
        helm push \
          "${SOURCE_CHART}-${SOURCE_VERSION}.tgz" \
          "${DEST_REPO}"

        # cleanup
        rm -rf "${UNTAR_DIR}"
        ```

    ??? step "Step 3 - Repository Credentials (if needed)"

        If your registry requires authentication, you will need to configure ArgoCD with credentials to access the repository.

        How you do this will depend on which [mode of operation](../modes.md) you are using:

        ??? config "ArgoCD Plugin Mode"
        
            Due to upstream limitations for ArgoCD plugins, it is not currently possible for the plugin to read from ArgoCD's credential store ([`argoproj/argo-cd#8820`](https://github.com/argoproj/argo-cd/issues/8820))
    
            You will need to create a `kubernetes.io/dockerconfigjson` type secret in the `argocd` namespace, and then update the _deployKF ArgoCD Plugin_ to use this secret.

            For example, to use the GitHub Container Registry (`ghcr.io/MY_GITHUB_USERNAME/helm-charts`) with a [Personal Access Token (PAT)](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens) you might run the following commands:
    
            ```shell
            kubectl create secret docker-registry "my-ghcr-config" \
              --namespace "argocd" \
              --docker-server="https://ghcr.io/v2/" \
              --docker-username="MY_GITHUB_USERNAME" \
              --docker-password="MY_GITHUB_PAT"
            ```

            Then you will need to apply the following patch to the `argocd-repo-server` Deployment:

            ```yaml
            apiVersion: apps/v1
            kind: Deployment
            metadata:
              name: argocd-repo-server
              namespace: argocd
            spec:
              template:
                spec:
                  containers:
                    - name: deploykf-plugin
                      env:
                        - name: HELM_REGISTRY_CONFIG
                          value: "/helm-working-dir/registry/.dockerconfigjson"
                      volumeMounts:
                        - name: registry
                          mountPath: /helm-working-dir/registry
                  volumes:
                    - name: registry
                      secret:
                        secretName: my-ghcr-config
            ```

            Either add it as an additional `patchesStrategicMerge` in the plugin [`kustomization.yaml`](https://github.com/deployKF/deployKF/blob/main/argocd-plugin/argocd-install/kustomization.yaml), or apply it directly to the cluster with `kubectl`:

            ```shell
            kubectl patch deployment "argocd-repo-server" \
              --namespace "argocd" \
              --patch-file=./my-patch.yaml
            ```

        ??? config "Manifests Repo Mode"
        
            In _manifests repo mode_, you may [configure ArgoCD itself](https://argo-cd.readthedocs.io/en/stable/user-guide/private-repositories/) with the required OCI registry credentials.  

            For example, to use GitHub Container Registry (`ghcr.io/MY_GITHUB_USERNAME/helm-charts`) with a [Personal Access Token (PAT)](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens):
    
            ```bash
            # create a secret with your GitHub credentials
            # NOTE: kubectl can't create and label a secret in one command, so we use a pipe
            kubectl create secret generic --dry-run=client -o yaml \
                "argocd-repository--ghcr-oci" \
                --namespace "argocd" \
                --from-literal=type="helm" \
                --from-literal=name="ghcr-oci" \
                --from-literal=enableOCI="true" \
                --from-literal=url="ghcr.io/MY_GITHUB_USERNAME/helm-charts" \
                --from-literal=username="MY_GITHUB_USERNAME" \
                --from-literal=password="MY_GITHUB_PAT" \
              | kubectl label --local --dry-run=client -o yaml -f - \
                "argocd.argoproj.io/secret-type"="repository" \
              | kubectl apply -f -
            ```

    ??? step "Step 4 - Set Helm Chart Values"

        Finally, you will need to update all the deployKF Helm chart values to use the mirrored charts.

        For example, you might override the `cert-manager`, `istio`, and `kyverno` charts with the following values:
        
        ```yaml
        
        deploykf_dependencies:
    
          cert_manager:
            charts:
              certManager:
                name: cert-manager
                version: X.Y.Z
                repository: "oci://ghcr.io/MY_GITHUB_USERNAME/helm-charts"
                #repository: https://charts.jetstack.io
    
          istio:
            charts:
              istioBase:
                name: base
                version: X.Y.Z
                repository: "oci://ghcr.io/MY_GITHUB_USERNAME/helm-charts"
                #repository: https://istio-release.storage.googleapis.com/charts
        
              istioDaemon:
                name: istiod
                version: X.Y.Z
                repository: "oci://ghcr.io/MY_GITHUB_USERNAME/helm-charts"
                #repository: https://istio-release.storage.googleapis.com/charts
    
          kyverno:
            name: kyverno
            version: X.Y.Z
            repository: "oci://ghcr.io/MY_GITHUB_USERNAME/helm-charts"
            #repository: https://kyverno.github.io/kyverno
        
        deploykf_core:
    
          deploykf_istio_gateway:
            charts:
              istioGateway:
                name: gateway
                version: X.Y.Z
                repository: "oci://ghcr.io/MY_GITHUB_USERNAME/helm-charts"
                #repository: https://istio-release.storage.googleapis.com/charts
        ```

=== "Disable the Helm Charts"

    Alternatively, you may disable the components which use these upstream Helm charts.

    ??? step "Step - Disable Components"
    
        Right now, the only components which use upstream Helm charts are ones which can be replaced with an existing deployment on your cluster.
    
        - [Use Existing __Istio__](../dependencies/istio.md#can-i-use-my-existing-istio)
        - [Use Existing __cert-manager__](../dependencies/cert-manager.md#can-i-use-my-existing-cert-manager)
        - [<s>Use Existing __Kyverno__</s>](../dependencies/kyverno.md#can-i-use-my-existing-kyverno) <small>(coming soon)</small>