# Generator Values (Configs)

The following is a summary of the generator __values__ (configs) available in __deployKF__.

!!! info

    The full list of values and their defaults can also be found in the [`generator/default_values.yaml`](https://github.com/deployKF/deployKF/blob/v{{ latest_deploykf_version }}/generator/default_values.yaml) file.

!!! tip

    The generator values are how you configure all aspects of deployKF.
    While there are many values available, you only need to specify the ones you want to change from their defaults.

    For more information about creating your custom values files, see the [getting started](../guides/getting-started.md#3-values-configuration) guide.

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