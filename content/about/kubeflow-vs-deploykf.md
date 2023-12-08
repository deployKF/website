---
icon: custom/kubeflow
description: >-
  How deployKF is related to Kubeflow and Kubeflow Manifests.

comparison_data:
  - aspect: Ease of Use
    deploykf:
      - Has a Helm-like interface, with [values](../reference/deploykf-values.md) for configuring all aspects of the deployment (no need to edit Kubernetes YAML)
      - Upgrades are easy because you can bring your existing config files to new versions. Furthermore, values only have minimal [changes between versions](../releases/changelog-deploykf.md).
    kubeflow_manifests:
      - Manual patching of YAML manifests required for any changes.
      - Upgrades are difficult because new versions require starting from scratch with the new manifests.
  - aspect: Capabilities
    deploykf:
      - Supports [leading tools](../reference/tools.md) from both Kubeflow, and other projects.
      - When a config or secret is changed, any affected components are automatically restarted.
      - Includes Argo Server UI with integrated single sign-on (user access is aligned to [profile memberships](../guides/platform/deploykf-profiles.md) ).
      - Optionally includes MinIO Console UI with integrated single sign-on (user access is aligned to [profile memberships](../guides/platform/deploykf-profiles.md)).
    kubeflow_manifests:
      - Limited to Kubeflow's tools.
  - aspect: Customization
    deploykf:
      - Allows selective deployment of MLOps tools through simple config values.
      - Allows bringing custom versions of dependencies like Istio, cert-manager, [MySQL](../guides/tools/external-mysql.md), [S3](..//guides/tools/external-object-store.md), and more.
    kubeflow_manifests:
      - Less customizable, and requires difficult patching of YAML manifests.
  - aspect: GitOps
    deploykf:
      - GitOps-native application with built-in support for Argo CD.
    kubeflow_manifests:
      - Lacks native support for Argo CD or other GitOps tools.
  - aspect: Security
    deploykf:
      - All secrets are randomly generated at install time, rather than being hardcoded in manifests.
      - Reduced attack vectors compared to Kubeflow Manifests, particularly in Istio configurations.
      - Utilizes standard auth tools (`oauth2-proxy`) over unknown tools (`arrikto/oidc-authservice`).
      - Automatically refreshes session cookies for active users in most cases (users will need to log in less often).
      - Uses Istio with [distroless images](https://istio.io/latest/docs/ops/configuration/security/harden-docker-images/) by default.
      - MinIO (or S3) access keys are isolated to each profile, not shared, and scoped to the minimum required permissions.
      - Supports [using AWS IRSA](../guides/tools/external-object-store.md#irsa-based-authentication) instead of S3 access keys.
    kubeflow_manifests:
      - Potentially more security vulnerabilities than deployKF.
      - Lacks session cookie refresh for active users in most cases.
      - HTTPS is NOT enabled by default.
---

# Kubeflow vs deployKF

This page unpacks how __deployKF__ is related to __Kubeflow__ and __Kubeflow Manifests__.

!!! info "Migrate to deployKF"

    When you're ready to start migrating from Kubeflow to deployKF, check out the [Migrate from Kubeflow Distributions](../guides/kubeflow-distributions.md) guide.

---

## _Kubeflow_ vs _deployKF_

!!! value ""

    Kubeflow and deployKF are two different but related projects:
      
    - :custom-deploykf-color: __deployKF__ is a tool for building Data and ML platforms on Kubernetes. It includes Kubeflow tools, as well as tools from other projects.
    - :custom-kubeflow-color: __Kubeflow__ is a project to develop MLOps tools for Kubernetes. Some popular Kubeflow tools are Kubeflow Pipelines, Kubeflow Notebooks, Katib, and KServe.

## _Kubeflow_ vs _Kubeflow Manifests_

!!! value ""

    The :custom-kubeflow-color: __Kubeflow__ project provides Kubernetes manifests for its tools under the name __Kubeflow Manifests__.
    These manifests are hosted in the [`kubeflow/manifests`](https://github.com/kubeflow/manifests) repo, and are used in some way by most Kubeflow distributions (including deployKF).
    
    The __Kubeflow Manifests__ are NOT intended to be used directly by end-users.
    They are simply a collection of Kustomize manifests, and require significant manual patching to use in production.

## _deployKF_ vs _Kubeflow Manifests_

!!! value ""

    While __deployKF__ and __Kubeflow Manifests__ can both be used to deploy Kubeflow tools on Kubernetes, they are not aimed at the same audience.
    
    - :custom-deploykf-color: __deployKF__ is intended to be used by organizations to build their Data and ML Platforms on Kubernetes.
      It provides a Helm-like interface for configuring and deploying Kubeflow (and other MLOps tools) on Kubernetes.
    - :custom-kubeflow-color: __Kubeflow Manifests__ are intended to be used by Kubeflow distribution maintainers, not end-users.
    They are simply a collection of Kustomize manifests, and require significant manual patching to use in production.

{{ render_comparison_table(comparison_data) }}

## Next Steps

- If you're ready to start migrating from Kubeflow to deployKF, check out the [Migrate from Kubeflow Distributions](../guides/kubeflow-distributions.md) guide.