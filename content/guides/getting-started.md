---
icon: material/rocket-launch
---

# Getting Started

This guide will explain how to get started with __production usage__ of deployKF on __any Kubernetes cluster__.

## About deployKF

Before starting, let us briefly introduce the deployKF project.

### What is deployKF?

!!! question ""

    deployKF is the best way to build reliable ML Platforms on Kubernetes.
    
    - deployKF supports leading [MLOps & Data tools](../reference/tools.md) from both Kubeflow, and other projects
    - deployKF has a Helm-like interface, with [values](../reference/deploykf-values.md) for configuring all aspects of the deployment (no need to edit Kubernetes YAML)
    - deployKF does NOT install resources directly in your cluster, instead it generates [ArgoCD Applications](https://argo-cd.readthedocs.io/en/stable/operator-manual/declarative-setup/#applications) to provide native GitOps support

### What ML/AI tools are in deployKF?

!!! question_secondary ""

    Currently, deployKF supports MLOps tools from the Kubeflow ecosystem like [Kubeflow Pipelines](../reference/tools.md#kubeflow-pipelines) and [Kubeflow Notebooks](../reference/tools.md#kubeflow-notebooks).
    We are actively adding support for other popular tools such as [MLFlow (Model Registry)](../reference/future-tools.md#mlflow-model-registry), [Apache Airflow](../reference/future-tools.md#apache-airflow), and [Feast](../reference/future-tools.md#feast). 
    
    For more information, please see [supported tools](../reference/tools.md) and [future tools](../reference/future-tools.md)!

### Who makes deployKF?

!!! question_secondary ""

    deployKF was originally created by [Mathew Wicks](https://www.linkedin.com/in/mathewwicks/) (GitHub: [@thesuperzapper](https://github.com/thesuperzapper)), a Kubeflow lead and maintainer of the popular [Apache Airflow Helm Chart](https://github.com/airflow-helm/charts).
    However, deployKF is now a community-led project that welcomes contributions from anyone who wants to help.

### Media Coverage

??? youtube "Intro / Demo - Kubeflow Community Call - July 2023"

    <iframe width="560" height="315" src="https://www.youtube.com/embed/VggtaOgtBJo" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

### Other Questions

??? question_secondary "Is commercial support available for deployKF?"

    The creator of deployKF (Mathew Wicks), operates a US-based MLOps company called [Aranui Solutions](https://www.aranui.solutions) that provides commercial support and consulting for deployKF.
    
    Connect on [LinkedIn](https://www.linkedin.com/in/mathewwicks/) or email [`sales@aranui.solutions`](mailto:sales@aranui.solutions?subject=%5BdeployKF%5D%20MY_SUBJECT) to learn more!

??? question_secondary "Who uses deployKF?"
  
    deployKF is a new project, and we are still building our community.

    Please consider adding your organization to our [list of adopters](https://github.com/deployKF/deployKF/blob/main/ADOPTERS.md).

??? question_secondary "Do you have a Slack or Mailing List?"

    __Slack:__

    - The deployKF community uses the __Kubeflow Slack__ for informal discussions among users and contributors.
    - Find us on the [`#deploykf`](https://kubeflow.slack.com/archives/C054H6WLNCB) channel!

    [:fontawesome-brands-slack: Join the Kubeflow Slack](https://invite.playplay.io/invite?team_id=T7QLHSH6U){ .md-button .md-button--secondary }

    ---

    __Mailing Lists:__

    - The [deploykf-users](https://groups.google.com/g/deploykf-users) mailing list is for users of deployKF to ask questions and share ideas.
    - The [deploykf-dev](https://groups.google.com/g/deploykf-dev) mailing list is for contributors to deployKF to discuss development and design.

    [:fontawesome-solid-envelope: Join the User Mailing List](https://groups.google.com/g/deploykf-users){ .md-button .md-button--secondary }

    [:fontawesome-solid-envelope: Join the Contributor Mailing List](https://groups.google.com/g/deploykf-dev){ .md-button .md-button--secondary }

??? question_secondary "Why does deployKF use Argo CD?"

    ML Platforms are made up of many components and interconnected dependencies, and it can be difficult to manage the state of all these components.
    
    This is where GitOps comes in, it allows us to define the state (i.e. Kubernetes manifests) of all the components in a single place (Git), and then use a tool to reconcile the actual state of our cluster to match the defined state.
    
    [Argo CD](https://argo-cd.readthedocs.io/en/stable/){target=_blank} is a great tool for this job, it is [widely used](https://github.com/argoproj/argo-cd/blob/master/USERS.md){target=_blank}, [part of the CNCF](https://www.cncf.io/projects/argo/){target=_blank}, and has a [great Web UI](../assets/images/argocd-ui.gif){target=_blank} for visualizing and managing the current state of your cluster.

    ---

    In the future, we plan to support other popular Kubernetes GitOps tools like [Flux CD](https://fluxcd.io/), but we have initially chosen to support Argo CD given its overwhelming popularity.

    ---

    It's important to note that [Argo CD](https://argo-cd.readthedocs.io/en/stable/){target=_blank} is __NOT__ the same as [Argo Workflows](https://argoproj.github.io/argo-workflows/){target=_blank}.
    
    - Argo CD is a __GitOps tool__ for Kubernetes, which means it uses Git as the source of truth for your cluster's state, rather than manually applying Kubernetes YAML with `kubectl apply` or `helm install`.
    - Argo Workflows is a __workflow engine__ for Kubernetes, which means it allows you to define and run DAG workflows in Pods on Kubernetes.

### Other Guides

!!! info "Migrate from Kubeflow to deployKF"
    
    If you have an __existing deployment of Kubeflow__, there is a [migration guide](./migrate-from-kubeflow-manifests.md) for you.

## 1. Requirements

The requirements for deployKF vary depending on which "mode of operation" you use.

Mode | Description
--- | ---
"Manifests Repo" Mode | In this mode, you use the [deployKF CLI](deploykf-cli.md) CLI to generate manifests and commit them to a "manifests git repo" before applying them with ArgoCD.
"ArgoCD Plugin" Mode | In this mode, you use the [deployKF ArgoCD Plugin](https://github.com/deployKF/deployKF/tree/main/argocd-plugin) to generate and apply the manifests in a single step (no git repo required).

The following table outlines the requirements for each mode.

Requirement<br><sub>:fontawesome-regular-circle-check:: required</sub><br><sub>:fontawesome-regular-circle:: optional</sub> | "Manifests Repo" Mode | "ArgoCD Plugin" Mode
--- | :---: | :---:
a Kubernetes cluster ([version compatibility](../releases/version-matrix.md#deploykf-dependencies)) | :fontawesome-regular-circle-check: | :fontawesome-regular-circle-check:
ArgoCD is [installed on Kubernetes](https://argo-cd.readthedocs.io/en/stable/getting_started/) | :fontawesome-regular-circle-check: | :fontawesome-regular-circle-check:
deployKF ArgoCD Plugin [is installed](https://github.com/deployKF/deployKF/tree/main/argocd-plugin#install-plugin-new-argocd) | - | :fontawesome-regular-circle-check:
deployKF CLI is [installed on local machine](deploykf-cli.md) | :fontawesome-regular-circle-check: | -
a private git repo, for generated manifests | :fontawesome-regular-circle-check: | -
external MySQL database | :fontawesome-regular-circle: | :fontawesome-regular-circle:
external S3-compatible object store | :fontawesome-regular-circle: | :fontawesome-regular-circle:

??? kubernetes "Supported Kubernetes Distributions"

    deployKF should work on any Kubernetes distribution!

    Here are some popular distributions of Kubernetes that users have reported success with.
    
    Platform | Kubernetes Distribution
    --- | ---
    Amazon Web Services | [Amazon Elastic Kubernetes Service (EKS)](https://aws.amazon.com/eks/)
    Microsoft Azure | [Azure Kubernetes Service (AKS)](https://azure.microsoft.com/en-us/products/kubernetes-service/)
    Google Cloud | [Google Kubernetes Engine (GKE)](https://cloud.google.com/kubernetes-engine)
    IBM Cloud | [IBM Cloud Kubernetes Service (IKS)](https://www.ibm.com/cloud/kubernetes-service)
    Local Machine | [k3d](https://k3d.io/), [kind](https://kind.sigs.k8s.io/), [minikube](https://minikube.sigs.k8s.io/)

!!! warning "Dedicated Kubernetes Cluster"

    Only __one__ deployKF platform can be deployed on a Kubernetes cluster at a time.

    Additionally, deployKF is not well suited to multi-tenant clusters.
    It uses cluster-wide components (e.g. Istio) and namespaces for user/team profiles.
    Therefore, we strongly recommend using a dedicated Kubernetes cluster for deployKF.

    ---

    If you are unable to create a new Kubernetes cluster, you may consider using [vcluster](https://github.com/loft-sh/vcluster) to create a virtual Kubernetes cluster within an existing one.

!!! warning "ARM Support"

    deployKF does not currently support ARM clusters, this is because a small number of Kubeflow components do not support ARM just yet,
    we expect this to change after the release of Kubeflow 1.8 in October 2023.

!!! warning "Default StorageClass"

    The default values assume your Kubernetes cluster has a default [StorageClass](https://kubernetes.io/docs/concepts/storage/storage-classes/) which has support for the `ReadWriteOnce` access mode.
    
    ---

    If you do not have a compatible default StorageClass, you can either:

    1. Configure [a default StorageClass](https://kubernetes.io/docs/tasks/administer-cluster/change-default-storage-class/) that has `ReadWriteOnce` support
    2. Explicitly set the `storageClass` value for the following components:
         - [`deploykf_opt.deploykf_minio.persistence.storageClass`](https://github.com/deployKF/deployKF/blob/v0.1.1/generator/default_values.yaml#L901-L905)
         - [`deploykf_opt.deploykf_mysql.persistence.storageClass`](https://github.com/deployKF/deployKF/blob/v0.1.1/generator/default_values.yaml#L1036-L1040)
    2. Disable components which require the StorageClass, and use external alternatives:
         - [`deploykf_opt.deploykf_minio.enabled`](https://github.com/deployKF/deployKF/blob/v0.1.1/generator/default_values.yaml#L853)
         - [`deploykf_opt.deploykf_mysql.enabled`](https://github.com/deployKF/deployKF/blob/v0.1.1/generator/default_values.yaml#L993)

## 2. Values / Configuration

deployKF is configured using YAML files containing configs named "values" which behave similarly to those in Helm.
There are a very large number of values (more than 1500), but you can start by defining a few important ones, and then grow your values file over time.

We recommend that you start your values file by copying the [`sample-values.yaml`](https://github.com/deployKF/deployKF/blob/v{{ latest_deploykf_version }}/sample-values.yaml) file, which includes reasonable defaults that should work on any Kubernetes cluster.

!!! tip "YAML Syntax"

    For a refresher on YAML syntax, we recommend [Learn YAML in Y minutes](https://learnxinyminutes.com/docs/yaml/) and [YAML Multiline Strings](https://yaml-multiline.info/)

!!! info "Values Reference"

    All the available values (and their defaults) are listed on the [values reference page](../reference/deploykf-values.md), and in the [`generator/default_values.yaml`](https://github.com/deployKF/deployKF/blob/v{{ latest_deploykf_version }}/generator/default_values.yaml) file.

### Required Values

??? warning ""Manifests Repo" Mode"

    When using the "manifests repo" mode, the following values are required:

    ??? value "[`argocd.source.repo.url`](https://github.com/deployKF/deployKF/blob/v0.1.1/generator/default_values.yaml#L39-L43)"

        This value is the URL of the git repo where the generated manifests are stored.

        For example, if you are using a GitHub repo named `deployKF/examples`, you might set this value to `"https://github.com/deployKF/examples"` or `"git@github.com:deployKF/examples.git"`
    
    ??? value "[`argocd.source.repo.revision`](https://github.com/deployKF/deployKF/blob/v0.1.1/generator/default_values.yaml#L45-L48)"

        This value is the git branch/tag/commit that ArgoCD should use to sync the manifests from.        

        For example, if you are using the `main` branch of your repo, you might set this value to `"main"`.
    
    ??? value "[`argocd.source.repo.path`](https://github.com/deployKF/deployKF/blob/v0.1.1/generator/default_values.yaml#L50-L54)"

        This value is the path within the git repo where the generated manifests are stored.        

        For example, if you are using a folder named `GENERATOR_OUTPUT` at the root of your repo, you might set this value to `"./GENERATOR_OUTPUT/"`.

### Configurations (Platform)

??? config "User Authentication and External Identity Providers"

    deployKF uses [dex](https://dexidp.io/) for user authentication.

    For more information about __defining static user accounts__, and __connecting external identity providers__, see the [User Authentication and External Identity Providers](./platform/deploykf-authentication.md) guide.

??? config "Manage Profiles/Namespaces and Assigning Users"

    A deployKF profile has a 1:1 relationship with a Kubernetes namespace.
    The profiles which a user is a member of determines their level of access to resources/tools in the cluster.

    To learn about managing profiles and assigning users, see the [Manage Profiles and Assigning Users](./platform/deploykf-profiles.md) guide.

??? config "Expose deployKF Gateway and configure HTTPS"

    By default, deployKF creates a LoadBalancer Service named `deploykf-gateway` in the `deploykf-istio-gateway` namespace.

    For more information about exposing the Gateway Service outside of the Kubernetes cluster, see the [Expose deployKF Gateway and configure HTTPS](./platform/deploykf-gateway.md) guide.

??? config "Customize the deployKF Dashboard"

    The deployKF dashboard is the web-based interface for deployKF, and is the primary way that users interact with the platform.
    The dashboard includes navigation menus with links to various tools and documentation which can be customized.

    For more information about customizing the dashboard, see the [Customize the deployKF Dashboard](./platform/deploykf-dashboard.md) guide.

### Configurations (Tools)

??? config "Connect an external MySQL Database"

    deployKF includes an embedded MySQL instance.
    However, we recommend using an external MySQL database for production usage.

    For more information, see the [Connect an external MySQL Database](./tools/external-mysql.md) guide.

??? config "Connect an external S3-like Object Store"

    deployKF includes an embedded MinIO instance.
    However, you may wish to replace this with an external S3-compatible object store.

    For more information, see the [Connect an external S3-like Object Store](./tools/external-object-store.md) guide.

??? config "Configure Kubeflow Notebooks (Images, CPU, GPU, etc.)"

    Kubeflow Notebooks allows users to spawn Pods running instances of __JupyterLab__, __Visual Studio Code (code-server)__, and __RStudio__ in profile namespaces.

    For more information about configuring Kubeflow Notebooks, see the [Configure Kubeflow Notebooks](./tools/kubeflow-notebooks.md) guide.

## 3. Generate & Apply Manifests

After creating your `custom-values.yaml` file(s), the method used to generate and apply the manifests to your Kubernetes cluster will depend on the deployKF "mode of operation" you have chosen.

#### Manifests Repo Mode

??? steps "Steps for Manifests Repo Mode"

    When using the "manifests repo" mode, you will need to:

    1. generate the manifests
    2. commit the generated manifests to a git repo
    3. manually apply the app-of-apps manifest

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

    ---

    __Step 3: Apply App-of-Apps Manifest__

    The only manifest you need to manually apply is the ArgoCD [app-of-apps](https://argo-cd.readthedocs.io/en/stable/operator-manual/cluster-bootstrapping/#app-of-apps-pattern), which creates all the other ArgoCD applications.
    
    The `app-of-apps.yaml` manifest is generated at the root of your `--output-dir` folder, so you can apply it with:
    
    ```shell
    kubectl apply --filename GENERATOR_OUTPUT/app-of-apps.yaml
    ```

#### ArgoCD Plugin Mode (Recommended)

??? steps "Steps for ArgoCD Plugin Mode"

    When using the "ArgoCD plugin" mode, you will need to:

    1. install the [deployKF ArgoCD plugin](https://github.com/deployKF/deployKF/tree/main/argocd-plugin) on your ArgoCD instance
    2. create an app-of-apps which uses the plugin
    3. apply your app-of-apps manifest

    ---
  
    __Step 1: Install the ArgoCD Plugin__

    We provide two options for installing the deployKF ArgoCD plugin:

    ??? config "New ArgoCD Installation"

        This method installs our pre-patched ArgoCD manifests with the plugin pre-installed.
        Use this method if you are installing ArgoCD for the first time.

        For specific information, see the [Install Plugin - New ArgoCD](https://github.com/deployKF/deployKF/tree/main/argocd-plugin#install-plugin---new-argocd) guide.

    ??? config "Patch an Existing ArgoCD Installation"

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

    For example, this app-of-apps manifest will use deployKF `{{ latest_deploykf_version }}` and read the `sample-values.yaml` from the `v{{ latest_deploykf_version }}` tag of the `deploykf/deploykf` repo:

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

## 4. Sync ArgoCD Applications

Now that the deployKF app-of-apps manifest has been applied, you must sync the ArgoCD applications that make up deployKF.

ArgoCD supports syncing applications via both its __Web UI__ and __CLI__.
We recommend using the Web UI when you are first getting started.

!!! warning "Private Git Repositories"
    
    If your app-of-apps source repo is private, you will need to [configure ArgoCD with git credentials](https://argo-cd.readthedocs.io/en/stable/user-guide/private-repositories/).

!!! warning "Sync Failures"

    Some applications, specifically `dkf-dep--cert-manager` and `dkf-core--deploykf-profiles-generator` may fail to sync on the first attempt, simply wait a few seconds and try the sync again.

!!! warning "Sync Order"

    You MUST sync each "group" of applications in the order described below, as they depend on each other.

### Sync with ArgoCD Web UI

??? steps "Steps to Sync using the ArgoCD Web UI"

    To sync the deployKF applications with the __ArgoCD Web UI__, you will need to:

    1. access the ArgoCD Web UI
    2. sync the applications
    
    ---

    __Step 1: Access the ArgoCD Web UI__

    ??? question_secondary "How do I access the ArgoCD Web UI?"
    
        If you have not publicly exposed the ArgoCD Web UI, you can access it by port-forwarding the `argocd-server` Service to your local machine.
    
        You can do this with the following `kubectl` command:
    
        ```shell
        kubectl port-forward --namespace "argocd" svc/argocd-server 8090:https
        ```
    
        You should now see the ArgoCD interface at [https://localhost:8090](https://localhost:8090).
    
        ---
        
        If this is the first time you are using ArgoCD, you will need to retrieve the initial password for the `admin` user.
    
        You can do this with the following `kubectl` command:
        
        ```shell
        echo $(kubectl -n argocd get secret/argocd-initial-admin-secret \
          -o jsonpath="{.data.password}" | base64 -d)
        ```
    
        You can now log in to ArgoCD with the `admin` user and the password you retrieved above.

    ---

    __Step 2: Sync the Applications__

    The deployKF applications are grouped into the following "groups", which must be synced in the order described.

    !!! stack "Group 0: "app-of-apps""
    
        First, you must sync the app-of-apps application:

        - `deploykf-app-of-apps`

    !!! stack "Group 1: "deploykf-dependencies""
    
        Second, you must sync the applications with the label `app.kubernetes.io/component=deploykf-dependencies`:

        - `dkf-dep--cert-manager` (may fail on first attempt)
        - `dkf-dep--istio`
        - `dkf-dep--kyverno`

    !!! stack "Group 2: "deploykf-core""

        Third, you must sync the applications with the label `app.kubernetes.io/component=deploykf-core`:

        - `dkf-core--deploykf-auth`
        - `dkf-core--deploykf-dashboard`
        - `dkf-core--deploykf-istio-gateway`
        - `dkf-core--deploykf-profiles-generator` (may fail on first attempt)

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

### Sync with ArgoCD CLI

??? steps "Steps to Sync using the ArgoCD CLI (Automated)"

    We provide the [`sync_argocd_apps.sh`](https://github.com/deployKF/deployKF/blob/main/scripts/sync_argocd_apps.sh) script to automatically sync all the deployKF applications using the ArgoCD CLI,
    learn more in the [`scripts` README](https://github.com/deployKF/deployKF/tree/main/scripts) of the deployKF repo.

??? steps "Steps to Sync using the ArgoCD CLI (Manual)"

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
    argocd app sync -l "app.kubernetes.io/name=deploykf-app-of-apps"

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

## 5. Use the Platform

Now that you have a working deployKF ML Platform, here are some things to try out!

### Access the Dashboard

The deployKF dashboard is a web-based interface and is the primary way that users interact with the platform.
You will need to expose its service (either publicly or privately) to access it.

??? steps "Steps to Expose Gateway Service (with Port-Forwarding)"

    If you have not publicly [exposed the deployKF Gateway Service](./platform/deploykf-gateway.md), you may access it via port-forwarding by:

    1. adding some lines to your machine's `/etc/hosts` file
    2. port-forwarding the `deploykf-gateway` Service with `kubectl`

    ---

    __Step 1: Modify Hosts File__

    You must add lines to your `/etc/hosts` file, this is because deployKF uses the "Host" header to route requests to the correct internal service, meaning that the IP address alone would NOT work.
    
    If the [`deploykf_core.deploykf_istio_gateway.gateway.hostname`](https://github.com/deployKF/deployKF/blob/v0.1.1/generator/default_values.yaml#L600) value is set as `"deploykf.example.com"`, you would add the following lines:
    
    ```text
    127.0.0.1 deploykf.example.com
    127.0.0.1 argo-server.deploykf.example.com
    127.0.0.1 minio-api.deploykf.example.com
    127.0.0.1 minio-console.deploykf.example.com
    ```
    
    ---

    __Step 2: Port-Forward the Gateway Service__

    You can port-forward the `deploykf-gateway` Service with the following `kubectl` command:

    ```shell
    kubectl port-forward \
      --namespace "deploykf-istio-gateway" \
      svc/deploykf-gateway 8080:http 8443:https
    ```

    You should now see the deployKF dashboard at: [https://deploykf.example.com:8443/](https://deploykf.example.com:8443/)

??? note "Default Login Credentials"

    The following table lists the default login credentials for the deployKF dashboard.

    Account | Username | Password | Notes
    --- | --- | --- | ---
    Admin | `admin@example.com` | `admin` | not for normal use (owns all profiles)
    User 1 | `user1@example.com` | `user1` |
    User 2 | `user2@example.com` | `user2` |

    !!! info "Dex StaticPasswords"

        These default login credentials are Dex StaticPasswords defined by the [`deploykf_core.deploykf_auth.dex.staticPasswords`](https://github.com/deployKF/deployKF/blob/v0.1.1/generator/default_values.yaml#L378-L401) value.

    !!! warning "Default Profile Owner"
        
        By default, [`"admin@example.com"` is the "owner" of all profiles](https://github.com/deployKF/deployKF/blob/v0.1.1/generator/default_values.yaml#L687-L693), but is not a "member" of any.
        This means that it does NOT have access to the "MinIO Console" or "Argo Workflows Server" interfaces.

### Additional Topics

Note, the audience for these next topics is __platform users__ rather than __platform operators__.

??? abstract "GitOps for Kubeflow Pipelines (Pipeline Definitions, Schedules)"

    We provide a reference implementation for managing Kubeflow Pipelines (pipeline definitions, schedules) using GitOps.
    For more information, see the [GitOps for Kubeflow Pipelines](../user-guides/gitops-for-kubeflow-pipelines.md) user guide.

??? abstract "Access Kubeflow Pipelines API"

    We provide information on how to authenticate with the Kubeflow Pipelines API from both inside and outside the cluster.
    For more information, see the [Access the Kubeflow Pipelines API](../user-guides/access-kubeflow-pipelines-api.md) user guide.

## Next Steps

- [Troubleshooting](troubleshooting.md)
- [Join the deployKF community](../about/community.md)
- [Get Support](../about/support.md)