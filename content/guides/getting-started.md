# Getting Started

This guide will help you get started with __deployKF__.

!!! tip
    
    If you have an existing deployment of __Kubeflow Manifests__, there is a [migration guide](migrate-from-kubeflow-manifests.md) for you.

## Step 1: understand deployKF

Before starting, you should read a little about what __deployKF__ is and how it works, a great place to start is the [Frequently Asked Questions (FAQ)](../faq.md) page.

## Step 2: prepare requirements

### Minimum Requirements

- a Kubernetes cluster with [ArgoCD](https://argo-cd.readthedocs.io/en/stable/getting_started/) installed (see [Kubernetes version compatability](../releases/version-matrix.md#deploykf-dependencies))
- the `deploykf` cli tool (see [Install the deployKF CLI](install-deploykf-cli.md))
- a private git repo in which to store your generated manifests

!!! warning "Dedicated Kubernetes Cluster"

    deployKF is a complex tool, and only __one instance__ can be deployed on a Kubernetes cluster at a time.

    It is strongly recommended that you create a __dedicated Kubernetes cluster__ for your deployment of deployKF.

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

## Step 3: TBA

TBA