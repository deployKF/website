---
icon: material/tune
---

# Generator Values

The following is a summary of the __generator values__ (configs) available in __deployKF__.

!!! question_secondary "What are Generator Values?"

    The generator values are how you configure all aspects of deployKF, including which tools are deployed, how they are configured, and what versions are used.
    
    For more information, see the [getting started](../guides/getting-started.md) guide to learn how to configure the values to suit your needs.

---

## Argo CD

Values for configuring Argo CD.

{{ render_values_csv_files(values_prefix="argocd") }}

## deployKF Dependencies

Values for configuring the dependencies of deployKF.

{{ render_values_csv_files(values_prefix="deploykf_dependencies.") }}

## deployKF Core

Values for configuring core deployKF components.

{{ render_values_csv_files(values_prefix="deploykf_core.") }}

## deployKF Opt

Values for configuring optional embedded applications that are used when external alternatives are not configured.

{{ render_values_csv_files(values_prefix="deploykf_opt.") }}

## deployKF Tools

Values for configuring MLOps tools from the deployKF ecosystem.

{{ render_values_csv_files(values_prefix="deploykf_tools.") }}

## Kubeflow Dependencies

Values for configuring dependencies of Kubeflow's MLOps tools.

{{ render_values_csv_files(values_prefix="kubeflow_dependencies.") }}

## Kubeflow Tools

Values for configuring MLOps tools from the Kubeflow ecosystem.

{{ render_values_csv_files(values_prefix="kubeflow_tools.") }}