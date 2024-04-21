---
icon: material/table
description: >-
  The versions of dependencies supported by each version of deployKF.
---

# Version Matrix

The versions of __dependencies__ supported by each version of deployKF.

---

!!! info "Table Key"

    - :fontawesome-solid-check: Supported
    - :fontawesome-solid-xmark: Not Supported
    - :fontawesome-regular-circle-check: Default Included Version

### Kubernetes

{{ read_csv("./version-matrix--kubernetes.csv", colalign=("right",)) }}

### Argo CD

!!! info "Existing Argo CD"

    To use deployKF with your existing Argo CD installation, please see [this guide](../guides/dependencies/argocd.md#can-i-use-my-existing-argo-cd).

{{ read_csv("./version-matrix--argocd.csv", colalign=("right",)) }}

### Cert-Manager

!!! info "Existing Cert-Manager"

    To use deployKF with your existing Cert-Manager installation, please see [this guide](../guides/dependencies/cert-manager.md#can-i-use-my-existing-cert-manager).

{{ read_csv("./version-matrix--cert-manager.csv", colalign=("right",)) }}

### Istio

!!! info "Existing Istio"

    To use deployKF with your existing Istio installation, please see [this guide](../guides/dependencies/istio.md#can-i-use-my-existing-istio).

{{ read_csv("./version-matrix--istio.csv", colalign=("right",)) }}

### Kyverno

!!! info "Existing Kyverno"

    To use deployKF with your existing Kyverno installation, please see [this guide](../guides/dependencies/kyverno.md#can-i-use-my-existing-kyverno).

{{ read_csv("./version-matrix--kyverno.csv", colalign=("right",)) }}