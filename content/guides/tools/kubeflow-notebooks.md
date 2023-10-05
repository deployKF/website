# Configure Kubeflow Notebooks

This guide explains how to __configure Kubeflow Notebooks__ in deployKF.

---

## Overview

Kubeflow Notebooks allows users to spawn Pods running instances of [JupyterLab](https://jupyter.org/), [Visual Studio Code (code-server)](https://github.com/coder/code-server), and [RStudio](https://github.com/rstudio/rstudio) in profile namespaces.

As the cluster administrator, you may configure which options are available to users when spawning a Notebook Pod:

- Container Images
- Container Resources (CPU, Memory, GPU)
- Storage Volumes
- Advanced Pod Options (Affinity, Tolerations, PodDefaults)
- Idle Notebook Culling

!!! warning "Kubeflow Notebooks Limitations"

    The current version of Kubeflow Notebooks exposes many Kubernetes-specific concepts to users, which may be confusing for non-technical users.
    There is an upstream proposal to abstract away these concepts in a more user-friendly way, see [`kubeflow/kubeflow#7156`](https://github.com/kubeflow/kubeflow/issues/7156) for more information.

    ---

    When the `kubeflow_tools.notebooks.spawnerFormDefaults` values are updated, this has no effect on existing Notebook Pods, only new Pods will use the updated values.

## Container Images

Container images are the "environment" which users will be working in when using a Notebook Pod, and can be configured to provide different tools and packages to users.

The following values configure which container images are available to users when spawning a Notebook Pod:

- __Jupyter-Like__: [`kubeflow_tools.notebooks.spawnerFormDefaults.image`](https://github.com/deployKF/deployKF/blob/v0.1.1/generator/default_values.yaml#L1306-L1320)
- __VSCode-like__: [`kubeflow_tools.notebooks.spawnerFormDefaults.imageGroupOne`](https://github.com/deployKF/deployKF/blob/v0.1.1/generator/default_values.yaml#L1322-L1336)
- __RStudio-like__: [`kubeflow_tools.notebooks.spawnerFormDefaults.imageGroupTwo`](https://github.com/deployKF/deployKF/blob/v0.1.1/generator/default_values.yaml#L1338-L1354)

## Container Resources

Container resources directly correspond to Kubernetes [Container Resources](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/) which are requested by the Notebook Pod.

The following values configure the resource requests/limits for containers in Notebook Pods:

- __CPU__: [`kubeflow_tools.notebooks.spawnerFormDefaults.cpu`](https://github.com/deployKF/deployKF/blob/v0.1.1/generator/default_values.yaml#L1356-L1366)
- __Memory__: [`kubeflow_tools.notebooks.spawnerFormDefaults.memory`](https://github.com/deployKF/deployKF/blob/v0.1.1/generator/default_values.yaml#L1368-L1378)
- __GPU__: [`kubeflow_tools.notebooks.spawnerFormDefaults.gpu`](https://github.com/deployKF/deployKF/blob/v0.1.1/generator/default_values.yaml#L1380-L1404)

!!! warning "Resource Requests"

    Kubernetes uses __resource requests__ when scheduling Pods, and does not strictly enforce them at runtime.
    User Notebooks are not well-behaved applications (from a resource perspective), so will likely impact other Pods running on the same node.

    However, setting __resource limits__ will have unintended consequences for users, as the Notebook Pod will be terminated if it exceeds certain limits (like memory), which may result in lost work.

    A common alternative is to use a dedicated node for each Notebook Pod, see [Advanced Pod Options](#advanced-pod-options) for information on how to do this with Affinity and Tolerations.

## Storage Volumes

Storage volumes are used to provide persistent storage to Notebook Pods between restarts, and are implemented using Kubernetes [Persistent Volumes](https://kubernetes.io/docs/concepts/storage/persistent-volumes/).

The following values configure the storage volumes for Notebook Pods:

- __Home Volume__: [`kubeflow_tools.notebooks.spawnerFormDefaults.workspaceVolume`](https://github.com/deployKF/deployKF/blob/v0.1.1/generator/default_values.yaml#L1406-L1428)
- __Data Volume__: [`kubeflow_tools.notebooks.spawnerFormDefaults.dataVolumes`](https://github.com/deployKF/deployKF/blob/v0.1.1/generator/default_values.yaml#L1430-L1451)

!!! warning "StorageClass and Performance"

    The [`kubeflow_tools.notebooks.spawnerFormDefaults.workspaceVolume.value.newPvc.spec.storageClassName`](https://github.com/deployKF/deployKF/blob/v0.1.1/generator/default_values.yaml#L1423) value defines which [Kubernetes StorageClass](https://kubernetes.io/docs/concepts/storage/storage-classes/) is used to provision the workspace volume.
    If a `storageClassName` is not specified, the cluster's default StorageClass is used.
    
    As ML workloads are often IO-intensive, it is recommended to use a StorageClass which provides high-performance, typically this is only possible with drives which are attached to the node, rather than network-attached storage.

## Advanced Pod Options

Advanced Pod Options are additional configurations for Notebook Pods which manage things like [Pod Affinity](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/#affinity-and-anti-affinity), [Node Tolerations](https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/), and Kubeflow's [PodDefaults](https://github.com/kubeflow/kubeflow/tree/master/components/admission-webhook).

The following values configure the advanced options for Notebook Pods:

- __Pod Affinity__: [`kubeflow_tools.notebooks.spawnerFormDefaults.affinityConfig`](https://github.com/deployKF/deployKF/blob/v0.1.1/generator/default_values.yaml#L1453-L1488)
- __Node Tolerations__: [`kubeflow_tools.notebooks.spawnerFormDefaults.tolerationGroup`](https://github.com/deployKF/deployKF/blob/v0.1.1/generator/default_values.yaml#L1490-L1530)
- __PodDefaults__: [`kubeflow_tools.notebooks.spawnerFormDefaults.configurations`](https://github.com/deployKF/deployKF/blob/v0.1.1/generator/default_values.yaml#L1540-L1549)

??? config "Dedicated Node for each Notebook Pod"

    Because Notebook Pods are not well-behaved applications (from a resource perspective), it is common to want a dedicated node for each Notebook Pod.
    With a combination of Pod Affinity and Node Tolerations, this can be achieved.

    Note, this will require your cluster to have node-autoscaling configured (e.g. [Cluster Autoscaler](https://github.com/kubernetes/autoscaler/tree/master/cluster-autoscaler) or [Karpenter](https://karpenter.sh/)), as the cluster will need to provision a new node for each Notebook Pod.

    ---

    First, you will need to make one or more groups of nodes that are tainted to prevent other Pods from being scheduled on them.
    In the following example, we have four groups of nodes with different CPU/Memory configurations, that are each tainted with a different value of the `dedicated` key with effect `NoSchedule`:

    - Key: `dedicated`, Value: `kubeflow-c5.xlarge`, Effect: `NoSchedule`
    - Key: `dedicated`, Value: `kubeflow-c5.2xlarge`, Effect: `NoSchedule`
    - Key: `dedicated`, Value: `kubeflow-c5.4xlarge`, Effect: `NoSchedule`
    - Key: `dedicated`, Value: `kubeflow-r5.8xlarge`, Effect: `NoSchedule` 

    Next, you will need to configure Pod Affinity configs that do not allow two Notebook Pods to be scheduled on the same node.
    In the following example, we do this by:

    - Using [`nodeAffinity`](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/#node-affinity) to require a Node with label `lifecycle=kubeflow-notebook`
    - Using [`podAntiAffinity`](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/#types-of-inter-pod-affinity-and-anti-affinity) to require a Node WITHOUT an existing Pod having `notebook-name` label


    Finally, you may use the following values to expose these options to users:

    ```yaml
    kubeflow_tools:
      notebooks:
        spawnerFormDefaults:
          ## Affinity
          ##  - note, setting `readOnly` to `true` to ensures that this affinity is always applied
          ##  - note, `namespaceSelector` was added in Kubernetes 1.22, 
          ##    so this will NOT work on older clusters
          ##
          affinityConfig:
            readOnly: true
            value: "dedicated_node_per_notebook"
            options:
              - configKey: "dedicated_node_per_notebook"
                displayName: "Dedicated Node Per Notebook"
                affinity:
                  ## Require a Node with label `lifecycle=kubeflow-notebook`
                  nodeAffinity:
                    requiredDuringSchedulingIgnoredDuringExecution:
                      nodeSelectorTerms:
                        - matchExpressions:
                            - key: "lifecycle"
                              operator: "In"
                              values:
                                - "kubeflow-notebook"

                  ## Require a Node WITHOUT an existing Pod having `notebook-name` label
                  podAntiAffinity:
                    requiredDuringSchedulingIgnoredDuringExecution:
                      - labelSelector:
                          matchExpressions:
                            - key: "notebook-name"
                              operator: "Exists"
                        topologyKey: "kubernetes.io/hostname"
                        namespaceSelector: {}

          ## Tolerations
          ##
          tolerationGroup:
            readOnly: false
            value: "group_1"
            options:
              - groupKey: "group_1"
                displayName: "4 CPU 8Gb Mem at ~$X.XXX USD per day"
                tolerations:
                  - key: "dedicated"
                    operator: "Equal"
                    value: "kubeflow-c5.xlarge"
                    effect: "NoSchedule"

              - groupKey: "group_2"
                displayName: "8 CPU 16Gb Mem at ~$X.XXX USD per day"
                tolerations:
                  - key: "dedicated"
                    operator: "Equal"
                    value: "kubeflow-c5.2xlarge"
                    effect: "NoSchedule"

              - groupKey: "group_3"
                displayName: "16 CPU 32Gb Mem at ~$X.XXX USD per day"
                tolerations:
                  - key: "dedicated"
                    operator: "Equal"
                    value: "kubeflow-c5.4xlarge"
                    effect: "NoSchedule"

              - groupKey: "group_4"
                displayName: "32 CPU 256Gb Mem at ~$X.XXX USD per day"
                tolerations:
                  - key: "dedicated"
                    operator: "Equal"
                    value: "kubeflow-r5.8xlarge"
                    effect: "NoSchedule"
    ```

    Users will then be able to select which group of nodes they want to use by choosing the corresponding "Toleration" group when spawning their Notebook.


??? config "PodDefault for Kubeflow Pipelines Authentication"

    The [`kubeflow_tools.pipelines.profileResourceGeneration.kfpApiTokenPodDefault`](https://github.com/deployKF/deployKF/blob/v0.1.1/generator/default_values.yaml#L1803-L1811) value 
    configures if a `PodDefault` named `"kubeflow-pipelines-api-token"` is automatically generated in each profile namespace.

    If the user selects this "configuration" when spawning their Notebook, they will be able to use the __Kubeflow Pipelines Python SDK__ from the Notebook without needing to manually authenticate.

    To have this "configuration" selected by default in the spawner, you may use the following values:

    ```yaml
    kubeflow_tools:
      notebooks:
        spawnerFormDefaults:
          configurations:
            value:
              - "kubeflow-pipelines-api-token"
    ```

    For more information, see the [Access Kubeflow Pipelines API](../../user-guides/access-kubeflow-pipelines-api.md) user guide.

## Idle Notebook Culling

Kubeflow Notebooks supports automatically culling idle Notebook Pods, which is configured by the [`kubeflow_tools.notebooks.notebookCulling`](https://github.com/deployKF/deployKF/blob/v0.1.1/generator/default_values.yaml#L1577-L1588) values.

For example, the following values will enable idle culling after 1 day of inactivity:

```yaml
kubeflow_tools:
  notebooks:
    notebookCulling:
      enabled: true
      idleTime: 1440 # 1 day in minutes
```

!!! warning "Jupyter Notebooks Only"

    Currently, only Jupyter Notebooks are supported for idle culling, see the upstream [design proposal](https://github.com/kubeflow/kubeflow/blob/master/components/proposals/20220121-jupyter-notebook-idleness.md) for more information.
