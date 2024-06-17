---
icon: material/lightbulb-on
description: >-
  An introduction to deployKF.
  Learn how deployKF combines the best of Kubeflow, Airflow, and MLflow.
---

# Introduction

An __introduction__ to deployKF.

---

## About deployKF

!!! question_secondary ""

    <strong><span class="deploykf-orange">deploy</span><span class="deploykf-blue">KF</span></strong> builds machine learning platforms on __Kubernetes__.
    We combine the best of 
    [:custom-kubeflow-color: __Kubeflow__](../reference/tools.md#kubeflow-ecosystem), 
    [:custom-airflow-color: __Airflow__](../reference/future-tools.md#apache-airflow)<sup>†</sup>, and 
    [:custom-mlflow-color: __MLflow__](../reference/future-tools.md#mlflow-model-registry)<sup>†</sup>
    into a complete platform that is easy to deploy and maintain.

    <small><sup>†</sup>Coming soon, see our [current](../reference/tools.md) and [future](../reference/future-tools.md) tools.</small>

### __Why use deployKF?__

!!! question_secondary ""

    deployKF combines the _ease of a managed service_ with the flexibility of a self-hosted solution. 

    Our goal is that __any Kubernetes user__ can build a machine learning platform for their organization, 
    without needing specialized MLOps knowledge, or a team of experts to maintain it.

    The key features of deployKF are:

    - Run on [__any Kubernetes cluster__](../guides/getting-started.md#kubernetes-cluster), including on-premises and in the cloud
    - Intuitive [__centralized configs__](../guides/values.md) for all aspects of the platform
    - Seamless [__in-place upgrades__](../guides/upgrade.md) and config updates
    - Connect your existing [:custom-istio-color: __Istio__](../guides/dependencies/istio.md#can-i-use-my-existing-istio), [:custom-cert-manager-color: __cert-manager__](../guides/dependencies/cert-manager.md#can-i-use-my-existing-cert-manager), [:custom-kyverno-color: __Kyverno__](../guides/dependencies/kyverno.md#can-i-use-my-existing-kyverno), [:custom-s3-color: __S3__](../guides/external/object-store.md#connect-an-external-object-store), and [:custom-mysql-color: __MySQL__](../guides/external/mysql.md#connect-an-external-mysql)
    - Use any [__identity provider__](../guides/platform/deploykf-authentication.md) via _OpenID Connect_ or _LDAP_
    - Native support for [__GitOps with ArgoCD__](../guides/dependencies/argocd.md#how-does-deploykf-use-argo-cd)

### __Video Introduction__

!!! info ""

    <div class="video-padding">
        <div class="youtube-video-container">
            <iframe src="https://www.youtube.com/embed/GDX4eLL_8E0?rel=0" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
        </div>
    </div>
    <div class="video-caption">
        Our presentation from [Kubeflow Summit 2023](https://www.kubeflow.org/events/kubeflow-summit-2023/), where we introduced deployKF to the community.
    </div>

### __User Stories__

!!! value ""

    We are always excited to see __how__ and __where__ deployKF is being used!

    Here are some stories of deployKF being used in the wild:

    Organization | Article / Video
    --- | ---
    :custom-cloudflare-color: Cloudflare | [_A look inside the Cloudflare ML Ops platform_](https://blog.cloudflare.com/mlops/)
    _Your Organization here!_ | [Join `ADOPTERS.md` List](https://github.com/deployKF/deployKF/blob/main/ADOPTERS.md) // [Contact Us](community.md#contact-us)

---

## Use deployKF

Now that you know what deployKF is, you can get started with the following guides:

<div class="mdx-hero__button-wrapper" markdown>

[Full Deployment](../guides/getting-started.md){ .md-button .md-button--primary .md-button--primary-right }
[Try Locally](../guides/local-quickstart.md){ .md-button .md-button--primary .md-button--primary-left }

</div>

### __Support the Project__

!!! warning ""

    deployKF is a new and growing project.
    If you like what we are doing, please help others discover us by __sharing the project__ with your colleagues and/or the wider community.

    We greatly appreciate [__GitHub Stars__ :star: on the `deployKF/deployKF`](https://github.com/deployKF/deployKF) repository:

    ![deployKF GitHub Star History (Dark Mode)](https://api.star-history.com/svg?repos=deployKF/deployKF&type=Date&theme=dark#only-dark){ .star-history_image }
    ![deployKF GitHub Star History (Light Mode)](https://api.star-history.com/svg?repos=deployKF/deployKF&type=Date#only-light){ .star-history_image }

---

## Other Resources

### __Community__

!!! support ""

    The [deployKF community](community.md) has a __Slack__ server for informal discussions among users and contributors:

    [Join the Slack<br>:fontawesome-brands-slack:](https://communityinviter.com/apps/deploykf/slack){ .md-button .md-button--primary }

### __Support__

!!! support ""

    Both __commercial__ and __open-source__ support is available for deployKF.

    [:material-briefcase: Commercial Support](support.md#commercial-support){ .md-button .md-button--primary }
    <br>
    [:material-hospital-box: Open-Source Support](support.md#open-source-support){ .md-button .md-button--secondary }

### __History of deployKF__

!!! value ""

    deployKF was originally created and is maintained by [Mathew Wicks](https://www.linkedin.com/in/mathewwicks/) (GitHub: [@thesuperzapper](https://github.com/thesuperzapper)), a Kubeflow lead and maintainer of the popular [Apache Airflow Helm Chart](https://github.com/airflow-helm/charts).
    deployKF is a community-led project that welcomes contributions from anyone who wants to help.