---
## Tools in current deployKF versions
tools_current:
  - name: Kubeflow Pipelines
    purpose: Workflow Orchestration
    owner: Kubeflow Project
    docs_url: https://www.kubeflow.org/docs/components/pipelines/
    github_repo: kubeflow/pipelines
    deploykf_version: 0.1.0
    deploykf_values: kubeflow_tools.pipelines
    description: |
      Kubeflow Pipelines (KFP) is a platform for building and running machine learning workflows on Kubernetes.      

      KFP provides higher-level abstractions for [Argo Workflows](https://argoproj.github.io/argo-workflows/) to reduce repetition when defining machine learning tasks. 
      KFP has abstractions for defining [pipelines](https://www.kubeflow.org/docs/components/pipelines/v2/pipelines/) and [reusable components](https://www.kubeflow.org/docs/components/pipelines/v2/components/) which it can compile and execute as Argo [`Workflows`](https://argoproj.github.io/argo-workflows/workflow-concepts/#the-workflow).
      
      The primary interface of KFP is the [Python SDK](https://kubeflow-pipelines.readthedocs.io/en/latest/), which allows you to define pipelines and reusable components with Python.
      KFP also provides a [Web UI](https://www.kubeflow.org/docs/components/pipelines/v1/overview/interfaces/) for managing and tracking experiments, pipeline definitions, and pipeline runs.
      Finally, KFP provides a [REST API](https://www.kubeflow.org/docs/components/pipelines/v2/reference/api/kubeflow-pipeline-api-spec/) that allows programmatic access to the platform.

  - name: Kubeflow Notebooks
    purpose: Development Environments
    owner: Kubeflow Project
    docs_url: https://www.kubeflow.org/docs/components/notebooks/
    github_repo: kubeflow/kubeflow
    deploykf_version: 0.1.0
    deploykf_values: kubeflow_tools.notebooks
    description: |
      Kubeflow Notebooks lets you run web-based development environments inside a Kubernetes cluster.

      Kubeflow Notebooks can run any web-based tool, but comes with pre-built images for [JupyterLab](https://github.com/jupyterlab/jupyterlab), [RStudio](https://github.com/rstudio/rstudio), and [Visual Studio Code](https://github.com/coder/code-server).
      
      Running development environments inside a Kubernetes cluster has several advantages:

      - Remote Resources: Users can work directly on the cluster, rather than locally on their workstations.
      - Standard Environments: Cluster admins can provide standard environment images for their organization, with required and approved packages pre-installed.
      - Sharing & Access control: Access is managed via role-based-access-control (RBAC), enabling easier notebook sharing and collaboration across the organization.

  - name: Katib
    purpose: Automated Machine Learning
    owner: Kubeflow Project
    docs_url: https://www.kubeflow.org/docs/components/katib/
    github_repo: kubeflow/katib
    deploykf_version: 0.1.0
    deploykf_values: kubeflow_tools.katib
    description: |
      Katib is an [Automated Machine Learning (AutoML)](https://en.wikipedia.org/wiki/Automated_machine_learning) platform for Kubernetes.
      
      The key features of Katib are:

      - Support for Multiple Techniques: Katib supports techniques like [Hyperparameter Tuning](https://en.wikipedia.org/wiki/Hyperparameter_optimization), [Early Stopping](https://en.wikipedia.org/wiki/Early_stopping), and [Neural Architecture Search](https://en.wikipedia.org/wiki/Neural_architecture_search).
      - Support for ML Frameworks: Katib natively supports many ML frameworks like [TensorFlow](https://www.tensorflow.org/), [PyTorch](https://pytorch.org/), [XGBoost](https://xgboost.readthedocs.io/en/latest/), and more.
      - Kubernetes Native: Katib can [manage training jobs](https://www.kubeflow.org/docs/components/katib/trial-template/) on any Kubernetes Resource, and has out-of-the-box support for [Kubeflow Training Operator](https://github.com/kubeflow/training-operator), [Argo Workflows](https://github.com/argoproj/argo-workflows), [Tekton Pipelines](https://github.com/tektoncd/pipeline), and more.

  - name: Kubeflow Training Operator
    purpose: Training Models on Kubernetes
    owner: Kubeflow Project
    docs_url: https://www.kubeflow.org/docs/components/training/
    github_repo: kubeflow/training-operator
    deploykf_version: 0.1.0
    deploykf_values: kubeflow_tools.training_operator
    description: |
      Kubeflow Training Operator helps you run machine learning training jobs on Kubernetes.
      
      It provides Kubernetes Custom Resources (CRDs) to define and monitor training jobs on Kubernetes.
      Some popular ML frameworks that are supported include [PyTorch](https://pytorch.org/), [TensorFlow](https://www.tensorflow.org/), [XGBoost](https://xgboost.readthedocs.io/en/latest/), and [MPI](https://www.open-mpi.org/).
      
  - name: Kubeflow Volumes
    purpose: Managing Kubernetes Volumes
    owner: Kubeflow Project
    docs_url: ~
    github_repo: kubeflow/kubeflow
    deploykf_version: 0.1.0
    deploykf_values: kubeflow_tools.volumes
    description: |
      Kubeflow Volumes is a web-based UI for creating and managing Kubernetes [Persistent Volumes](https://kubernetes.io/docs/concepts/storage/persistent-volumes/).

  - name: Kubeflow TensorBoards
    purpose: Managing TensorBoards
    owner: Kubeflow Project
    docs_url: ~
    github_repo: kubeflow/kubeflow
    deploykf_version: 0.1.0
    deploykf_values: kubeflow_tools.tensorboards
    description: |
      Kubeflow TensorBoards is a web-based UI for creating and managing [TensorBoard](https://www.tensorflow.org/tensorboard) instances on Kubernetes.
---

# Supported Tools

This page lists the ML & Data tools which are __currently supported__ by __deployKF__.

!!! tip "Build Your Platform"
    
    You don't need to install all of the tools listed here, deployKF makes it easy to build your own platform by selecting only the tools you need,
    just toggle the tool's [`enabled` value](deploykf-values.md).

!!! tip "Future Tools"
    
    __deployKF__ is always growing, for a list of tools that are coming soon, please see the [Future Tools](future-tools.md) page.

!!! note "Tool Versions"
    
    For information about which versions of each tool are supported by deployKF, please refer to the [deployKF Tools](../releases/version-matrix.md#deploykf-tools) and [Kubeflow Tools](../releases/version-matrix.md#kubeflow-tools) sections of the Version Matrix page.

## Index

{{ render_current_tools_index(tools_current) }}

{{ render_current_tools_details(tools_current) }}