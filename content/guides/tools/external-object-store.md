---
description: >-
  Learn how to use external S3-like object stores with Kubeflow Pipelines in deployKF.
---

# Connect an external Object Store

Learn how to use __external S3-like object stores__ with __Kubeflow Pipelines__ in deployKF.

---

## Introduction

deployKF includes an embedded [MinIO](https://min.io/) instance. 
However, you will likely want to replace this with an external S3-like object store for production usage.

!!! danger "Embedded MinIO is NOT for Production"

    Currently, the [embedded MinIO](https://github.com/deployKF/deployKF/tree/v0.1.3/generator/templates/manifests/deploykf-opt/deploykf-minio) is only intended for development and testing purposes as it only supports a single replica.
    In future, we may add support for a multi-replica MinIO deployment, but for now you should always use an external S3-like object store for production usage.

!!! warning "MinIO License"

    If you choose to use the embedded MinIO, please ensure you are familiar with MinIO's licence.
    At the time of writing it was [AGPLv3](https://github.com/minio/minio/blob/master/LICENSE).
    However, rest assured that deployKF itself __does NOT contain any code from MinIO__, and is licensed under the [Apache 2.0 License](https://github.com/deployKF/deployKF/blob/main/LICENSE).

## 1. Disable Embedded MinIO

The [`deploykf_opt.deploykf_minio.enabled`](https://github.com/deployKF/deployKF/blob/v0.1.1/generator/default_values.yaml#L853) value controls if the embedded MinIO instance is deployed.

For example, to disable MinIO, set the following value:

```yaml
deploykf_opt:
  deploykf_minio:
    enabled: false
```

## 2. Create Buckets

You must manually create the buckets that Kubeflow Pipelines will use.
Please refer to the documentation for your object store for instructions on how to create buckets.
For example, if you are using S3 you may use the [AWS Console](https://docs.aws.amazon.com/AmazonS3/latest/userguide/creating-bucket.html) or the [AWS CLI](https://docs.aws.amazon.com/cli/latest/reference/s3api/create-bucket.html).

Here are some object stores which can be used with Kubeflow Pipelines:

Platform | Object Store | XML API Endpoint
--- | --- | ---
Amazon Web Services | [Amazon S3](https://aws.amazon.com/s3/) | `s3.amazonaws.com`
Google Cloud | [Google Cloud Storage](https://cloud.google.com/storage) | [`storage.googleapis.com`](https://cloud.google.com/storage/docs/xml-api/overview)
Microsoft Azure | [Azure Blob Storage](https://azure.microsoft.com/en-us/services/storage/blobs/) | No first-party S3 API, but translation layers like [S3Proxy](https://github.com/gaul/s3proxy) can be used.
Alibaba Cloud | [Alibaba Cloud Object Storage Service (OSS)](https://www.alibabacloud.com/product/oss) | [`s3.oss-{region}.aliyuncs.com`](https://www.alibabacloud.com/help/en/oss/developer-reference/use-amazon-s3-sdks-to-access-oss)
IBM Cloud | [IBM Cloud Object Storage](https://www.ibm.com/cloud/object-storage) | [`	s3.{region}.cloud-object-storage.appdomain.cloud`](https://cloud.ibm.com/docs/cloud-object-storage?topic=cloud-object-storage-endpoints)
Other | [MinIO](https://min.io/), [Ceph](https://ceph.io/), [Wasabi](https://wasabi.com/) | See provider documentation.

!!! warning "S3-compatible APIs Only"

    Currently, Kubeflow Pipelines only supports object stores which have an S3-compatible XML API.
    This means that while you can use services like [Google Cloud Storage](https://cloud.google.com/storage), you will need to use their [XML API](https://cloud.google.com/storage/docs/xml-api/overview), and features like [GKE Workload Identity](https://cloud.google.com/kubernetes-engine/docs/how-to/workload-identity) will NOT work.

    If you would like Kubeflow Pipelines to implement support for the native APIs of your object store, please raise this with the upstream Kubeflow Pipelines community.

!!! info "Object Prefixes"

    The following table shows bucket prefixes used by Kubeflow Pipelines:
    
    Object Prefix | Purpose | Config Value
    --- | --- | ---
    `/pipelines` | pipeline definitions | (can not be changed)
    `/artifacts/{profile_name}` | pipeline run artifacts (KFP v1) | [`kubeflow_dependencies.kubeflow_argo_workflows.artifactRepository.keyFormat`](https://github.com/deployKF/deployKF/blob/v0.1.3/generator/default_values.yaml#L1229-L1232)
    `/v2/artifacts/{profile_name}` | pipeline run artifacts (KFP v2) | [`kubeflow_tools.pipelines.kfpV2.defaultPipelineRoot`](https://github.com/deployKF/deployKF/blob/v0.1.3/generator/default_values.yaml#L1786-L1793)

!!! info "Bucket IAM Policies"

    When using the embedded MinIO, we automatically configure prefix-based IAM Policies for each profile.

    This is possible because of the "key format" structure we use for pipeline artifacts, which includes the name of the executing namespace/profile at the start of the key:

    - [`kubeflow_dependencies.kubeflow_argo_workflows.artifactRepository.keyFormat`](https://github.com/deployKF/deployKF/blob/v0.1.1/generator/default_values.yaml#L1179)
    - [`kubeflow_tools.pipelines.kfpV2.defaultPipelineRoot`](https://github.com/deployKF/deployKF/blob/v0.1.1/generator/default_values.yaml#L1740)

    To replicate this in your external object store, you may assign an IAM Policy for each profile that is similar to the ones generated by deployKF.

    The following IAM Policy is used by the Kubeflow Pipelines BACKEND:

    ```json
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Effect": "Allow",
          "Action": [
            "s3:GetBucketLocation",
            "s3:ListBucket"
          ],
          "Resource": [
            "arn:aws:s3:::<BUCKET_NAME>"
          ]
        },
        {
          "Effect": "Allow",
          "Action": [
            "s3:GetObject",
            "s3:PutObject",
            "s3:DeleteObject"
          ],
          "Resource": [
            "arn:aws:s3:::<BUCKET_NAME>/artifacts/*",
            "arn:aws:s3:::<BUCKET_NAME>/pipelines/*",
            "arn:aws:s3:::<BUCKET_NAME>/v2/artifacts/*"
          ]
        }
      ]
    }
    ```

    A version of the following IAM Policy is used by each PROFILE:

    ```json
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Effect": "Allow",
          "Action": [
            "s3:GetBucketLocation",
            "s3:ListBucket"
          ],
          "Resource": [
            "arn:aws:s3:::<BUCKET_NAME>"
          ]
        },
        {
          "Effect": "Allow",
          "Action": [
            "s3:GetObject",
            "s3:PutObject",
            "s3:DeleteObject"
          ],
          "Resource": [
            "arn:aws:s3:::<BUCKET_NAME>/artifacts/<PROFILE_NAME>/*",
            "arn:aws:s3:::<BUCKET_NAME>/v2/artifacts/<PROFILE_NAME>/*"
          ]
        }
      ]
    }
    ```

## 3. Connect Kubeflow Pipelines

### Key-based Authentication

Key-based authentication is the simplest way to connect Kubeflow Pipelines to an external object store.
The following values are needed to configure key-based auth:

Value | Purpose
--- | ---
[`deploykf_core.deploykf_profiles_generator.profileDefaults.tools.kubeflowPipelines.objectStoreAuth`](https://github.com/deployKF/deployKF/blob/v0.1.1/generator/default_values.yaml#L746-L774) | Default bucket authentication used in profiles that do NOT have `tools.kubeflowPipelines.objectStoreAuth` defined in their [`deploykf_core.deploykf_profiles_generator.profiles`](https://github.com/deployKF/deployKF/blob/v0.1.1/generator/default_values.yaml#L800-L839) list entry.
[`kubeflow_tools.pipelines.objectStore`](https://github.com/deployKF/deployKF/blob/v0.1.3/generator/default_values.yaml#L1722-L1757) | Connection details & bucket authentication used by the KFP backend (not profiles).
[`kubeflow_tools.pipelines.bucket`](https://github.com/deployKF/deployKF/blob/v0.1.3/generator/default_values.yaml#L1716-L1720) | Bucket name and region configs.

For example, these values will connect Kubeflow Pipelines to an external object store using __key-based__ authentication:

```yaml
deploykf_core:
  deploykf_profiles_generator:
    
    ## NOTE: you may also define `tools.kubeflowPipelines.objectStoreAuth`
    ##       in a specific profile to override the default auth for that profile
    profileDefaults:
      tools:
        kubeflowPipelines:
          objectStoreAuth:
            ## (OPTION 1):
            ##  - all profiles share the same access key (NOT RECOMMENDED)
            ##  - note, you will need to create the Kubernetes Secret
            ##    named `existingSecret` in `existingSecretNamespace`
            ##  - in this approach, the IAM Policy bound to this access key
            ##    must have access to all KFP artifacts in the bucket
            existingSecret: "my-secret-name"
            existingSecretNamespace: "my-namespace"
            existingSecretAccessKeyKey: "access_key"
            existingSecretSecretKeyKey: "secret_key"
            
            ## (OPTION 2):
            ##  - each profile has its own access key
            ##  - for each profile you need to create a Kubernetes Secret 
            ##    matching `existingSecret` in `existingSecretNamespace`,
            ##  - instances of '{profile_name}' in `existingSecret` 
            ##    are replaced with the profile name
            ##  - the default `existingSecretNamespace` is the kubeflow namespace
            ##  - in this approach, the IAM Policy bound to each access key
            ##    can be restricted to only access KFP artifacts of the profile
            #existingSecret: "kubeflow-pipelines--profile-object-store-auth--{profile_name}"
            #existingSecretNamespace: "my-namespace"
            #existingSecretAccessKeyKey: "access_key"
            #existingSecretSecretKeyKey: "secret_key"

    ## example of a profile which overrides the default auth
    #profiles:
    #  - name: "my-profile"
    #    members: []
    #    tools:
    #      kubeflowPipelines:
    #        objectStoreAuth:
    #          existingSecret: "my-secret-name"
    #          existingSecretNamespace: "" # defaults to the profile's namespace
    #          existingSecretAccessKeyKey: "access_key"
    #          existingSecretSecretKeyKey: "secret_key"

kubeflow_tools:
  pipelines:
    bucket:
      ## this specifies the name of your bucket (and region, if applicable)
      name: kubeflow-pipelines
      region: ""
    
    objectStore:
      useExternal: true
      
      ## this specifies the XML REST endpoint of your object store
      host: s3.amazonaws.com
      port: ""
      useSSL: true

      ## these credentials are used by the KFP backend (not profiles)
      auth:
        ## (OPTION 1):
        ##  - set keys with values (NOT RECOMMENDED)
        #accessKey: my-access-key
        #secretKey: my-secret-key

        ## (OPTION 2):
        ##  - read a kubernetes secret from the 'kubeflow' namespace
        ##  - note, `existingSecret*Key` specifies the KEY NAMES in the 
        ##    secret itself, which contain the secret values
        existingSecret: "my-secret-name"
        existingSecretAccessKeyKey: "AWS_ACCESS_KEY_ID"
        existingSecretSecretKeyKey: "AWS_SECRET_ACCESS_KEY"

    ## NOTE: only required if you are using 'sample-values.yaml' as a base
    ##       as `minioFix` can only be 'true' when using the embedded MinIO
    #kfpV2:
    #  minioFix: false
```

### IRSA-based Authentication

!!! warning "IRSA is only supported on EKS"

    IRSA is only supported when connecting to S3 from an EKS cluster.
    If you are using a different platform, you will need to use [key-based authentication](#key-based-authentication).

If you are using EKS and S3, you may use [IAM roles for service accounts](https://docs.aws.amazon.com/eks/latest/userguide/iam-roles-for-service-accounts.html) (IRSA) to authenticate with your object store.
The following values are needed to configure IRSA-based auth:

Value | Purpose
--- | ---
[`deploykf_core.deploykf_profiles_generator.profileDefaults.plugins`](https://github.com/deployKF/deployKF/blob/v0.1.1/generator/default_values.yaml#L706-L730) | Default profile-plugins, used by profiles which do NOT have `plugins` defined in their [`deploykf_core.deploykf_profiles_generator.profiles`](https://github.com/deployKF/deployKF/blob/v0.1.1/generator/default_values.yaml#L800-L839) list entry.<br><br>Note, the `AwsIamForServiceAccount` plugin is used to configure AWS IRSA-based auth by annotating the `default-editor` and `default-viewer` ServiceAccounts in each profile.
[`kubeflow_dependencies.kubeflow_argo_workflows.controller.serviceAccount`](https://github.com/deployKF/deployKF/blob/v0.1.1/generator/default_values.yaml#L1185-L1190) | Kubernetes ServiceAccount used by the __Argo Workflows Controller__
[`kubeflow_dependencies.kubeflow_argo_workflows.server.serviceAccount`](https://github.com/deployKF/deployKF/blob/v0.1.1/generator/default_values.yaml#L1196-L1201) | Kubernetes ServiceAccount used by the __Argo Server UI__
[`kubeflow_tools.pipelines.serviceAccounts.apiServer`](https://github.com/deployKF/deployKF/blob/v0.1.1/generator/default_values.yaml#L1651-L1655) | Kubernetes ServiceAccount used by the __Kubeflow Pipelines API Server__
[`kubeflow_tools.pipelines.serviceAccounts.frontend`](https://github.com/deployKF/deployKF/blob/v0.1.1/generator/default_values.yaml#L1657-L1661) | Kubernetes ServiceAccount used by the __Kubeflow Pipelines Frontend__
[`kubeflow_tools.pipelines.objectStore.auth.fromEnv`](https://github.com/deployKF/deployKF/blob/v0.1.1/generator/default_values.yaml#L1699) | If `true`, disables all other auth methods, so the [AWS Credential Provider Chain](https://docs.aws.amazon.com/sdkref/latest/guide/standardized-credentials.html#credentialProviderChain) will try to use IRSA-based auth.

For example, these values will connect Kubeflow Pipelines to an external object store using __IRSA-based__ authentication:

```yaml
deploykf_core:
  deploykf_profiles_generator:
    
    ## NOTE: if you want to have a different set of plugins for each profile,
    ##       for example, to have some profiles use a different IAM role,
    ##       you can define the `plugins` list explicitly in a profile 
    ##       to override the default plugins
    profileDefaults:
      plugins:
        - kind: AwsIamForServiceAccount
          spec:
            awsIamRole: "arn:aws:iam::MY_ACCOUNT_ID:role/MY_ROLE_NAME"
            AnnotateOnly: true
    
    ## example of a profile which overrides the default plugins
    #profiles:
    #  - name: "my-profile"
    #    members: []
    #    plugins:
    #      - kind: AwsIamForServiceAccount
    #        spec:
    #          awsIamRole: "arn:aws:iam::MY_ACCOUNT_ID:role/MY_ROLE_NAME"
    #          AnnotateOnly: true

kubeflow_dependencies:
  kubeflow_argo_workflows:
    controller:
      serviceAccount:
        annotations:
          eks.amazonaws.com/role-arn: "arn:aws:iam::MY_ACCOUNT_ID:role/MY_ROLE_NAME"
    server:
      serviceAccount:
        annotations:
          eks.amazonaws.com/role-arn: "arn:aws:iam::MY_ACCOUNT_ID:role/MY_ROLE_NAME"

kubeflow_tools:
  pipelines:
    serviceAccounts:
      apiServer:
        annotations:
          eks.amazonaws.com/role-arn: "arn:aws:iam::MY_ACCOUNT_ID:role/MY_ROLE_NAME"
      frontend:
        annotations:
          eks.amazonaws.com/role-arn: "arn:aws:iam::MY_ACCOUNT_ID:role/MY_ROLE_NAME"

    bucket:
      name: kubeflow-pipelines
      region: ""

    objectStore:
      useExternal: true
      
      ## for IRSA, this should always be 's3.amazonaws.com'
      host: s3.amazonaws.com
      port: ""
      useSSL: true

      auth:
        ## setting `fromEnv` to `true` disables all other auth methods
        ## so the AWS Credential Provider Chain will try to use IRSA-based auth
        fromEnv: true

    ## NOTE: only required if you are using 'sample-values.yaml' as a base
    ##       as `minioFix` can only be 'true' when using the embedded MinIO
    #kfpV2:
    #  minioFix: false
```
