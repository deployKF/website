# deployKF Values (Configs)

The following is a summary of the __values (configs)__ available in __deployKF__.

!!! tip
    The full list of __values__ and their defaults can be found in the [`default_values.yaml` file in the source code](https://github.com/deployKF/deployKF/blob/main/generator/default_values.yaml).

## Argo CD

Values for configuring ArgoCD.

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

Values for configuring dependencies of Kubeflow tools.

{{ render_values_csv_files(values_prefix="kubeflow_dependencies.") }}

## Kubeflow Tools

Values for configuring MLOps tools from the Kubeflow ecosystem.

{{ render_values_csv_files(values_prefix="kubeflow_tools.") }}