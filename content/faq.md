---
hide:
  - navigation
faq_schema:
  - question: What is deployKF?
    include_in_schema: true
    pre_expand_answer: true
    answer: |-
      __deployKF__ is the best way build reliable ML Platforms on Kubernetes.
        
      - _deployKF_ supports all the top ML tools from both Kubeflow (KF), and other projects
      - _deployKF_ has a Helm-like interface, with central [values (configs)](/reference/deploykf-values/) for configuring all aspects of the deployment (no need to edit Kubernetes YAML directly)
      - _deployKF_ does NOT install resources into your cluster, instead it generates [Argo CD Applications](https://argo-cd.readthedocs.io/en/stable/operator-manual/declarative-setup/#applications) which you apply to your cluster and then [sync with the Argo CD UI](https://argo-cd.readthedocs.io/en/stable/getting_started/#syncing-via-ui)

  - question: Who created deployKF?
    include_in_schema: true
    pre_expand_answer: true
    answer: |-
      __deployKF__ was originally created by [Mathew Wicks](https://www.linkedin.com/in/mathewwicks/) ([GitHub: @thesuperzapper](https://github.com/thesuperzapper)).
      However, deployKF is now a community owned project, and welcomes contributions from anyone who wants to help.

  - question: What is the difference between Kubeflow and deployKF?
    include_in_schema: true
    pre_expand_answer: true
    answer: |-
      __deployKF__ and __Kubeflow__ are two different projects, but they are related:
      
      - _deployKF_ is a tool for deploying Kubeflow and other MLOps tools on Kubernetes.
      - _Kubeflow_ is a project that develops many MLOps tools, including Kubeflow Pipelines, Kubeflow Notebooks, Katib, and more.
      - _deployKF_ is NOT a fork of Kubeflow, but it does allow you to deploy Kubeflow's MLOps tools.
      
      For more details, see our [comparison between __deployKF__ and __Kubeflow__](/about/kubeflow-vs-deploykf/). 

  - question: How is deployKF licensed?
    include_in_schema: false
    pre_expand_answer: false
    answer: |-
      __deployKF__ is licensed under the [Apache License 2.0](https://github.com/deployKF/deployKF/blob/main/LICENSE).
      However, some of the tools that deployKF can help deploy are licensed differently.
      Please ensure you are aware of the licenses of the tools you are deploying.

  - question: How does deployKF work under the hood?
    include_in_schema: false
    pre_expand_answer: false
    answer: |-
      __deployKF__ has two user-facing components:
      
      1. __deployKF CLI:__ a command line program who's primary purpose is to generate a set of folders containing GitOps-ready Kubernetes manifests, from configs provided in one or more values files
      2. __deployKF Generator:__ a versioned `.zip` package which contains all the templates and helpers needed to generate the output folders

      For more details, see our [architecture page](/about/architecture/).
---

# Frequently Asked Questions

{{ render_faq_schema(faq_schema) }}