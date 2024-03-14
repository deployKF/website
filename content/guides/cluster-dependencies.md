---
icon: material/view-list
description: >-
  Learn about the cluster dependencies of deployKF and how to configure them.
---

# Cluster Dependencies

Learn about the cluster dependencies of deployKF and how to configure them.

---

## Overview

deployKF has __"cluster dependencies"__ which are required to run the platform.
In this case "cluster" means Kubernetes applications or services (e.g. istio, cert-manager).

!!! tip "Existing Versions"

    By default, all cluster dependencies are installed as part of deployKF.
    However, you may __use existing versions of these dependencies__, if you already have them installed.

## Cluster Dependency Guides

The following table lists the cluster dependencies, and how to use an existing version:

Dependency | Purpose in deployKF | Use Existing Version
--- | --- | ---
[Argo CD](./dependencies/argocd.md#what-is-argo-cd) | [Used to deploy and manage the lifecycle of the platform.](./dependencies/argocd.md#how-does-deploykf-use-argo-cd) | [Required](./dependencies/argocd.md#can-i-use-my-existing-argo-cd)
[Cert-Manager](./dependencies/cert-manager.md#what-is-cert-manager) | [Generating and maintaining TLS/HTTPS certificates.](./dependencies/cert-manager.md#how-does-deploykf-use-cert-manager) | [Optional](./dependencies/cert-manager.md#can-i-use-my-existing-cert-manager)
[Istio](./dependencies/istio.md#what-is-istio) | [Network service mesh for the platform, used to enforce client authentication and secure internal traffic.](./dependencies/istio.md#how-does-deploykf-use-istio) | [Optional](./dependencies/istio.md#can-i-use-my-existing-istio)
[Kyverno](./dependencies/kyverno.md#what-is-kyverno) | [Mutating resources, replicating secrets across namespaces, and restarting Pods when configs change.](./dependencies/kyverno.md#how-does-deploykf-use-kyverno) | <s>[Optional](./dependencies/kyverno.md#can-i-use-my-existing-kyverno)</s><br><small>(coming soon)</small>