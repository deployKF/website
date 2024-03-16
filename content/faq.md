---
icon: material/help-circle-outline
description: >-
  Frequently Asked Questions about deployKF.

hide:
  - navigation
faq_schema:
  - question: What is deployKF?
    highlight_answer: true
    include_in_schema: true
    pre_expand_answer: true
    answer: |-
      <strong><span class="deploykf-orange">deploy</span><span class="deploykf-blue">KF</span></strong> builds machine learning platforms on __Kubernetes__.
      We combine the best of 
      [:custom-kubeflow-color: __Kubeflow__](./reference/tools.md#kubeflow-ecosystem), 
      [:custom-airflow-color: __Airflow__](./reference/future-tools.md#apache-airflow)<sup>†</sup>, and 
      [:custom-mlflow-color: __MLflow__](./reference/future-tools.md#mlflow-model-registry)<sup>†</sup>
      into a complete platform that is easy to deploy and maintain.
  
      <small><sup>†</sup>Coming soon, see our [current](./reference/tools.md) and [future](./reference/future-tools.md) tools.</small>

  - question: Why use deployKF?
    highlight_answer: true
    include_in_schema: true
    pre_expand_answer: true
    answer: |-
      deployKF combines the _ease of a managed service_ with the flexibility of a self-hosted solution. 

      Our vision is that ___anyone with Kubernetes experience___ can build a _machine learning platform_ for their organization, without needing _specialized MLOps knowledge_,
      and a team of experts to maintain it.
  
      The key features of deployKF are:
  
      - Run on [__any Kubernetes cluster__](./guides/getting-started.md#kubernetes-cluster), including on-premises and in the cloud
      - Intuitive [__centralized configs__](./guides/values.md) for all aspects of the platform
      - Seamless [__in-place upgrades__](./guides/upgrade.md) and config updates
      - Connect your existing [:custom-istio-color: __Istio__](./guides/dependencies/istio.md#can-i-use-my-existing-istio), [:custom-cert-manager-color: __cert-manager__](./guides/dependencies/cert-manager.md#can-i-use-my-existing-cert-manager), [:custom-kyverno-color: __Kyverno__](./guides/dependencies/kyverno.md#can-i-use-my-existing-kyverno), [:custom-s3-color: __S3__](./guides/external/object-store.md#connect-an-external-object-store), and [:custom-mysql-color: __MySQL__](./guides/external/mysql.md#connect-an-external-mysql)
      - Use any [__identity provider__](./guides/platform/deploykf-authentication.md) via _OpenID Connect_ or _LDAP_
      - Native support for [__GitOps with ArgoCD__](./guides/dependencies/argocd.md#how-does-deploykf-use-argo-cd)

  - question: Is there commercial support for deployKF?
    include_in_schema: true
    pre_expand_answer: true
    admonition_type: support
    answer: |-
      To discuss commercial support options for deployKF, please connect with [:custom-aranui-solutions-color: __Aranui Solutions__](https://www.aranui.solutions/), the company started by the creators of deployKF.

      [:material-open-in-new: Visit Website](https://www.aranui.solutions/){ .md-button .md-button--secondary }
      [:fontawesome-solid-envelope: Email Aranui Solutions](mailto:sales@aranui.solutions?subject=%5BdeployKF%5D%20MY_SUBJECT){ .md-button .md-button--secondary }

  - question: Which ML and AI tools are in deployKF?
    include_in_schema: true
    pre_expand_answer: false
    answer: |-
      deployKF supports all tools from the [Kubeflow Ecosystem](./reference/tools.md#kubeflow-ecosystem) including [Kubeflow Pipelines](./reference/tools.md#kubeflow-pipelines) and [Kubeflow Notebooks](./reference/tools.md#kubeflow-notebooks).
      We are actively adding support for other popular tools such as [MLflow](./reference/future-tools.md#mlflow-model-registry), [Airflow](./reference/future-tools.md#apache-airflow), and [Feast](./reference/future-tools.md#feast). 
      For more information, please see our [current](./reference/tools.md) and [future](./reference/future-tools.md) tools!

  - question: Who created deployKF?
    include_in_schema: true
    pre_expand_answer: false
    answer: |-
      deployKF was originally created and is maintained by [Mathew Wicks](https://www.linkedin.com/in/mathewwicks/) (GitHub: [@thesuperzapper](https://github.com/thesuperzapper)), a Kubeflow lead and maintainer of the popular [Apache Airflow Helm Chart](https://github.com/airflow-helm/charts).
      deployKF is a community-led project that welcomes contributions from anyone who wants to help.

  - question: Who has adopted deployKF?
    include_in_schema: false
    pre_expand_answer: false
    answer: |-
      deployKF is a new project, and we are still building our community, consider [adding your organization](https://github.com/deployKF/deployKF/blob/main/ADOPTERS.md) to our list of adopters.

  - question: How are Kubeflow and deployKF related?
    include_in_schema: true
    pre_expand_answer: false
    answer: |-
      Kubeflow and deployKF are two different but related projects.
      For more details, please see our [deployKF vs Kubeflow](./about/kubeflow-vs-deploykf.md) comparison.

  - question: How can I get involved with deployKF?
    include_in_schema: false
    pre_expand_answer: false
    answer: |-
      The deployKF project is a welcoming community of contributors and users. 
      We encourage participation from anyone who shares our mission of making it easy to build open ML Platforms on Kubernetes.
      For more details, see our [community page](./about/community.md).

  - question: How is deployKF licensed?
    include_in_schema: false
    pre_expand_answer: false
    answer: |-
      __deployKF__ is licensed under the [Apache License 2.0](https://github.com/deployKF/deployKF/blob/main/LICENSE).
      However, some of the tools that deployKF can help deploy are licensed differently.
      Please ensure you are aware of how the tools you deploy are licenced.
---

# Frequently Asked Questions

Frequently asked questions about deployKF.

{{ render_faq_schema(faq_schema) }}