---
icon: material/rocket-launch
description: >-
  Learn how to use deployKF in production.
  Easily deploy Kubeflow and other MLOps tools as a complete platform!
  
search:
  boost: 2
---

# Getting Started

Learn how to use <strong><span class="deploykf-orange">deploy</span><span class="deploykf-blue">KF</span></strong> in production.
<br>
Easily deploy the [best of Kubeflow](../reference/tools.md#kubeflow-ecosystem) and other MLOps tools as a complete platform!

---

## Introduction

This page is about using deployKF in production, it will cover the requirements, configuration options, deployment process, and basic usage of the platform.

We suggest new users start with the __About deployKF__ and __Local Quickstart__ pages:

[About deployKF<br><small>(Introduction)</small>](../about/introduction.md#about-deploykf){ .md-button .md-button--secondary }
[Local Quickstart<br><small>(Try Locally)</small>](./local-quickstart.md){ .md-button .md-button--secondary }

!!! value ""

    We encourage you to [join our community](../about/community.md) and learn about [support options](../about/support.md)!
    
    [:material-account-group: Join the Community](../about/community.md){ .md-button .md-button--secondary }
    [:material-headset: Get Support](../about/support.md){ .md-button .md-button--secondary }

    For existing Kubeflow users, we have a _migration guide_:
        
    [Migrate from :custom-kubeflow: Kubeflow Distributions](./kubeflow-distributions.md#about-migrating){ .md-button .md-button--secondary }


## 1. Requirements

### __Kubernetes Cluster__

deployKF can run on any [:custom-kubernetes-color: __Kubernetes__](https://kubernetes.io/) cluster, in __any cloud or environment__.
See the [__version matrix__](../releases/version-matrix.md#kubernetes) for a list of supported Kubernetes versions.

Here are some Kubernetes distributions which are supported by deployKF:

Target Platform | Kubernetes Distribution
--- | ---
Amazon Web Services | [Amazon Elastic Kubernetes Service (EKS)](https://aws.amazon.com/eks/)
Microsoft Azure | [Azure Kubernetes Service (AKS)](https://azure.microsoft.com/en-us/products/kubernetes-service/)<br><small>:material-alert: [see special requirements](https://github.com/deployKF/deployKF/issues/61#issuecomment-1949658332) :material-alert:</small> 
Google Cloud | [Google Kubernetes Engine (GKE)](https://cloud.google.com/kubernetes-engine)
IBM Cloud | [IBM Cloud Kubernetes Service (IKS)](https://www.ibm.com/cloud/kubernetes-service)
Self-Hosted | [Rancher (RKE)](https://ranchermanager.docs.rancher.com/) // [kOps](https://kops.sigs.k8s.io/) // [Kubespray](https://kubespray.io/) // [kubeadm](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/)
Edge | [k3s](https://k3s.io/) // [k0s](https://k0sproject.io/) // [MicroK8s](https://microk8s.io/)
Local Machine | [k3d](https://k3d.io/) // [Kind](https://kind.sigs.k8s.io/) // [Minikube](https://minikube.sigs.k8s.io/) 

!!! warning "Dedicated Cluster"

    We strongly recommend using a __dedicated cluster__ for deployKF.
    This is because deployKF has a number of cluster-level dependencies which may conflict with other applications.

    <small>If you are unable to create a new Kubernetes cluster, you may consider using [vCluster](https://github.com/loft-sh/vcluster) to create a virtual Kubernetes cluster within an existing one.</small>

### __Kubernetes Configurations__

deployKF requires some specific Kubernetes configurations to work correctly.

The following table lists these configurations and their requirements:

Configuration | Requirement
--- | ---
Node Resources | The nodes must collectively have at least `4 vCPUs` and `16 GB RAM`, and `64 GB Storage`.
CPU Architecture | The cluster must have `x86_64` Nodes.
Cluster Domain | The [`clusterDomain`](https://kubernetes.io/docs/reference/config-api/kubelet-config.v1beta1/#kubelet-config-k8s-io-v1beta1-KubeletConfiguration) of your kubelet must be `"cluster.local"`.
Service Type | By default, the cluster must have a `LoadBalancer` service type.<br><small>:material-alert: be careful not to expose your platform on the public internet by mistake :material-alert: </small>
Default StorageClass | The default [`StorageClass`](https://kubernetes.io/docs/concepts/storage/storage-classes/) must support the `ReadWriteOnce` access mode.
Existing Argo Workflows | The cluster __must NOT__ already have [Argo Workflows](https://github.com/argoproj/argo-workflows) installed.<br><small>See [`deployKF/deployKF#116`](https://github.com/deployKF/deployKF/issues/116) to join the discussion.</small>

??? info "ARM64 Support"

    Currently, deployKF only supports `x86_64` architecture clusters.

    The next minor version of deployKF (`v0.2.0`) should have native `ARM64` for all core components.
    However, some upstream apps like _Kubeflow Pipelines_ will need extra work to be production ready ([`#10309`](https://github.com/kubeflow/pipelines/issues/10309), [`#10308`](https://github.com/kubeflow/pipelines/issues/10308)).

??? info "Air-Gapped Clusters"

    deployKF can be used in offline and air-gapped clusters, but there are additional steps required.

    Please see the [Air-Gapped Clusters](./platform/offline.md) guide for more information.

??? config "Override Service Type"

    By default, deployKF uses a `LoadBalancer` service type for the gateway.

    If you do not want this, you may override the service type to `ClusterIP` by setting the following value:

    ```yaml
    deploykf_core:
      deploykf_istio_gateway:
        gatewayService:
          type: "ClusterIP"
    ```

    However, for real-world usage, you should review the [Expose the Gateway Service](./platform/deploykf-gateway.md#expose-the-gateway-service) guide.

??? config "Override Default StorageClass"

    By default, deployKF requires a __default StorageClass__ that supports the `ReadWriteOnce` access mode.

    If you do NOT have a compatible default StorageClass, you might consider the following options:

    1. Configure [a default StorageClass](https://kubernetes.io/docs/tasks/administer-cluster/change-default-storage-class/) that has `ReadWriteOnce` support
    2. Explicitly set the `storageClass` value for the following components:
         - [`deploykf_opt.deploykf_minio.persistence.storageClass`](https://github.com/deployKF/deployKF/blob/v0.1.1/generator/default_values.yaml#L901-L905)
         - [`deploykf_opt.deploykf_mysql.persistence.storageClass`](https://github.com/deployKF/deployKF/blob/v0.1.1/generator/default_values.yaml#L1036-L1040)
    2. Disable components which require the StorageClass, and use external alternatives:
         - [Connect an External __Object Store__](./external/object-store.md#connect-an-external-object-store)
         - [Connect an External __MySQL__](./external/mysql.md#connect-an-external-mysql)

---

## 2. Platform Configuration

deployKF is very configurable, you can use it to deploy a wide variety of machine learning platforms and integrate with your existing infrastructure.

### __deployKF Values__

All aspects of your deployKF platform are configured with YAML-based configs named __"values"__.
See the [values](./values.md) page for more information.

### __deployKF Versions__

The __"version"__ of your platform is the version of the [generator package](../releases/changelog-deploykf.md) you are using.
For information about upgrading, see the [upgrade guide](./upgrade.md#upgrading-versions) and [changelog](../releases/changelog-deploykf.md).

??? question_secondary "Can I be notified of new releases?"

    Yes. Watch the [`deployKF/deployKF`](https://github.com/deployKF/deployKF) repo on GitHub.
    <br>
    At the top right, click `Watch` → `Custom` → `Releases` then confirm by selecting `Apply`.

### __Cluster Dependencies__

deployKF has a number of cluster dependencies including __Istio__, __cert-manager__, and __Kyverno__.
See the [cluster dependencies](./cluster-dependencies.md) page for an overview.

!!! warning "Existing Cluster Dependencies"

    deployKF installs its own versions of the cluster dependencies by default.
    <br>
    If you have existing versions on the cluster, you MUST configure deployKF to use them:

    - [Use Existing __Istio__](./dependencies/istio.md#can-i-use-my-existing-istio)
    - [Use Existing __cert-manager__](./dependencies/cert-manager.md#can-i-use-my-existing-cert-manager)
    - [<s>Use Existing __Kyverno__</s>](./dependencies/kyverno.md#can-i-use-my-existing-kyverno) <small>(coming soon)</small>

### __External Dependencies__

deployKF has a number of external dependencies including __MySQL__ and an __Object Store__.
See the [external dependencies](./external-dependencies.md) page for an overview.

!!! warning "Connect External Dependencies"

    deployKF includes embedded versions of MySQL and MinIO for development and testing.
    <br>
    We strongly recommend connecting external versions for production use:

    - [Connect External __MySQL__](./external/mysql.md#connect-an-external-mysql)
    - [Connect External __Object Store__](./external/object-store.md#connect-an-external-object-store)

---

## 3. Deploy the Platform

### __:star: Create ArgoCD Applications :star:__

deployKF [uses ArgoCD](./dependencies/argocd.md#how-does-deploykf-use-argo-cd) to manage the deployment of the platform.
The process to create the ArgoCD [`Applications`](./dependencies/argocd.md#argo-cd-applications) will depend on which [mode of operation](modes.md) you have chosen.

=== ":star: ArgoCD Plugin Mode :star:"

    ??? step "Step 1 - Prepare ArgoCD"

        You will need to have ArgoCD deployed on your cluster, this ArgoCD instance must have the [_deployKF ArgoCD Plugin_](./dependencies/argocd.md#what-is-the-deploykf-argocd-plugin) installed.
        Follow the appropriate guide for your situation:

        - [New ArgoCD](https://github.com/deployKF/deployKF/tree/main/argocd-plugin#new-argocd)
        - [Existing ArgoCD (Deployed with Helm)](https://github.com/deployKF/deployKF/tree/main/argocd-plugin#existing-argocd---helm)
        - [Existing ArgoCD (Deployed with Kustomize)](https://github.com/deployKF/deployKF/tree/main/argocd-plugin#existing-argocd---kustomize)

        __TIP:__ If you use an ArgoCD "management cluster" pattern, see the [off-cluster ArgoCD](./dependencies/argocd.md#can-i-use-an-off-cluster-argocd) guide.

    ??? step "Step 2 - Learn about Values"

        deployKF is configured by [centralized values](./values.md) which define the desired state of the platform.

        ---

        <h4>Sample Values:</h4>

        Each version of deployKF has [sample values](./values.md#sample-values) with all [ML & Data tools](../reference/tools.md#tool-index) enabled, along with some sensible security defaults.
        We recommend using the sample values as a starting point for your custom values.

        Here are the [`sample-values.yaml`](https://github.com/deployKF/deployKF/blob/v{{ latest_deploykf_version }}/sample-values.yaml) for deployKF `{{ latest_deploykf_version }}`.

        ---

        <h4>Custom Values:</h4>

        In _ArgoCD Plugin Mode_, values can be defined __inline__ _(`values`)_, or from a  __git repository__ _(`values_files`)_.
        
        Both methods may be used together.
        When a value is defined in multiple places, the result is calculated by [merging](./values.md#merging-values), with files listed later taking precedence, and inline values having the highest precedence.

        !!! tip

            Learn about common configuration tasks in the [:star: __Configure deployKF__ :star:](./configs.md) guide.

    ??? step "Step 3 - Define an App-of-Apps"

        Create a local file named `deploykf-app-of-apps.yaml` with the contents of the YAML below.

        In this example, we will define an app-of-apps that:

        - Clones the `deploykf/deploykf` repo at the [`v{{ latest_deploykf_version }}`](https://github.com/deployKF/deployKF/tree/v{{ latest_deploykf_version }}) tag.
        - Sets the `source_version` parameter to use [deployKF version](#deploykf-versions) `{{ latest_deploykf_version }}`.
        - Sets the `values_files` parameter to read the [`sample-values.yaml`](https://github.com/deployKF/deployKF/blob/v{{ latest_deploykf_version }}/sample-values.yaml) from the repo.
        - Sets the `values` parameter with inline values that override the `sample-values.yaml`.

        ??? question_secondary "What is an App-of-Apps?"

            An _app-of-apps_ is a special ArgoCD [`Application`](./dependencies/argocd.md#argo-cd-applications) which manages other applications.

        ??? question_secondary "Can I read values from my own repo?"
            
            Yes.
            In this example, we only use the `deploykf/deploykf` repo to easily read the default `sample-values.yaml` file.
            See Step 4 to read values from a different repo.

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

          ## NOTE: if not "default", you MUST ALSO set the `argocd.project` value
          project: "default"

          source:
            ## source git repo configuration
            ##  - we use the 'deploykf/deploykf' repo so we can read its 'sample-values.yaml'
            ##    file, but you may use any repo (even one with no files)
            ##
            repoURL: "https://github.com/deployKF/deployKF.git"
            targetRevision: "v{{ latest_deploykf_version }}"
            path: "."
        
            ## plugin configuration
            ##
            plugin:
              name: "deploykf"
              parameters:
        
                ## the deployKF generator version
                ##  - available versions: https://github.com/deployKF/deployKF/releases
                ##
                - name: "source_version"
                  string: "{{ latest_deploykf_version }}"
        
                ## paths to values files within the `repoURL` repository
                ##  - the values in these files are merged, with later files taking precedence
                ##  - we strongly recommend using 'sample-values.yaml' as the base of your values
                ##    so you can easily upgrade to newer versions of deployKF
                ##
                - name: "values_files"
                  array:
                    - "./sample-values.yaml"
        
                ## a string containing the contents of a values file
                ##  - this parameter allows defining values without needing to create a file in the repo
                ##  - these values are merged with higher precedence than those defined in `values_files`
                ##
                - name: "values"
                  string: |
                    ##
                    ## This demonstrates how you might structure overrides for the 'sample-values.yaml' file.
                    ## For a more comprehensive example, see the 'sample-values-overrides.yaml' in the main repo.
                    ##
                    ## Notes:
                    ##  - YAML maps are RECURSIVELY merged across values files
                    ##  - YAML lists are REPLACED in their entirety across values files
                    ##  - Do NOT include empty/null sections, as this will remove ALL values from that section.
                    ##    To include a section without overriding any values, set it to an empty map: `{}`
                    ##
        
                    ## --------------------------------------------------------------------------------
                    ##                                      argocd
                    ## --------------------------------------------------------------------------------
                    argocd:
                      namespace: argocd
                      project: default

                    ## --------------------------------------------------------------------------------
                    ##                                    kubernetes
                    ## --------------------------------------------------------------------------------
                    kubernetes:
                      {} # <-- REMOVE THIS, IF YOU INCLUDE VALUES UNDER THIS SECTION!

                    ## --------------------------------------------------------------------------------
                    ##                              deploykf-dependencies
                    ## --------------------------------------------------------------------------------
                    deploykf_dependencies:
        
                      ## --------------------------------------
                      ##             cert-manager
                      ## --------------------------------------
                      cert_manager:
                        {} # <-- REMOVE THIS, IF YOU INCLUDE VALUES UNDER THIS SECTION!
        
                      ## --------------------------------------
                      ##                 istio
                      ## --------------------------------------
                      istio:
                        {} # <-- REMOVE THIS, IF YOU INCLUDE VALUES UNDER THIS SECTION!
        
                      ## --------------------------------------
                      ##                kyverno
                      ## --------------------------------------
                      kyverno:
                        {} # <-- REMOVE THIS, IF YOU INCLUDE VALUES UNDER THIS SECTION!
        
                    ## --------------------------------------------------------------------------------
                    ##                                  deploykf-core
                    ## --------------------------------------------------------------------------------
                    deploykf_core:
        
                      ## --------------------------------------
                      ##             deploykf-auth
                      ## --------------------------------------
                      deploykf_auth:
                        {} # <-- REMOVE THIS, IF YOU INCLUDE VALUES UNDER THIS SECTION!
        
                      ## --------------------------------------
                      ##        deploykf-istio-gateway
                      ## --------------------------------------
                      deploykf_istio_gateway:
                        {} # <-- REMOVE THIS, IF YOU INCLUDE VALUES UNDER THIS SECTION!
        
                      ## --------------------------------------
                      ##      deploykf-profiles-generator
                      ## --------------------------------------
                      deploykf_profiles_generator:
                        {} # <-- REMOVE THIS, IF YOU INCLUDE VALUES UNDER THIS SECTION!
        
                    ## --------------------------------------------------------------------------------
                    ##                                   deploykf-opt
                    ## --------------------------------------------------------------------------------
                    deploykf_opt:
        
                      ## --------------------------------------
                      ##            deploykf-minio
                      ## --------------------------------------
                      deploykf_minio:
                        {} # <-- REMOVE THIS, IF YOU INCLUDE VALUES UNDER THIS SECTION!
        
                      ## --------------------------------------
                      ##            deploykf-mysql
                      ## --------------------------------------
                      deploykf_mysql:
                        {} # <-- REMOVE THIS, IF YOU INCLUDE VALUES UNDER THIS SECTION!
        
                    ## --------------------------------------------------------------------------------
                    ##                                  kubeflow-tools
                    ## --------------------------------------------------------------------------------
                    kubeflow_tools:
        
                      ## --------------------------------------
                      ##                 katib
                      ## --------------------------------------
                      katib:
                        {} # <-- REMOVE THIS, IF YOU INCLUDE VALUES UNDER THIS SECTION!
        
                      ## --------------------------------------
                      ##               notebooks
                      ## --------------------------------------
                      notebooks:
                        {} # <-- REMOVE THIS, IF YOU INCLUDE VALUES UNDER THIS SECTION!
        
                      ## --------------------------------------
                      ##               pipelines
                      ## --------------------------------------
                      pipelines:
                        {} # <-- REMOVE THIS, IF YOU INCLUDE VALUES UNDER THIS SECTION!
        
          destination:
            server: "https://kubernetes.default.svc"
            namespace: "argocd"
        ```

    ??? step "Step 4 - Read Values from Git <small>(optional)</small>"

        You may use the `values_files` parameter to read values from a git repo.
        This lets you version your values files in git, and easily update them without changing the app-of-apps resource.

        ---

        !!! danger

            We __STRONGLY RECOMMEND__ using a __PRIVATE__ repo for your values files!

        If your git repo is private, you must [configure ArgoCD](https://argo-cd.readthedocs.io/en/stable/user-guide/private-repositories/) with credentials to access the repo.
        For example, when using a GitHub repo, you might create a Secret with a [Personal Access Token (PAT)](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens) as follows:

        ```bash
        # create a secret with your GitHub credentials
        # NOTE: kubectl can't create and label a secret in one command, so we use a pipe
        kubectl create secret generic --dry-run=client -o yaml \
            "argocd-repository--MY_GITHUB_REPO" \
            --namespace "argocd" \
            --from-literal=type="git" \
            --from-literal=url="https://github.com/MY_GITHUB_ORG/MY_GITHUB_REPO.git" \
            --from-literal=username="MY_GITHUB_USERNAME" \
            --from-literal=password="MY_GITHUB_PAT" \
          | kubectl label --local --dry-run=client -o yaml -f - \
            "argocd.argoproj.io/secret-type"="repository" \
          | kubectl apply -f -
        ```

        ---

        If you use the upstream `sample-values.yaml` as a base, you will also need to push that file to your repo.

        The following command will download the [`sample-values.yaml`](https://github.com/deployKF/deployKF/blob/v{{ latest_deploykf_version }}/sample-values.yaml) file for deployKF `{{ latest_deploykf_version }}`:

        ```bash
        # download the `sample-values.yaml` file
        curl -fL -o "sample-values-{{ latest_deploykf_version }}.yaml" \
          "https://raw.githubusercontent.com/deployKF/deployKF/v{{ latest_deploykf_version }}/sample-values.yaml"
        ```

        ---

        For example, say you now have the following files in your repo:

        - `sample-values-{{ latest_deploykf_version }}.yaml`
        - `values-1.yaml`
        - `values-2.yaml`

        Your app-of-apps resource may then be updated to look like this:

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
          project: "default"
          source:

            ## source git repo configuration
            ##
            repoURL: "https://github.com/MY_GITHUB_ORG/MY_GITHUB_REPO.git"
            targetRevision: "main"
            path: "."
        
            ## plugin configuration
            ##
            plugin:
              name: "deploykf"
              parameters:
        
                ## the deployKF generator version
                ##
                - name: "source_version"
                  string: "{{ latest_deploykf_version }}"
        
                ## paths to values files within the `repoURL` repository
                ##
                - name: "values_files"
                  array:
                    - "./sample-values-{{ latest_deploykf_version }}.yaml"
                    - "./values-1.yaml"
                    - "./values-2.yaml"

                ## a string containing the contents of a values file
                ##  - this parameter allows defining values without needing to create a file in the repo
                ##  - these values are merged with higher precedence than those defined in `values_files`
                ##
                #- name: "values"
                #  string: |
                #    ...
                #    values file contents
                #    ...
        
          destination:
            server: "https://kubernetes.default.svc"
            namespace: "argocd"
        ```

    ??? step "Step 5 - Apply App-of-Apps Resource"

        Apply the `deploykf-app-of-apps.yaml` file to your cluster with the following command:

        ```bash
        kubectl apply -f ./deploykf-app-of-apps.yaml
        ```

=== "Manifests Repo Mode"

    ??? step "Step 1 - Prepare ArgoCD"

        If you have not already deployed ArgoCD on your cluster, you will need to do so.
        <br>
        Please see the [ArgoCD Getting Started Guide](https://argo-cd.readthedocs.io/en/stable/getting_started/) for instructions.

        __TIP:__ If you use an ArgoCD "management cluster" pattern, see the [off-cluster ArgoCD](./dependencies/argocd.md#can-i-use-an-off-cluster-argocd) guide.
      
    ??? step "Step 2 - Install the deployKF CLI"

        If you have not already installed the `deploykf` CLI on your local machine, you will need to do so.

        Please see the [CLI Installation Guide](deploykf-cli.md#install-the-cli) for instructions.

    ??? step "Step 3 - Prepare a Git Repo"

        You will need to create a git repo to store your generated manifests.

        !!! danger

            We __STRONGLY RECOMMEND__ using a __PRIVATE__ repo for your manifests!

        If your git repo is private, you must [configure ArgoCD](https://argo-cd.readthedocs.io/en/stable/user-guide/private-repositories/) with credentials to access the repo.
        For example, when using a GitHub repo, you might create a Secret with a [Personal Access Token (PAT)](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens) as follows:

        ```bash
        # create a secret with your GitHub credentials
        # NOTE: kubectl can't create and label a secret in one command, so we use a pipe
        kubectl create secret generic --dry-run=client -o yaml \
            "argocd-repository--MY_GITHUB_REPO" \
            --namespace "argocd" \
            --from-literal=type="git" \
            --from-literal=url="https://github.com/MY_GITHUB_ORG/MY_GITHUB_REPO.git" \
            --from-literal=username="MY_GITHUB_USERNAME" \
            --from-literal=password="MY_GITHUB_PAT" \
          | kubectl label --local --dry-run=client -o yaml -f - \
            "argocd.argoproj.io/secret-type"="repository" \
          | kubectl apply -f -
        ```

    ??? step "Step 4 - Create Values Files"

        deployKF is configured by [centralized values](./values.md) which define the desired state of the platform.

        ---

        <h4>Sample Values:</h4>

        Each version of deployKF has [sample values](./values.md#sample-values) with all [ML & Data tools](../reference/tools.md#tool-index) enabled, along with some sensible security defaults.
        We recommend using the sample values as a starting point for your custom values.

        The following command will download the [`sample-values.yaml`](https://github.com/deployKF/deployKF/blob/v{{ latest_deploykf_version }}/sample-values.yaml) file for deployKF `{{ latest_deploykf_version }}`:

        ```bash
        # download the `sample-values.yaml` file
        curl -fL -o "sample-values-{{ latest_deploykf_version }}.yaml" \
          "https://raw.githubusercontent.com/deployKF/deployKF/v{{ latest_deploykf_version }}/sample-values.yaml"
        ```

        ---

        <h4>Custom Values:</h4>

        In _Manifests Repo Mode_, values are passed to the `deploykf generate` command as YAML files.
        When a value is defined in multiple files, the result is calculated by [merging](./values.md#merging-values), with files listed later taking precedence.

        To make upgrades easier, we recommend using the sample values as a base, and applying custom override files with _only the values you want to change_.
        This allows you to swap out the sample values for a newer version in the future.

        !!! tip

            Learn about common configuration tasks in the [:star: __Configure deployKF__ :star:](./configs.md) guide.

        For example, you might structure your `custom-overrides.yaml` file like this:

        ```yaml
        ##
        ## Notes:
        ##  - YAML maps are RECURSIVELY merged across values files
        ##  - YAML lists are REPLACED in their entirety across values files
        ##  - Do NOT include empty/null sections, as this will remove ALL values from that section.
        ##    To include a section without overriding any values, set it to an empty map: `{}`
        ##

        ## --------------------------------------------------------------------------------
        ##                                      argocd
        ## --------------------------------------------------------------------------------
        argocd:
          namespace: argocd
          project: default

          source:
            ## the git repo where you will store your generated manifests
            ##  - url: the URL of the git repo
            ##  - revision: the git branch/tag/commit to read from
            ##  - path: the repo folder path where the generated manifests are stored
            ##
            repo:
              url: "https://github.com/deployKF/examples.git"
              revision: "main"
              path: "./GENERATOR_OUTPUT/"

        ## --------------------------------------------------------------------------------
        ##                                    kubernetes
        ## --------------------------------------------------------------------------------
        kubernetes:
          {} # <-- REMOVE THIS, IF YOU INCLUDE VALUES UNDER THIS SECTION!

        ## --------------------------------------------------------------------------------
        ##                              deploykf-dependencies
        ## --------------------------------------------------------------------------------
        deploykf_dependencies:

          ## --------------------------------------
          ##             cert-manager
          ## --------------------------------------
          cert_manager:
            {} # <-- REMOVE THIS, IF YOU INCLUDE VALUES UNDER THIS SECTION!

          ## --------------------------------------
          ##                 istio
          ## --------------------------------------
          istio:
            {} # <-- REMOVE THIS, IF YOU INCLUDE VALUES UNDER THIS SECTION!

          ## --------------------------------------
          ##                kyverno
          ## --------------------------------------
          kyverno:
            {} # <-- REMOVE THIS, IF YOU INCLUDE VALUES UNDER THIS SECTION!

        ## --------------------------------------------------------------------------------
        ##                                  deploykf-core
        ## --------------------------------------------------------------------------------
        deploykf_core:

          ## --------------------------------------
          ##             deploykf-auth
          ## --------------------------------------
          deploykf_auth:
            {} # <-- REMOVE THIS, IF YOU INCLUDE VALUES UNDER THIS SECTION!

          ## --------------------------------------
          ##        deploykf-istio-gateway
          ## --------------------------------------
          deploykf_istio_gateway:
            {} # <-- REMOVE THIS, IF YOU INCLUDE VALUES UNDER THIS SECTION!

          ## --------------------------------------
          ##      deploykf-profiles-generator
          ## --------------------------------------
          deploykf_profiles_generator:
            {} # <-- REMOVE THIS, IF YOU INCLUDE VALUES UNDER THIS SECTION!

        ## --------------------------------------------------------------------------------
        ##                                   deploykf-opt
        ## --------------------------------------------------------------------------------
        deploykf_opt:

          ## --------------------------------------
          ##            deploykf-minio
          ## --------------------------------------
          deploykf_minio:
            {} # <-- REMOVE THIS, IF YOU INCLUDE VALUES UNDER THIS SECTION!

          ## --------------------------------------
          ##            deploykf-mysql
          ## --------------------------------------
          deploykf_mysql:
            {} # <-- REMOVE THIS, IF YOU INCLUDE VALUES UNDER THIS SECTION!

        ## --------------------------------------------------------------------------------
        ##                                  kubeflow-tools
        ## --------------------------------------------------------------------------------
        kubeflow_tools:

          ## --------------------------------------
          ##                 katib
          ## --------------------------------------
          katib:
            {} # <-- REMOVE THIS, IF YOU INCLUDE VALUES UNDER THIS SECTION!

          ## --------------------------------------
          ##               notebooks
          ## --------------------------------------
          notebooks:
            {} # <-- REMOVE THIS, IF YOU INCLUDE VALUES UNDER THIS SECTION!

          ## --------------------------------------
          ##               pipelines
          ## --------------------------------------
          pipelines:
            {} # <-- REMOVE THIS, IF YOU INCLUDE VALUES UNDER THIS SECTION!
        ```

    ??? step "Step 5 - Generate Manifests"

        The `deploykf generate` command writes manifests into a folder based on your values.
        When more than one `--values` file is provided, they are [merged](./values.md#merging-values), with later files taking precedence.

        For example, to generate manifests using [deployKF version](#deploykf-versions) `{{ latest_deploykf_version }}` under `./GENERATOR_OUTPUT/`:
    
        ```shell
        deploykf generate \
            --source-version "{{ latest_deploykf_version }}" \
            --values ./sample-values-{{ latest_deploykf_version }}.yaml \
            --values ./custom-overrides.yaml \
            --output-dir ./GENERATOR_OUTPUT
        ```

        !!! warning "Do NOT Edit Manifests Directly"
        
            In general, you should NOT edit the manifests generated by deployKF.
            Changes in the `--output-dir` will be __overwritten__ each time the `deploykf generate` command runs.

            If you need to change something which is not configurable via values, please [raise an issue](https://github.com/deployKF/deployKF/issues) so we can understand your use-case and potentially add a new configuration option.

    ??? step "Step 6 - Commit Generated Manifests"

        After running `deploykf generate`, you will need to commit the manifests to your repo, so ArgoCD can apply them to your cluster:

        ```shell
        # for example, to directly commit changes to the 'main' branch of your repo
        git add GENERATOR_OUTPUT
        git commit -m "my commit message"
        git push origin main
        ```

    ??? step "Step 7 - Apply App-of-Apps Manifest"

        The only manifest you need to manually apply is the [app-of-apps](https://argo-cd.readthedocs.io/en/stable/operator-manual/cluster-bootstrapping/#app-of-apps-pattern), which creates all the other ArgoCD applications.

        The `app-of-apps.yaml` manifest is generated at the root of your `--output-dir` folder, so you can apply it with:
        
        ```shell
        kubectl apply --filename GENERATOR_OUTPUT/app-of-apps.yaml
        ```

### __:star: Sync ArgoCD Applications :star:__

Now that your deployKF app-of-apps has been applied, you must sync the ArgoCD applications to deploy your platform.
Syncing an application will cause ArgoCD to reconcile the actual state in the cluster, to match the state defined by the application resource.

!!! danger

    __DO NOT__ sync all the `Applications` at once!!!

    The deployKF `Applications` depend on each other, they MUST be synced in the correct order to avoid errors.
    If you manually sync them all, you may need to [uninstall](./uninstall.md) and start over.

There are a few ways to sync the applications, you only need to use ONE of them.

=== ":star: Sync: Automated Script :star:"

    The recommended way to sync the applications is with the automated script.
    
    ??? step "Step - Run the Sync Script"

        We provide the [`sync_argocd_apps.sh`](https://github.com/deployKF/deployKF/blob/main/scripts/sync_argocd_apps.sh) script to automatically sync the applications that make up deployKF.
        Learn more about the automated sync script from the [`scripts` folder README](https://github.com/deployKF/deployKF/tree/main/scripts) .
    
        For example, to run the script, you might use the following commands:

        ```bash
        # clone the deploykf repo
        # NOTE: we use 'main', as the latest script always lives there
        git clone -b main https://github.com/deployKF/deployKF.git ./deploykf
        
        # ensure the script is executable
        chmod +x ./deploykf/scripts/sync_argocd_apps.sh
        
        # run the script
        bash ./deploykf/scripts/sync_argocd_apps.sh
        ```

        ---
    
        !!! note "About the sync script"
        
            - The script can take around 5-10 minutes to run on first install.
            - If the script fails or is interrupted, you can safely re-run it, and it will pick up where it left off.
            - There are a number of configuration variables at the top of the script which change the default behavior.
            - Learn more about the automated sync script from the [`scripts` folder README](https://github.com/deployKF/deployKF/tree/main/scripts) in the deployKF repo.
    
            Please be aware of the following issue when using the automated sync script:
            
            ??? bug "Bug in ArgoCD v2.9"
            
                There is a known issue ([`deploykf/deploykf#70`](https://github.com/deployKF/deployKF/issues/70), [`argoproj/argo-cd#16266`](https://github.com/argoproj/argo-cd/issues/16266)) with all `2.9.X` versions of the ArgoCD CLI that will cause the sync script to fail with the following error:
            
                ```text
                ==========================================================================================
                Logging in to ArgoCD...
                ==========================================================================================
                FATA[0000] cannot find pod with selector: [app.kubernetes.io/name=] - use the --{component}-name flag in this command or set the environmental variable (Refer to https://argo-cd.readthedocs.io/en/stable/user-guide/environment-variables), to change the Argo CD component name in the CLI
                ```
            
                Please upgrade your `argocd` CLI to at least version `2.10.0` to resolve this issue.

=== "Sync: ArgoCD Web UI"

    Alternatively, you can sync the applications using the ArgoCD Web UI.

    ??? step "Step 1 - Access ArgoCD Web UI"

        For production usage, you may want to [expose ArgoCD with a `LoadBalancer` or `Ingress`](https://argo-cd.readthedocs.io/en/stable/getting_started/#3-access-the-argo-cd-api-server).

        For testing, you may use `kubectl` port-forwarding to expose the ArgoCD Web UI on your local machine:

        ```shell
        kubectl port-forward --namespace "argocd" svc/argocd-server 8090:https
        ```

        The ArgoCD Web UI should now be available at the following URL:

          :material-arrow-right-bold: [https://localhost:8090](https://localhost:8090)

        ---

        If this is the first time you are using ArgoCD, you will need to retrieve the initial password for the `admin` user:
        
        ```shell
        echo $(kubectl -n argocd get secret/argocd-initial-admin-secret \
          -o jsonpath="{.data.password}" | base64 -d)
        ```

        Once you log in with the `admin` user and above password, the Web UI should look like this:
    
        ![ArgoCD Web UI (Dark Mode)](../assets/images/argocd-ui-DARK.png#only-dark)
        ![ArgoCD Web UI (Light Mode)](../assets/images/argocd-ui-LIGHT.png#only-light)

    ??? step "Step 2 - Sync Applications"

        You MUST sync the deployKF applications in the correct order.
        For each application, click the `SYNC` button, and wait for the application to become "Healthy" before syncing the next.

        The applications are grouped and ordered as follows:
    
        !!! stack "Group 0: "app-of-apps""
        
            First, you must sync the app-of-apps application:
    
            1. `deploykf-app-of-apps`
            2. `deploykf-namespaces` (only exists when using [off-cluster ArgoCD](./dependencies/argocd.md#can-i-use-an-off-cluster-argocd))
    
        !!! stack "Group 1: "deploykf-dependencies""
        
            Second, you must sync the applications with the label `app.kubernetes.io/component=deploykf-dependencies`:
    
            1. `dkf-dep--cert-manager` (may fail on first attempt)
            2. `dkf-dep--istio`
            3. `dkf-dep--kyverno`
    
            __WARNING:__ for this group, each application MUST be synced INDIVIDUALLY and the preceding application MUST be "Healthy" before syncing the next.
    
        !!! stack "Group 2: "deploykf-core""
    
            Third, you must sync the applications with the label `app.kubernetes.io/component=deploykf-core`:
    
            1. `dkf-core--deploykf-istio-gateway`
            2. `dkf-core--deploykf-auth`
            3. `dkf-core--deploykf-dashboard`
            4. `dkf-core--deploykf-profiles-generator` (may fail on first attempt)
    
        !!! stack "Group 3: "deploykf-opt""
    
            Fourth, you must sync the applications with the label `app.kubernetes.io/component=deploykf-opt`:
    
            - `dkf-opt--deploykf-minio`
            - `dkf-opt--deploykf-mysql`
    
        !!! stack "Group 4: "deploykf-tools""
    
            Fifth, you must sync the applications with the label `app.kubernetes.io/component=deploykf-tools`:
    
            - (none yet)
    
        !!! stack "Group 5: "kubeflow-dependencies""
    
            Sixth, you must sync the applications with the label `app.kubernetes.io/component=kubeflow-dependencies`:
    
            - `kf-dep--argo-workflows`
    
        !!! stack "Group 6: "kubeflow-tools""
    
            Seventh, you must sync the applications with the label `app.kubernetes.io/component=kubeflow-tools`:
    
            - `kf-tools--katib`
            - `kf-tools--notebooks--jupyter-web-app`
            - `kf-tools--notebooks--notebook-controller`
            - `kf-tools--pipelines`
            - `kf-tools--poddefaults-webhook`
            - `kf-tools--tensorboards--tensorboard-controller`
            - `kf-tools--tensorboards--tensorboards-web-app`
            - `kf-tools--training-operator`
            - `kf-tools--volumes--volumes-web-app`

---

## 4. Use the Platform

Now that you have a working deployKF machine learning platform, here are some things to try out!

### __:star: Expose the deployKF Dashboard :star:__

The _deployKF dashboard_ is the web-based interface for deployKF, it gives users authenticated access to tools like [Kubeflow Pipelines](../reference/tools.md#kubeflow-pipelines), [Kubeflow Notebooks](../reference/tools.md#kubeflow-notebooks), and [Katib](../reference/tools.md#katib).

![deployKF Dashboard (Dark Mode)](../assets/images/deploykf-dashboard-DARK.png#only-dark)
![deployKF Dashboard (Light Mode)](../assets/images/deploykf-dashboard-LIGHT.png#only-light)

All public deployKF services (including the dashboard) are accessed via the deployKF Istio Gateway, you will need to expose its Kubernetes Service.

??? step "Step 1 - Expose the Gateway"

    You may expose the deployKF Istio Gateway Service in a number of ways:
    
    - [Expose with: `kubectl port-forward`](./platform/deploykf-gateway.md#use-kubectl-port-forward) <small>(for local testing only)</small>
    - [Expose with: `LoadBalancer` Service](./platform/deploykf-gateway.md#use-a-loadbalancer-service)
    - [Expose with: `Ingress`](./platform/deploykf-gateway.md#use-a-kubernetes-ingress)

??? step "Step 2 - Configure DNS"

    Trying to access deployKF with an IP address will __NOT__ work, you __MUST__ use a domain name.

    See [Configure DNS Records](./platform/deploykf-gateway.md#configure-dns-records) for more information.

    !!! danger ""

        This step is __REQUIRED__, you __MUST__ configure DNS records or local `/etc/hosts` entries.

??? step "Step 3 - Configure TLS <small>(optional)</small>"

    We recommend configuring valid TLS/HTTPS certificates to avoid browser warnings for your users.

    See the [Configure TLS Certificates](./platform/deploykf-gateway.md#configure-tls-certificates) guide for more information.

    !!! tip ""

        If you want to configure TLS later, just skip this step for now.
        <br>
        We use a self-signed certificate by default.

??? step "Step 4 - User Authentication <small>(optional)</small>"

    See the following guides to configure user authentication on your platform:

    - [External Identity Providers](./platform/deploykf-authentication.md#external-identity-providers)
    - [Static User/Password Combinations](./platform/deploykf-authentication.md#static-userpassword-combinations)

    !!! tip ""

        If you want to configure authentication later, just skip this step for now.
        <br>
        We provide a few static credentials by default.

??? step "Step 5 - Define Profiles <small>(optional)</small>"

    deployKF uses the concept of "Profiles" to group users and resources together.
    You might define profiles for different teams, projects, or even individual users.

    See the [User Authorization and Profile Management](./platform/deploykf-profiles.md) guide for more information.

    !!! tip ""

        If you want to define profiles later, just skip this step for now.
        <br>
        We provide default profiles named `team-1` and `team-1-prod`.

??? step "Step 6 - Log In"

    You should now be presented with a "Log In" screen when you visit the exposed URL.

    !!! danger ""

        Remember, you can __NOT__ access deployKF with an IP address, you __MUST__ use a domain name.

    ---

    By default, there are a few static credentials set by the [`deploykf_core.deploykf_auth.dex.staticPasswords`](https://github.com/deployKF/deployKF/blob/v0.1.4/generator/default_values.yaml#L469-L492) value:

    ??? key "Credentials: User 1"

        __Username:__ `user1@example.com`
        <br>
        __Password:__ `user1`

        - This account has [write access to `team-1` profile](https://github.com/deployKF/deployKF/blob/v0.1.2/generator/default_values.yaml#L830-L833).
        - This account has [read access to `team-1-prod`](https://github.com/deployKF/deployKF/blob/v0.1.2/generator/default_values.yaml#L837-L840).

    ??? key "Credentials: User 2"

        __Username:__ `user2@example.com`
        <br>
        __Password:__ `user2`

        - This account has [write access to `team-1` profile](https://github.com/deployKF/deployKF/blob/v0.1.2/generator/default_values.yaml#L830-L833).
        - This account has [read access to `team-1-prod`](https://github.com/deployKF/deployKF/blob/v0.1.2/generator/default_values.yaml#L837-L840).

    ??? key "Credentials: Admin <small>(DO NOT USE - will be removed in future versions)</small>"

        __Username:__ `admin@example.com`
        <br>
        __Password:__ `admin`

        - This account is the [default "owner"](https://github.com/deployKF/deployKF/blob/v0.1.2/generator/default_values.yaml#L688-L694) of all profiles.
        - This account does NOT have access to "MinIO Console" or "Argo Server UI".
        - We recommend NOT using this account, and actually removing its [`staticPasswords` entry](https://github.com/deployKF/deployKF/blob/v0.1.2/generator/default_values.yaml#L394-L396).
        - We recommend leaving this account as the default "owner", even with `@example.com` as the domain (because profile owners can't be changed).

??? step "Step 7 - Explore the Tools"

    deployKF includes many tools which address different stages of the data & machine learning lifecycle:
    
    - [Kubeflow Pipelines](../reference/tools.md#kubeflow-pipelines)
    - [Kubeflow Notebooks](../reference/tools.md#kubeflow-notebooks)
    - [Other Tools](../reference/tools.md#tool-index)

    We also provide a number of user-focused guides for these tools:
  
    <table markdown="span">
      <tr>
        <th>Tool</th>
        <th>User Guide</th>
      </tr>
      <tr markdown>
        <td markdown>Kubeflow Pipelines</td>
        <td markdown>[Access Kubeflow Pipelines API](../user-guides/access-kubeflow-pipelines-api.md)</td>
      </tr>
      <tr markdown>
        <td markdown>Kubeflow Pipelines</td>
        <td markdown>[GitOps for Kubeflow Pipelines Schedules](../user-guides/gitops-for-kubeflow-pipelines.md)</td>
      </tr>
    </table>

## Next Steps

- [:material-account-group: Join the deployKF community!](../about/community.md)
- [:star: Support us with a star on GitHub!](https://github.com/deployKF/deployKF)
- [<span style="color: #ff1f1f">:material-hospital-box:</span> Get support from our experts!](../about/support.md)