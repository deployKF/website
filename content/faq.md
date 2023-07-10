---
hide:
  - navigation
faq_schema:
  - question: What is deployKF?
    include_in_schema: true
    pre_expand_answer: true
    answer: |-
      deployKF is the best way to build reliable ML Platforms on Kubernetes.

      - deployKF supports leading [MLOps & Data tools](/reference/tools/) from both Kubeflow, and other projects
      - deployKF has a Helm-like interface, with [values](/reference/deploykf-values/) for configuring all aspects of the deployment (no need to edit Kubernetes YAML)
      - deployKF does NOT install resources directly in your cluster, instead it generates [ArgoCD Applications](https://argo-cd.readthedocs.io/en/stable/operator-manual/declarative-setup/#applications) to provide native GitOps support

  - question: What tools does deployKF support?
    include_in_schema: true
    pre_expand_answer: true
    answer: |-
      deployKF currently supports MLOps tools from the Kubeflow ecosystem like [Kubeflow Pipelines](/reference/tools/#kubeflow-pipelines) and [Kubeflow Notebooks](/reference/tools/#kubeflow-notebooks), for the full list of current tools, please see the [supported tools page](/reference/tools/).
      
      We are actively adding support for other popular tools such as [MLflow Model Registry](/reference/future-tools/#mlflow-model-registry), [Apache Airflow](/reference/future-tools/#apache-airflow), and [Feast](/reference/future-tools/#feast). 
      For a more complete list of planned tools, please see the [future tools page](/reference/future-tools/).

  - question: Who created deployKF?
    include_in_schema: true
    pre_expand_answer: true
    answer: |-
      deployKF was originally created by [Mathew Wicks](https://www.linkedin.com/in/mathewwicks/) ([GitHub: @thesuperzapper](https://github.com/thesuperzapper)), a Kubeflow lead and maintainer of the popular [Apache Airflow Helm Chart](https://github.com/airflow-helm/charts).
      However, deployKF is now a community-led project that welcomes contributions from anyone who wants to help.
      
      For commercial services related to deployKF, please see the [support page](/about/support/#commercial-support).

  - question: Who uses deployKF?
    include_in_schema: false
    pre_expand_answer: true
    answer: |-
      deployKF is a new project, and we are still building our community.
      
      If you are using deployKF, please consider adding your organization to our [list of adopters](https://github.com/deployKF/deployKF/blob/main/ADOPTERS.md).

  - question: What is the difference between Kubeflow and deployKF?
    include_in_schema: true
    pre_expand_answer: true
    answer: |-
      Kubeflow and deployKF are two different but related projects:
      
      - deployKF is a tool for deploying Kubeflow and other MLOps tools on Kubernetes as a cohesive platform.
      - Kubeflow is a project that develops MLOps tools, including Kubeflow Pipelines, Kubeflow Notebooks, Katib, and more.
      
      For more details, see our [comparison between Kubeflow and deployKF](/about/kubeflow-vs-deploykf/).

  - question: How can I get involved with deployKF?
    include_in_schema: false
    pre_expand_answer: true
    answer: |-
      The deployKF project is a welcoming community of contributors and users. 
      We encourage participation from anyone who shares our mission of making it easy to build open ML Platforms on Kubernetes.
      
      For more details, see our [community page](/about/community/).

  - question: How is deployKF licensed?
    include_in_schema: false
    pre_expand_answer: true
    answer: |-
      __deployKF__ is licensed under the [Apache License 2.0](https://github.com/deployKF/deployKF/blob/main/LICENSE).
      However, some of the tools that deployKF can help deploy are licensed differently.
      Please ensure you are aware of how the tools you deploy are licenced.
---

# Frequently Asked Questions

{{ render_faq_schema(faq_schema) }}