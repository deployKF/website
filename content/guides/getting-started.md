# Getting Started

This guide will help you get started with __deployKF__.

!!! tip
    
    If you have an existing deployment of __Kubeflow Manifests__, there is a [migration guide](migrate-from-kubeflow-manifests.md) for you.

## 1. Understand deployKF

Before starting, you should learn a little about __deployKF__ and how it works.

### What is deployKF?

__deployKF__ is the best way to build reliable ML Platforms on Kubernetes.
  
- _deployKF_ supports all the top [ML & Data tools](../reference/tools.md) from both Kubeflow, and other projects
- _deployKF_ has a Helm-like interface, with central [values (configs)](../reference/deploykf-values.md) for configuring all aspects of the deployment (no need to edit Kubernetes YAML directly)
- _deployKF_ does NOT install resources into your cluster, instead it generates [Argo CD Applications](https://argo-cd.readthedocs.io/en/stable/operator-manual/declarative-setup/#applications){target=_blank} which you apply to your cluster and then [sync with the Argo CD UI](https://argo-cd.readthedocs.io/en/stable/getting_started/#syncing-via-ui){target=_blank}

### Why use Argo CD?

ML Platforms are made up of many components and interconnected dependencies,
attempting to install (let alone upgrade) all these components with `kubectl` or `helm` is a recipe for disaster.

This is where GitOps comes in, it allows us to define the state (i.e. Kubernetes manifests) of all the components in a single place (Git), and then use a tool to reconcile the actual state of our cluster to match the defined state.

[__Argo CD__](https://argo-cd.readthedocs.io/en/stable/){target=_blank} is a great tool for this job, it is [__widely used__](https://github.com/argoproj/argo-cd/blob/master/USERS.md){target=_blank}, [__part of the CNCF__](https://www.cncf.io/projects/argo/){target=_blank}, and has a [__great Web UI__](/assets/images/argocd-ui.gif){target=_blank} for visualizing and managing the current state of your cluster.

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

## 2. Prepare Requirements

### Minimum Requirements

- a Kubernetes cluster with [Argo CD](https://argo-cd.readthedocs.io/en/stable/getting_started/) installed (see [Kubernetes version compatability](../releases/version-matrix.md#deploykf-dependencies))
- the `deploykf` cli tool (see [Install the deployKF CLI](install-deploykf-cli.md))
- a private git repo in which to store your generated manifests

!!! warning "Dedicated Kubernetes Cluster"

    deployKF is a complex tool, and only __one instance__ can be deployed on a Kubernetes cluster at a time.
    It is strongly recommended that you create a __dedicated Kubernetes cluster__ for your deployment of deployKF.

!!! tip "Virtual Kubernetes Clusters"

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

!!! warning "MinIO License"
  
    If you choose to not connect an external S3-compatible object store, deployKF will use [MinIO](https://github.com/minio/minio), ensure you are familiar with MinIO's licence, which at the time of writing is [AGPLv3](https://github.com/minio/minio/blob/master/LICENSE).
    However, rest assured that deployKF __does NOT contain any code from MinIO__, and is licensed under the [Apache 2.0 License](https://github.com/deployKF/deployKF/blob/main/LICENSE).

??? info "Managed MySQL Services"

    Here are some popular managed MySQL services listed by platform.
    
    Platform | Managed MySQL Service
    --- | ---
    Amazon Web Services | [Amazon Relational Database Service (RDS)](https://aws.amazon.com/rds/)
    Microsoft Azure | [Azure Database for MySQL](https://azure.microsoft.com/en-us/services/mysql/)
    Google Cloud | [Cloud SQL](https://cloud.google.com/sql)
    Alibaba Cloud | [ApsaraDB RDS for MySQL](https://www.alibabacloud.com/product/apsaradb-for-rds-mysql)
    IBM Cloud | [IBM Cloud Databases for MySQL](https://www.ibm.com/cloud/databases-for-mysql)

??? info "S3-Compatible Object Stores"

    Here are some popular S3-compatible object stores listed by platform.
    
    Platform | S3-compatible Object Store
    --- | ---
    Amazon Web Services | [Amazon Simple Storage Service (S3)](https://aws.amazon.com/s3/)
    Microsoft Azure | [Azure Blob Storage](https://azure.microsoft.com/en-us/services/storage/blobs/)
    Google Cloud | [Google Cloud Storage](https://cloud.google.com/storage)
    Alibaba Cloud | [Alibaba Cloud Object Storage Service (OSS)](https://www.alibabacloud.com/product/oss)
    IBM Cloud | [IBM Cloud Object Storage](https://www.ibm.com/cloud/object-storage)
    Other | [MinIO](https://min.io/), [Ceph](https://ceph.io/), [Wasabi](https://wasabi.com/)

## 3. TBA

deployKF is currently in development, this guide will be updated when it is ready for use.