---
icon: material/arrow-up-circle
description: >-
  Learn how to upgrade your deployKF version and values.
---

# Upgrading

Learn how to upgrade your deployKF version and values.

---

## Overview

Upgrading deployKF is usually a straightforward process.
By "upgrading", we mean updating the [version of deployKF](../releases/changelog-deploykf-cli.md) and/or the [values](./values.md) used to configure it.

## Upgrading Versions

Typically, you can upgrade deployKF in-place by updating your `--source-version` (or `source_version` when using the plugin) and then re-syncing your ArgoCD Applications as normal.

This may result in downtime, so you should plan accordingly.

!!! danger
    
    Before upgrading, review the [changelog](../releases/changelog-deploykf.md) for any upgrade notes.

## Updating Values

Typically, you can update your deployKF values by simply changing them and re-syncing your ArgoCD Applications.
Depending on the changes, you may need to sync with __pruning enabled__ to remove old resources.


!!! warning "Pruning"

    In general, if ArgoCD says pruning is required, you should sync with pruning enabled.
    Otherwise, deployKF may not function correctly.

    ---

    Due to an issue with ArgoCD ([`argoproj/argo-cd#14338`](https://github.com/argoproj/argo-cd/issues/14338)), resources that we annotate as [`argocd.argoproj.io/compare-options: IgnoreExtraneous`](https://argo-cd.readthedocs.io/en/stable/user-guide/compare-options/#ignoring-resources-that-are-extraneous) and [`argocd.argoproj.io/sync-options: Prune=false`](https://argo-cd.readthedocs.io/en/stable/user-guide/sync-options/#no-prune-resources) will show as "requires pruning" in the UI.
    These resources will NOT actually be pruned during a sync, but they are hard to distinguish from those that will.

    deployKF will always have a number of these "extraneous" resources.
    This is because we replicate secrets to other namespaces which are themselves managed by ArgoCD applications.
    ArgoCD tracks the resources it "owns" with the [`app.kubernetes.io/instance`](https://argo-cd.readthedocs.io/en/stable/user-guide/resource_tracking/) label (which will be unchanged in the replicated secret).
    This is actually a good thing, as it means if you delete the source application, the replicated secret will also be deleted.