---
icon: material/delete
description: >-
  Learn how to uninstall deployKF.

search:
  boost: 1.5
---

# Uninstall

Learn how to uninstall deployKF.

---

## Overview

Uninstalling deployKF is usually a straightforward process.
Take care to ensure you have __backed up any important data__ before proceeding.

## 1. Remove Applications

First, we will delete all the ArgoCD Applications that were installed by deployKF. 
This should remove almost all the resources that were created by deployKF.

!!! danger

    This will delete ALL resources that were created by deployKF (including Profile Namespaces).
    Ensure you have __backed up any important data__ before proceeding (e.g. PersistentVolumeClaims).

!!! warning

    Deleting the app-of-apps with `kubectl` will NOT delete the internal applications.
    You MUST delete the app-of-apps with the `argocd` CLI or the ArgoCD Web UI.

    If you accidentally delete the app-of-apps with `kubectl`, you will need to re-apply it so you can delete it properly.

The following commands will delete the `deploykf-app-of-apps` application (and its internal apps) using the `argocd` CLI:

```bash
# set configuration variables
export ARGOCD_NAMESPACE="argocd"
export ARGOCD_USERNAME="admin"
export ARGOCD_PASSWORD=$(
  # NOTE: this will only work if you have not changed the password
  #       otherwise, replace this with your password
  kubectl get secret \
    "argocd-initial-admin-secret" \
    --namespace "$ARGOCD_NAMESPACE" \
    --output jsonpath="{.data.password}" \
  | base64 -d
)

# login to argocd
argocd login \
  --username "$ARGOCD_USERNAME" \
  --password "$ARGOCD_PASSWORD" \
  --port-forward \
  --port-forward-namespace "$ARGOCD_NAMESPACE"

# delete the app-of-apps application
# NOTE: you may see "PermissionDenied" if the app does not exist
argocd app delete deploykf-app-of-apps \
  --port-forward \
  --port-forward-namespace "$ARGOCD_NAMESPACE"
```

## 2. Remove Webhooks

Kyverno is badly behaved and does not clean up its webhooks when it is uninstalled ([`kyverno/kyverno#9551`](https://github.com/kyverno/kyverno/issues/9551)).

The following commands will delete the `ValidatingWebhookConfigurations` and `MutatingWebhookConfigurations` that were created by Kyverno:

```bash
# remove ValidatingWebhookConfigurations
kubectl delete validatingwebhookconfigurations \
  --selector=webhook.kyverno.io/managed-by=kyverno

# remove MutatingWebhookConfigurations
kubectl delete mutatingwebhookconfigurations \
  --selector=webhook.kyverno.io/managed-by=kyverno
```

## 3. Remove Namespaces

deployKF will leave behind all Namespaces that it creates (except for Profile Namespaces).

The following command will delete all Namespaces that were created by deployKF:

```bash
# WARNING: remove `--dry-run=client` after you have verified the output
#          ONLY contains Namespaces you are happy to delete
kubectl delete namespaces --dry-run=client \
  --selector=app.kubernetes.io/instance=deploykf-app-of-apps
```

## 4. Remove ArgoCD

If you no longer need ArgoCD, you can remove it with the following command:

```bash
kubectl delete namespace argocd
```