---
icon: material/table
description: >-
  The versions of ML & Data tools included with each version of deployKF.
---

# Tool Versions

The versions of __ML & Data tools__ included with each version of deployKF.

---

## Kubeflow Ecosystem

This section lists which versions of tools from the [Kubeflow Ecosystem](../reference/tools.md#kubeflow-ecosystem) are included with each version of deployKF.

### Kubeflow Pipelines

The [Kubeflow Pipelines](../reference/tools.md#kubeflow-pipelines) component versions:

{{ read_csv("./tool-versions--kubeflow-pipelines.csv", colalign=("right",)) }}

!!! info "Kubeflow Pipelines Fork"

    Due to upstream issues with Kubeflow Pipelines, we maintain a fork in the [`deployKF/kubeflow-pipelines`](https://github.com/deployKF/kubeflow-pipelines) repository.
    From an end-user perspective, the fork is functionally identical to upstream, and works with the official [`kfp`](https://pypi.org/project/kfp/) Python SDK.

!!! warning "`2.0.0-alpha.7` is NOT KFP v2"

    Confusingly, the `2.0.0-alpha.7` version is actually part of the KFP v1 line, so you must use `1.X.X` SDK versions with it, for example: [`kfp==1.8.22`](https://pypi.org/project/kfp/1.8.22/).

!!! warning "Argo Workflows"

    By default, deployKF will install the correct version of Argo Workflows for the version of Kubeflow Pipelines you are using.
    Right now, its a little complex to bring your own Argo Workflows version. 

    See [`deployKF/deployKF#116`](https://github.com/deployKF/deployKF/issues/116) to join the discussion.

### Kubeflow Notebooks

The [Kubeflow Notebooks](../reference/tools.md#kubeflow-notebooks) component versions:

{{ read_csv("./tool-versions--kubeflow-notebooks.csv", colalign=("right",)) }}

### Kubeflow Katib

The [Kubeflow Katib](../reference/tools.md#kubeflow-katib) component versions:

{{ read_csv("./tool-versions--kubeflow-katib.csv", colalign=("right",)) }}

### Kubeflow Training Operator

The [Kubeflow Training Operator](../reference/tools.md#kubeflow-training-operator) component versions:

{{ read_csv("./tool-versions--kubeflow-training-operator.csv", colalign=("right",)) }}

### Kubeflow Volumes

The [Kubeflow Volumes](../reference/tools.md#kubeflow-volumes) component versions:

{{ read_csv("./tool-versions--kubeflow-volumes.csv", colalign=("right",)) }}

### Kubeflow TensorBoards

The [Kubeflow TensorBoards](../reference/tools.md#kubeflow-tensorboards) component versions:

{{ read_csv("./tool-versions--kubeflow-tensorboards.csv", colalign=("right",)) }}