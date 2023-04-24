---
hide:
  - navigation
faq_schema:
  - question: What is deployKF?
    include_in_schema: true
    pre_expand_answer: true
    answer: |-
      __deployKF__ is the best way to deploy KF (Kubeflow) and other MLOps tools on Kubernetes to create custom, open, and cohesive ML Platforms.

  - question: Who created deployKF?
    include_in_schema: true
    pre_expand_answer: true
    answer: |-
      __deployKF__ was originally created by [Mathew Wicks](https://www.linkedin.com/in/mathewwicks/) ([GitHub: @thesuperzapper](https://github.com/thesuperzapper)).
      However, deployKF is now a community owned project, and welcomes contributions from anyone who wants to help.

  - question: What is the difference between Kubeflow and deployKF?
    include_in_schema: true
    pre_expand_answer: false
    answer: |-
      __deployKF__ and __Kubeflow__ are two different projects, but they are related:
      
      - deployKF is a tool for deploying Kubeflow and other MLOps tools on Kubernetes.
      - Kubeflow is a project made up of many different tools, including Kubeflow Pipelines, Kubeflow Notebooks, Katib, and more.
      - deployKF is NOT a fork of Kubeflow, but it does allow you to deploy the Kubeflow MLOps components.

  - question: What are the components of deployKF?
    include_in_schema: false
    pre_expand_answer: false
    answer: |-
      __deployKF__ has two main components:
      
      1. [deployKF CLI](https://github.com/deployKF/cli): a command line tool for generating GitOps-ready Kubernetes manifests
      2. [deployKF Generator](https://github.com/deployKF/deployKF): a package of templated Kubernetes manifests for use with the deployKF CLI

  - question: How is deployKF licensed?
    include_in_schema: false
    pre_expand_answer: false
    answer: |-
      __deployKF__ is licensed under the [Apache License 2.0](https://github.com/deployKF/deployKF/blob/main/LICENSE).
      However, some of the tools that deployKF can help deploy are licensed differently.
      Please ensure you are aware of the licenses of the tools you are deploying.
---

# Frequently Asked Questions

{{ render_faq_schema(faq_schema) }}