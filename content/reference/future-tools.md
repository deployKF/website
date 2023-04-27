---
## Tools planned for future deployKF versions
tools_planned:
  - name: MLflow Model Registry
    purpose: Model Registry
    owner: Databricks
    docs_url: https://www.mlflow.org/docs/latest/model-registry.html
    github_repo: mlflow/mlflow
    deploykf_priority: 1
    description: |
      MLflow Model Registry is an open source machine learning model registry.
      
      A model registry decouples __model training__ from __model deployment__, allowing you to break the model lifecycle down into three __separate concerns__.
      
      1. Model Training: Training new versions of models and logging them into the registry.
      2. Model Evaluation: Evaluating versions of models and logging the results into the registry.
      3. Model Deployment: Making informed decisions about which models to deploy and then deploying them.

      This separation enables you to have well-scoped pipelines, rather than trying to go from training to deployment all at once.

      The key features of MLflow Model Registry are:
      
      - [Model Versioning](https://mlflow.org/docs/latest/model-registry.html#adding-an-mlflow-model-to-the-model-registry): Version your model artifacts and attach metadata to each version.
      - [Model Stage Transitions](https://mlflow.org/docs/latest/model-registry.html#transitioning-an-mlflow-models-stage): Transition models between stages (e.g. staging to production).
      - [Web UI](https://www.mlflow.org/docs/latest/model-registry.html#ui-workflow): A graphical web interface for managing models.
      - [Python API](https://www.mlflow.org/docs/latest/model-registry.html#api-workflow): A Python API for managing models.
      - [REST API](https://www.mlflow.org/docs/latest/rest-api.html): A REST API for managing models.  

  - name: Apache Airflow
    purpose: Workflow Orchestration
    owner: Apache Software Foundation
    docs_url: https://airflow.apache.org/docs/
    github_repo: apache/airflow
    deploykf_priority: 1
    description: |
      Apache Airflow is by far [the most popular](https://github.com/apache/airflow/blob/main/INTHEWILD.md) open-source workflow orchestration tool in the world.
      
      The versatility and extensibility of Apache Airflow make it a great fit for many different use cases, including machine learning.
      
      The key features of Apache Airflow are:      

      - Python Centered: Airflow is written in Python and uses a [Python DSL to define workflows](https://airflow.apache.org/docs/apache-airflow/stable/index.html#what-is-airflow).
      - Dynamic Workflows: Airflow's code-driven workflow definitions enable powerful patterns like [dynamically generating workflows](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dags.html#dynamic-dags).
      - Extensive Plugins: Airflow has a rich ecosystem of [plugins and integrations with other tools](https://airflow.apache.org/docs/).
      - User Interface: Airflow is known for its [powerful user interface](https://airflow.apache.org/docs/apache-airflow/stable/ui.html) which allows users to monitor and manage workflows.
  
  - name: Feast
    purpose: Feature Store
    owner: Tecton
    docs_url: https://docs.feast.dev/
    github_repo: feast-dev/feast
    deploykf_priority: 2
    description: |
      Feast is an open-source feature store for machine learning.
      
      A good way to understand the purpose of a feature store is to think about the __data access patterns__ encountered during the model lifecycle.
      
      - Feature Engineering: Accesses and transforms historical data to create features.
      - Target Engineering: Accesses and transforms historical data to create targets.
      - Model Training: Accesses features and targets to train and evaluate the model.
      - Model Inference: Accesses features of new data to predict the target.

      A feature store should somehow make these data access patterns easier.
      
      The key features of Feast are:
      
      - [Feature Registry](https://docs.feast.dev/getting-started/architecture-and-components/registry): Where Feast persists __feature definitions__ (not data) that are registered with with it (e.g. Local-Files, S3, GCS).
      - [Python SDK](https://rtd.feast.dev/en/master/): The primary interface for managing __feature definitions__, and retrieving __feature values__ from Feast.
      - [Offline Data Stores](https://docs.feast.dev/reference/offline-stores): A store which Feast can read __feature values__ from, for historical data retrieval (e.g. Snowflake, BigQuery, Redshift).
      - [Online Data Stores](https://docs.feast.dev/reference/online-stores): A store which Feast can materialize (write) __feature values__ into, for online model inference (e.g. Snowflake, Redis, DynamoDB, Bigtable).
      - [Batch Materialization Engine](https://docs.feast.dev/reference/batch-materialization): A data processing engine which Feast can use to materialize __feature values__ from an __Offline Store__ into an __Online Store__ (e.g. Snowflake, Spark, Bytewax).

      !!! tip
      
          A good feature store is __NOT a database__, but rather a __data access layer__ between your data sources and your ML models.
          Be very wary of feature stores that require you to load your data into them.

  - name: BentoML Yatai
    purpose: Model Registry & Serving
    owner: BentoML
    docs_url: https://docs.bentoml.org/projects/yatai/en/latest/index.html
    github_repo: bentoml/Yatai
    deploykf_priority: 2
    description: |
      BentoML Yatai is a platform for managing the lifecycle of BentoML models on Kubernetes.
      
      The core features of BentoML Yatai are:
      
      - [Model Registry](https://docs.bentoml.org/en/latest/concepts/model.html#push-and-pull-with-yatai): A central registry for [packaged Bentos](https://docs.bentoml.org/en/latest/concepts/bento.html).
      - [Model Deployment](https://docs.bentoml.org/en/latest/concepts/deploy.html#deploy-with-yatai): Managing the deployment of BentoML models to Kubernetes, including [building model container images](https://docs.bentoml.org/projects/yatai/en/latest/concepts/bentorequest_crd.html).
      - [Web UI](https://docs.bentoml.org/en/latest/concepts/deploy.html#deploy-via-web-ui): A graphical web interface for viewing, deploying, and monitoring models.
      - [REST APIs](https://docs.bentoml.org/en/latest/concepts/deploy.html#deploy-via-api): A REST API for viewing, deploying, and monitoring models.
      - [Kubernetes CRDs](https://docs.bentoml.org/en/latest/concepts/deploy.html#deploy-via-api): Manage the deployment of models in a DevOps-friendly way.

  - name: KServe
    purpose: Model Serving
    owner: LF AI & Data
    docs_url: https://kserve.github.io/website/
    github_repo: kserve/kserve
    deploykf_priority: 2
    description: |
      KServe provides comprehensive interfaces for deploying, managing, and monitoring ML models on Kubernetes.
      
      The core features of KServe are:
      
      - [Support for Many Frameworks](https://kserve.github.io/website/0.10/modelserving/v1beta1/serving_runtime/): KServe natively supports many ML frameworks (e.g. PyTorch, TensorFlow, scikit-learn, XGBoost).
      - [Autoscaling, Even to Zero](https://kserve.github.io/website/0.10/modelserving/autoscaling/autoscaling/): KServe can autoscale model replicas to meet demand, even scaling to zero when there are no requests.
      - [Model Monitoring](https://kserve.github.io/website/0.10/modelserving/detect/alibi_detect/alibi_detect/): KServe integrates tools like [Alibi Detect](https://github.com/SeldonIO/alibi-detect) to provide model monitoring for drift and outlier detection.
      - [Model Explainability](https://kserve.github.io/website/0.10/modelserving/explainer/explainer/): KServe integrates tools like [Alibi Explain](https://github.com/SeldonIO/alibi) to provide model explainability.
      - [Request Batching](https://kserve.github.io/website/0.10/modelserving/batcher/batcher/): KServe can batch requests to your model, improving throughput and reducing cost.
      - [Canary Deployments](https://kserve.github.io/website/0.10/modelserving/v1beta1/rollout/canary/): KServe can deploy new versions of your model alongside old versions, and route requests to the new version based on a percentage.
      - [Feature Transformers](https://kserve.github.io/website/0.10/modelserving/v1beta1/transformer/feast/): KServe can do feature pre/post processing alongside model inference (e.g. using Feast).
      - [Inference Graphs](https://kserve.github.io/website/0.10/modelserving/inference_graph/): KServe can chain multiple models together to form an inference graph.

  - name: Seldon Core
    purpose: Model Serving
    owner: Seldon
    docs_url: https://docs.seldon.io/projects/seldon-core/en/latest/
    github_repo: SeldonIO/seldon-core
    deploykf_priority: 2
    description: |
      Seldon Core provides interfaces for converting ML models into REST/gRPC microservices on Kubernetes.
      
      The core features of Seldon Core are:
      
      - [Support for Many Frameworks](https://docs.seldon.io/projects/seldon-core/en/latest/servers/overview.html): Seldon Core natively supports many ML frameworks (e.g. TensorFlow, scikit-learn, XGBoost, HuggingFace, NVIDIA Triton).
      - [Reusable Model Servers](https://docs.seldon.io/projects/seldon-core/en/latest/workflow/overview.html#two-types-of-model-servers): Seldon Core removes the need to build a container image for each model, by providing a system to download model artifacts at runtime.
      - [Model Deployment CRD](https://docs.seldon.io/projects/seldon-core/en/latest/workflow/overview.html#seldon-deployment-crd) Seldon Core provides a simple, yet powerful, Kubernetes CRD for deploying models.

  - name: DataHub
    purpose: Data Catalog
    owner: Acryl Data
    docs_url: https://datahubproject.io/docs/
    github_repo: datahub-project/datahub
    deploykf_priority: 3
    description: |
      DataHub is an open-source metadata platform for discovering, managing, and understanding data.
      
      The core features of DataHub are:
      
      - [Support for Many Data Sources](https://datahubproject.io/docs/metadata-ingestion/): DataHub supports ingestion of metadata from many sources.
      - [Search & Discovery](https://datahubproject.io/docs/how/search/): DataHub provides a search interface for discovering data.
      - [Data Lineage](https://datahubproject.io/docs/lineage/lineage-feature-guide/): DataHub can capture and visualize complex data lineage.

  - name: Airbyte
    purpose: Data Integration Platform
    owner: Airbyte
    docs_url: https://docs.airbyte.com/
    github_repo: airbytehq/airbyte
    deploykf_priority: 3
    description: |
      Airbyte is a data integration platform which aims to make it easy to move data from any source to any destination.
      
      The core features of Airbyte are:
      
      - [Comprehensive Connector Catalog](https://docs.airbyte.com/integrations/): Airbyte has an extremely large catalog of connectors for data sources and destinations.
      - [Airbyte Web UI](https://demo.airbyte.io/): Airbyte provides a graphical web interface for managing data connectors and orchestrating data syncs.

  - name: Label Studio
    purpose: Data Labeling
    owner: Heartex
    docs_url: https://labelstud.io/guide/
    github_repo: heartexlabs/label-studio
    deploykf_priority: 3
    description: |
      Label Studio is an open-source data labeling platform which supports a variety of data types and labeling tasks.
      
      The core features of Label Studio are:
      
      - [Data Types](https://labelstud.io/guide/tasks.html#Types-of-data-you-can-import-into-Label-Studio): Label Studio supports a variety of data types, including text, images, audio, video, and time series.
      - [Task Templates](https://labelstud.io/templates): Label Studio provides many templates for common labeling tasks, including text classification, named entity recognition, and object detection.
      - [Label Studio Web UI](https://labelstud.io/guide/get_started.html#Terminology): Label Studio provides a graphical web interface for labeling data and managing labeling projects.

---

# Future Tools

This page lists the ML & Data tools which are __planned__ for future versions of __deployKF__.

!!! tip "Request or Contribute"
    
    If you would like to __request__ or __contribute__ support for a tool, please [raise an issue on GitHub](https://github.com/deployKF/deployKF/issues), or join the discussion on an existing issue.

## Index

{{ render_planned_tools_index(tools_planned) }}

{{ render_planned_tools_details(tools_planned) }}