# Quickstart Guide

## Step 1. prepare requirements

!!! info

    To use `deployKF` you will need a Kubernetes cluster with [ArgoCD](https://argoproj.github.io/cd/) installed.

    Here are some popular distributions of Kubernetes, listed by platform.
    
    Platform | Kubernetes Distribution
    --- | ---
    Local Machine | [k3d](https://k3d.io/)
    Local Machine | [kind](https://kind.sigs.k8s.io/)
    Local Machine | [minikube](https://minikube.sigs.k8s.io/)
    Amazon Web Services | [Amazon Elastic Kubernetes Service (EKS)](https://aws.amazon.com/eks/)
    Microsoft Azure | [Azure Kubernetes Service (AKS)](https://azure.microsoft.com/en-au/services/kubernetes-service/)
    Google Cloud | [Google Kubernetes Engine (GKE)](https://cloud.google.com/kubernetes-engine)
    Alibaba Cloud | [Alibaba Cloud Container Service for Kubernetes (ACK)](https://www.alibabacloud.com/product/kubernetes)
    IBM Cloud | [IBM Cloud Kubernetes Service (IKS)](https://www.ibm.com/cloud/kubernetes-service)

### Remote Dependencies

- Kubernetes ([version compatability matrix](../reference/version-compatibility-matrix.md#kubernetes))
- ArgoCD ([deploying ArgoCD](https://argo-cd.readthedocs.io/en/stable/getting_started/))
- (Optional) an external MySQL database ([connecting your database](../topics/production-usage/external-mysql-database.md))
- (Optional) an external S3-compatible object store ([connecting your object store](../topics/production-usage/external-object-store.md))

### Local Dependencies

- Gomplate ([installing gomplate](https://docs.gomplate.ca/installing/))


## Step 2. TBA

TBA