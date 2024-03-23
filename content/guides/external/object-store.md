---
icon: material/shape
description: >-
  Learn how and why deployKF needs an object store.
  Learn how to use any S3-compatible object store with Kubeflow Pipelines.

# disable the mkdocs-macros-plugin for this page
render_macros: false
---

# Object Store

Learn how and why deployKF needs an object store.
Learn how to use any S3-compatible object store with Kubeflow Pipelines.

---

## __What is an Object Store?__

An [__object store__](https://en.wikipedia.org/wiki/Object_storage) is a type of storage system that manages data as objects, as opposed to traditional file systems which manage data as files.
Each object typically includes the data itself, a variable amount of metadata, and a globally unique identifier.

### __What is an S3-compatible Object Store?__

The most well-known object store is [:custom-s3-color: __Amazon S3__](https://aws.amazon.com/s3/).
Given its popularity, many other object stores have implemented S3-compatible APIs, which allows them to be used with tools that are designed to work with S3.

---

## __Why does deployKF use an Object Store?__

An S3-compatible object store is a dependency of [:custom-kubeflow-color: __Kubeflow Pipelines__](../../reference/tools.md#kubeflow-pipelines), which uses it to store pipeline definitions and artifacts from pipeline runs.

---

## __Connect an External Object Store__

By default, deployKF includes an [embedded MinIO instance](https://github.com/deployKF/deployKF/tree/v0.1.4/generator/templates/manifests/deploykf-opt/deploykf-minio).
However, to improve the performance and reliability of Kubeflow Pipelines, we recommend using an external S3-compatible object store.

!!! danger "Embedded MinIO"

    You should ALWAYS use an external S3-compatible object store.
    The embedded MinIO is only intended for testing purposes as it only supports a single replica, and has no backups.

!!! warning "MinIO License"

    Please ensure you are familiar with MinIO's licence, at the time of writing it was [AGPLv3](https://github.com/minio/minio/blob/master/LICENSE).

    deployKF is licensed under [Apache 2.0](https://github.com/deployKF/deployKF/blob/main/LICENSE) and __does NOT contain any code from MinIO__, instead, we provide links so that you may download MinIO directly from official sources, at your own discretion.

### __1. Prepare Object Store__

You may use any S3-compatible object store, as long as it is accessible from the Kubernetes cluster where deployKF is running.

You may consider using one of the following services.
Note, we have listed the _S3-compatible Endpoint_ for each service.

Platform | Object Store | S3-compatible Endpoint
--- | --- | ---
Amazon Web Services | [Amazon S3](https://aws.amazon.com/s3/) | `s3.amazonaws.com`
Google Cloud | [Google Cloud Storage](https://cloud.google.com/storage) | [`storage.googleapis.com`](https://cloud.google.com/storage/docs/xml-api/overview)<br><small>:material-alert: you must use [HMAC Keys](https://cloud.google.com/storage/docs/authentication/hmackeys) for authentication :material-alert:</small>
Microsoft Azure | [Azure Blob Storage](https://azure.microsoft.com/en-us/services/storage/blobs/) | No first-party API.<br><small>Third-party translation layers like [S3Proxy](https://github.com/gaul/s3proxy) can be used.</small>
Alibaba Cloud | [Alibaba Cloud Object Storage Service (OSS)](https://www.alibabacloud.com/product/oss) | [`s3.oss-{region}.aliyuncs.com`](https://www.alibabacloud.com/help/en/oss/developer-reference/use-amazon-s3-sdks-to-access-oss)
IBM Cloud | [IBM Cloud Object Storage](https://www.ibm.com/cloud/object-storage) | [`	s3.{region}.cloud-object-storage.appdomain.cloud`](https://cloud.ibm.com/docs/cloud-object-storage?topic=cloud-object-storage-endpoints)
Other | [MinIO](https://min.io/), [Ceph](https://ceph.io/), [Wasabi](https://wasabi.com/) | See provider documentation.

!!! warning "S3-compatible APIs Only"

    Currently, Kubeflow Pipelines only supports object stores which have an S3-compatible XML API.
    This means that while you can use services like [Google Cloud Storage](https://cloud.google.com/storage), you will need to use their [XML API](https://cloud.google.com/storage/docs/xml-api/overview), and features like [GKE Workload Identity](https://cloud.google.com/kubernetes-engine/docs/how-to/workload-identity) will NOT work.

    If you would like Kubeflow Pipelines to implement support for the native APIs of your object store, please raise this with the upstream Kubeflow Pipelines community.

### __2. Create Buckets and IAM Policies__

You must create a bucket for Kubeflow Pipelines, and then configure _IAM Policies_ for the bucket and its contents.
Please refer to the documentation for your object store for instructions on how to create buckets and IAM Policies.

For example, if you are using AWS S3, you may use the following methods:

- [Create S3 bucket (AWS Console)](https://docs.aws.amazon.com/AmazonS3/latest/userguide/creating-bucket.html)
- [Create S3 bucket (AWS CLI)](https://docs.aws.amazon.com/cli/latest/reference/s3api/create-bucket.html)
- [Create IAM Policies (AWS Console)](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_create-console.html)
- [Create IAM Policies (AWS CLI)](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_create-cli.html)

#### __Bucket IAM Policies__

When using the embedded MinIO, deployKF will automatically generate IAM Policies for each profile, and for the KFP backend.
You may use them as a reference when creating IAM Policies for your external object store.

All Kubeflow Pipelines artifacts are stored in the same bucket, but are separated by _object key prefixes_.
The following table shows the prefixes used by Kubeflow Pipelines:

Key Prefix | Purpose | Config Value
--- | --- | ---
`/pipelines/` | pipeline definitions | (can not be changed)
`/artifacts/{profile_name}/` | pipeline run artifacts (KFP v1) | [`kubeflow_dependencies.kubeflow_argo_workflows.artifactRepository.keyFormat`](https://github.com/deployKF/deployKF/blob/v0.1.3/generator/default_values.yaml#L1229-L1232)
`/v2/artifacts/{profile_name}/` | pipeline run artifacts (KFP v2) | [`kubeflow_tools.pipelines.kfpV2.defaultPipelineRoot`](https://github.com/deployKF/deployKF/blob/v0.1.3/generator/default_values.yaml#L1786-L1793)

!!! tip "Key Format"

    Notice that the key format includes `{profile_name}` at the START of the key,
    this is so that prefix-based IAM Policies can ensure each profile only has access to its own artifacts.

The Kubeflow Pipelines backend will need access to all artifacts, while each profile will only need access to its own artifacts.

!!! code "IAM Policy - Backend"

    The following IAM Policy can be used by the __Kubeflow Pipelines BACKEND__, replace `<BUCKET_NAME>` with the name of your bucket.

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

!!! code "IAM Policy - Profile"

    The following IAM Policy can be used by __each PROFILE namespace__, replace `<BUCKET_NAME>` with the name of your bucket, and `<PROFILE_NAME>` with the name of the profile.

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

### __3. Disable Embedded MinIO__

The [`deploykf_opt.deploykf_minio.enabled`](https://github.com/deployKF/deployKF/blob/v0.1.4/generator/default_values.yaml#L1022) value controls if the embedded MinIO instance is deployed.

The following values will disable the embedded MinIO instance:

```yaml
deploykf_opt:
  deploykf_minio:
    enabled: false
```

### __4. Connect Kubeflow Pipelines__

How you connect Kubeflow Pipelines to your external object store depends on the _authentication method_ you want to use.
There are two authentication methods available:

Method | Description
--- | ---
Key-Based Authentication | use access tokens to authenticate with your object store
IRSA-Based Authentication | use [IRSA](https://docs.aws.amazon.com/eks/latest/userguide/iam-roles-for-service-accounts.html) to authenticate with S3 (only supported for EKS + S3)

The following sections will show you how to configure each method.

=== ":star: Key-Based Authentication :star:"
    
    Key-based authentication is the simplest, clients will use _HMAC Keys_ (that is, an `access_key` and `secret_key`) to authenticate with your object store.
    
    First, create a secret for the Kubeflow Pipelines backend:
    
    ```bash
    ## create a secret for the KFP backend
    kubectl create secret generic \
      "kubeflow-pipelines--backend-object-store-auth" \
      --namespace "kubeflow" \
      --from-literal AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE \
      --from-literal AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
    ```

    !!! info

        - The backend secret MUST be in the `kubeflow` namespace, as this is where the KFP backend is deployed.
        - The backend secret should have access to all KFP artifacts in the bucket.
        - See the [Example IAM Policies](#bucket-iam-policies).

    Next, create a secret for each profile that will use Kubeflow Pipelines:
    
    ```bash
    ## create a secret for the "team-1" profile
    kubectl create secret generic \
      "kubeflow-pipelines--profile-object-store-auth--team-1" \
      --namespace "my-namespace" \
      --from-literal AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE \
      --from-literal AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY

    ## create a secret for the "team-2" profile
    kubectl create secret generic \
      "kubeflow-pipelines--profile-object-store-auth--team-2" \
      --namespace "my-namespace" \
      --from-literal AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE \
      --from-literal AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
    ```

    !!! info
      
        - The profile secrets can be in __any namespace__, deployKF will automatically clone the correct secret into the profile namespace and configure KFP to use it.
        - It is common to store all the profile secrets in a single namespace, as this makes them easier to manage.
        - Each profile secret should only have the minimum permissions required for that profile.
        - See the [Example IAM Policies](#bucket-iam-policies).

    The following values configure key-based authentication:
    
    Value | Purpose
    --- | ---
    [`deploykf_core.deploykf_profiles_generator.profileDefaults.tools.kubeflowPipelines.objectStoreAuth`](https://github.com/deployKF/deployKF/blob/v0.1.1/generator/default_values.yaml#L746-L774) | Default bucket authentication used in profiles that do NOT have `tools.kubeflowPipelines.objectStoreAuth` defined in their [`deploykf_core.deploykf_profiles_generator.profiles`](https://github.com/deployKF/deployKF/blob/v0.1.1/generator/default_values.yaml#L800-L839) list entry.
    [`kubeflow_tools.pipelines.objectStore`](https://github.com/deployKF/deployKF/blob/v0.1.3/generator/default_values.yaml#L1722-L1757) | Connection details & bucket authentication used by the KFP backend (not profiles).
    [`kubeflow_tools.pipelines.bucket`](https://github.com/deployKF/deployKF/blob/v0.1.3/generator/default_values.yaml#L1716-L1720) | Bucket name and region configs.
    
    The following values will connect Kubeflow Pipelines to an external object store using __key-based__ authentication:
    
    ```yaml
    deploykf_core:
      deploykf_profiles_generator:
        
        ## NOTE: each profile can override the defaults 
        ##       see under `profiles` for an example of a profile 
        ##       which overrides the default auth pattern
        ##
        profileDefaults:
          tools:
            kubeflowPipelines:
              objectStoreAuth:
                ## (OPTION 1):
                ##  - all profiles share the same access key (NOT RECOMMENDED)
                ##  - the `existingSecretAccessKeyKey` and `existingSecretSecretKeyKey`
                ##    reference the KEY NAMES in the Kubernetes Secret you create
                ##
                #existingSecret: "my-secret-name"
                #existingSecretNamespace: "my-namespace"
                #existingSecretAccessKeyKey: "AWS_ACCESS_KEY_ID"
                #existingSecretSecretKeyKey: "AWS_SECRET_ACCESS_KEY"
                
                ## (OPTION 2):
                ##  - each profile has its own access key
                ##  - instances of '{profile_name}' in `existingSecret` 
                ##    are replaced with the profile name
                ##  - the `existingSecretAccessKeyKey` and `existingSecretSecretKeyKey`
                ##    reference the KEY NAMES in the Kubernetes Secret you create
                ##
                existingSecret: "kubeflow-pipelines--profile-object-store-auth--{profile_name}"
                existingSecretNamespace: "my-namespace"
                existingSecretAccessKeyKey: "AWS_ACCESS_KEY_ID"
                existingSecretSecretKeyKey: "AWS_SECRET_ACCESS_KEY"
    
        ## example of a profile which overrides the default auth
        #profiles:
        #  - name: "my-profile"
        #    members: []
        #    tools:
        #      kubeflowPipelines:
        #        objectStoreAuth:
        #          existingSecret: "my-secret-name"
        #          existingSecretNamespace: "" # defaults to the profile's namespace
        #          existingSecretAccessKeyKey: "AWS_ACCESS_KEY_ID"
        #          existingSecretSecretKeyKey: "AWS_SECRET_ACCESS_KEY"
    
    kubeflow_tools:
      pipelines:
        bucket:
          ## this specifies the name of your bucket (and region, if applicable)
          name: kubeflow-pipelines
          region: ""
        
        objectStore:
          useExternal: true
          
          ## this specifies the S3-compatible endpoint of your object store
          host: s3.amazonaws.com
          port: ""
          useSSL: true
    
          ## these credentials are used by the KFP backend (not profiles)
          auth:
            ## (OPTION 1):
            ##  - set keys with values (NOT RECOMMENDED)
            #accessKey: "AKIAIOSFODNN7EXAMPLE"
            #secretKey: "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
    
            ## (OPTION 2):
            ##  - read a kubernetes secret from the 'kubeflow' namespace
            ##  - note, `existingSecretKey` specifies the KEY NAMES in the 
            ##    secret itself, which contain the secret values
            existingSecret: "kubeflow-pipelines--backend-object-store-auth"
            existingSecretAccessKeyKey: "AWS_ACCESS_KEY_ID"
            existingSecretSecretKeyKey: "AWS_SECRET_ACCESS_KEY"
    
        ## NOTE: only required if you are using 'sample-values.yaml' as a base
        ##       as `minioFix` can only be 'true' when using the embedded MinIO
        #kfpV2:
        #  minioFix: false
    ```

=== "IRSA-Based Authentication"
    
    !!! warning "IRSA is only supported on EKS"
    
        IRSA is only supported when connecting to S3 from an EKS cluster.
        If you are using a different platform, you will need to use __key-based authentication__.
    
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
    
    The following values will connect Kubeflow Pipelines to an external object store using __IRSA-based__ authentication:
    
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
