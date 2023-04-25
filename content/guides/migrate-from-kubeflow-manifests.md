# Migrate from Kubeflow Manifests

This guide will help you migrate from an existing deployment of __Kubeflow Manifests__ to __deployKF__.

## 1. Understand the Differences

Before migrating, you may wish to review our detailed [comparison between __deployKF__ and  __Kubeflow__](../about/kubeflow-vs-deploykf.md).

## 2. Create a New Deployment

The best way to migrate from __Kubeflow Manifests__ to __deployKF__ is to create a new deployment of deployKF alongside your existing Kubeflow Manifests deployment, in a separate Kubernetes cluster.

!!! warning

    Kubeflow Manifests and deployKF __can NOT be deployed concurrently__ in the same Kubernetes cluster, doing so will result in unexpected behavior.

!!! tip "Virtual Kubernetes Clusters"

    If you are unable to create a new Kubernetes cluster, you may consider using [vcluster](https://github.com/loft-sh/vcluster) to create a virtual Kubernetes cluster within an existing one.
    This approach has additional benefits because deployKF uses cluster-wide components (e.g. Istio) and namespaces for user/team profiles, so is not well suited to multi-tenant clusters.

To create a new deployment of deployKF, follow the [Getting Started](getting-started.md) guide.

## 3. Migrate your data

Once you have a new deployment of deployKF, you can migrate the data from specific Kubeflow tools to their deployKF equivalents.

### Migrate Kubeflow Pipelines data

TBA

### Migrate Kubeflow Notebooks data

TBA