---
icon: custom/kubeflow
description: >-
  Learn how to use Kubeflow PodDefaults to mutate Pods as they are created.
  Make changes like adding sidecars, volumes, environment variables, and more.

# TODO: remove status, after a while
status: new
---

# Use Kubeflow PodDefaults

Learn how to use __Kubeflow PodDefaults__ to mutate Pods as they are created.
Make changes like adding sidecars, volumes, environment variables, and more.

---

## Overview

Kubeflow PodDefaults allow you to change (mutate) the definition of Pods as they are created.
The central config is the `PodDefault` CRD that defines how to select Pods, and what changes to make.

Some common use cases for PodDefaults include:

- Adding extra [`sidecars`](https://kubernetes.io/docs/concepts/workloads/pods/sidecar-containers/) or [`init-containers`](https://kubernetes.io/docs/concepts/workloads/pods/init-containers/) to Pods.
- Setting [`imagePullSecrets`](https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/) of Pods.
- Mounting extra volumes to Pods.
- Adding extra environment variables to Pods.

!!! info "Similarity to Kyverno"

    [:custom-kyverno-color: __Kyverno__](https://github.com/kyverno/kyverno) is a general-purpose policy engine for Kubernetes which also allows [mutating resources](https://kyverno.io/docs/writing-policies/mutate/) as they are created.
    However, Kyverno is more general-purpose and can be used to mutate any resource, not just Pods, and includes the ability to [mutate existing resources](https://kyverno.io/docs/writing-policies/mutate/#mutate-existing-resources).

    Because deployKF [depends on Kyverno](../dependencies/kyverno.md#how-does-deploykf-use-kyverno), you will have access to both tools.

## Create a PodDefault

To use PodDefaults, you need to create a `PodDefault` resource in the namespace where you want to mutate Pods.

!!! warning
   
    PodDefaults only affect Pods __as they are created__, and only __in the namespace__ where the CRD is defined, existing Pods which match the selector are __NOT__ affected.

!!! info

    To learn  more about all the options in the `PodDefault` CRD, review the `admission-webhook` code from the `kubeflow/kubeflow` repository under the [`admission-webhook/pkg/apis/settings/v1alpha1/poddefault_types.go`](https://github.com/kubeflow/kubeflow/blob/v1.7.0/components/admission-webhook/pkg/apis/settings/v1alpha1/poddefault_types.go#L27-L89) file.

Here is the full spec of a `PodDefault` resource, with all the possible options set:

```yaml
apiVersion: kubeflow.org/v1alpha1
kind: PodDefault
metadata:
  name: kubeflow-pipelines-api-token
  namespace: MY_NAMESPACE
spec:
  ## a human-readable description of what this PodDefault does
  ##
  desc: "..."

  ## a selector to match Pods
  ##  - spec for LabelSelector:
  ##    https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.27/#labelselector-v1-meta
  ##
  selector:

    ## match Pods with these labels
    ##
    matchLabels:
      my-label: "my-value"

    ## match Pods with these expressions
    ##  - WARNING: Kubeflow Notebooks has issues with `matchExpressions`
    ##             https://github.com/kubeflow/kubeflow/issues/7552
    ##
    #matchExpressions:
    #  - key: kubeflow-pipelines-api-token
    #    operator: In
    #    values:
    #      - "true"

  ## extra annotations for the Pod metadata
  ##
  annotations: {}

  ## extra labels for the Pod metadata
  ##
  labels: {}

  ## extra `initContainers` for the PodSpec
  ##  - spec for Container:
  ##    https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.27/#container-v1-core
  ##
  initContainers: []

  ## extra `containers` for the PodSpec
  ##  - spec for Container:
  ##    https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.27/#container-v1-core
  ##
  sidecars: []
  
  ## extra `imagePullSecrets` for the PodSpec
  ##  - spec for LocalObjectReference:
  ##    https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.27/#localobjectreference-v1-core
  ##
  imagePullSecrets: []

  ## override the `serviceAccountName` of the PodSpec
  ##
  serviceAccountName: ""

  ## override the `automountServiceAccountToken` of the PodSpec
  ##
  automountServiceAccountToken: true

  ## extra `env` for the containers in the PodSpec
  ##  - spec for EnvVar:
  ##    https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.27/#envvar-v1-core
  ##
  env: []

  ## extra `envFrom` for the containers in the PodSpec
  ##  - spec for EnvFromSource:
  ##    https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.27/#envfromsource-v1-core
  ##
  envFrom: []

  ## extra `volumes` for the PodSpec
  ##  - spec for Volume:
  ##    https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.27/#volume-v1-core
  ##
  volumes: []

  ## extra `volumeMounts` for the containers in the PodSpec
  ##  - spec for VolumeMount:
  ##    https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.27/#volumemount-v1-core
  ##
  volumeMounts: []

  ## extra `tolerations` for the PodSpec
  ##
  tolerations: []

  ## set the `command` of containers in the PodSpec
  ##  - note, this will NOT affect containers that already have `command` set
  ##
  command: []

  ## set the `args` of containers in the PodSpec
  ##  - note, this will NOT affect containers that already have `args` set
  ##
  args: []
```

## Examples

While the full spec for a `PodDefault` is quite complex, here are some examples of common changes you might want to make.

### Add a Sidecar

When this `PodDefault` is applied to a cluster, Pods in the `MY_NAMESPACE` namespace with the label `add-sidecar: "true"` will have a sidecar container added to them.

```yaml
apiVersion: kubeflow.org/v1alpha1
kind: PodDefault
metadata:
  name: add-sidecar
  namespace: MY_NAMESPACE
spec:
  desc: "Add a sidecar to the Pod"

  selector:
    matchLabels:
      add-sidecar: "true"

  sidecars:
    - name: my-sidecar
      image: ubuntu:22.04
      imagePullPolicy: IfNotPresent
      command:
        - "/bin/sh"
        - "-c"
      args:
        - |
          ## to break the infinite loop when we receive SIGTERM
          trap "exit 0" TERM;

          ## keep the container running (so people can `kubectl exec -it` into it)
          while true; do
            echo "I am alive...";
            sleep 30;
          done
```

### Kubeflow Pipelines API Token

When this `PodDefault` is applied to a cluster, Pods in the `MY_NAMESPACE` namespace with the label `kubeflow-pipelines-api-token: "true"` will have a service account token mounted at `/var/run/secrets/ml-pipeline/token` which allows [authentication with the Kubeflow Pipelines API](../../user-guides/access-kubeflow-pipelines-api.md#kubernetes-serviceaccount-token).

!!! info

    This example is actually the `PodDefault` which deployKF creates in each profile namespace when the [`kubeflow_tools.pipelines.profileResourceGeneration.kfpApiTokenPodDefault`](https://github.com/deployKF/deployKF/blob/v0.1.5/generator/default_values.yaml#L1982-L1990) value is enabled.

```yaml
apiVersion: kubeflow.org/v1alpha1
kind: PodDefault
metadata:
  name: kubeflow-pipelines-api-token
  namespace: MY_NAMESPACE
spec:
  desc: "Mount a serviceAccountToken to authenticate with Kubeflow Pipelines API"

  selector:
    matchLabels:
      kubeflow-pipelines-api-token: "true"

  ## set the `KF_PIPELINES_SA_TOKEN_PATH` environment variable
  env:
    - name: KF_PIPELINES_SA_TOKEN_PATH
      value: "/var/run/secrets/ml-pipeline/token"

  ## mount the serviceAccountToken at `/var/run/secrets/ml-pipeline/token`
  volumeMounts:
    - mountPath: "/var/run/secrets/ml-pipeline"
      name: volume-ml-pipeline-token
      readOnly: true

  ## define a projected volume to mount the serviceAccountToken
  volumes:
    - name: volume-ml-pipeline-token
      projected:
        sources:
          - serviceAccountToken:
              audience: pipelines.kubeflow.org
              expirationSeconds: 7200
              path: token
```