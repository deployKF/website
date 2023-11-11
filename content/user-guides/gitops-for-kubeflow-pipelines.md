# GitOps for Kubeflow Pipelines Schedules

This guide explains how to __use GitOps to manage Kubeflow Pipelines__, including _pipeline definitions_ and _pipeline schedules_.

---

## Overview

Initially, most users of [Kubeflow Pipelines](../reference/tools.md#kubeflow-pipelines) manually create and run workflows with the UI or Python SDK, as this is the fastest way to get started.
When the number of pipelines grows, it becomes increasingly difficult and error-prone to manage them manually; this is where GitOps comes in.

## Reference Implementation

We provide a reference implementation for managing pipeline definitions and their schedules using GitOps in the `deployKF/kubeflow-pipelines-gitops` GitHub repo.

[:fontawesome-brands-github: Check out the Reference Repository](https://github.com/deployKF/kubeflow-pipelines-gitops){ .md-button .md-button--secondary }

The reference architecture is logically grouped into four steps:

Step | Description
--- | ---
[Step 1: __Render Pipelines__](https://github.com/deployKF/kubeflow-pipelines-gitops#step-1-render-pipelines) | Render pipeline definitions into their static YAML representation.
[Step 2: __Run Pipelines__](https://github.com/deployKF/kubeflow-pipelines-gitops#step-2-run-pipelines) | Run the rendered pipelines ad-hoc.
[Step 3: __Schedule Pipelines__](https://github.com/deployKF/kubeflow-pipelines-gitops#step-3-schedule-pipelines) | Schedule the rendered pipelines.
[Step 4: __Automatic Reconciliation__](https://github.com/deployKF/kubeflow-pipelines-gitops#step-4-automatic-reconciliation) | Automatically reconcile the schedule configs.