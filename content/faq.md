---
icon: material/help-circle-outline
hide:
  - navigation
faq_schema:
  - question: What is deployKF?
    highlight_answer: true
    include_in_schema: true
    pre_expand_answer: false
    answer: |-
      deployKF builds world-class ML Platforms on __any Kubernetes cluster__, within __any cloud or environment__, in minutes.
      
      - deployKF includes [__leading ML & Data tools__](./reference/tools.md#tool-index) from Kubeflow and more
      - deployKF has [__centralized configs__](./reference/deploykf-values.md) that manage all aspects of the platform
      - deployKF supports __in-place upgrades__ and can __autonomously__ roll out config changes
      - deployKF lets you __bring your own__ cluster dependencies like __istio__ and __cert-manager__, if desired
      - deployKF uses __ArgoCD Applications__ to provide native GitOps support

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
      deployKF was originally created by [Mathew Wicks](https://www.linkedin.com/in/mathewwicks/) (GitHub: [@thesuperzapper](https://github.com/thesuperzapper)), a Kubeflow lead and maintainer of the popular [Apache Airflow Helm Chart](https://github.com/airflow-helm/charts).
      deployKF is a community-led project that welcomes contributions from anyone who wants to help.
   
  - question: Do you offer commercial support for deployKF?
    include_in_schema: true
    pre_expand_answer: false
    answer: |-
      The creator of deployKF (Mathew Wicks), operates a US-based ML & Data company named [Aranui Solutions](https://www.aranui.solutions) which provides commercial support and advisory services.
      Connect on [LinkedIn](https://www.linkedin.com/in/mathewwicks/) or email [`sales@aranui.solutions`](mailto:sales@aranui.solutions?subject=%5BdeployKF%5D%20MY_SUBJECT) to learn more!

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

{{ render_faq_schema(faq_schema) }}