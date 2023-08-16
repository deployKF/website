# GitOps for Kubeflow Pipelines

This guide explains how to use __GitOps__ to manage Kubeflow Pipelines (pipeline definitions, schedules).

## Overview

We provide a reference implementation for managing Kubeflow Pipelines (pipeline definitions, schedules) using GitOps in the [`deployKF/kubeflow-pipelines-gitops`](https://github.com/deployKF/kubeflow-pipelines-gitops) GitHub repo.

This repository is logically grouped into four steps:

1. __[Render Pipelines](https://github.com/deployKF/kubeflow-pipelines-gitops#step-1-render-pipelines)__: demonstrates how to __render__ pipelines
2. __[Run Pipelines](https://github.com/deployKF/kubeflow-pipelines-gitops#step-2-run-pipelines)__: demonstrates how __run__ the rendered pipelines
3. __[Schedule Pipelines](https://github.com/deployKF/kubeflow-pipelines-gitops#step-3-schedule-pipelines)__: demonstrates how to __schedule__ the rendered pipelines
4. __[Automatic Reconciliation](https://github.com/deployKF/kubeflow-pipelines-gitops#step-4-automatic-reconciliation)__: demonstrates how to __automatically reconcile__ the schedule configs
