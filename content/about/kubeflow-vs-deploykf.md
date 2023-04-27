---
comparison_data:
  - aspect: Ease of Use
    deploykf:
      - Has a [single set of config values](../reference/deploykf-values.md), no manual YAML manifest patching needed.
      - Upgrades are easy because config values only have minimal [changes between versions](../releases/changelog-deploykf.md).
      - Simplifies [multi-cluster configurations](../topics/production-usage/multiple-clusters.md) with support for shared common values and environment-specific overlays.
      - Options to easily bring and configure your own dependencies like Istio, cert-manager, Argo Workflows, MySQL, S3, and more.
    kubeflow_manifests:
      - Manual patching of YAML manifests required for any changes.
      - Upgrades are difficult because new versions require starting from scratch with the new manifests.
  - aspect: Capabilities
    deploykf:
      - Supports [many ML & Data tools](../reference/tools.md) in addition to Kubeflow's tools.
      - Includes Argo Workflows UI with integrated single sign-on.
      - Optionally includes MinIO Console UI with integrated single sign-on.
    kubeflow_manifests:
      - Limited to Kubeflow's tools.
  - aspect: Customization
    deploykf:
      - Allows selective deployment of MLOps tools through simple config values.
    kubeflow_manifests:
      - Less customizable, and requires difficult patching of YAML manifests.
  - aspect: GitOps
    deploykf:
      - GitOps-native application with built-in support for Argo CD.
    kubeflow_manifests:
      - Lacks native support for Argo CD or other GitOps tools.
  - aspect: Security
    deploykf:
      - Reduced attack vectors compared to Kubeflow Manifests, particularly in Istio configurations.
      - Utilizes standard tools (e.g. `oauth2-proxy`) over unknown tools (e.g. `arrikto/oidc-authservice`).
      - Refreshes session cookies for active users in most cases.
    kubeflow_manifests:
      - Potentially more security vulnerabilities than deployKF.
      - Lacks session cookie refresh for active users in most cases.
---

# Kubeflow vs deployKF

This page aims unpack the differences between __deployKF__ and __Kubeflow__.

## Introduction

__deployKF__ and __Kubeflow__ are two different projects, but they are related:

- _deployKF_ is a tool for deploying Kubeflow and other MLOps tools on Kubernetes.
- _Kubeflow_ is a project that develops many MLOps tools, including Kubeflow Pipelines, Kubeflow Notebooks, Katib, and more.
- _deployKF_ is NOT a fork of Kubeflow, but it does allow you to deploy Kubeflow's MLOps tools.

## Kubeflow vs Kubeflow Manifests

Before a more detailed comparison can be made, it is important to understand the distinction between __Kubeflow__ and __Kubeflow Manifests__.

| Kubeflow                                                                                                     | Kubeflow Manifests                                                                                                                                                |
|--------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| A project that develops many MLOps tools, including Kubeflow Pipelines, Kubeflow Notebooks, Katib, and more. | A set of Kubernetes manifests that can be used to deploy Kubeflow's MLOps tools on Kubernetes, found in the [`kubeflow/manifests`](https://github.com/kubeflow/manifests) repo. |

## deployKF vs Kubeflow Manifests

Hopefully, it is now clear the most useful comparison is between __deployKF__ and __Kubeflow Manifests__ (not the Kubeflow project as a whole).

{{ render_comparison_table(comparison_data) }}

!!! tip "Packaged distributions of Kubeflow"
    
    Most [packaged distribution of Kubeflow](https://www.kubeflow.org/docs/started/installing-kubeflow/#packaged-distributions-of-kubeflow), are using __largely unmodified__ versions of the Kubeflow Manifests, so this comparison is still relevant for them.

## Next Steps

 - If you're ready to start migrating from Kubeflow to deployKF, check out the [Migrate from Kubeflow Manifests](../guides/migrate-from-kubeflow-manifests.md) guide.
