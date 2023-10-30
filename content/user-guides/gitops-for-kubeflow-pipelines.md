# GitOps for Kubeflow Pipelines

This guide explains how to __use GitOps to manage Kubeflow Pipelines__, including _pipeline definitions_ and _pipeline schedules_.

---

## Overview

Initially, most users of [Kubeflow Pipelines](../reference/tools.md#kubeflow-pipelines) manually create and run workflows with the UI or Python SDK, as this is the fastest way to get started.

As the number of pipelines and schedules grow, it becomes increasingly difficult and error-prone to manage them manually; this is where GitOps comes in.

We provide a reference implementation for managing pipeline definitions and their schedules using GitOps in the [`deployKF/kubeflow-pipelines-gitops`](https://github.com/deployKF/kubeflow-pipelines-gitops) GitHub repo.

The reference architecture is logically grouped into four steps:

1. __[Render Pipelines](https://github.com/deployKF/kubeflow-pipelines-gitops#step-1-render-pipelines)__: demonstrates how to __render__ pipelines
2. __[Run Pipelines](https://github.com/deployKF/kubeflow-pipelines-gitops#step-2-run-pipelines)__: demonstrates how to __run__ the rendered pipelines
3. __[Schedule Pipelines](https://github.com/deployKF/kubeflow-pipelines-gitops#step-3-schedule-pipelines)__: demonstrates how to __schedule__ the rendered pipelines
4. __[Automatic Reconciliation](https://github.com/deployKF/kubeflow-pipelines-gitops#step-4-automatic-reconciliation)__: demonstrates how to __automatically reconcile__ the schedule configs
