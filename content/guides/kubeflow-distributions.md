---
icon: material/swap-horizontal
description: >-
  Learn about migrating to deployKF from Kubeflow Distributions like Kubeflow Manifests, Kubeflow on AWS, Kubeflow on GCP, and Charmed Kubeflow.
---

# Migrate from Kubeflow Distributions

Learn about migrating to __deployKF__ from other __Kubeflow Distributions__ like _Kubeflow Manifests_, _Kubeflow on AWS_, _Kubeflow on GCP_ and _Charmed Kubeflow_.

---

## About Migrating

Here are some common questions about migrating from other Kubeflow Distributions to deployKF.
To learn how to migrate, please see the [Steps to Migrate](#steps-to-migrate) section below.

### __What is deployKF?__

!!! question_secondary ""

    <strong><span class="deploykf-orange">deploy</span><span class="deploykf-blue">KF</span></strong> builds machine learning platforms on Kubernetes.
    
    To learn more about deployKF itself, please see the introduction page:

    [Introduction to deployKF](../about/introduction.md#about-deploykf){ .md-button .md-button--secondary }

### __How are Kubeflow and deployKF related?__

!!! question_secondary ""

    Kubeflow and deployKF are two different but related projects.
    By using deployKF, you get everything that Kubeflow offers, plus a lot more.

    To learn more about the differences, please see the comparison page:

    [Comparison between :custom-deploykf-color: _deployKF_ and :custom-kubeflow-color: _Kubeflow_](../about/kubeflow-vs-deploykf.md){ .md-button .md-button--secondary }

### __Why migrate to deployKF?__

!!! question_secondary ""

    We have seen many users struggle with the complexity of deploying Kubeflow.
    Many users spend days or weeks trying to get Kubeflow working, only to give up in frustration.
    This is why we created deployKF.
    
    Unlike other distributions, deployKF behaves like a __Helm Chart for Kubeflow__,
    with centralized [configuration values](../guides/values.md) for all aspects of the platform, so you should __never__ need to edit Kubernetes YAML files or deal with Kustomize patches.

### __Other Questions__

??? question_secondary "Does deployKF support ArgoCD?"

    Yes, deployKF actually [requires ArgoCD](./dependencies/argocd.md#how-does-deploykf-use-argo-cd).

    In the future, we may add support for other GitOps tools or implement our own. 
    Also note, the [deployKF ArgoCD Plugin](./dependencies/argocd.md#what-is-the-deploykf-argocd-plugin) can optionally be used, which makes deployKF behave even more like a Helm Chart.

??? question_secondary "Is deployKF a Helm Chart for Kubeflow?"

    No. 
    The very short answer is that _Kubeflow is too complex to be deployed as a single Helm Chart_, it's closer to an entire cloud platform than a single app.
    
    The slightly longer answer is that Kubeflow is a cluster-wide platform of many different components and dependencies.
    Helm lacks the sequencing and dependency management features required to deploy Kubeflow in a single chart.
    deployKF addresses these challenges by being a __collection of Helm Charts__ (and some Kustomize apps) which are configured by a [single set of values](../guides/values.md).
    You may think of them like "global" Helm values as they control multiple internal apps.

---

## Steps to Migrate

Once you have decided to migrate to deployKF, you will need to follow these steps.

### 1. Create a New Deployment

The best way to migrate from __Kubeflow Manifests__ to __deployKF__ is to spin up deployKF in a separate Kubernetes cluster, and then migrate your data manually.

To create a new deployment of deployKF, follow the [Getting Started](getting-started.md) guide.

!!! warning
    
    Kubeflow Manifests and deployKF __can NOT be deployed concurrently__ in the same Kubernetes cluster, doing so will result in unexpected behavior.

### 2. Migrate your data

Once you have a new deployment of deployKF, you can migrate the data from specific Kubeflow tools to their deployKF equivalents.

For example, you will likely need to migrate your existing __Kubeflow Pipelines__ (scheduled runs, pipeline definitions) and __Kubeflow Notebooks__ (user volume data) to the new deployment.