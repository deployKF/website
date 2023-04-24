---
comparison_data:
  - aspect: Ease of Use
    deploykf:
      - Has a [single set of config values](../reference/deploykf-values.md), no manual YAML manifest patching needed.
      - Upgrades are easy because config values only have minimal [changes between versions](../releases/changelog-deploykf.md).
      - Simplifies [multi-cluster configurations](../topics/production-usage/multiple-clusters.md) with support for shared common values and environment-specific overlays.
    kubeflow_manifests:
      - Manual patching of YAML manifests required for any changes.
      - Upgrades are difficult because new versions require starting from scratch with the new manifests.
  - aspect: GitOps Support
    deploykf:
      - GitOps-native application with built-in support for ArgoCD.
    kubeflow_manifests:
      - Lacks native support for ArgoCD or other GitOps tools.
  - aspect: Capabilities
    deploykf:
      - Supports not only [Kubeflow MLOps tools](../releases/version-matrix.md#kubeflow-tools) but also other [best-in-class MLOps tools](../releases/version-matrix.md#deploykf-tools).
      - Includes Argo Workflows UI with single sign-on (SSO).
      - Optionally includes MinIO Console UI with SSO.
    kubeflow_manifests:
      - Limited to Kubeflow MLOps tools.
  - aspect: Customization
    deploykf:
      - Allows selective deployment of MLOps tools through single config values.
      - Option to easily bring and configure your own dependencies (Istio, cert-manager, Argo Workflows, MySQL, etc.).
    kubeflow_manifests:
      - Less customizable than deployKF.
  - aspect: Security
    deploykf:
      - Reduced attack vectors compared to Kubeflow Manifests, particularly in Istio configurations.
      - Utilizes standard tools (e.g. `oauth2-proxy`) over unknown tools (e.g. `arrikto/oidc-authservice`).
      - Refreshes session cookies for active users in most cases.
    kubeflow_manifests:
      - Potentially more security vulnerabilities than deployKF.
      - Lacks session cookie refresh for active users in most cases.
---

# Migrate from Kubeflow Manifests

This guide will help you migrate from an existing deployment of __Kubeflow Manifests__ to __deployKF__.

## Step 1: understand the differences

### Kubeflow vs Kubeflow Manifests

First, let's clarify the distinction between __Kubeflow__ and the __Kubeflow Manifests__.

| Kubeflow                                                                                                     | Kubeflow Manifests                                                                                                                                                |
|--------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| A project that develops many MLOps tools, including Kubeflow Pipelines, Kubeflow Notebooks, Katib, and more. | A set of Kubernetes manifests that can be used to deploy Kubeflow on Kubernetes, found in the [`kubeflow/manifests`](https://github.com/kubeflow/manifests) repo. |

!!! note
    
    Even if you currently use a [packaged distribution of Kubeflow](https://www.kubeflow.org/docs/started/installing-kubeflow/#packaged-distributions-of-kubeflow), you are likely still using a __largely unmodified__ version of the Kubeflow Manifests.

### deployKF vs Kubeflow Manifests

Now, let's look at the differences between __deployKF__ and __Kubeflow Manifests__.

{{ render_comparison_table(comparison_data) }}

## Step 2: create a new deployment

The best way to migrate from __Kubeflow Manifests__ to __deployKF__ is to create a new deployment of deployKF alongside your existing Kubeflow Manifests deployment, in a separate Kubernetes cluster.

!!! warning

    Kubeflow Manifests and deployKF __can NOT be deployed concurrently__ in the same Kubernetes cluster, doing so will result in unexpected behavior.

To create a new deployment of deployKF, follow the [Getting Started](getting-started.md) guide.

## Step 3: migrate your data

Once you have a new deployment of deployKF, you can migrate the data from specific Kubeflow tools to their deployKF equivalents.

### Migrate Kubeflow Pipelines data

TBA

### Migrate Kubeflow Notebooks data

TBA