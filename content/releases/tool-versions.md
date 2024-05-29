---
icon: material/table
description: >-
  The versions of ML & Data tools included with each version of deployKF.
---

# Tool Version Matrix

The versions of [__ML & Data tools__](../reference/tools.md) included with each version of deployKF.

---

## Kubeflow Ecosystem

This section lists the versions of tools in the [Kubeflow Ecosystem](../reference/tools.md#kubeflow-ecosystem) which are included in each version of deployKF.

### Kubeflow Pipelines

The [Kubeflow Pipelines](../reference/tools.md#kubeflow-pipelines) component versions:

{{ read_csv("./tool-versions--kubeflow-pipelines.csv", colalign=("right",)) }}


!!! warning "Kubeflow Pipelines SDK Versions"

    You MUST use the correct version of the [Kubeflow Pipelines Python SDK](https://pypi.org/project/kfp/), using the wrong version of the SDK will result in errors.
    The following table shows the correct SDK version to use with each version of deployKF:

    deployKF Version | Kubeflow Pipelines | SDK Version
    --- | --- | ---
    `0.1.4` and earlier | v1 | `pip install kfp==1.18.22`
    `0.1.5` and later | v2 | `pip install kfp>=2.0.0,<3`

??? question_secondary "What does the `-deploykf.X` version suffix mean?"

    Due to upstream issues with Kubeflow Pipelines, we maintain a fork in the [`deployKF/kubeflow-pipelines`](https://github.com/deployKF/kubeflow-pipelines) repository.
    From an end-user perspective, the fork is functionally identical to upstream, and works with the official [`kfp`](https://pypi.org/project/kfp/) Python SDK.

??? question_secondary "Can I bring my own version of Argo Workflows?"

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