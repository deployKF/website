---
comparison_data:
  - aspect: Ease of Use
    deploykf:
      - Has a Helm-like interface, with [values](../reference/deploykf-values.md) for configuring all aspects of the deployment (no need to edit Kubernetes YAML)
      - Upgrades are easy because config values only have minimal [changes between versions](../releases/changelog-deploykf.md).
    kubeflow_manifests:
      - Manual patching of YAML manifests required for any changes.
      - Upgrades are difficult because new versions require starting from scratch with the new manifests.
  - aspect: Capabilities
    deploykf:
      - Supports leading [MLOps & Data tools](../reference/tools.md) from both Kubeflow, and other projects.
      - When a config or secret is changed, any affected components are automatically restarted.
      - Includes Argo Server UI with integrated single sign-on where access is aligned to profile membership.
      - Optionally includes MinIO Console UI with integrated single sign-on where access is aligned to profile membership.
    kubeflow_manifests:
      - Limited to Kubeflow's tools.
  - aspect: Customization
    deploykf:
      - Allows selective deployment of MLOps tools through simple config values.
      - Allows brining custom versions of dependencies like Istio, cert-manager, MySQL, S3, and more.
      - Simplifies multi-cluster configurations with support for shared common values and environment-specific overlays.
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
      - Automatically refreshes session cookies for active users in most cases.
      - Uses Istio with [distroless images](https://istio.io/latest/docs/ops/configuration/security/harden-docker-images/) by default.
      - MinIO (or S3) access keys are isolated to each profile, not shared, and scoped to the minimum required permissions.
      - Supports using [AWS IRSA](https://github.com/deployKF/deployKF/blob/v0.1.0/generator/default_values.yaml#L1651-L1668) instead of S3 access keys.
    kubeflow_manifests:
      - Potentially more security vulnerabilities than deployKF.
      - Lacks session cookie refresh for active users in most cases.
---

# Kubeflow vs deployKF

This page aims to unpack the differences between __deployKF__ and __Kubeflow__.

!!! warning "Packaged distributions of Kubeflow"
    
    The other [distributions of Kubeflow](https://www.kubeflow.org/docs/started/installing-kubeflow/#packaged-distributions-of-kubeflow), are using __mostly unmodified__ versions of the Kubeflow Manifests, so the following comparison is still relevant for them.

---

## Overview

__Kubeflow__ and __deployKF__ are two different but related projects:
  
- deployKF is a tool for deploying Kubeflow and other MLOps tools on Kubernetes as a cohesive platform.
- Kubeflow is a project that develops MLOps tools, including Kubeflow Pipelines, Kubeflow Notebooks, Katib, and more.

## Kubeflow vs Kubeflow Manifests

Before a more detailed comparison can be made, it is important to understand the distinction between __Kubeflow__ and __Kubeflow Manifests__.

<table>
  <tr>
    <th>
      Kubeflow
    </th>
    <td>
      A project that develops many MLOps tools, including Kubeflow Pipelines, Kubeflow Notebooks, Katib, and more.
    </td>
  </tr>
  <tr>
    <th>
      Kubeflow Manifests
    </th>
    <td>
      A set of Kubernetes manifests that can be used to deploy Kubeflow's MLOps tools on Kubernetes, found in the <a href="https://github.com/kubeflow/manifests"><code>kubeflow/manifests</code></a> repo.
    </td>
  </tr>
</table>

## deployKF vs Kubeflow Manifests

Hopefully, it is now clear the most useful comparison is between __deployKF__ and __Kubeflow Manifests__ (not the Kubeflow project as a whole).

The following table compares the two projects across a number of different aspects:

{{ render_comparison_table(comparison_data) }}

## Next Steps

- If you're ready to start migrating from Kubeflow to deployKF, check out the [Migrate from Kubeflow Manifests](../guides/migrate-from-kubeflow-manifests.md) guide.