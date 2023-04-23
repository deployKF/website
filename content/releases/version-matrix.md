# Version Matrix

The following tables are a summary of which dependency versions are supported by each version of __deployKF__.

!!! tip
    The version wrapped with `()` is the default version included with __deployKF__.

## deployKF Dependencies

Dependencies of deployKF.

{{ read_csv("./version-matrix--deploykf-dependencies.csv", colalign=("right",)) }}

## deployKF Core

Applications that are used in core components like `deploykf-auth` and `deploykf-dashboard`.

{{ read_csv("./version-matrix--deploykf-core.csv", colalign=("right",)) }}

## deployKF Opt

Optional embedded applications that are used when external alternatives are not configured.

{{ read_csv("./version-matrix--deploykf-opt.csv", colalign=("right",)) }}

## deployKF Tools

MLOps tools from the deployKF ecosystem.

{{ read_csv("./version-matrix--deploykf-tools.csv", colalign=("right",)) }}

## Kubeflow Dependencies

Dependencies of Kubeflow tools.

{{ read_csv("./version-matrix--kubeflow-dependencies.csv", colalign=("right",)) }}

## Kubeflow Tools

MLOps tools from the Kubeflow ecosystem.

{{ read_csv("./version-matrix--kubeflow-tools.csv", colalign=("right",)) }}