---
icon: material/wrench

## Tools in current deployKF versions
tools_current:
  - name: Kubeflow Pipelines
    purpose: Workflow Orchestration
    maintainer: Kubeflow Project
    docs_url: https://www.kubeflow.org/docs/components/pipelines/
    github_repo: kubeflow/pipelines
    deploykf_version: 0.1.0
    deploykf_values: kubeflow_tools.pipelines
    introduction: |
      [__Kubeflow Pipelines (KFP)__](https://github.com/kubeflow/pipelines) is a platform for building and running machine learning workflows on Kubernetes.
    description: |
      KFP provides higher-level abstractions for [Argo Workflows](https://argoproj.github.io/argo-workflows/) to reduce repetition when defining machine learning tasks. 
      KFP has abstractions for defining [pipelines](https://www.kubeflow.org/docs/components/pipelines/v2/pipelines/) and [reusable components](https://www.kubeflow.org/docs/components/pipelines/v2/components/) which it can compile and execute as Argo [`Workflows`](https://argoproj.github.io/argo-workflows/workflow-concepts/#the-workflow).
      
      The primary interface of KFP is the [Python SDK](https://kubeflow-pipelines.readthedocs.io/en/latest/), which allows you to define pipelines and reusable components with Python.
      KFP also provides a [Web UI](https://www.kubeflow.org/docs/components/pipelines/v1/overview/interfaces/) for managing and tracking experiments, pipeline definitions, and pipeline runs.
      Finally, KFP provides a [REST API](https://www.kubeflow.org/docs/components/pipelines/v2/reference/api/kubeflow-pipeline-api-spec/) that allows programmatic access to the platform.
    footnote: ""

  - name: Kubeflow Notebooks
    purpose: Hosting Developer Environments
    maintainer: Kubeflow Project
    docs_url: https://www.kubeflow.org/docs/components/notebooks/
    github_repo: kubeflow/kubeflow
    deploykf_version: 0.1.0
    deploykf_values: kubeflow_tools.notebooks
    introduction: |
      [__Kubeflow Notebooks__](https://www.kubeflow.org/docs/components/notebooks/overview/) lets you run web-based development environments inside a Kubernetes cluster.
    description: |
      Kubeflow Notebooks can run any web-based tool, but comes with pre-built images for [JupyterLab](https://github.com/jupyterlab/jupyterlab), [RStudio](https://github.com/rstudio/rstudio), and [Visual Studio Code](https://github.com/coder/code-server).
      
      Running development environments inside a Kubernetes cluster has several advantages:

      - __Remote Resources__: Users can work directly on the cluster, rather than locally on their workstations.
      - __Standard Environments__: Cluster admins can provide standard environment images for their organization, with required and approved packages pre-installed.
      - __Sharing & Access Control__: Access is managed via role-based-access-control (RBAC), enabling easier notebook sharing and collaboration across the organization.
    footnote: ""

  - name: Katib
    purpose: Automated Machine Learning
    maintainer: Kubeflow Project
    docs_url: https://www.kubeflow.org/docs/components/katib/
    github_repo: kubeflow/katib
    deploykf_version: 0.1.0
    deploykf_values: kubeflow_tools.katib
    introduction: |
      [__Katib__](https://www.kubeflow.org/docs/components/katib/overview/) is an [Automated Machine Learning (AutoML)](https://en.wikipedia.org/wiki/Automated_machine_learning) platform for Kubernetes.
    description: |
      The key features of Katib are:

      - __Support for Multiple Techniques__: Katib supports techniques like [Hyperparameter Tuning](https://en.wikipedia.org/wiki/Hyperparameter_optimization), [Early Stopping](https://en.wikipedia.org/wiki/Early_stopping), and [Neural Architecture Search](https://en.wikipedia.org/wiki/Neural_architecture_search).
      - __Support for ML Frameworks__: Katib natively supports many ML frameworks like [TensorFlow](https://www.tensorflow.org/), [PyTorch](https://pytorch.org/), [XGBoost](https://xgboost.readthedocs.io/en/latest/), and more.
      - __Kubernetes Native__: Katib can [manage training jobs](https://www.kubeflow.org/docs/components/katib/trial-template/) on any Kubernetes Resource, and has out-of-the-box support for [Kubeflow Training Operator](https://github.com/kubeflow/training-operator), [Argo Workflows](https://github.com/argoproj/argo-workflows), [Tekton Pipelines](https://github.com/tektoncd/pipeline), and more.
    footnote: ""

  - name: Kubeflow Training Operator
    purpose: Managing Training Jobs
    maintainer: Kubeflow Project
    docs_url: https://www.kubeflow.org/docs/components/training/
    github_repo: kubeflow/training-operator
    deploykf_version: 0.1.0
    deploykf_values: kubeflow_tools.training_operator
    introduction: |
      [__Kubeflow Training Operator__](https://github.com/kubeflow/training-operator) helps you run machine learning training jobs on Kubernetes.
    description: |
      The core function of the  Kubeflow Training Operator is to provide _Kubernetes Custom Resources_ (CRDs) that define and monitor training jobs on Kubernetes.
      
      Many popular ML frameworks have been integrated with the Training Operator, including:
      
      - [__PyTorch__](https://pytorch.org/)
      - [__TensorFlow__](https://www.tensorflow.org/)
      - [__XGBoost__](https://xgboost.readthedocs.io/en/latest/)
      - [__MPI__](https://www.open-mpi.org/)
    footnote: ""

  - name: Kubeflow Volumes
    purpose: Managing Kubernetes Volumes
    maintainer: Kubeflow Project
    docs_url: ~
    github_repo: kubeflow/kubeflow
    deploykf_version: 0.1.0
    deploykf_values: kubeflow_tools.volumes
    introduction: |
      __Kubeflow Volumes__ is a web-based UI for creating and managing Kubernetes [Persistent Volumes](https://kubernetes.io/docs/concepts/storage/persistent-volumes/).
    description: ""
    footnote: ""

  - name: Kubeflow TensorBoards
    purpose: Managing TensorBoards
    maintainer: Kubeflow Project
    docs_url: ~
    github_repo: kubeflow/kubeflow
    deploykf_version: 0.1.0
    deploykf_values: kubeflow_tools.tensorboards
    introduction: |
      __Kubeflow TensorBoards__ is a web-based UI for creating and managing [TensorBoard](https://www.tensorflow.org/tensorboard) instances on Kubernetes.
    description: ""
    footnote: ""

---

# ML & Data Tools (Current)

This page lists __ML & Data tools__ which are __currently supported__ by deployKF.

!!! question_secondary "What versions of each tool are supported?"
    
    See the [version matrix](../releases/version-matrix.md) to learn which versions of each tool are supported by each version of deployKF.

!!! question_secondary "What tools are planned for future releases?"

    See the [future tools](future-tools.md) page for a list of tools which are planned for future releases.

---

## Tool Index

The following is an index of currently supported tools, __grouped by ecosystem__.

!!! tip

     Click the name of a tool for more information about it.

### Kubeflow Ecosystem

[Kubeflow](https://en.wikipedia.org/wiki/Kubeflow) is an "MLOps on Kubernetes" ecosystem which is [owned by the CNCF](https://www.cncf.io/blog/2023/07/25/kubeflow-brings-mlops-to-the-cncf-incubator/), and provides various tools for building and deploying ML applications on Kubernetes.

{{ render_current_tools_index(tools_current) }}

### deployKF Ecosystem

!!! value ""
   
    Coming soon... See [future tools](future-tools.md) for more information.

## Tool Details

The following sections provide details and descriptions for each tool.

{{ render_current_tools_details(tools_current) }}