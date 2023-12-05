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

To learn about deployKF and why you might want to use it, please see the [Introduction](../about/introduction.md).

[:material-lightbulb-on: Read: _Introduction to deployKF_](../about/introduction.md#about-deploykf){ .md-button .md-button--primary }
[:material-lightbulb-on: Watch: _Introduction Video_](../about/introduction.md#video-introduction){ .md-button .md-button--secondary }

### Modes of Operation

There are currently two "modes of operation" for deployKF, they differ by how manifests are generated and applied to your Kubernetes cluster.

Both modes [require ArgoCD](#about-argocd), because we use it to manage the state of the platform.
In the future, we may add support for other GitOps tools or implement our own.

Mode | Description
--- | ---
ArgoCD Plugin Mode (Recommended) | The [`deployKF ArgoCD Plugin`](https://github.com/deployKF/deployKF/tree/main/argocd-plugin) directly turns the config values into manifests which it can apply to your cluster (no git repo required).
Manifests Repo Mode | You generate manifests with the [`deployKF CLI`](deploykf-cli.md) and commit them to a git repo for ArgoCD to apply to your cluster.

## 1. Requirements

First, you need a Kubernetes cluster with a version that is [supported](../releases/version-matrix.md#deploykf-dependencies) by deployKF.

??? kubernetes "Which distributions of Kubernetes are supported?"

    deployKF is designed to work on __any Kubernetes cluster__, within __any cloud__ or __local environment__.

    Here are some popular Kubernetes distributions that users have reported success with:
    
    Platform | Kubernetes Distribution
    --- | ---
    Amazon Web Services | [Amazon Elastic Kubernetes Service (EKS)](https://aws.amazon.com/eks/)
    Microsoft Azure | [Azure Kubernetes Service (AKS)](https://azure.microsoft.com/en-us/products/kubernetes-service/)
    Google Cloud | [Google Kubernetes Engine (GKE)](https://cloud.google.com/kubernetes-engine)
    IBM Cloud | [IBM Cloud Kubernetes Service (IKS)](https://www.ibm.com/cloud/kubernetes-service)
    N/A | [Rancher Kubernetes Engine (RKE)](https://rancher.com/docs/rke/latest/en/)
    N/A | [Canonical Kubernetes (MicroK8s)](https://microk8s.io/)
    Local Machine | [k3d](https://k3d.io/), [kind](https://kind.sigs.k8s.io/), [minikube](https://minikube.sigs.k8s.io/)

Other requirements vary depending on the ["mode of operation"](#modes-of-operation) you have chosen:

Requirement<br><small>:fontawesome-solid-star: → required // :fontawesome-solid-o: → optional</small> | [ArgoCD Plugin Mode](#modes-of-operation) | [Manifests Repo Mode](#modes-of-operation)
--- | :---: | :---:
a Kubernetes cluster ([version compatibility](../releases/version-matrix.md#deploykf-dependencies)) | :fontawesome-solid-star: | :fontawesome-solid-star:
ArgoCD is [installed](https://argo-cd.readthedocs.io/en/stable/getting_started/) on your Kubernetes | :fontawesome-solid-star: | :fontawesome-solid-star:
ArgoCD has the [deployKF Plugin](https://github.com/deployKF/deployKF/tree/main/argocd-plugin) | :fontawesome-solid-star: | -
deployKF's CLI is [installed](deploykf-cli.md) locally | - | :fontawesome-solid-star:
a private git repo (for generated manifests) | - | :fontawesome-solid-star: 
external MySQL database ([connecting guide](tools/external-mysql.md)) | :fontawesome-solid-o: | :fontawesome-solid-o:
external S3-like object store ([connecting guide](tools/external-object-store.md)) | :fontawesome-solid-o: | :fontawesome-solid-o:

!!! warning "Dedicated Kubernetes Cluster"

    Only __one__ deployKF platform can be deployed on a Kubernetes cluster at a time.

    Additionally, deployKF is not well suited to multi-tenant clusters.
    It uses cluster-wide components (e.g. Istio) and namespaces for user/team profiles.
    Therefore, we strongly recommend using a dedicated Kubernetes cluster for deployKF.

    If you are unable to create a new Kubernetes cluster, you may consider using [vCluster](https://github.com/loft-sh/vcluster) to create a virtual Kubernetes cluster within an existing one.

!!! warning "Cluster Domain"

    deployKF currently requires the Kubernetes kubelet [`clusterDomain`](https://kubernetes.io/docs/reference/config-api/kubelet-config.v1beta1/#kubelet-config-k8s-io-v1beta1-KubeletConfiguration) be left as the default of `cluster.local`.
    This is caused by a small number of Kubeflow components hard-coding this value, with no way to change it.

!!! warning "ARM Processors"

    deployKF does NOT currently support ARM clusters. 
    A small number of Kubeflow components do not support ARM just yet, we expect this to change after the release of Kubeflow 1.8 in October 2023.

!!! warning "Default StorageClass"

    The default values assume your Kubernetes cluster has a default [StorageClass](https://kubernetes.io/docs/concepts/storage/storage-classes/) which has support for the `ReadWriteOnce` access mode.
    
    ??? question_secondary "What if I don't have a compatible default StorageClass?"

        If you do NOT have a compatible default StorageClass, you have a few options:
    
        1. Configure [a default StorageClass](https://kubernetes.io/docs/tasks/administer-cluster/change-default-storage-class/) that has `ReadWriteOnce` support
        2. Explicitly set the `storageClass` value for the following components:
             - [`deploykf_opt.deploykf_minio.persistence.storageClass`](https://github.com/deployKF/deployKF/blob/v0.1.1/generator/default_values.yaml#L901-L905)
             - [`deploykf_opt.deploykf_mysql.persistence.storageClass`](https://github.com/deployKF/deployKF/blob/v0.1.1/generator/default_values.yaml#L1036-L1040)
        2. Disable components which require the StorageClass, and use external alternatives:
             - [`deploykf_opt.deploykf_minio.enabled`](https://github.com/deployKF/deployKF/blob/v0.1.1/generator/default_values.yaml#L853)
             - [`deploykf_opt.deploykf_mysql.enabled`](https://github.com/deployKF/deployKF/blob/v0.1.1/generator/default_values.yaml#L993)

## 2. Platform Configuration

### About Values

All aspects of your deployKF platform are configured with YAML-based configs named "values".
There are a very large number of values (more than 1500), but as deployKF supports _in-place upgrades_ you can start with a few important ones, and then grow your values file over time.

### Create Values Files

We recommend using the [`sample-values.yaml`](https://github.com/deployKF/deployKF/blob/v{{ latest_deploykf_version }}/sample-values.yaml) file as a starting point for your values.
These sample values (which are different for each deployKF version) have all ML & Data tools enabled, along with some sensible security defaults.

You may copy and make changes to the sample values, or directly use it as a base, and override specific values in a separate file.
We provide the [`sample-values-overrides.yaml`](https://github.com/deployKF/deployKF/blob/v{{ latest_deploykf_version }}/sample-values-overrides.yaml) file as an example of this approach.

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
    <th>Guide</th>
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
    <th>Guide</th>
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

[ArgoCD](https://argo-cd.readthedocs.io/en/stable/) is an extremely widely-used tool that helps you programmatically manage the applications deployed on your cluster.

??? question_secondary "Why does deployKF use Argo CD?"

    We use [Argo CD](https://argo-cd.readthedocs.io/) to manage the state of the platform.

    ArgoCD gives us a pre-built system to determine the sync-state of the apps we deploy (if resources need to be updated), and also makes cleaning up old resources much easier.

    Argo CD is a great tool for this job given its [__widespread adoption__](https://github.com/argoproj/argo-cd/blob/master/USERS.md), and __well designed interface__ for visualizing and managing the current state of your cluster.
    
    In the future, we plan to support other Kubernetes GitOps tools (like [Flux CD](https://fluxcd.io/)), or even build a deployKF-specific solution, but we have initially chosen to use Argo CD due to its overwhelming popularity.

??? info "Argo CD vs Argo Workflows"

    It's important to note that _Argo CD_ is NOT the same as _Argo Workflows_, they just have similar names:
    
    - [__Argo CD__](https://argo-cd.readthedocs.io/en/stable/) is a __GitOps Tool__, it manages the state of Kubernetes resources
    - [__Argo Workflows__](https://argoproj.github.io/argo-workflows/) is a __Workflow Engine__, it defines and runs DAG workflows in Pods on Kubernetes

### About ArgoCD Applications

The main config for ArgoCD is the [`Application`](https://argo-cd.readthedocs.io/en/stable/user-guide/application-specification/), a Kubernetes [custom resource](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/) that specifies Kubernetes manifests that ArgoCD should deploy and manage (typically from a git repository).

An _"app of apps"_ is a pattern where a single ArgoCD `Application` contains other `Application` definitions, this is typically done to make bootstrapping large applications easier.

### deployKF Versions

The "source version" chooses which version of the deployKF generator will be used.
Each version may include different tools, and may support different versions of external dependencies (like Kubernetes, Istio and cert-manager).

The [version matrix](../releases/version-matrix.md) lists which tools and dependency versions are supported by each deployKF release.
Specific information about each release (including important upgrade notes), can be found in the [deployKF generator changelog](../releases/changelog-deploykf.md).

### Generate & Apply Manifests

How you generate and apply the deployKF manifests to your Kubernetes cluster will depend on the ["mode of operation"](#modes-of-operation) you have chosen.

??? steps "Generate & Apply Manifests - _ArgoCD Plugin Mode_ :star:"

    To generate and apply the manifests when using ["ArgoCD Plugin Mode"](#modes-of-operation), you will need to:

    1. install the [deployKF ArgoCD plugin](https://github.com/deployKF/deployKF/tree/main/argocd-plugin) on your ArgoCD instance
    2. create an app-of-apps which uses the plugin
    3. apply your app-of-apps manifest

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

??? steps "Generate & Apply Manifests - _Manifests Repo Mode_"

    To generate and apply the manifests when using ["Manifests Repo Mode"](#modes-of-operation), you will need to:

    1. generate the manifests
    2. commit the generated manifests to a git repo
    3. apply the generated app-of-apps manifest

    ---

    __Step 1: Generate Manifests__

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

    __Step 2: Commit Generated Manifests__

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

    __Step 3: Apply App-of-Apps Manifest__

    The only manifest you need to manually apply is the ArgoCD [app-of-apps](https://argo-cd.readthedocs.io/en/stable/operator-manual/cluster-bootstrapping/#app-of-apps-pattern), which creates all the other ArgoCD applications.
    
    The `app-of-apps.yaml` manifest is generated at the root of your `--output-dir` folder, so you can apply it with:
    
    ```shell
    kubectl apply --filename GENERATOR_OUTPUT/app-of-apps.yaml
    ```

??? warning "Required Values (Only for Manifests Repo Mode)"

    When using "manifests repo mode", the following values MUST be defined in your values file(s).
    
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

### Sync ArgoCD Applications

Now that your deployKF app-of-apps has been applied, you must sync the ArgoCD applications to deploy your platform.
Syncing an application will cause ArgoCD to reconcile the actual state in the cluster, to match the state defined by the application resource.

ArgoCD supports syncing applications both _graphically (Web UI)_ and _programmatically (CLI)_.
If you are new to ArgoCD, we recommend taking a look at the Web UI, as it provides a visual overview of each application and its sync status.

!!! warning "Sync Order"

    It is important to note that deployKF applications depend on each other, so you MUST sync them in the correct order.

There are a few ways to sync the applications, but you only need to use one of them:

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