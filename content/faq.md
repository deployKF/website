---
hide:
  - navigation
faq_schema:
  - question: What is deployKF?
    highlight_answer: true
    include_in_schema: true
    pre_expand_answer: false
    answer: |-
      deployKF is the best way to build reliable ML Platforms on Kubernetes.
      
      - deployKF supports leading [ML & Data tools](./reference/tools.md) from both Kubeflow, and other projects
      - deployKF has a Helm-like interface, with [values](./reference/deploykf-values.md) for configuring all aspects of the deployment
      - deployKF uses [ArgoCD Applications](./guides/getting-started.md#4-sync-argocd-applications) to provide native GitOps support

  - question: What ML/AI tools are in deployKF?
    include_in_schema: true
    pre_expand_answer: false
    answer: |-
      Currently, deployKF supports MLOps tools from the Kubeflow ecosystem like [Kubeflow Pipelines](./reference/tools.md#kubeflow-pipelines) and [Kubeflow Notebooks](./reference/tools.md#kubeflow-notebooks).
      We are actively adding support for other popular tools such as [MLFlow (Model Registry)](./reference/future-tools.md#mlflow-model-registry), [Apache Airflow](./reference/future-tools.md#apache-airflow), and [Feast](./reference/future-tools.md#feast). 
      
      For more information, please see [supported tools](./reference/tools.md) and [future tools](./reference/future-tools.md)!

  - question: Who makes deployKF?
    include_in_schema: true
    pre_expand_answer: false
    answer: |-
      deployKF was originally created by [Mathew Wicks](https://www.linkedin.com/in/mathewwicks/) (GitHub: [@thesuperzapper](https://github.com/thesuperzapper)), a Kubeflow lead and maintainer of the popular [Apache Airflow Helm Chart](https://github.com/airflow-helm/charts).
      However, deployKF is now a community-led project that welcomes contributions from anyone who wants to help.
   
  - question: Is commercial support available for deployKF?
    include_in_schema: true
    pre_expand_answer: false
    answer: |-
      The creator of deployKF (Mathew Wicks), operates a US-based MLOps company called [Aranui Solutions](https://www.aranui.solutions) that provides commercial support and consulting for deployKF.
    
      Connect on [LinkedIn](https://www.linkedin.com/in/mathewwicks/) or email [`sales@aranui.solutions`](mailto:sales@aranui.solutions?subject=%5BdeployKF%5D%20MY_SUBJECT) to learn more!

  - question: Who uses deployKF?
    include_in_schema: false
    pre_expand_answer: false
    answer: |-
      deployKF is a new project, and we are still building our community.
      
      Please consider adding your organization to our [list of adopters](https://github.com/deployKF/deployKF/blob/main/ADOPTERS.md).

  - question: What is the difference between Kubeflow and deployKF?
    include_in_schema: true
    pre_expand_answer: false
    answer: |-
      Kubeflow and deployKF are two different but related projects:
      
      - deployKF is a tool for deploying Kubeflow and other MLOps tools on Kubernetes as a cohesive platform.
      - Kubeflow is a project that develops MLOps tools, including Kubeflow Pipelines, Kubeflow Notebooks, Katib, and more.
      
      For more details, see our detailed [__deployKF__ vs  __Kubeflow__](./about/kubeflow-vs-deploykf.md) comparison.

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