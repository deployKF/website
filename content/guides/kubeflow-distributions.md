---
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

    To learn more about deployKF itself, please see the [Introduction](../about/introduction.md).

### __Why migrate to deployKF?__

!!! question_secondary ""

    We have seen many users struggle with the complexity of deploying Kubeflow.
    Many users spend days or weeks trying to get Kubeflow working, only to give up in frustration.
    This is why we created __deployKF__.
    
    Unlike other distributions, deployKF behaves like a __Helm Chart for Kubeflow__.
    deployKF has centralized [configuration values](../reference/deploykf-values.md) for all aspects of the platform, so you should __never__ need to edit Kubernetes YAML files or deal with Kustomize patches.
    
### __How are Kubeflow and deployKF related?__

!!! question_secondary ""

    Kubeflow and deployKF are two different but related projects.

    You may wish to review our detailed [:custom-deploykf-color: __deployKF__ vs :custom-kubeflow-color: __Kubeflow Manifests__](../about/kubeflow-vs-deploykf.md#deploykf-vs-kubeflow-manifests) comparison.
    Note, most other [distributions of Kubeflow](https://www.kubeflow.org/docs/started/installing-kubeflow/#packaged-distributions-of-kubeflow) use __largely unmodified__ versions of the Kubeflow Manifests. 
    So the comparison is also relevant to them.

### __Is deployKF a Helm Chart for Kubeflow?__

!!! question_secondary ""

    The very short answer is that _Kubeflow is too complex to be deployed as a single Helm Chart_ (we tried... it was not pretty and was impossible to maintain).
    
    The slightly longer answer is that Kubeflow is a cluster-wide platform of many different components and dependencies.
    Helm lacks the sequencing and dependency management features required to deploy Kubeflow in a single chart.
    
    deployKF addresses these challenges by being a __collection of Helm Charts__ (and some Kustomize apps) which are configured by a [single set of values](../reference/deploykf-values.md).
    You may think of them like "global" Helm values as you only need to configure them once, even though they control multiple internal apps.
    
### __Does deployKF support ArgoCD and GitOps?__

!!! question_secondary ""

    Yes, deployKF actually [depends on ArgoCD](getting-started.md#3-platform-deployment).

    We use ArgoCD because it gives a pre-built system to determine the sync-state of the apps we deploy (if resources need to be updated), and also makes cleaning up old resources much easier.
    In the future, we may add support for other GitOps tools or implement our own.
    
    Note, the [deployKF ArgoCD Plugin](./dependencies/argocd.md#what-is-the-deploykf-argocd-plugin) can optionally be used instead of rendering the manifests into a git repo, which makes deployKF behave even more like a Helm Chart.

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