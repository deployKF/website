---
icon: material/table
---

# Version Matrix

The following tables summarize which tools and versions are supported by each version of __deployKF__.

!!! info "Tool Versions"

    The version wrapped with `()` is the default version included with that version of deployKF.

    Versions that are <s>`struck through`</s> do not work with that version of deployKF.

## deployKF Dependencies

Dependencies of deployKF.

{{ read_csv("./version-matrix--deploykf-dependencies.csv", colalign=("right",)) }}

## deployKF Core

Core components of deployKF like `deploykf-auth` and `deploykf-dashboard`.

{{ read_csv("./version-matrix--deploykf-core.csv", colalign=("right",)) }}

## deployKF Opt

Optional embedded applications that are used when external alternatives are not configured.

{{ read_csv("./version-matrix--deploykf-opt.csv", colalign=("right",)) }}

## deployKF Tools

MLOps tools from the deployKF ecosystem.

!!! tip

    For detailed descriptions about the purpose of each tool, see the [Supported Tools](../reference/tools.md) page.

{{ read_csv("./version-matrix--deploykf-tools.csv", colalign=("right",)) }}

## Kubeflow Dependencies

Dependencies of Kubeflow's MLOps tools.

{{ read_csv("./version-matrix--kubeflow-dependencies.csv", colalign=("right",)) }}

## Kubeflow Tools

MLOps tools from the Kubeflow ecosystem.

!!! tip

    For detailed descriptions about the purpose of each tool, see the [Supported Tools](../reference/tools.md) page.

{{ read_csv("./version-matrix--kubeflow-tools.csv", colalign=("right",)) }}