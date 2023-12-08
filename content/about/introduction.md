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

    <strong><span class="deploykf-orange">deploy</span><span class="deploykf-blue">KF</span></strong> helps you build world-class data and machine learning platforms on __any Kubernetes cluster__, in any cloud or environment.

    Our vision is that __anyone with Kubernetes experience__ can effortlessly build and support a _custom data and machine learning platform_ for their organization, without requiring specialized MLOps knowledge.

### __Why use deployKF?__

!!! question_secondary ""

    deployKF combines the <em>ease of a managed service</em> with the flexibility of a self-hosted solution. 
    Create a platform that is tailored to your organization's needs, while not also requiring a team of MLOps experts to build and maintain it.

    The key features of deployKF are:

    - Runs on __any Kubernetes__, including on-premises and in the cloud
    - Deploy leading Data and ML tools like [__Kubeflow__](../reference/tools.md#kubeflow-ecosystem), [__Airflow__](../reference/future-tools.md#apache-airflow)<sup>†</sup>, and [__MLflow__](../reference/future-tools.md#mlflow-model-registry)<sup>†</sup>
    - Intuitive [__centralized configs__](../reference/deploykf-values.md) to manage all aspects of the platform
    - Seamless __in-place upgrades__ and config rollouts
    - Connect with __existing services__ like Istio and cert-manager, [S3](../guides/tools/external-object-store.md), and [MySQL](../guides/tools/external-mysql.md).
    - Native support for __GitOps__ via ArgoCD

    <small><sup>†</sup>Coming soon, see our [current](../reference/tools.md) and [future](../reference/future-tools.md) tools.</small>

### __Video Introduction__

!!! abstract ""

    <div class="video-padding">
        <div class="youtube-video-container">
            <iframe src="https://www.youtube.com/embed/GDX4eLL_8E0?rel=0" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
        </div>
    </div>
    <div class="video-caption">
        Our presentation from [Kubeflow Summit 2023](https://www.kubeflow.org/events/kubeflow-summit-2023/), where we introduced deployKF to the community.
    </div>

### __Featured Stories__

!!! info ""

    We are always excited to see __how and where__ deployKF is being used!

    Here are some stories of deployKF being used in the wild:

    Organization | Article / Video
    --- | ---
    Cloudflare | [_ML Ops Platform at Cloudflare_](https://blog.cloudflare.com/mlops/)

    <small>
      <em>Have a story to share? [Let us know](community.md#contact-us)!</em>
      <br>
      <em>Also, you can add your organization to the [Adopters List](https://github.com/deployKF/deployKF/blob/main/ADOPTERS.md).</em>
    </small>

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

### Support the Project

!!! warning ""

    deployKF is a new and growing project.
    If you like what we are doing, please help others discover us by __sharing the project__ with your colleagues and/or the wider community.

    We greatly appreciate [__GitHub Stars__ :star: on the `deployKF/deployKF`](https://github.com/deployKF/deployKF) repository:

    ![deployKF GitHub Star History (Dark Mode)](https://api.star-history.com/svg?repos=deployKF/deployKF&type=Date&theme=dark#only-dark){ .star-history_image }
    ![deployKF GitHub Star History (Light Mode)](https://api.star-history.com/svg?repos=deployKF/deployKF&type=Date#only-light){ .star-history_image }

---

## Other Resources

### Common Questions

??? question_secondary "How are Kubeflow and deployKF related?"

    Kubeflow and deployKF are two different but related projects.

    You may wish to review our detailed [:custom-deploykf-color: __deployKF__ vs :custom-kubeflow-color: __Kubeflow Manifests__](../about/kubeflow-vs-deploykf.md#deploykf-vs-kubeflow-manifests) comparison.
    Note, most other [distributions of Kubeflow](https://www.kubeflow.org/docs/started/installing-kubeflow/#packaged-distributions-of-kubeflow) use __largely unmodified__ versions of the Kubeflow Manifests. 
    So the comparison is also relevant to them.

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

    <div class="image-wrapper">
    ![deployKF Dashboard (Dark Mode)](../assets/images/deploykf-dashboard-DARK.png#only-dark)
    ![deployKF Dashboard (Light Mode)](../assets/images/deploykf-dashboard-LIGHT.png#only-light)
    </div>
    <div class="image-caption">
    The [__deployKF Dashboard__](https://github.com/deployKF/dashboard) is the web-based interface that end-users interact with the platform through.
    </div>

### Media and Presentations

??? youtube "Intro / Demo - Kubeflow Community Call - July 2023"

    <div class="video-padding">
        <div class="youtube-video-container">
            <iframe src="https://www.youtube.com/embed/VggtaOgtBJo?rel=0" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
        </div>
    </div>
    <div class="video-caption">
        A recording of the __Kubeflow Community Call__ from July 2023, where we first introduced deployKF to the community.
    </div>
