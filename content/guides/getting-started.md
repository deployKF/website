---
icon: material/rocket-launch
description: >-
  Learn how to build a data and machine learning platform on any Kubernetes cluster with deployKF.
  Use our powerful Helm-like interface to deploy Kubeflow and other MLOps tools with ease.
---

# Getting Started

Learn how to build a __data and machine learning platform__ on __any Kubernetes cluster__ with deployKF.
Use our powerful Helm-like interface to deploy Kubeflow and other MLOps tools with ease.

!!! tip "Other Resources"

    - [__Local Quickstart__](local-quickstart.md) - try deployKF on your local machine
    - [__Migrate from Kubeflow Distributions__](kubeflow-distributions.md) - how and why to migrate from other Kubeflow distributions

---

## Introduction

To learn about :custom-deploykf-color: <strong><span class="deploykf-orange">deploy</span><span class="deploykf-blue">KF</span></strong> and why you should use it, see the [introduction](../about/introduction.md) page.

[Read Introduction<br>:material-lightbulb-on:](../about/introduction.md#about-deploykf){ .md-button .md-button--primary }
[Watch Introduction<br>:material-youtube:](../about/introduction.md#video-introduction){ .md-button .md-button--primary }

## Modes of Operation

deployKF has two "modes of operation" that change how Kubernetes manifests are generated and applied to your cluster.

Mode | Description | Notes
--- | --- | ---
[ArgoCD Plugin Mode](#argocd-plugin-mode) | The [`deployKF ArgoCD Plugin`](./dependencies/argocd.md#what-is-the-deploykf-argocd-plugin) adds a new kind of [ArgoCD Application](./dependencies/argocd.md#argo-cd-applications) which understands deployKF config values and can generate manifests directly, without requiring a git repo.<br><br><small>:star: __The best option for most organizations__. :star:</small> | Even though manifests do not require a git repo, config values can still be managed using GitOps.<br><br>Requires ArgoCD Pods have access to the internet, so they can download the deployKF generator zip from GitHub.
[Manifests Repo Mode](#manifests-repo-mode) | The [`deployKF CLI`](deploykf-cli.md) is used to generate manifests which are committed to a git repo for ArgoCD to apply to your cluster. | For organizations which require that Kubernetes manifests are committed to a git repo before being applied (e.g. for auditing or compliance reasons).

## 1. Requirements

This guide assumes you have an existing Kubernetes cluster, and are familiar with the basics of Kubernetes.
To try deployKF on your local machine, please see the [Local Quickstart](local-quickstart.md).

### Kubernetes Cluster

deployKF can run on any [:custom-kubernetes-color: __Kubernetes__](https://kubernetes.io/) cluster, in any cloud or local environment.
See our [version matrix](../releases/version-matrix.md#deploykf-dependencies) for a list of supported Kubernetes versions.

Here are some of the Kubernetes distributions which are supported by deployKF:

Platform | Kubernetes Distribution
--- | ---
Amazon Web Services | [Amazon Elastic Kubernetes Service (EKS)](https://aws.amazon.com/eks/)
Microsoft Azure | [Azure Kubernetes Service (AKS)](https://azure.microsoft.com/en-us/products/kubernetes-service/)<sup>[[:material-alert: see special requirements :material-alert:](https://github.com/deployKF/deployKF/issues/61#issuecomment-1949658332)]</sup> 
Google Cloud | [Google Kubernetes Engine (GKE)](https://cloud.google.com/kubernetes-engine)
IBM Cloud | [IBM Cloud Kubernetes Service (IKS)](https://www.ibm.com/cloud/kubernetes-service)
Self-Hosted | [Rancher Kubernetes Engine (RKE)](https://rancher.com/docs/rke/latest/en/),<br>[Canonical Kubernetes (MicroK8s)](https://microk8s.io/)
Local Machine | [k3d](https://k3d.io/), [kind](https://kind.sigs.k8s.io/), [minikube](https://minikube.sigs.k8s.io/)

!!! warning "Dedicated Kubernetes Cluster"

    Only __ONE__ deployKF platform can be on a Kubernetes cluster at a time.

    Additionally, deployKF is not well suited to multi-tenant clusters.
    It uses cluster-wide components (e.g. Istio) and Namespaces for profiles.
    We strongly recommend __using a dedicated cluster__ for deployKF.

    If you are unable to create a new Kubernetes cluster, you may consider using [vCluster](https://github.com/loft-sh/vcluster) to create a virtual Kubernetes cluster within an existing one.

### Kubernetes Configurations

The following Kubernetes configurations are required for deployKF to work correctly:

!!! info "CPU Architecture"

    deployKF requires `x86_64` CPU Architecture, `ARM64` clusters are NOT currently supported.

    The next minor version of deployKF (`v0.2.0`) should have native `ARM64` for all core components.
    However, some upstream apps like _Kubeflow Pipelines_ will need extra work to be production ready ([`#10309`](https://github.com/kubeflow/pipelines/issues/10309), [`#10308`](https://github.com/kubeflow/pipelines/issues/10308)).

!!! info "Cluster Domain"

    deployKF requires the Kubernetes kubelet [`clusterDomain`](https://kubernetes.io/docs/reference/config-api/kubelet-config.v1beta1/#kubelet-config-k8s-io-v1beta1-KubeletConfiguration) be left as the default of `cluster.local`.
    This is caused by a small number of Kubeflow components hard-coding this value, with no way to change it.

!!! info "Service Type"

    By default, deployKF uses a `LoadBalancer` service type for the _Istio Ingress Gateway_.
    Take care to ensure this does not accidentally expose your platform to the public internet.

    ??? question_secondary "How can I use a different Service Type?"
    
        To use a different service type, you can override the `deploykf_core.deploykf_istio_gateway.gatewayService.type` value:

        ```yaml
        deploykf_core:
          deploykf_istio_gateway:
            gatewayService:
              type: "NodePort" # or "ClusterIP"
        ```

        For real-world usage, you should review the [Expose Gateway and configure HTTPS](./platform/deploykf-gateway.md) guide.

!!! info "Default StorageClass"

    By default, deployKF assumes your Kubernetes cluster has a default [`StorageClass`](https://kubernetes.io/docs/concepts/storage/storage-classes/) which has support for the `ReadWriteOnce` access mode.

    ??? question_secondary "What if I don't have a default StorageClass?"
    
        If you do NOT have a compatible default StorageClass, you might consider the following options:
    
        1. Configure [a default StorageClass](https://kubernetes.io/docs/tasks/administer-cluster/change-default-storage-class/) that has `ReadWriteOnce` support
        2. Explicitly set the `storageClass` value for the following components:
             - [`deploykf_opt.deploykf_minio.persistence.storageClass`](https://github.com/deployKF/deployKF/blob/v0.1.1/generator/default_values.yaml#L901-L905)
             - [`deploykf_opt.deploykf_mysql.persistence.storageClass`](https://github.com/deployKF/deployKF/blob/v0.1.1/generator/default_values.yaml#L1036-L1040)
        2. Disable components which require the StorageClass, and use external alternatives:
             - [`deploykf_opt.deploykf_minio.enabled`](https://github.com/deployKF/deployKF/blob/v0.1.1/generator/default_values.yaml#L853)
             - [`deploykf_opt.deploykf_mysql.enabled`](https://github.com/deployKF/deployKF/blob/v0.1.1/generator/default_values.yaml#L993)

### ArgoCD Configuration

deployKF requires [:custom-argocd-color: __Argo CD__](./dependencies/argocd.md#what-is-argo-cd) to manage lifecycle and state ([learn why](./dependencies/argocd.md#how-does-deploykf-use-argo-cd)).
See our [version matrix](../releases/version-matrix.md#deploykf-dependencies) for a list of supported Argo CD versions.
How you configure ArgoCD depends on which ["mode of operation"](#modes-of-operation) you have chosen.

The following table lists the requirements in each mode:

=== "ArgoCD Plugin Mode :star:"

    Requirement | Guides
    --- | ---
    ArgoCD installed | [Install ArgoCD](https://argo-cd.readthedocs.io/en/stable/getting_started/)<br>[Install ArgoCD (+ Plugin)](https://github.com/deployKF/deployKF/tree/main/argocd-plugin#install-plugin---new-argocd)
    deployKF ArgoCD Plugin | [Install Plugin](https://github.com/deployKF/deployKF/tree/main/argocd-plugin#install-plugin---existing-argocd)<br>[Install Plugin (+ ArgoCD)](https://github.com/deployKF/deployKF/tree/main/argocd-plugin#install-plugin---new-argocd)

=== "Manifests Repo Mode"

    Requirement | Guides
    --- | ---
    ArgoCD installed | [Install ArgoCD](https://argo-cd.readthedocs.io/en/stable/getting_started/)
    _deployKF CLI_ installed locally | [Install deployKF CLI](deploykf-cli.md)
    A private git repo | Used to store generated manifests.

!!! tip

    If you are unsure which mode to use, we recommend the _ArgoCD Plugin Mode_.

### Cluster Dependencies

deployKF uses a number of cluster-level dependencies which are __installed by default__.
If you have an existing version of a dependency, deployKF can be configured to use it instead.

The following table lists these dependencies and how to use an existing version:

Dependency | Purpose | Guides
--- | --- | ---
Cert-Manager | Generating and maintaining TLS/HTTPS certificates. | [What is Cert-Manager?](./dependencies/cert-manager.md) / [Use my existing Cert-Manager.](./dependencies/cert-manager.md#can-i-use-my-existing-cert-manager)
Istio | Network service mesh for the platform, used to enforce client authentication and secure internal traffic. | [What is Istio?](./dependencies/istio.md) / [Use my existing Istio.](./dependencies/istio.md#can-i-use-my-existing-istio)
Kyverno | Mutating resources, replicating secrets across namespaces, and restarting Pods when configs change. | <s>[What is Kyverno?](./dependencies/kyverno.md)</s> / <s>[Use my existing Kyverno.](./dependencies/kyverno.md#can-i-use-my-existing-kyverno)</s> (coming soon)

### Optional Dependencies

deployKF has some optional dependencies which may improve the performance or reliability of your platform in production.

Dependencies | Purpose | Guides
--- | --- | ---
MySQL Database | Used by [Kubeflow Pipelines](../reference/tools.md#kubeflow-pipelines) and [Katib](../reference/tools.md#katib).<br><br>The embedded MySQL is ONLY recommended for testing and development. In production, we ALWAYS recommend using an external MySQL database. | [Connect an External MySQL](./tools/external-mysql.md)
Object Store | Used by [Kubeflow Pipelines](../reference/tools.md#kubeflow-pipelines).<br><br>The embedded MinIO is ONLY recommended for testing and development. In production, we ALWAYS recommend using an external S3-compatible object store. | [Connect an External S3-like Object Store.](./tools/external-object-store.md)

## 2. Platform Configuration

All aspects of your deployKF platform are configured with YAML-based configs named "values".
There are a very large number of values (more than 1500), but as deployKF supports _in-place upgrades_ you can start with a few important ones, and then grow your values file over time.

### Create Values Files

We recommend using the [`sample-values.yaml`](https://github.com/deployKF/deployKF/blob/v{{ latest_deploykf_version }}/sample-values.yaml) file as a starting point for your values.
These sample values (which are different for each deployKF version) have all ML & Data tools enabled, along with some sensible security defaults.

You may copy and make changes to the sample values, or directly use it as a base, and override specific values in a separate file.
We provide the [`sample-values-overrides.yaml`](https://github.com/deployKF/deployKF/blob/v{{ latest_deploykf_version }}/sample-values-overrides.yaml) file as an example of this approach.

deployKF has many additional values not found in the sample files.
For your reference, ALL values and their defaults are listed on the [values reference](../reference/deploykf-values.md) page, which is generated from the full [`default_values.yaml`](https://github.com/deployKF/deployKF/blob/v{{ latest_deploykf_version }}/generator/default_values.yaml) file.

!!! note "YAML Syntax"

    For a refresher on YAML syntax, we recommend the following resources:
    
    - [Learn YAML in Y minutes](https://learnxinyminutes.com/docs/yaml/)
    - [YAML Multiline Strings](https://yaml-multiline.info/)

### Configuration Guides

deployKF is incredibly configurable, so we provide a number of guides to help you get started with common configuration tasks.

#### Platform Configuration

<table markdown="span">
  <tr>
    <th>Guide<br><small>(Click for Details)</small></th>
    <th>Description</th>
  </tr>
  <tr markdown>
    <td markdown>[User Authentication](./platform/deploykf-authentication.md)</td>
    <td>Integrate with your existing user authentication system (GitHub, Google, Okta, etc.) and define static user accounts.</td>
  </tr>
  <tr markdown>
    <td markdown>[User Authorization and Profile Management](./platform/deploykf-profiles.md)</td>
    <td>Manage user permissions by defining profiles and assigning users to them.</td>
  </tr>
  <tr markdown>
    <td markdown>[Expose Gateway and configure HTTPS](./platform/deploykf-gateway.md)</td>
    <td>Make deployKF available publicly and configure valid HTTPS certificates.</td>
  </tr>
  <tr markdown>
    <td markdown>[Customize the Dashboard](./platform/deploykf-dashboard.md)</td>
    <td>Customize the deployKF dashboard with your own branding and links.</td>
  </tr>
</table>

#### Tool Configuration

<table markdown="span">
  <tr>
    <th>Guide<br><small>(Click for Details)</small></th>
    <th>Description</th>
  </tr>
  <tr markdown>
    <td markdown>[Connect an external MySQL Database](./tools/external-mysql.md)</td>
    <td>Replace the embedded MySQL instance with a production-ready external database service.</td>
  </tr>
  <tr markdown>
    <td markdown>[Connect an external Object Store](./tools/external-object-store.md)</td>
    <td>Replace the embedded MinIO instance with an external S3-compatible object store.</td>
  </tr>
  <tr markdown>
    <td markdown>[Configure Kubeflow Notebooks](./tools/kubeflow-notebooks.md)</td>
    <td>Configure Kubeflow Notebooks with custom server images and compute resources, including GPUs.</td>
  </tr>
</table>

## 3. Platform Deployment

### About ArgoCD

Learn more _["about ArgoCD"](./dependencies/argocd.md#what-is-argo-cd)_ and _["how deployKF uses ArgoCD"](./dependencies/argocd.md#how-does-deploykf-use-argo-cd)_ on the dedicated page.

### deployKF Versions

Each deployKF "source version" may include different tools, and may support different versions of cluster dependencies.
The [version matrix](../releases/version-matrix.md) is a list of which tools and versions are supported by each deployKF release.

The [deployKF changelog](../releases/changelog-deploykf.md) gives detailed information about what has changed in each release, including important tips for upgrading.

!!! tip "Be notified about new releases"

    Be notified about new deployKF releases by watching the [`deployKF/deployKF`](https://github.com/deployKF/deployKF) repo on GitHub,
    at the top right, click `Watch` → `Custom` → `Releases` then confirm by selecting `Apply`.

### Generate & Apply Manifests

How you generate and apply the deployKF manifests to your Kubernetes cluster will depend on the [mode of operation](#modes-of-operation) you have chosen.

#### ArgoCD Plugin Mode

These steps show how to generate and apply manifests with the [ArgoCD Plugin Mode](#modes-of-operation):

??? steps "Generate & Apply Manifests - _ArgoCD Plugin Mode_ :star:"

    To generate and apply the manifests when using ["ArgoCD Plugin Mode"](#modes-of-operation), you will need to:

    1. install the [deployKF ArgoCD plugin](https://github.com/deployKF/deployKF/tree/main/argocd-plugin) on your ArgoCD instance
    2. create an app-of-apps which uses the plugin
    3. apply your app-of-apps manifest

    !!! warning "ArgoCD Internet Access"
    
        Default usage of the _deployKF ArgoCD Plugin_ requires that ArgoCD Pods have access to the internet, so they can download the deployKF generator zip from GitHub.

    ---
  
    __Step 1: Install the ArgoCD Plugin__

    We provide two options for installing the deployKF ArgoCD plugin:

    ??? config "Install Plugin - New ArgoCD"

        This method installs our pre-patched ArgoCD manifests with the plugin pre-installed.
        Use this method if you are installing ArgoCD for the first time.

        For specific information, see the [Install Plugin - New ArgoCD](https://github.com/deployKF/deployKF/tree/main/argocd-plugin#install-plugin---new-argocd) guide.

    ??? config "Install Plugin - Patch Existing ArgoCD"

        This method explains how to patch an existing ArgoCD installation to include the plugin.
        Use this method if you already have an ArgoCD installation.

        For more information, see the [Install Plugin - Existing ArgoCD](https://github.com/deployKF/deployKF/tree/main/argocd-plugin#install-plugin---existing-argocd) guide.

    ---

    __Step 2: Create an App-of-Apps Manifest__

    The "deploykf" plugin has the following parameters:

    Parameter | Type | Description
    --- | --- | ---
    `source_version` | String | the version of deployKF to use (see [changelog](../releases/changelog-deploykf.md) for available versions)
    `values_files` | Array | a list of paths to values files in your ArgoCD Application's `source` repo (relative to the `source.path`)
    `values` | String | a string containing the contents of a values file (these take precedence when being merged with values from `values_files`)

    For example, the following _"app of apps"_ specification will use deployKF `{{ latest_deploykf_version }}` and read the [`sample-values.yaml`](https://github.com/deployKF/deployKF/blob/v{{ latest_deploykf_version }}/sample-values.yaml) (from the `v{{ latest_deploykf_version }}` tag of the `deploykf/deploykf` repo) while also showing how to set values with the `values` parameter:

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

    ---

    __Step 3: Apply App-of-Apps Manifest__

    After writing your app-of-apps manifest to a local file named `app-of-apps.yaml`, you may apply it with:

    ```shell
    kubectl apply --filename ./app-of-apps.yaml --namespace "argocd"
    ```

#### Manifests Repo Mode

These steps show how to generate and apply manifests with the [Manifests Repo Mode](#modes-of-operation):

??? steps "Generate & Apply Manifests - _Manifests Repo Mode_"

    To generate and apply the manifests when using ["Manifests Repo Mode"](#modes-of-operation), you will need to:

    1. set required values
    2. generate the manifests
    3. commit the generated manifests to a git repo
    4. apply the generated app-of-apps manifest

    ---

    __Step 1: Set Required Values__

    When using "manifests repo mode", the following values MUST be defined:
    
    <table markdown>
      <tr>
        <th>Value</th>
        <th>Description</th>
        <th>Example</th>
      </tr>
      <tr markdown>
        <td markdown>[`argocd.source.repo.url`](https://github.com/deployKF/deployKF/blob/v0.1.2/generator/default_values.yaml#L39-L43)</td>
        <td>the URL of the git repo where your generated manifests are stored</td>
        <td markdown>if you are using a GitHub repo named `deployKF/examples`, you might set this value to `"https://github.com/deployKF/examples"` or `"git@github.com:deployKF/examples.git"`</td>
      </tr>
      <tr markdown>
        <td markdown>[`argocd.source.repo.revision`](https://github.com/deployKF/deployKF/blob/v0.1.2/generator/default_values.yaml#L45-L48)</td>
        <td>is the git branch/tag/commit that ArgoCD should sync the manifests from</td>
        <td markdown>if you are using the `main` branch of your repo, you might set this value to `"main"`</td>
      </tr>
      <tr markdown>
        <td markdown>[`argocd.source.repo.path`](https://github.com/deployKF/deployKF/blob/v0.1.2/generator/default_values.yaml#L50-L54)</td>
        <td>is the folder path under the git repo where your generated manifests are stored</td>
        <td markdown>if you are using a folder named `GENERATOR_OUTPUT` at the root of your repo, you might set this value to `"./GENERATOR_OUTPUT/"`</td>
      </tr>
    </table>

    For example, you might set the following values:

    ```yaml
    argocd:
      source:
        repo:
          url: "https://github.com/deployKF/examples.git"
          revision: "main"
          path: "./GENERATOR_OUTPUT/"
    ```

    ---

    __Step 2: Generate Manifests__

    The `deploykf generate` command writes generated manifests into a folder, using one or more values files.

    The required arguments of the `deploykf generate` command are:

    Argument | Description
    --- | ---
    `--source-version` | the version of deployKF to use (see [changelog](../releases/changelog-deploykf.md) for available versions)
    `--values` | one or more values files to use for generating the manifests
    `--output-dir` | the directory where the generated manifests will be written

    For example, this command will use deployKF `{{ latest_deploykf_version }}` to generate manifests under `GENERATOR_OUTPUT/`, from a values file named `custom-values.yaml`:

    ```shell
    deploykf generate \
        --source-version "{{ latest_deploykf_version }}" \
        --values ./custom-values.yaml \
        --output-dir ./GENERATOR_OUTPUT
    ```

    !!! warning "Avoid Manual Changes"
    
        Manual changes in the `--output-dir` will be __overwritten__ each time the `deploykf generate` command runs.
        If you find yourself needing to make manual changes, please [raise an issue](https://github.com/deployKF/deployKF/issues) so we may consider adding a new value to support your use-case.

    !!! info "Multiple Values Files"
        
        If you specify `--values` multiple times, they will be merged with later ones taking precedence.
        Note, values which are YAML lists are NOT merged, they are replaced in full.

    ---

    __Step 3: Commit Generated Manifests__

    After running `deploykf generate`, you will likely want to commit the changes to your repo:
    
    ```shell
    # for example, to directly commit changes to the 'main' branch of your repo
    git add GENERATOR_OUTPUT
    git commit -m "my commit message"
    git push origin main
    ```

    !!! warning "Private Git Repositories"
        
        If your app-of-apps source repo is private, you will need to [configure ArgoCD with git credentials](https://argo-cd.readthedocs.io/en/stable/user-guide/private-repositories/).

    ---

    __Step 4: Apply App-of-Apps Manifest__

    The only manifest you need to manually apply is the ArgoCD [app-of-apps](https://argo-cd.readthedocs.io/en/stable/operator-manual/cluster-bootstrapping/#app-of-apps-pattern), which creates all the other ArgoCD applications.
    
    The `app-of-apps.yaml` manifest is generated at the root of your `--output-dir` folder, so you can apply it with:
    
    ```shell
    kubectl apply --filename GENERATOR_OUTPUT/app-of-apps.yaml
    ```

### Sync ArgoCD Applications

Now that your deployKF app-of-apps has been applied, you must sync the ArgoCD applications to deploy your platform.
Syncing an application will cause ArgoCD to reconcile the actual state in the cluster, to match the state defined by the application resource.

ArgoCD supports syncing applications both _graphically (Web UI)_ and _programmatically (CLI)_.
If you are new to ArgoCD, we recommend taking a look at the Web UI, as it provides a visual overview of each application and its sync status.

!!! warning "Sync Order"

    It is important to note that deployKF applications depend on each other, so you MUST sync them in the correct order.

Here are a few ways to sync the applications, you only need to use ONE of them.
If you are unsure which to use, we recommend using the _automated sync script_.

??? steps "Sync Applications - _ArgoCD Web UI_"

    To sync the deployKF applications with the __ArgoCD Web UI__, you will need to:

    1. access the ArgoCD Web UI
    2. sync the applications
    
    ---

    __Step 1: Access the ArgoCD Web UI__

    ??? question_secondary "How do I access the ArgoCD Web UI?"
    
        If this is the first time you are using ArgoCD, you will need to retrieve the initial password for the `admin` user:
        
        ```shell
        echo $(kubectl -n argocd get secret/argocd-initial-admin-secret \
          -o jsonpath="{.data.password}" | base64 -d)
        ```
        
        ---
        
        If you don't want to [expose ArgoCD with a `LoadBalancer` or `Ingress`](https://argo-cd.readthedocs.io/en/stable/getting_started/#3-access-the-argo-cd-api-server), you may use `kubectl` port-forwarding to access the ArgoCD Web UI:
    
        ```shell
        kubectl port-forward --namespace "argocd" svc/argocd-server 8090:https
        ```
        
        You will now be able to access ArgoCD at [https://localhost:8090](https://localhost:8090) in your browser.
        
        Log in with the `admin` user, and the password you retrieved above.

        ---

        The ArgoCD Web UI will look like this:
    
        ![ArgoCD Web UI (Dark Mode)](../assets/images/argocd-ui-DARK.png#only-dark)
        ![ArgoCD Web UI (Light Mode)](../assets/images/argocd-ui-LIGHT.png#only-light)

    ---

    __Step 2: Sync the Applications__

    The deployKF applications are grouped into the following "groups", which must be synced in the order described.

    !!! stack "Group 0: "app-of-apps""
    
        First, you must sync the app-of-apps application:

        1. `deploykf-app-of-apps`
        2. `deploykf-namespaces` (will only appear if using a remote destination)

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

??? steps "Sync Applications - _ArgoCD CLI (Automated)_ :star:"

    We provide the [`sync_argocd_apps.sh`](https://github.com/deployKF/deployKF/blob/main/scripts/sync_argocd_apps.sh) script to automatically sync the applications that make up deployKF.

    Learn more about the automated sync script from the [`scripts` folder README](https://github.com/deployKF/deployKF/tree/main/scripts) in the deployKF repo.

??? steps "Sync Applications - _ArgoCD CLI (Manual)_"

    To sync the deployKF applications with the __ArgoCD CLI__, you will need to:

    1. install the ArgoCD CLI
    2. expose the ArgoCD API server
    3. log in to ArgoCD
    4. sync the applications

    ---

    __Step 1: Install the ArgoCD CLI__

    You can install by following the [ArgoCD CLI Installation](https://argo-cd.readthedocs.io/en/stable/cli_installation/) instructions.

    ---

    __Step 2: Expose the ArgoCD API Server__

    You can expose the ArgoCD API server by port-forwarding the `argocd-server` Service to your local machine.

    You can do this with the following `kubectl` command:

    ```shell
    kubectl port-forward svc/argocd-server --namespace "argocd" 8090:https
    ```

    ---

    __Step 3: Log in to ArgoCD__

    If this is the first time you are using ArgoCD, you will need to retrieve the initial password for the `admin` user.

    You can do this with the following `kubectl` command:

    ```shell
    echo $(kubectl -n argocd get secret/argocd-initial-admin-secret \
      -o jsonpath="{.data.password}" | base64 -d)
    ```

    You can now log in to ArgoCD with the `admin` user and the password you retrieved above.

    ```shell
    ARGOCD_PASSWORD="<YOUR_PASSWORD_HERE>"
    argocd login localhost:8090 --username "admin" --password "$ARGOCD_PASSWORD" --insecure
    ```

    ---

    __Step 4: Sync the Applications__

    The deployKF applications are grouped into the following "groups", which must be synced in the order described.

    !!! warning "Sync Waves and Race Conditions"

        Within each group, there is an additional order defined by the `argocd.argoproj.io/sync-wave` annotation,
        this order is NOT respected by the following commands, but is respected by [the automated script](https://github.com/deployKF/deployKF/tree/main/scripts#sync_argocd_appssh).

    ```shell
    # sync the "deploykf-app-of-apps" application
    argocd app sync -l "app.kubernetes.io/name=deploykf-app-of-apps"

    # sync the "deploykf-namespaces" application
    # NOTE: This will only be present if you are using a remote destination
    argocd app sync -l "app.kubernetes.io/name=deploykf-namespaces"

    # sync all applications in the "deploykf-dependencies" group
    argocd app sync -l "app.kubernetes.io/component=deploykf-dependencies"

    # sync all applications in the "deploykf-core" group
    argocd app sync -l "app.kubernetes.io/component=deploykf-core"

    # sync all applications in the "deploykf-opt" group
    argocd app sync -l "app.kubernetes.io/component=deploykf-opt"

    # sync all applications in the "deploykf-tools" group
    argocd app sync -l "app.kubernetes.io/component=deploykf-tools"

    # sync all applications in the "kubeflow-dependencies" group
    argocd app sync -l "app.kubernetes.io/component=kubeflow-dependencies"

    # sync all applications in the "kubeflow-tools" group
    argocd app sync -l "app.kubernetes.io/component=kubeflow-tools"
    ```

Please be aware of the following issue when using the automated sync script:

!!! bug "Bug in ArgoCD v2.9"

    There is a known issue ([`deploykf/deploykf#70`](https://github.com/deployKF/deployKF/issues/70), [`argoproj/argo-cd#16266`](https://github.com/argoproj/argo-cd/issues/16266)) with all `2.9.X` versions of the ArgoCD CLI that will cause the sync script to fail with the following error:

    ```text
    ==========================================================================================
    Logging in to ArgoCD...
    ==========================================================================================
    FATA[0000] cannot find pod with selector: [app.kubernetes.io/name=] - use the --{component}-name flag in this command or set the environmental variable (Refer to https://argo-cd.readthedocs.io/en/stable/user-guide/environment-variables), to change the Argo CD component name in the CLI
    ```

    ---

    Please downgrade to version `2.8.6` of the ArgoCD CLI if you encounter this issue.

    === "macOS"

        On macOS, you can use the following commands to downgrade the ArgoCD CLI:

        ```bash
        # this URL is for version `2.8.6` of `argocd` brew formula
        wget https://raw.githubusercontent.com/Homebrew/homebrew-core/67082a334f219440f90dd221ad939d0ef6756409/Formula/a/argocd.rb
        
        # remove any existing argocd
        brew remove argocd
        
        # install from the local formula
        brew install ./argocd.rb
        
        # pin the version to prevent `brew upgrade`
        brew pin argocd
        ```

    === "Linux"

        On Linux, replace your `argocd` binary with the version from the [`v2.8.6`](https://github.com/argoproj/argo-cd/releases/tag/v2.8.6) release:

        ```bash
        VERSION="v2.8.6"
        curl -sSL -o argocd-linux-amd64 "https://github.com/argoproj/argo-cd/releases/download/${VERSION}/argocd-linux-amd64"
        sudo install -m 555 argocd-linux-amd64 /usr/local/bin/argocd
        rm argocd-linux-amd64
        ```

    === "Windows"

        On Windows, follow the "macOS" instructions to install version `2.8.6` from Homebrew in a WSL shell.

## 4. Use the Platform

Now that you have a working deployKF ML Platform, here are some things to try out!

### The Dashboard

The _deployKF dashboard_ is the web-based interface for deployKF, it gives users [authenticated access](./platform/deploykf-authentication.md) to tools like [Kubeflow Pipelines](../reference/tools.md#kubeflow-pipelines), [Kubeflow Notebooks](../reference/tools.md#kubeflow-notebooks), and [Katib](../reference/tools.md#katib).

![deployKF Dashboard (Dark Mode)](../assets/images/deploykf-dashboard-DARK.png#only-dark)
![deployKF Dashboard (Light Mode)](../assets/images/deploykf-dashboard-LIGHT.png#only-light)

!!! config "Customize the Dashboard"

    If you would like to make changes to the _deployKF dashboard_, such as adding custom links to the sidebar or homepage, see the [dashboard customization guide](./platform/deploykf-dashboard.md).

### Expose the Gateway

All public deployKF services (including the dashboard) are accessed via your _deployKF Istio Gateway_, to use the gateway, you will need to expose its Kubernetes Service.

??? steps "Expose Gateway - _Production Usage_"

    To make effective use of your deployKF platform in the real-world, you should expose the _deployKF Istio Gateway_ using a method that is appropriate for your environment.

    We provide a comprehensive guide named ["Expose Gateway and configure HTTPS"](./platform/deploykf-gateway.md) for your reference.

??? steps "Expose Gateway - _Local Testing_"

    If you are just testing deployKF, and don't want to [expose the gateway more widely](./platform/deploykf-gateway.md), you may use local `kubectl` port-forwarding with the following steps:

    1. modify your __local__ machine's `/etc/hosts` file
    2. port-forward the `deploykf-gateway` Service with `kubectl`

    ---

    __Step 1: Modify Hosts File__

    You will need to add some lines to your __local__ `/etc/hosts` file of your __local machine__.

    If the `deploykf_core.deploykf_istio_gateway.gateway.hostname` value has been left as the default of [`"deploykf.example.com"`](https://github.com/deployKF/deployKF/blob/v0.1.3/generator/default_values.yaml#L653), you should add the following lines to `/etc/hosts`:
    
    ```text
    127.0.0.1 deploykf.example.com
    127.0.0.1 argo-server.deploykf.example.com
    127.0.0.1 minio-api.deploykf.example.com
    127.0.0.1 minio-console.deploykf.example.com
    ```
    
    !!! question_secondary "Why do I need these entries in my hosts file?"

        The _deployKF Istio Gateway_ uses the HTTP `Host` header to route requests to the correct internal service, meaning that using `localhost` or `127.0.0.1` will NOT work.

    ---

    __Step 2: Port-Forward the Gateway Service__

    You may now port-forward the `deploykf-gateway` Service with the following `kubectl` command:

    ```shell
    kubectl port-forward \
      --namespace "deploykf-istio-gateway" \
      svc/deploykf-gateway 8080:http 8443:https
    ```

    ---

    The deployKF dashboard should now be available on your local machine at:
        
      :material-arrow-right-bold: [https://deploykf.example.com:8443/](https://deploykf.example.com:8443/)

### Default Login Credentials

The default values include [static user/password combinations](./platform/deploykf-authentication.md#static-userpassword-combinations) defined by the [`deploykf_core.deploykf_auth.dex.staticPasswords`](https://github.com/deployKF/deployKF/blob/v0.1.2/generator/default_values.yaml#L393-L402) value, which can be used for testing.

This table lists the default login credentials:

Username | Password | Notes
--- | --- | ---
`admin@example.com` | `admin` | The [default "owner"](https://github.com/deployKF/deployKF/blob/v0.1.2/generator/default_values.yaml#L688-L694) of all profiles, but a "member" of none, meaning it does NOT have access to "MinIO Console" or "Argo Workflows Server".<br><br>In production, we recommend leaving this account as the default "owner" but excluding its [`staticPasswords` entry](https://github.com/deployKF/deployKF/blob/v0.1.2/generator/default_values.yaml#L394-L396), so it can't be used to log in. 
`user1@example.com` | `user1` | Has [write access to `team-1` profile](https://github.com/deployKF/deployKF/blob/v0.1.2/generator/default_values.yaml#L830-L833), and [read access to `team-1-prod`](https://github.com/deployKF/deployKF/blob/v0.1.2/generator/default_values.yaml#L837-L840).
`user2@example.com` | `user2` | Has [write access to `team-1` profile](https://github.com/deployKF/deployKF/blob/v0.1.2/generator/default_values.yaml#L830-L833), and [read access to `team-1-prod`](https://github.com/deployKF/deployKF/blob/v0.1.2/generator/default_values.yaml#L837-L840).

### ML & Data Tools

deployKF includes [many tools](../reference/tools.md#tool-index) that address different stages of the ML & Data lifecycle.
The following links give more specific information about some of our most popular tools:

- [Kubeflow Pipelines](../reference/tools.md#kubeflow-pipelines)
- [Kubeflow Notebooks](../reference/tools.md#kubeflow-notebooks)

### User Reference Guides

We also provide a number of user-focused reference guides to help them deliver value with the platform faster.
You should share these guides with your users to help them get started.

<table markdown="span">
  <tr>
    <th>User Guide</th>
    <th>Description</th>
  </tr>
  <tr markdown>
    <td markdown>[Access Kubeflow Pipelines API](../user-guides/access-kubeflow-pipelines-api.md)</td>
    <td>Learn how to access the Kubeflow Pipelines API from both inside and outside the cluster with the _Kubeflow Pipelines SDK_.</td>
  </tr>
  <tr markdown>
    <td markdown>[GitOps for Kubeflow Pipelines Schedules](../user-guides/gitops-for-kubeflow-pipelines.md)</td>
    <td>Learn how to use GitOps to manage Kubeflow Pipelines schedules (rather than manually creating them with the UI or Python SDK).</td>
  </tr>
</table>

## Next Steps

- [:material-account-group: Join the deployKF community!](../about/community.md)
- [:star: Support us with a star on GitHub!](https://github.com/deployKF/deployKF)
- [<span style="color: #ff1f1f">:material-hospital-box:</span> Get support from our experts!](../about/support.md)