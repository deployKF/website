---
icon: material/lightbulb-on
description: >-
  An introduction to deployKF.
  Learn how deployKF helps you build and support a custom data and machine learning platform on Kubernetes.

# TODO: remove status, after a while
status: new
---

# Introduction

An __introduction__ to deployKF.

---

## About deployKF

### __What is deployKF?__

!!! question_secondary ""

    deployKF helps you build world-class data and machine learning platforms on __any Kubernetes cluster__, in any cloud or environment.
    Our vision is that __anyone with Kubernetes experience__ can effortlessly build and support a _custom data and machine learning platform_ for their organization, without requiring specialized MLOps knowledge.

### __Why use deployKF?__

!!! question_secondary ""

    By combining the <em>ease of a managed service</em> with the flexibility of a self-hosted solution; 
    deployKF creates a platform tailored to your organization's needs, while not also requiring a team of MLOps experts to build and maintain it.

    Some of the key features include:

    - Runs on __any Kubernetes__, including on-premises and in the cloud
    - Support for leading __Data and MLOps tools__ including [__Kubeflow__](../reference/tools.md#kubeflow-ecosystem), [__Airflow__](../reference/future-tools.md#apache-airflow)<sup>†</sup>, and [__MLflow__](../reference/future-tools.md#mlflow-model-registry)<sup>†</sup>
    - Intuitive [__centralized configs__](../reference/deploykf-values.md) to manage all aspects of the platform
    - Seamless __in-place upgrades__ and config rollouts
    - Connect with __existing services__ like Istio and cert-manager, [S3](../guides/tools/external-object-store.md), and [MySQL](../guides/tools/external-mysql.md).
    - Native support for __GitOps__ via ArgoCD

    <small><sup>†</sup>Coming soon, see our [current](../reference/tools.md) and [future](../reference/future-tools.md) tools.</small>

---

## Using deployKF

### Getting Started

!!! question_secondary ""

    To help you get started with deployKF, we have prepared a number of guides:

    - [__Getting Started__ :star:](../guides/getting-started.md) - learn how to run deployKF anywhere
    - [__Local Quickstart__](../guides/local-quickstart.md) - try deployKF on your local machine
    - [__Migrate from Kubeflow Distributions__](../guides/kubeflow-distributions.md) - how and why to migrate from other Kubeflow distributions

### Commercial Support

!!! support ""

    If you need commercial support for deployKF, please contact [__Aranui Solutions__](https://www.aranui.solutions/).
    Aranui Solutions is a US-based company founded by the creators of deployKF to help organizations build ML & Data Platforms on Kubernetes.
    
    [Visit: _Aranui Solutions Website_](https://www.aranui.solutions/){ .md-button .md-button--secondary }
    [Email: _`sales@aranui.solutions`_](mailto:sales@aranui.solutions?subject=%5BdeployKF%5D%20MY_SUBJECT){ .md-button .md-button--secondary }

---

## Other Resources

### Common Questions

??? question_secondary "Who maintains deployKF?"

    deployKF was originally created and is maintained by [Mathew Wicks](https://www.linkedin.com/in/mathewwicks/) (GitHub: [@thesuperzapper](https://github.com/thesuperzapper)), a Kubeflow lead and maintainer of the popular [Apache Airflow Helm Chart](https://github.com/airflow-helm/charts).
    deployKF is a community-led project that welcomes contributions from anyone who wants to help.

??? question_secondary "Do you have a Slack or Mailing List?"

    __Slack:__

    - The deployKF community uses the __Kubeflow Slack__ for informal discussions among users and contributors.
    - Find us on the [`#deploykf`](https://kubeflow.slack.com/archives/C054H6WLNCB) channel!

    [:fontawesome-brands-slack: Join the Kubeflow Slack](https://invite.playplay.io/invite?team_id=T7QLHSH6U){ .md-button .md-button--secondary }

    ---

    __Mailing Lists:__

    - [__deploykf-users__](https://groups.google.com/g/deploykf-users) is for deployKF users to ask questions and share ideas.
    - [__deploykf-dev__](https://groups.google.com/g/deploykf-dev) is for deployKF contributors to discuss development and design.
    
    [:fontawesome-solid-envelope: Join: _User Mailing List_](https://groups.google.com/g/deploykf-users){ .md-button .md-button--secondary }
    [:fontawesome-solid-envelope: Join: _Contributor Mailing List_](https://groups.google.com/g/deploykf-dev){ .md-button .md-button--secondary }

### Screenshots

??? image "deployKF Dashboard"

    The [__deployKF Dashboard__](https://github.com/deployKF/dashboard) is the web-based interface for deployKF, and is the primary way that users interact with the platform.

    ![deployKF Dashboard (Dark Mode)](../assets/images/deploykf-dashboard-DARK.png#only-dark)
    ![deployKF Dashboard (Light Mode)](../assets/images/deploykf-dashboard-LIGHT.png#only-light)

### Media and Presentations

??? youtube "Intro / Demo - Kubeflow Community Call - July 2023"

    This is a recording of the Kubeflow Community Call from July 2021, where we first introduced deployKF to the community.

    <iframe width="560" height="315" src="https://www.youtube.com/embed/VggtaOgtBJo" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>