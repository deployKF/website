# Getting Started

This guide will help you get started with __deployKF__.

!!! tip
    
    If you have an existing deployment of __Kubeflow Manifests__, there is a [migration guide](migrate-from-kubeflow-manifests.md) for you.

## 1. Understand deployKF

Before starting, you should learn a little about __deployKF__ and how it works.

### What is deployKF?

deployKF is the best way to build reliable ML Platforms on Kubernetes.

- deployKF supports leading [MLOps & Data tools](../reference/tools.md) from both Kubeflow, and other projects
- deployKF has a Helm-like interface, with [values](../reference/deploykf-values.md) for configuring all aspects of the deployment (no need to edit Kubernetes YAML)
- deployKF does NOT install resources directly in your cluster, instead it generates [ArgoCD Applications](https://argo-cd.readthedocs.io/en/stable/operator-manual/declarative-setup/#applications) to provide native GitOps support

### Why use Argo CD?

ML Platforms are made up of many components and interconnected dependencies, and it can be difficult to manage the state of all these components.

This is where GitOps comes in, it allows us to define the state (i.e. Kubernetes manifests) of all the components in a single place (Git), and then use a tool to reconcile the actual state of our cluster to match the defined state.

[Argo CD](https://argo-cd.readthedocs.io/en/stable/){target=_blank} is a great tool for this job, it is [widely used](https://github.com/argoproj/argo-cd/blob/master/USERS.md){target=_blank}, [part of the CNCF](https://www.cncf.io/projects/argo/){target=_blank}, and has a [great Web UI](/assets/images/argocd-ui.gif){target=_blank} for visualizing and managing the current state of your cluster.

!!! note "Argo CD vs Argo Workflows"

    It's important to note that [Argo CD](https://argo-cd.readthedocs.io/en/stable/){target=_blank} is __NOT__ the same as [Argo Workflows](https://argoproj.github.io/argo-workflows/){target=_blank}.
    
    - __Argo CD__ is a __GitOps__ tool for Kubernetes, which means it uses Git as the source of truth for your cluster's state, rather than manually applying Kubernetes YAML with `kubectl` or `helm`.
    - __Argo Workflows__ is a __workflow engine__ for Kubernetes, which means it allows you to define and run DAG workflows in Pods on Kubernetes.

### Other Resources

- [Frequently Asked Questions](../faq.md)
- [Supported Tools](../reference/tools.md)
- [Future Tools](../reference/future-tools.md)
- [Kubeflow vs deployKF](../about/kubeflow-vs-deploykf.md)
- [Architecture of deployKF](../about/architecture.md)

## 2. Prepare requirements

### Minimum Requirements

- the `deploykf` cli tool (see [Install the deployKF CLI](install-deploykf-cli.md))
- a Kubernetes cluster (see [version compatibility](../releases/version-matrix.md#deploykf-dependencies))
- ArgoCD is [deployed on your cluster](https://argo-cd.readthedocs.io/en/stable/getting_started/)
- a private git repo (in which to store your generated manifests)

!!! warning "Dedicated Kubernetes Cluster"

    deployKF is a complex tool, and only __one instance__ can be deployed on a Kubernetes cluster at a time.
    It is strongly recommended that you create a __dedicated Kubernetes cluster__ for your deployment of deployKF.

??? tip "Virtual Kubernetes Clusters"

    If you are unable to create a new Kubernetes cluster, you may consider using [vcluster](https://github.com/loft-sh/vcluster) to create a virtual Kubernetes cluster within an existing one.
    This approach has additional benefits because deployKF uses cluster-wide components (e.g. Istio) and namespaces for user/team profiles, so is not well suited to multi-tenant clusters.

??? info "Distributions of Kubernetes"

    Here are some popular distributions of Kubernetes listed by platform.
    
    Platform | Kubernetes Distribution
    --- | ---
    Amazon Web Services | [Amazon Elastic Kubernetes Service (EKS)](https://aws.amazon.com/eks/)
    Microsoft Azure | [Azure Kubernetes Service (AKS)](https://azure.microsoft.com/en-us/products/kubernetes-service/)
    Google Cloud | [Google Kubernetes Engine (GKE)](https://cloud.google.com/kubernetes-engine)
    Alibaba Cloud | [Alibaba Cloud Container Service for Kubernetes (ACK)](https://www.alibabacloud.com/product/kubernetes)
    IBM Cloud | [IBM Cloud Kubernetes Service (IKS)](https://www.ibm.com/cloud/kubernetes-service)
    Local Machine | [k3d](https://k3d.io/), [kind](https://kind.sigs.k8s.io/), [minikube](https://minikube.sigs.k8s.io/)

### Optional Requirements

- An external MySQL database (see [Use an external MySQL database](../topics/production-usage/external-mysql-database.md))
- An external S3-compatible object store (see [Use an external S3-compatible object store](../topics/production-usage/external-object-store.md))

??? warning "MinIO License"
  
    If you choose to not connect an external S3-compatible object store, deployKF will use [MinIO](https://github.com/minio/minio), ensure you are familiar with MinIO's licence, which at the time of writing is [AGPLv3](https://github.com/minio/minio/blob/master/LICENSE).
    However, rest assured that deployKF itself __does NOT contain any code from MinIO__, and is licensed under the [Apache 2.0 License](https://github.com/deployKF/deployKF/blob/main/LICENSE).

## 3. Create values file

deployKF is configured using YAML files containing configs named "values" which behave similarly to those in Helm.

deployKF has a very large number of configurable values (more than 1500), but you can start by defining a few important ones, and then grow your values file over time.

We recommend you start by copying the [`sample-values.yaml`](https://github.com/deployKF/deployKF/blob/v{{ latest_deploykf_version }}/sample-values.yaml) file, which includes reasonable defaults that should work on any Kubernetes cluster.
The following values will need to be changed to match your environment:

| Value                                                                                                                   | Description                                                                                                                                                                                                                                                                                                                                                                                                                                            |
|-------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [`argocd.source.repo.url`](https://github.com/deployKF/deployKF/blob/v0.1.0/generator/default_values.yaml#L23-L27)      | <ul><li>the URL of your manifest git repo</li><li>for example, if you are using a GitHub repo named `deployKF/examples`, you might set this value to `"https://github.com/deployKF/examples"` or `"git@github.com:deployKF/examples.git"`</li><li>TIP: if you are using a private repo, you will need to [configure your ArgoCD with the appropriate credentials](https://argo-cd.readthedocs.io/en/stable/user-guide/private-repositories/)</li></ul> |
| [`argocd.source.repo.revision`](https://github.com/deployKF/deployKF/blob/v0.1.0/generator/default_values.yaml#L29-L32) | <ul><li>the git revision which contains your generated manifests</li><li>for example, if you are using the `main` branch of your repo, you might set this value to `"main"`</li></ul>                                                                                                                                                                                                                                                                  |
| [`argocd.source.repo.path`](https://github.com/deployKF/deployKF/blob/v0.1.0/generator/default_values.yaml#L34-L38)     | <ul><li>the path within your repo where the generated manifests are stored</li><li>for example, if you are using a folder named `GENERATOR_OUTPUT` at the root of your repo, you might set this value to `"./GENERATOR_OUTPUT/"`</li></ul>                                                                                                                                                                                                             |

We are actively working on detailed "production usage" guides, but for now, here are some other values you might want to change:

| Value                                                                                                                                                                                           | Description                                                                                |
|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------|
| [`deploykf_core.deploykf_auth.dex.connectors`](https://github.com/deployKF/deployKF/blob/v0.1.0/generator/default_values.yaml#L385-L396)                                                        | connect with an external identity provider (e.g. Microsoft AD, Okta, GitHub, Google, etc.) |
| [`deploykf_core.deploykf_auth.dex.staticPasswords`](https://github.com/deployKF/deployKF/blob/v0.1.0/generator/default_values.yaml#L360-L383)                                                   | create user accounts for your team (if not using an external identity provider)            |
| [`deploykf_core.deploykf_dashboard.navigation.externalLinks`](https://github.com/deployKF/deployKF/blob/v0.1.0/generator/default_values.yaml#L520-L529)                                         | add custom links to the dashboard navigation menu                                          |
| [`deploykf_core.deploykf_istio_gateway`](https://github.com/deployKF/deployKF/blob/v0.1.0/generator/default_values.yaml#L566-L628)                                                              | configure the istio ingress gateway (make it accessible from outside the cluster)          |
| [`deploykf_core.deploykf_profiles_generator.profiles`](https://github.com/deployKF/deployKF/blob/v0.1.0/generator/default_values.yaml#L747-L810)                                                | create profiles (namespaces) and assign groups and users to them                           |
| [`kubeflow_tools.katib.mysql`](https://github.com/deployKF/deployKF/blob/v0.1.0/generator/default_values.yaml#L1208-L1222)                                                                      | configure an external MySQL database for Katib                                             |
| [`kubeflow_tools.notebooks.spawnerFormDefaults`](https://github.com/deployKF/deployKF/blob/v0.1.0/generator/default_values.yaml#L1252-L1325)                                                    | configure Kubeflow Notebooks, including notebook images, GPU resources, and more           |
| [`kubeflow_tools.pipelines.mysql`](https://github.com/deployKF/deployKF/blob/v0.1.0/generator/default_values.yaml#L1677-L1691)                                                                  | configure an external MySQL database for Kubeflow Pipelines                                |
| [`kubeflow_tools.pipelines.objectStore`](https://github.com/deployKF/deployKF/blob/v0.1.0/generator/default_values.yaml#L1640-L1675)                                                            | configure an external object store (like S3) for Kubeflow Pipelines                        |

For information about other values, you can refer to the following resources:

- docstrings in [`generator/default_values.yaml`](https://github.com/deployKF/deployKF/blob/v{{ latest_deploykf_version }}/generator/default_values.yaml), which contains defaults for all values
- the [values reference page](../reference/deploykf-values.md), which contains a list of all values with links to their docstrings
- the "topics" section of the website, which has information about achieving specific goals, such as [using an external S3-compatible object store](../topics/production-usage/external-object-store.md)

??? tip "YAML Syntax"

    For a refresher on YAML syntax, we recommend [Learn YAML in Y minutes](https://learnxinyminutes.com/docs/yaml/) and [YAML Multiline Strings](https://yaml-multiline.info/)

## 4. Generate manifests

You must generate your manifests and commit them to a git repo before ArgoCD can deploy them to your cluster.

The `generate` command of the [`deploykf` CLI](https://github.com/deployKF/cli) creates a manifests folder for a specific version of deployKF and one or more values files:

```shell
deploykf generate \
    --source-version {{ latest_deploykf_version }} \
    --values ./custom-values.yaml \
    --output-dir ./GENERATOR_OUTPUT
```

After running `deploykf generate`, you will likely want to commit the changes to your repo:

```shell
# for example, to directly commit changes to the 'main' branch of your repo
git add GENERATOR_OUTPUT
git commit -m "my commit message"
git push origin main
```

??? tip "Source Versions"
    
    The `--source-version` can be any valid deployKF version, see the [changelog](../releases/changelog-deploykf.md) for a list of versions.

??? tip "Multiple Values Files"
    
    If you specify `--values` multiple times, they will be merged with later ones taking precedence (note, YAML lists are not merged, they are replaced in full).

??? tip "Output Directory Changes"

    Any manual changes made in the `--output-dir` will be overwritten each time the `deploykf generate` command runs, so please only make changes in your `--values` files. 
    If you find yourself needing to make manual changes, this indicates we might need a new value, so please [raise an issue](https://github.com/deployKF/deployKF/issues) to help us improve the project!

## 5. Apply app-of-apps

The only manifest you need to manually apply is the ArgoCD [app-of-apps](https://argo-cd.readthedocs.io/en/stable/operator-manual/cluster-bootstrapping/#app-of-apps-pattern), which creates all the other ArgoCD applications.

The `app-of-apps.yaml` manifest is generated at the root of your `--output-dir` folder, so you can apply it with:

```shell
kubectl apply --filename GENERATOR_OUTPUT/app-of-apps.yaml
```

## 6. Access ArgoCD

If this is the first time you are using ArgoCD, you will need to retrieve the initial password for the `admin` user:

```shell
echo $(kubectl -n argocd get secret/argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d)
```

This `kubectl` command will port-forward the `argocd-server` Service to your local machine:

```shell
kubectl port-forward --namespace "argocd" svc/argocd-server 8090:https
```

You should now see the ArgoCD interface at [https://localhost:8090](https://localhost:8090), where you can log in with the `admin` user and the password you retrieved in the previous step.

## 7. Sync applications

You can now sync the ArgoCD applications which make up deployKF.

| Group Name              | Group Label                                         | ArgoCD Application Names                                                                                                                                                                                                                                                                                                             |
|-------------------------|-----------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `app-of-apps`           |                                                     | `deploykf-app-of-apps`                                                                                                                                                                                                                                                                                                               |
| `deploykf-dependencies` | `app.kubernetes.io/component=deploykf-dependencies` | `dkf-dep--cert-manager`, `dkf-dep--istio`, `dkf-dep--kyverno`                                                                                                                                                                                                                                                                        |
| `deploykf-core`         | `app.kubernetes.io/component=deploykf-core`         | `dkf-core--deploykf-auth`, `dkf-core--deploykf-dashboard`, `dkf-core--deploykf-istio-gateway`, `dkf-core--deploykf-profiles-generator`                                                                                                                                                                                               |
| `deploykf-opt`          | `app.kubernetes.io/component=deploykf-opt`          | `dkf-opt--deploykf-minio`, `dkf-opt--deploykf-mysql`                                                                                                                                                                                                                                                                                 |
| `deploykf-tools`        | `app.kubernetes.io/component=deploykf-tools`        | N/A                                                                                                                                                                                                                                                                                                                                  |
| `kubeflow-dependencies` | `app.kubernetes.io/component=kubeflow-dependencies` | `kf-dep--argo-workflows`                                                                                                                                                                                                                                                                                                             |
| `kubeflow-tools`        | `app.kubernetes.io/component=kubeflow-tools`        | `kf-tools--katib`, `kf-tools--notebooks--jupyter-web-app`, `kf-tools--notebooks--notebook-controller`, `kf-tools--pipelines`, `kf-tools--poddefaults-webhook`, `kf-tools--tensorboards--tensorboard-controller`, `kf-tools--tensorboards--tensorboards-web-app`, `kf-tools--training-operator`, `kf-tools--volumes--volumes-web-app` |

!!! warning "Sync Order"

    You must sync each "group" of applications in the same order as the table to avoid dependency issues.

!!! warning "Sync Failures"

    Some applications, specifically `dkf-dep--cert-manager` and `dkf-core--deploykf-profiles-generator` may fail to sync on the first attempt, simply wait a few seconds and try the sync again.

??? tip "Syncing with ArgoCD CLI"

    You may also sync the applications with the [`argocd` CLI](https://argo-cd.readthedocs.io/en/stable/cli_installation/), but we recommend syncing with the web interface when you are first getting started so you can debug any issues:
    
    ```shell
    # expose ArgoCD API server
    kubectl port-forward svc/argocd-server -n argocd 8090:https
    
    # get the admin password (if you have not changed it)
    argocd "admin" initial-password -n argocd
    
    # log in to ArgoCD
    ARGOCD_PASSWORD="<YOUR_PASSWORD_HERE>"
    argocd login localhost:8090 --username "admin" --password "$ARGOCD_PASSWORD" --insecure
    
    # sync the apps
    argocd app sync "deploykf-app-of-apps"
    argocd app sync -l "app.kubernetes.io/component=deploykf-dependencies"
    argocd app sync -l "app.kubernetes.io/component=deploykf-core"
    argocd app sync -l "app.kubernetes.io/component=deploykf-opt"
    argocd app sync -l "app.kubernetes.io/component=deploykf-tools"
    argocd app sync -l "app.kubernetes.io/component=kubeflow-dependencies"
    argocd app sync -l "app.kubernetes.io/component=kubeflow-tools"
    ```

## 8. Access deployKF

If you have not configured a public Service for your `deploykf-istio-gateway`, you may access the deployKF web interface with `kubectl` port-forwarding.

First, you will need to add some lines to your `/etc/hosts` file (this is needed because Istio uses the `Host` header to route requests to the correct VirtualService).
For example, if you have set the `deploykf_core.deploykf_istio_gateway.gateway.hostname` value to `"deploykf.example.com"`, you would add the following lines:

```
127.0.0.1 deploykf.example.com
127.0.0.1 argo-server.deploykf.example.com
127.0.0.1 minio-api.deploykf.example.com
127.0.0.1 minio-console.deploykf.example.com
```

Finally, this `kubectl` command will port-forward the `deploykf-gateway` Service to your local machine:

```shell
kubectl port-forward --namespace "deploykf-istio-gateway" svc/deploykf-gateway 8080:http 8443:https
```

You should now see the deployKF dashboard at [https://deploykf.example.com:8443/](https://deploykf.example.com:8443/), where you can use one of the following credentials (if you have not changed them):

| User                  | Username            | Password |
|-----------------------|---------------------|----------|
| Admin (Profile Owner) | `admin@example.com` | `admin`  |
| User 1                | `user1@example.com` | `user1`  |
| User 2                | `user2@example.com` | `user2`  |


## Next Steps

- [Join the deployKF community](../about/community.md)
- [Get Support](../about/support.md)