---
icon: material/wrench-clock
description: >-
  A list of ML & Data tools which may be part of future versions of deployKF.

## Tools planned for future deployKF versions
tools_planned:
  - name: MLflow Model Registry
    purpose: Model Registry
    maintainer: Databricks
    docs_url: https://www.mlflow.org/docs/latest/model-registry.html
    github_repo: mlflow/mlflow
    deploykf_priority: 1
    introduction: |
      [__MLflow Model Registry__](https://www.mlflow.org/docs/latest/model-registry.html) is an open source machine learning model registry.
    description: |
      A model registry decouples _model training_ from _model deployment_, allowing you to break the model lifecycle down into three _separate concerns_.
      This separation enables you to have well-scoped pipelines, rather than trying to go from training to deployment all at once.
      
      1. __Model Training__: Training new versions of models and logging them into the registry.
      2. __Model Evaluation__: Evaluating versions of models and logging the results into the registry.
      3. __Model Deployment__: Making informed decisions about which models to deploy and then deploying them.

      The key features of MLflow Model Registry are:
      
      - [__Model Versioning__](https://mlflow.org/docs/latest/model-registry.html#adding-an-mlflow-model-to-the-model-registry): Version your model artifacts and attach metadata to each version.
      - [__Model Stage Transitions__](https://mlflow.org/docs/latest/model-registry.html#transitioning-an-mlflow-models-stage): Transition models between stages (e.g. staging to production).
      - [__Web UI__](https://www.mlflow.org/docs/latest/model-registry.html#ui-workflow): A graphical web interface for managing models.
      - [__Python API__](https://www.mlflow.org/docs/latest/model-registry.html#api-workflow): A Python API for managing models.
      - [__REST API__](https://www.mlflow.org/docs/latest/rest-api.html): A REST API for managing models.
    footnote: ""

  - name: KServe
    purpose: Model Serving
    maintainer: Linux Foundation
    docs_url: https://kserve.github.io/website/
    github_repo: kserve/kserve
    deploykf_priority: 1
    introduction: |
      [__KServe__](https://kserve.github.io/website/) provides comprehensive interfaces for deploying, managing, and monitoring ML models on Kubernetes.
    description: |
      The core features of KServe are:
      
      - [__Support for Many Frameworks__](https://kserve.github.io/website/0.10/modelserving/v1beta1/serving_runtime/): KServe natively supports many ML frameworks (e.g. PyTorch, TensorFlow, scikit-learn, XGBoost).
      - [__Autoscaling, Even to Zero__](https://kserve.github.io/website/0.10/modelserving/autoscaling/autoscaling/): KServe can autoscale model replicas to meet demand, even scaling to zero when there are no requests.
      - [__Model Monitoring__](https://kserve.github.io/website/0.10/modelserving/detect/alibi_detect/alibi_detect/): KServe integrates tools like [Alibi Detect](https://github.com/SeldonIO/alibi-detect) to provide model monitoring for drift and outlier detection.
      - [__Model Explainability__](https://kserve.github.io/website/0.10/modelserving/explainer/explainer/): KServe integrates tools like [Alibi Explain](https://github.com/SeldonIO/alibi) to provide model explainability.
      - [__Request Batching__](https://kserve.github.io/website/0.10/modelserving/batcher/batcher/): KServe can batch requests to your model, improving throughput and reducing cost.
      - [__Canary Deployments__](https://kserve.github.io/website/0.10/modelserving/v1beta1/rollout/canary/): KServe can deploy new versions of your model alongside old versions, and route requests to the new version based on a percentage.
      - [__Feature Transformers__](https://kserve.github.io/website/0.10/modelserving/v1beta1/transformer/feast/): KServe can do feature pre/post processing alongside model inference (e.g. using Feast).
      - [__Inference Graphs__](https://kserve.github.io/website/0.10/modelserving/inference_graph/): KServe can chain multiple models together to form an inference graph.
    footnote: ""

  - name: Apache Airflow
    purpose: Workflow Orchestration
    maintainer: Apache Software Foundation
    docs_url: https://airflow.apache.org/docs/
    github_repo: apache/airflow
    deploykf_priority: 2
    introduction: |
      [__Apache Airflow__](https://airflow.apache.org/) is by far the [most popular](https://github.com/apache/airflow/blob/main/INTHEWILD.md) open-source workflow orchestration tool in the world.
    description: |
      The versatility and extensibility of Apache Airflow make it a great fit for many different use cases, including machine learning.
      
      The key features of Apache Airflow are:

      - __Python Centered__: Airflow is written in Python and uses a [Python DSL](https://airflow.apache.org/docs/apache-airflow/stable/index.html#what-is-airflow) to define workflows.
      - __Dynamic Workflows__: Airflow's code-driven workflow definitions enable powerful patterns like [dynamically generating workflows](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dags.html#dynamic-dags).
      - __Extensive Plugins__: Airflow has a rich ecosystem of [plugins and integrations](https://airflow.apache.org/docs/) with other tools.
      - __User Interface__: Airflow is known for its [powerful user interface](https://airflow.apache.org/docs/apache-airflow/stable/ui.html) which allows users to monitor and manage workflows.
    footnote: ""

  - name: Feast
    purpose: Feature Store
    maintainer: Tecton
    docs_url: https://docs.feast.dev/
    github_repo: feast-dev/feast
    deploykf_priority: 2
    introduction: |
      [__Feast__](https://feast.dev/) is an open-source feature store for machine learning.
    description: |
      A good way to understand the purpose of a feature store is to think about the _data access patterns_ encountered during the model lifecycle.
      A feature store should somehow make these data access patterns easier.
      
      - __Feature Engineering__: Accesses and transforms historical data to create features.
      - __Target Engineering__: Accesses and transforms historical data to create targets.
      - __Model Training__: Accesses features and targets to train and evaluate the model.
      - __Model Inference__: Accesses features of new data to predict the target.
      
      The key features of Feast are:
      
      - [__Feature Registry__](https://docs.feast.dev/getting-started/architecture-and-components/registry): Where Feast persists _feature definitions_ (not data) that are registered with with it (e.g. Local-Files, S3, GCS).
      - [__Python SDK__](https://rtd.feast.dev/en/master/): The primary interface for managing _feature definitions_, and retrieving _feature values_ from Feast.
      - [__Offline Data Stores__](https://docs.feast.dev/reference/offline-stores): A store which Feast can read _feature values_ from, for historical data retrieval (e.g. Snowflake, BigQuery, Redshift).
      - [__Online Data Stores__](https://docs.feast.dev/reference/online-stores): A store which Feast can materialize (write) _feature values_ into, for online model inference (e.g. Snowflake, Redis, DynamoDB, Bigtable).
      - [__Batch Materialization Engine__](https://docs.feast.dev/reference/batch-materialization): A data processing engine which Feast can use to materialize _feature values_ from an _Offline Store_ into an _Online Store_ (e.g. Snowflake, Spark, Bytewax).
    footnote: |
      !!! warning ""
          
          A good feature store is __NOT a database__, but rather a __data access layer__ between your data sources and your ML models.
          Be very wary of any feature store that requires you to load your data into it directly.

  - name: Seldon Core
    purpose: Model Serving
    maintainer: Seldon
    docs_url: https://docs.seldon.io/projects/seldon-core/en/latest/
    github_repo: SeldonIO/seldon-core
    deploykf_priority: 3
    introduction: |
      [__Seldon Core__](https://www.seldon.io/solutions/open-source-projects/core) provides interfaces for converting ML models into REST/gRPC microservices on Kubernetes.
    description: |
      The core features of Seldon Core are:
      
      - [__Support for Many Frameworks__](https://docs.seldon.io/projects/seldon-core/en/latest/servers/overview.html): Seldon Core natively supports many ML frameworks (e.g. TensorFlow, scikit-learn, XGBoost, HuggingFace, NVIDIA Triton).
      - [__Reusable Model Servers__](https://docs.seldon.io/projects/seldon-core/en/latest/workflow/overview.html#two-types-of-model-servers): Seldon Core removes the need to build a container image for each model, by providing a system to download model artifacts at runtime.
      - [__Model Deployment CRD__](https://docs.seldon.io/projects/seldon-core/en/latest/workflow/overview.html#seldon-deployment-crd) Seldon Core provides a simple, yet powerful, Kubernetes CRD for deploying models.
    footnote: ""

  - name: BentoML Yatai
    purpose: Model Serving
    maintainer: BentoML
    docs_url: https://docs.yatai.io/en/latest/index.html
    github_repo: bentoml/Yatai
    deploykf_priority: 3
    introduction: |
      [__BentoML Yatai__](https://docs.yatai.io/en/latest/index.html) is a platform for managing the lifecycle of BentoML models on Kubernetes.
    description: |
      The core features of BentoML Yatai are:
      
      - [__Model Registry__](https://docs.bentoml.org/en/latest/concepts/model.html#push-and-pull-with-yatai): A central registry for [packaged Bentos](https://docs.bentoml.org/en/latest/concepts/bento.html).
      - [__Model Deployment__](https://docs.bentoml.org/en/latest/concepts/deploy.html#deploy-with-yatai): Managing the deployment of BentoML models to Kubernetes, including [building model container images](https://docs.bentoml.org/projects/yatai/en/latest/concepts/bentorequest_crd.html).
      - [__Web UI__](https://docs.bentoml.org/en/latest/concepts/deploy.html#deploy-via-web-ui): A graphical web interface for viewing, deploying, and monitoring models.
      - [__REST APIs__](https://docs.bentoml.org/en/latest/concepts/deploy.html#deploy-via-api): A REST API for viewing, deploying, and monitoring models.
      - [__Kubernetes CRDs__](https://docs.bentoml.org/en/latest/concepts/deploy.html#deploy-via-api): Manage the deployment of models in a DevOps-friendly way.
    footnote: ""

  - name: DataHub
    purpose: Data Catalog
    maintainer: Acryl Data
    docs_url: https://datahubproject.io/docs/
    github_repo: datahub-project/datahub
    deploykf_priority: 3
    introduction: |
      [__DataHub__](https://datahubproject.io/) is an open-source metadata platform for discovering, managing, and understanding data.
    description: |
      The core features of DataHub are:
      
      - [__Support for Many Data Sources__](https://datahubproject.io/docs/metadata-ingestion/): DataHub supports ingestion of metadata from many sources.
      - [__Search & Discovery__](https://datahubproject.io/docs/how/search/): DataHub provides a search interface for discovering data.
      - [__Data Lineage__](https://datahubproject.io/docs/lineage/lineage-feature-guide/): DataHub can capture and visualize complex data lineage.
    footnote: ""

  - name: Airbyte
    purpose: Data Integration
    maintainer: Airbyte
    docs_url: https://docs.airbyte.com/
    github_repo: airbytehq/airbyte
    deploykf_priority: 3
    introduction: |
      [__Airbyte__](https://airbyte.com/) is a data integration platform which aims to make it easy to move data from any source to any destination.
    description: |
      The core features of Airbyte are:
      
      - [__Comprehensive Connector Catalog__](https://docs.airbyte.com/integrations/): Airbyte has an extremely large catalog of connectors for data sources and destinations.
      - [__Airbyte Web UI__](https://demo.airbyte.io/): Airbyte provides a graphical web interface for managing data connectors and orchestrating data syncs.
    footnote: ""

  - name: Label Studio
    purpose: Data Labeling
    maintainer: Heartex
    docs_url: https://labelstud.io/guide/
    github_repo: heartexlabs/label-studio
    deploykf_priority: 3
    introduction: |
      [__Label Studio__](https://labelstud.io/) is an open-source data labeling platform which supports a variety of data types and labeling tasks.
    description: |
      The core features of Label Studio are:
      
      - [__Data Types__](https://labelstud.io/guide/tasks.html#Types-of-data-you-can-import-into-Label-Studio): Label Studio supports a variety of data types, including text, images, audio, video, and time series.
      - [__Task Templates__](https://labelstud.io/templates): Label Studio provides many templates for common labeling tasks, including text classification, named entity recognition, and object detection.
      - [__Label Studio Web UI__](https://labelstud.io/guide/get_started.html#Terminology): Label Studio provides a graphical web interface for labeling data and managing labeling projects.
    footnote: ""
---

# Future Tools

A list of __ML & Data tools__ which may be part of __future__ versions of deployKF.

---

## Tool Roadmap

The following is a roadmap of planned tools, __grouped by priority__.

!!! question_secondary "How do I request or contribute a tool?"
    
    If you would like to __request__ or __contribute__ support for a tool, please [raise an issue on GitHub](https://github.com/deployKF/deployKF/issues), or join the discussion on an existing issue.

{{ render_planned_tools_index(tools_planned) }}

## Tool Details

The following sections provide details and descriptions for each tool.

{{ render_planned_tools_details(tools_planned) }}