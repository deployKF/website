# Migrate from Kubeflow Manifests

This guide explains how to migrate from an existing deployment of __Kubeflow__ to __deployKF__.

## 1. Understand the Differences

Before migrating, you may wish to review our detailed [__deployKF__ vs  __Kubeflow__](../about/kubeflow-vs-deploykf.md) comparison.

## 2. Create a New Deployment

The best way to migrate from __Kubeflow Manifests__ to __deployKF__ is to spin up deployKF in a separate Kubernetes cluster, and then migrate your data manually.

To create a new deployment of deployKF, follow the [Getting Started](getting-started.md) guide.

!!! warning
    
    Kubeflow Manifests and deployKF __can NOT be deployed concurrently__ in the same Kubernetes cluster, doing so will result in unexpected behavior.

## 3. Migrate your data

Once you have a new deployment of deployKF, you can migrate the data from specific Kubeflow tools to their deployKF equivalents.

For example, you will likely need to migrate your existing __Kubeflow Pipelines__ (scheduled runs, pipeline definitions) and __Kubeflow Notebooks__ (user volume data) to the new deployment.