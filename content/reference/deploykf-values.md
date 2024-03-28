---
icon: material/cogs
description: >-
  Reference for the generator values (configs) available in deployKF.
---

# Generator Values

The following is a summary of the __generator values__ (configs) available in __deployKF__.

---

!!! question_secondary "What are Generator Values?"

    The generator values configure all aspects of deployKF, including which tools are deployed, how they are configured, and what versions are used.
    
    These values are conceptually similar to Helm Chart values, but they are all "global".
    This means you only need to configure them once, even though they control multiple internal Helm Charts and Kustomize apps.

    For more information, see the [values](../guides/values.md) page.

<div class="use-compact-tables" markdown>

## Argo CD

Values related to [Argo CD](../guides/dependencies/argocd.md#what-is-argo-cd).

{{ render_values_csv_files(values_prefix="argocd") }}

## Kubernetes

Values related to the [Kubernetes cluster](../guides/getting-started.md#kubernetes-cluster).

{{ render_values_csv_files(values_prefix="kubernetes") }}

## deployKF Dependencies

Values for configuring dependencies of deployKF.

{{ render_values_csv_files(values_prefix="deploykf_dependencies.") }}

## deployKF Core

Values for configuring core deployKF components.

{{ render_values_csv_files(values_prefix="deploykf_core.") }}

## deployKF Opt

Values for configuring optional embedded applications, which are used when external alternatives are not configured.

{{ render_values_csv_files(values_prefix="deploykf_opt.") }}

## deployKF Tools

Values for configuring tools from the deployKF ecosystem.

{{ render_values_csv_files(values_prefix="deploykf_tools.") }}

## Kubeflow Dependencies

Values for configuring the __dependencies__ of tools in the [Kubeflow ecosystem](./tools.md#kubeflow-ecosystem).

{{ render_values_csv_files(values_prefix="kubeflow_dependencies.") }}

## Kubeflow Tools

Values for configuring tools from the [Kubeflow ecosystem](./tools.md#kubeflow-ecosystem).

{{ render_values_csv_files(values_prefix="kubeflow_tools.") }}

</div>