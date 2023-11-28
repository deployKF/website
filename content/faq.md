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
      deployKF helps you build world-class data and machine learning platforms on __any Kubernetes cluster__, in any cloud or environment.
      
      Our vision is that __anyone with Kubernetes experience__ can effortlessly build and support a _custom data and machine learning platform_ for their organization, without requiring specialized MLOps knowledge.

  - question: Why use deployKF?
    highlight_answer: true
    include_in_schema: true
    pre_expand_answer: true
    answer: |-
      By combining the <em>ease of a managed service</em> with the flexibility of a self-hosted solution; 
      deployKF creates a platform tailored to your organization's needs, while not also requiring a team of MLOps experts to build and maintain it.
      
      The key features of deployKF are:
      
      - Runs on __any Kubernetes__, including on-premises and in the cloud
      - Support for leading __Data and MLOps tools__ including [__Kubeflow__](./reference/tools.md#kubeflow-ecosystem), [__Airflow__](./reference/future-tools.md#apache-airflow)<sup>†</sup>, and [__MLflow__](./reference/future-tools.md#mlflow-model-registry)<sup>†</sup>
      - Intuitive [__centralized configs__](./reference/deploykf-values.md) to manage all aspects of the platform
      - Seamless __in-place upgrades__ and config rollouts
      - Connect with __existing services__ like Istio and cert-manager, [S3](./guides/tools/external-object-store.md), and [MySQL](./guides/tools/external-mysql.md).
      - Native support for __GitOps__ via ArgoCD
  
      <small><sup>†</sup>Coming soon, see our [current](./reference/tools.md) and [future](./reference/future-tools.md) tools.</small>

  - question: Is there commercial support for deployKF?
    include_in_schema: true
    pre_expand_answer: true
    admonition_type: support
    answer: |-
      If you need commercial support for deployKF, please contact __Aranui Solutions__.
      Aranui Solutions is a US-based company founded by the creators of deployKF to help organizations build ML & Data Platforms on Kubernetes.

      [Visit: _Aranui Solutions Website_](https://www.aranui.solutions/){ .md-button .md-button--secondary }
      [Email: _`sales@aranui.solutions`_](mailto:sales@aranui.solutions?subject=%5BdeployKF%5D%20MY_SUBJECT){ .md-button .md-button--secondary }

  - question: Which ML and AI tools are in deployKF?
    include_in_schema: true
    pre_expand_answer: false
    answer: |-
      deployKF supports all tools from the [Kubeflow Ecosystem](./reference/tools.md#kubeflow-ecosystem) including [Kubeflow Pipelines](./reference/tools.md#kubeflow-pipelines) and [Kubeflow Notebooks](./reference/tools.md#kubeflow-notebooks).
      We are actively adding support for other popular tools such as [MLflow](./reference/future-tools.md#mlflow-model-registry), [Airflow](./reference/future-tools.md#apache-airflow), and [Feast](./reference/future-tools.md#feast). 
      For more information, please see our [current](./reference/tools.md) and [future](./reference/future-tools.md) tools!

  - question: Who maintains deployKF?
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