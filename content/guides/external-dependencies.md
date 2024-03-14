---
icon: material/view-list
description: >-
  Learn about the external dependencies of deployKF and how to configure them.
---

# External Dependencies

Learn about the external dependencies of deployKF and how to configure them.

---

## Overview

deployKF has __"external dependencies"__ which are required to run the platform.
In this case "external" means non-Kubernetes applications or services (e.g. databases, object stores).

!!! tip "External Versions"

    By default, we deploy embedded (on-cluster) versions of the external dependencies so that you can get started quickly.
    However, __we recommend connecting to external versions__ for better performance and reliability.

## External Dependency Guides

The following table lists the external dependencies, and how to use an existing version:

Dependencies | Purpose in deployKF | Use External Version
--- | --- | ---
[MySQL](./external/mysql.md#what-is-mysql) | [Persisting state in __Kubeflow Pipelines__ and __Katib__.](./external/mysql.md#why-does-deploykf-use-mysql) | [Optional](./external/mysql.md#connect-an-external-mysql)<br><small>:material-alert: recommended :material-alert:</small>
[Object Store<br><small>(S3-compatible)</small>](./external/object-store.md#what-is-an-object-store) | [Storing pipelines and their results in __Kubeflow Pipelines__.](./external/object-store.md#why-does-deploykf-use-an-object-store) | [Optional](./external/object-store.md#connect-an-external-object-store)<br><small>:material-alert: recommended :material-alert:</small>
