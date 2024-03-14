---
icon: material/view-list
description: >-
  Learn about the "modes of operation" in deployKF.
---

# Modes of Operation

Learn about the "modes of operation" in deployKF.

---

## Overview

There are two ways to use deployKF which we call ___"modes of operation"___.
These modes change how the Kubernetes manifests are generated and applied to your cluster.

The following table summarizes the two modes:

Mode | Description
--- | ---
ArgoCD Plugin Mode | You install the [__deployKF ArgoCD Plugin__](./dependencies/argocd.md#what-is-the-deploykf-argocd-plugin) on your ArgoCD instance. The plugin adds a new kind of ArgoCD `Application` which understands deployKF config values and can generate manifests directly, without requiring a git repo.
Manifests Repo Mode | You use the [`deploykf` CLI](deploykf-cli.md#about-the-cli) to generate manifests (including ArgoCD `Applications`). You commit these generated manifests to a git repo for ArgoCD to apply to your cluster.

To learn how to use each mode, see the [Getting Started](./getting-started.md#create-argocd-applications) guide.

!!! tip "Recommended _Mode of Operation_"

    For most users, we recommend the __ArgoCD Plugin Mode__.