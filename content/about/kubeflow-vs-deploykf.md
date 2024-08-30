---
icon: custom/kubeflow
description: >-
  Understand the differences between Kubeflow and deployKF.

comparison_data:
  - aspect: Ease of Use
    features:
      - name: Easy Configuration
        deploykf: 
          has_feature: true
          description: |-
            Configured with [centralized values](../guides/values.md).
        kubeflow_manifests:
          has_feature: false
          description: |-
            Manual patching of Kustomize manifests.
      - name: Easy Upgrades
        deploykf: 
          has_feature: true
          description: |-
            In-place [upgrades](../guides/upgrade.md) are supported.
            Bring values forward to new versions.
        kubeflow_manifests:
          has_feature: false
          description: |-
            Must start from scratch with each new version.
      - name: Easy Uninstall
        deploykf: 
          has_feature: true
          description: |-
            Straightforward [uninstall](../guides/uninstall.md) process.
        kubeflow_manifests:
          has_feature: false
          description: |-
            No built-in uninstall process.

  - aspect: Tools and Ecosystem
    features:
      - name: |-
          [Kubeflow Ecosystem](../reference/tools.md#kubeflow-ecosystem)
        deploykf: 
          has_feature: true
          description: |-
            Optionally included.
        kubeflow_manifests:
          has_feature: true
          description: |-
            Included.
      - name: Argo Server<br><small>(Web interface of __Argo Workflows__)</small>
        deploykf: 
          has_feature: true
          description: |-
            Optionally included.
            Integrated with single sign-on.
            User access is aligned to [profile memberships](../guides/platform/deploykf-profiles.md).
        kubeflow_manifests:
          has_feature: false
          description: |-
            Not included.
      - name: MinIO Console<br><small>(Web interface of __MinIO__)</small>
        deploykf: 
          has_feature: true
          description: |-
            Optionally included.
            Integrated with single sign-on.
            User access is aligned to [profile memberships](../guides/platform/deploykf-profiles.md).
        kubeflow_manifests:
          has_feature: false
          description: |-
            Not included.

  - aspect: Flexibility and Customization
    features:
      - name: Selectively Enable Tools
        deploykf: 
          has_feature: true
          description: |-
            Each tool has as single `enabled` value.
            [Enable or disable tools](../guides/tools/choose-tools.md).
        kubeflow_manifests:
          has_feature: false
          description: |-
            Requires manual patching of Kustomize manifests.
      - name: Use Existing Cluster Dependencies
        deploykf: 
          has_feature: true
          description: |-
            Easily use existing cluster dependencies.
            [Connect your existing __Istio__](../guides/dependencies/istio.md#can-i-use-my-existing-istio).
            [Connect your existing __cert-manager__](../guides/dependencies/cert-manager.md#can-i-use-my-existing-cert-manager).
            [Connect your existing __Kyverno__](../guides/dependencies/kyverno.md#can-i-use-my-existing-kyverno).
        kubeflow_manifests:
          has_feature: false
          description: |-
            Requires manual patching of Kustomize manifests.
      - name: Connect to Identity Providers
        deploykf: 
          has_feature: true
          description: |-
            Easily connect any identity provider.
            [Connect via __OpenID Connect__ or __LDAP__](../guides/platform/deploykf-authentication.md#provider-examples).
        kubeflow_manifests:
          has_feature: false
          description: |-
            Requires manual patching of Kustomize manifests.
      - name: Connect to External Services
        deploykf: 
          has_feature: true
          description: |-
            Easily connect external services.
            [Connect external __S3__ / __Object Store__](../guides/external/object-store.md#connect-an-external-object-store).
            [Connect external __MySQL__](../guides/external/mysql.md#connect-an-external-mysql).
        kubeflow_manifests:
          has_feature: false
          description: |-
            Requires manual patching of Kustomize manifests.

  - aspect: Special Features
    features:
      - name: ArgoCD Support<br><small>(GitOps)</small>
        deploykf: 
          has_feature: true
          description: |-
            Native support for [GitOps with ArgoCD](../guides/dependencies/argocd.md#how-does-deploykf-use-argo-cd).
        kubeflow_manifests:
          has_feature: false
          description: |-
            No built-in support for ArgoCD.
      - name: Automatic Restarts<br><small>(Config and Secret Changes)</small>
        deploykf: 
          has_feature: true
          description: |-
            When a config or secret is changed, any affected components are automatically restarted using [Kyverno](../guides/dependencies/kyverno.md).
        kubeflow_manifests:
          has_feature: false
          description: |-
            Manual pod restarts are required.
      - name: Declarative Profiles<br><small>(Users and team access)</small>
        deploykf: 
          has_feature: true
          description: |-
            Profiles are [defined via values](../guides/platform/deploykf-profiles.md).
            Easily assign multiple users to a profile.
        kubeflow_manifests:
          has_feature: false
          description: |-
            Profiles are manually created.
      - name: Browser Login Flow<br><small>(Kubeflow Pipelines)</small>
        deploykf: 
          has_feature: true
          description: |-
            Users can authenticate the Kubeflow Pipelines SDK from off-cluster, [using a web browser](../user-guides/access-kubeflow-pipelines-api.md#browser-login-flow).
        kubeflow_manifests:
          has_feature: false
          description: |-
            Not supported.

  - aspect: Security
    features:
      - name: Random Secrets
        deploykf: 
          has_feature: true
          description: |-
            Secrets are randomly generated at install time.
        kubeflow_manifests:
          has_feature: false
          description: |-
            Secrets are hardcoded in manifests.
      
      - name: Hardened Kubeflow Pipelines
        deploykf: 
          has_feature: true
          description: >-
            [Object Store](../guides/external/object-store.md) access keys are isolated to each profile and scoped to the minimum required permissions.
            All access keys are randomly generated.
        kubeflow_manifests:
          has_feature: false
          description: >-
            Object Store access keys are shared across all profiles.
            Access keys are not randomly generated.

      - name: Hardened Istio
        deploykf: 
          has_feature: true
          description: |-
            Easy to update Istio.
            Uses [distroless images](https://istio.io/latest/docs/ops/configuration/security/harden-docker-images/).
            Additional security patches.
            
        kubeflow_manifests:
          has_feature: false
          description: |-
            Istio is difficult to update.
            Standard images.
            
      - name: Standard Auth Tools
        deploykf: 
          has_feature: true
          description: |-
            Uses standard tools including [Envoy](https://github.com/envoyproxy/envoy) (via [Istio](https://github.com/istio/istio)), [oauth2-proxy](https://github.com/oauth2-proxy/oauth2-proxy), and [dex](https://github.com/dexidp/dex).
        kubeflow_manifests:
          has_feature: false
          description: |-
            Uses non-standard [`arrikto/oidc-authservice`](https://github.com/arrikto/oidc-authservice) and often outdated [dex](https://github.com/dexidp/dex).

      - name: HTTPS by Default
        deploykf: 
          has_feature: true
          description: |-
            HTTPS is enabled by default.
        kubeflow_manifests:
          has_feature: false
          description: |-
            HTTPS is NOT enabled by default.

---

# Kubeflow vs deployKF

Understand the differences between Kubeflow and deployKF.

!!! tip "Migrate to deployKF"

    When you're ready to start migrating from vanilla Kubeflow to deployKF, check out our migration guide:

    [Migrate from :custom-kubeflow: Kubeflow Distributions](../guides/kubeflow-distributions.md#steps-to-migrate){ .md-button .md-button--secondary }

---

## Introduction

Kubeflow and deployKF are different but related projects.
By using deployKF, you get everything that Kubeflow offers, plus a lot more.

Before we dive into the differences, let's define each project:

Project | What is it?
--- | ---
:custom-deploykf-color: __deployKF__ | A tool for building Data and Machine Learning platforms on Kubernetes.
:custom-kubeflow-color: __Kubeflow__ | A CNCF project to develop [MLOps tools](../reference/tools.md#kubeflow-ecosystem) that run on Kubernetes.
:custom-kubeflow-color: __Kubeflow Manifests__ | A collection of Kustomize manifests provided by the Kubeflow project.

## **deployKF vs Kubeflow Manifests**

_deployKF_ and _Kubeflow Manifests_ are both used to deploy Kubeflow.
However, they are designed for different purposes and have different features.

|| :custom-kubeflow-color: Kubeflow Manifests | :custom-deploykf-color: deployKF
--- | --- | ---
__Purpose__ | To be used as a base for packaged Kubeflow distributions by vendors. | Enable organizations to build their Data and ML Platforms on Kubernetes.
__Key Feature__ | A collection of Kustomize manifests requiring significant manual patching to use in production. | A [centralized config system](../guides/values.md) to manage all aspects of the platform, very similar to Helm Chart values.

{{ render_comparison_table(comparison_data) }}

## Next Steps

- If you're ready to start migrating from Kubeflow to deployKF, check out the [Migrate from Kubeflow Distributions](../guides/kubeflow-distributions.md) guide.