---
icon: material/tools
description: >-
  Customize which tools are in your deployKF platform.
  Build a platform that fits your needs by enabling or disabling specific tools.

# TODO: remove status, after a while
status: new
---

# Enable or Disable Tools

Customize which tools are in your deployKF platform.

## Overview

Every [tool which is available](../../reference/tools.md) in deployKF can be enabled or disabled with its corresponding `enabled` value.
This allows you to build a platform that fits your needs by including only the tools you want to use.

The [sample values](../values.md#sample-values) for each release of deployKF will have __all tools enabled__, along with on-cluster versions of any [external dependencies](../external-dependencies.md) required by those tools.
If you are using the sample values as a base for your own configuration and wish to disable a specific tool, see the following sections for instructions.

!!! info

    After updating your values, remember to [sync __all__ applications](../getting-started.md#sync-argocd-applications) to apply the changes to your cluster.
    
    Additionally, because deployKF will never delete namespaces (except [profile namespaces](../platform/deploykf-profiles.md#profile-definitions)), you may want to manually clean up those that are no longer needed to avoid the `deploykf-app-of-apps` always being out-of-sync.

## Kubeflow Tools

deployKF includes a number of tools from the [Kubeflow ecosystem](../../reference/tools.md#kubeflow-ecosystem), which can be enabled or disabled individually.

### Kubeflow Pipelines

??? steps "Disable Kubeflow Pipelines"
    
    The following values will disable [Kubeflow Pipelines](../../reference/tools.md#kubeflow-pipelines) and its dependencies _Argo Workflows_, _MinIO_, and _MySQL_:

    ```yaml
    deploykf_opt:
      deploykf_minio:
        ## NOTE: other tools may still require MinIO to be enabled, unless they
        ##       are also disabled or connected to an external object store
        enabled: false
      
      deploykf_mysql:
        ## NOTE: other tools may still require MySQL to be enabled, unless they
        ##       are also disabled or connected to an external database
        enabled: false
    
    kubeflow_dependencies:
      kubeflow_argo_workflows:
        enabled: false
    
    kubeflow_tools:
      pipelines:
        enabled: false
    ```

### Kubeflow Notebooks

??? steps "Disable Kubeflow Notebooks"

    The following values will disable [Kubeflow Notebooks](../../reference/tools.md#kubeflow-notebooks):

    ```yaml
    kubeflow_tools:
      notebooks:
        enabled: false
    ```

### Kubeflow Katib

??? steps "Disable Kubeflow Katib"

    The following values will disable [Kubeflow Katib](../../reference/tools.md#kubeflow-katib) and its dependency _MySQL_:
    
    ```yaml
    deploykf_opt: 
      deploykf_mysql:
        ## NOTE: other tools may still require MySQL to be enabled, unless they
        ##       are also disabled or connected to an external database
        enabled: false
    
    kubeflow_tools:
      katib:
        enabled: false
    ```

### Kubeflow Training Operator

??? steps "Disable Kubeflow Training Operator"

    The following values will disable the [Kubeflow Training Operator](../../reference/tools.md#kubeflow-training-operator):

    ```yaml
    kubeflow_tools:
      training_operator:
        enabled: false
    ```

### Kubeflow Volumes

??? steps "Disable Kubeflow Volumes"

    The following values will disable [Kubeflow Volumes](../../reference/tools.md#kubeflow-volumes):

    ```yaml
    kubeflow_tools:
      volumes:
        enabled: false
    ```

### Kubeflow TensorBoards

??? steps "Disable Kubeflow TensorBoards"

    The following values will disable [Kubeflow TensorBoards](../../reference/tools.md#kubeflow-tensorboards):

    ```yaml
    kubeflow_tools:
      tensorboards:
        enabled: false
    ```

### Kubeflow PodDefaults Webhook

??? steps "Disable Kubeflow PodDefaults Webhook"

    The following values will disable the [Kubeflow PodDefaults Webhook](kubeflow-poddefaults.md):

    ```yaml
    kubeflow_tools:
      poddefaults_webhook:
        enabled: false
    ```