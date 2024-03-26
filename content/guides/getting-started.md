---
icon: material/rocket-launch
description: >-
  Learn how to use deployKF in production.
  Easily deploy Kubeflow and other MLOps tools as a complete platform!
---

# Getting Started

Learn how to use <strong><span class="deploykf-orange">deploy</span><span class="deploykf-blue">KF</span></strong> in __production__.
<br>Easily deploy the [best of Kubeflow](../reference/tools.md#kubeflow-ecosystem) and other MLOps tools as a complete platform!

---

## Introduction

This page is about __production-ready__ usage of deployKF.
We will cover the requirements, deployment, and configuration of your machine learning platform.

We suggest new users start with the __About deployKF__ and __Local Quickstart__ pages:

[About deployKF<br><small>(Introduction)</small>](../about/introduction.md#about-deploykf){ .md-button .md-button--secondary }
[Local Quickstart<br><small>(Try Locally)</small>](./local-quickstart.md){ .md-button .md-button--secondary }

For existing Kubeflow users, we have a _migration guide_:

[Migrate from :custom-kubeflow: Kubeflow Distributions](./kubeflow-distributions.md#about-migrating){ .md-button .md-button--secondary }

!!! value ""

    We encourage you to _join our community_ and learn about _support options_!
    
    [:material-account-group: Join the Community](../about/community.md){ .md-button .md-button--secondary }
    [:material-headset: Get Support](../about/support.md){ .md-button .md-button--secondary }

---

## 1. Requirements

### __Kubernetes Cluster__

deployKF can run on any [:custom-kubernetes-color: __Kubernetes__](https://kubernetes.io/) cluster, in __any cloud or environment__.
See the [__version matrix__](../releases/version-matrix.md#deploykf-dependencies) for a list of supported Kubernetes versions.

Here are some Kubernetes distributions which are supported by deployKF:

Target Platform | Kubernetes Distribution
--- | ---
Amazon Web Services | [Amazon Elastic Kubernetes Service (EKS)](https://aws.amazon.com/eks/)
Microsoft Azure | [Azure Kubernetes Service (AKS)](https://azure.microsoft.com/en-us/products/kubernetes-service/)<br><small>:material-alert: [see special requirements](https://github.com/deployKF/deployKF/issues/61#issuecomment-1949658332) :material-alert:</small> 
Google Cloud | [Google Kubernetes Engine (GKE)](https://cloud.google.com/kubernetes-engine)
IBM Cloud | [IBM Cloud Kubernetes Service (IKS)](https://www.ibm.com/cloud/kubernetes-service)
Self-Hosted | [Rancher (RKE)](https://ranchermanager.docs.rancher.com/) // [kOps](https://kops.sigs.k8s.io/) // [Kubespray](https://kubespray.io/) // [kubeadm](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/)
Edge | [k3s](https://k3s.io/) // [k0s](https://k0sproject.io/) // [MicroK8s](https://microk8s.io/)
Local Machine | [k3d](https://k3d.io/) // [Kind](https://kind.sigs.k8s.io/) // [Minikube](https://minikube.sigs.k8s.io/) 

!!! warning "Dedicated Cluster"

    We strongly recommend using a __dedicated cluster__ for deployKF.
    This is because deployKF has a number of cluster-level dependencies which may conflict with other applications.

    <small>If you are unable to create a new Kubernetes cluster, you may consider using [vCluster](https://github.com/loft-sh/vcluster) to create a virtual Kubernetes cluster within an existing one.</small>

### __Kubernetes Configurations__

deployKF requires some specific Kubernetes configurations to work correctly.

The following table lists these configurations and their requirements:

Configuration | Requirement
--- | ---
Node Resources | Your nodes must collectively have at least `4 vCPUs` and `16 GB RAM`.
CPU Architecture | The cluster must have `x86_64` Nodes.
Cluster Domain | The [`clusterDomain`](https://kubernetes.io/docs/reference/config-api/kubelet-config.v1beta1/#kubelet-config-k8s-io-v1beta1-KubeletConfiguration) of your kubelet must be `"cluster.local"`.
Service Type | By default, the cluster must have a `LoadBalancer` service type.<br><small>:material-alert: be careful not to expose your platform on the public internet by mistake :material-alert: </small>
Default StorageClass | The default [`StorageClass`](https://kubernetes.io/docs/concepts/storage/storage-classes/) must support the `ReadWriteOnce` access mode.
Existing Argo Workflows | The cluster __must NOT__ already have [Argo Workflows](https://github.com/argoproj/argo-workflows) installed.<br><small>See [`deployKF/deployKF#116`](https://github.com/deployKF/deployKF/issues/116) to join the discussion.</small>

??? question_secondary "What about ARM Nodes?"

    The next minor version of deployKF (`v0.2.0`) should have native `ARM64` for all core components.
    However, some upstream apps like _Kubeflow Pipelines_ will need extra work to be production ready ([`#10309`](https://github.com/kubeflow/pipelines/issues/10309), [`#10308`](https://github.com/kubeflow/pipelines/issues/10308)).

??? question_secondary "Can I use a different Service Type?"

    For real-world usage, you should review the [Expose Gateway and configure HTTPS](./platform/deploykf-gateway.md) guide.

    To use a different service type, you can override the `deploykf_core.deploykf_istio_gateway.gatewayService.type` value:

    ```yaml
    deploykf_core:
      deploykf_istio_gateway:
        gatewayService:
          type: "NodePort" # or "ClusterIP"
    ```

??? question_secondary "What if I don't have a default StorageClass?"

    If you do NOT have a compatible default StorageClass, you might consider the following options:

    1. Configure [a default StorageClass](https://kubernetes.io/docs/tasks/administer-cluster/change-default-storage-class/) that has `ReadWriteOnce` support
    2. Explicitly set the `storageClass` value for the following components:
         - [`deploykf_opt.deploykf_minio.persistence.storageClass`](https://github.com/deployKF/deployKF/blob/v0.1.1/generator/default_values.yaml#L901-L905)
         - [`deploykf_opt.deploykf_mysql.persistence.storageClass`](https://github.com/deployKF/deployKF/blob/v0.1.1/generator/default_values.yaml#L1036-L1040)
    2. Disable components which require the StorageClass, and use external alternatives:
         - [Connect an External S3-compatible Object Store](./external/object-store.md#connect-an-external-object-store)
         - [Connect an External MySQL Database](./external/mysql.md#connect-an-external-mysql)

## 2. Platform Configuration

deployKF is very configurable, you can use it to deploy a wide variety of machine learning platforms and integrate with your existing infrastructure.

### __deployKF Versions__

Each deployKF version may include different [ML & Data tools](../reference/tools.md) or support different versions of cluster dependencies.
See the [version matrix](../releases/version-matrix.md) for an overview, and the [changelog](../releases/changelog-deploykf.md) for detailed information about what changed in each release (including important tips for upgrading).

??? question_secondary "Can I be notified about new releases?"

    Yes. Watch the [`deployKF/deployKF`](https://github.com/deployKF/deployKF) repo on GitHub.
    At the top right, click `Watch` → `Custom` → `Releases` then confirm by selecting `Apply`.

### __About Values__

All aspects of deployKF are configured via a centralized set of YAML-based configs named "values".
Learn more about __creating your own values files__ on the [values](./values.md) page.

[Topic: Values](./values.md){ .md-button .md-button--secondary }

### __Cluster Dependencies__

deployKF has a number of cluster dependencies including __Istio__, __cert-manager__, and __Kyverno__.
To learn about the cluster dependencies, and how to use your existing version (rather than the one which comes with deployKF), see the [cluster dependencies](./cluster-dependencies.md) guide.

[Topic: Cluster Dependencies](./cluster-dependencies.md){ .md-button .md-button--secondary }

### __External Dependencies__

deployKF has a number of external dependencies including __MySQL__ and an __Object Store (like S3)__.
To learn about the cluster dependencies, and how to connect to an external version (rather than the one which comes with deployKF), see the [external dependencies](./external-dependencies.md) guide.

[Topic: External Dependencies](./external-dependencies.md){ .md-button .md-button--secondary }

!!! warning "Embedded Dependencies"

    We strongly recommend NOT using the embedded MySQL and MinIO instances in production.
    See the [Connect an External MySQL](./external/mysql.md#connect-an-external-mysql) and [Connect an External Object Store](./external/object-store.md#connect-an-external-object-store) guides for more information.

### __Modes of Operation__

There are two ways to use deployKF which we call ___"modes of operation"___.
These modes change how the Kubernetes manifests are generated and applied to your cluster.
Learn more on the [modes of operation](./modes.md) page.

[Topic: Modes of Operation](./modes.md){ .md-button .md-button--secondary }

!!! tip "Recommended _Mode of Operation_"

    For most users, we recommend the __ArgoCD Plugin Mode__.

---

## 3. Deploy the Platform

To deploy the platform, you will need to create [ArgoCD `Applications`](./dependencies/argocd.md#argo-cd-applications), and then sync them.

### __:star: Create ArgoCD Applications :star:__

deployKF [uses ArgoCD](./dependencies/argocd.md#how-does-deploykf-use-argo-cd) to manage the deployment of the platform.

The process to create the ArgoCD `Applications` will depend on which [mode of operation](#modes-of-operation) you have chosen.
For most users, we recommend using __ArgoCD Plugin Mode__.

=== ":star: ArgoCD Plugin Mode :star:"

    !!! step "Step 1 - Install the ArgoCD Plugin"

        Your ArgoCD instance must have the _deployKF ArgoCD plugin_ installed.

        Depending on your situation, you may either:

        - [Add the deployKF plugin to an existing ArgoCD](https://github.com/deployKF/deployKF/tree/main/argocd-plugin#install-plugin---existing-argocd)
        - [Install a new ArgoCD (with the deployKF plugin pre-installed)](https://github.com/deployKF/deployKF/tree/main/argocd-plugin#install-plugin---new-argocd)

    !!! step "Step 2 - Define App-of-Apps Resource"

        The only resource you manually create is the `deploykf-app-of-apps`, this resource generates all the other `Application` resources.
        Think of it as a _"single source of truth"_ for the desired state of your platform.

        If you want to customize the platform, see the [:star: __Configure deployKF__ :star:](./configs.md) guide.

        ---

        Create a local file named `deploykf-app-of-apps.yaml` with the contents of the YAML below.

        This will use deployKF [version](#deploykf-versions) `{{ latest_deploykf_version }}`, 
        read the [`sample-values.yaml`](https://github.com/deployKF/deployKF/blob/v{{ latest_deploykf_version }}/sample-values.yaml) from the `deploykf/deploykf` repo, 
        and combine those values with the overrides defined in the `values` parameter.

        ```yaml
        apiVersion: argoproj.io/v1alpha1
        kind: Application
        metadata:
          name: deploykf-app-of-apps
          namespace: argocd
          labels:
            app.kubernetes.io/name: deploykf-app-of-apps
            app.kubernetes.io/part-of: deploykf
        spec:

          ## NOTE: if not "default", you MUST ALSO set the `argocd.project` value
          project: "default"

          source:
            ## source git repo configuration
            ##  - we use the 'deploykf/deploykf' repo so we can read its 'sample-values.yaml'
            ##    file, but you may use any repo (even one with no files)
            ##
            repoURL: "https://github.com/deployKF/deployKF.git"
            targetRevision: "v{{ latest_deploykf_version }}"
            path: "."
        
            ## plugin configuration
            ##
            plugin:
              name: "deploykf"
              parameters:
        
                ## the deployKF generator version
                ##  - available versions: https://github.com/deployKF/deployKF/releases
                ##
                - name: "source_version"
                  string: "{{ latest_deploykf_version }}"
        
                ## paths to values files within the `repoURL` repository
                ##  - the values in these files are merged, with later files taking precedence
                ##  - we strongly recommend using 'sample-values.yaml' as the base of your values
                ##    so you can easily upgrade to newer versions of deployKF
                ##
                - name: "values_files"
                  array:
                    - "./sample-values.yaml"
        
                ## a string containing the contents of a values file
                ##  - this parameter allows defining values without needing to create a file in the repo
                ##  - these values are merged with higher precedence than those defined in `values_files`
                ##
                - name: "values"
                  string: |
                    ##
                    ## This demonstrates how you might structure overrides for the 'sample-values.yaml' file.
                    ## For a more comprehensive example, see the 'sample-values-overrides.yaml' in the main repo.
                    ##
                    ## Notes:
                    ##  - YAML maps are RECURSIVELY merged across values files
                    ##  - YAML lists are REPLACED in their entirety across values files
                    ##  - Do NOT include empty/null sections, as this will remove ALL values from that section.
                    ##    To include a section without overriding any values, set it to an empty map: `{}`
                    ##
        
                    ## --------------------------------------------------------------------------------
                    ##                                      argocd
                    ## --------------------------------------------------------------------------------
                    argocd:
                      namespace: argocd
                      project: default

                    ## --------------------------------------------------------------------------------
                    ##                                    kubernetes
                    ## --------------------------------------------------------------------------------
                    kubernetes:
                      {} # <-- REMOVE THIS, IF YOU INCLUDE VALUES UNDER THIS SECTION!

                    ## --------------------------------------------------------------------------------
                    ##                              deploykf-dependencies
                    ## --------------------------------------------------------------------------------
                    deploykf_dependencies:
        
                      ## --------------------------------------
                      ##             cert-manager
                      ## --------------------------------------
                      cert_manager:
                        {} # <-- REMOVE THIS, IF YOU INCLUDE VALUES UNDER THIS SECTION!
        
                      ## --------------------------------------
                      ##                 istio
                      ## --------------------------------------
                      istio:
                        {} # <-- REMOVE THIS, IF YOU INCLUDE VALUES UNDER THIS SECTION!
        
                      ## --------------------------------------
                      ##                kyverno
                      ## --------------------------------------
                      kyverno:
                        {} # <-- REMOVE THIS, IF YOU INCLUDE VALUES UNDER THIS SECTION!
        
                    ## --------------------------------------------------------------------------------
                    ##                                  deploykf-core
                    ## --------------------------------------------------------------------------------
                    deploykf_core:
        
                      ## --------------------------------------
                      ##             deploykf-auth
                      ## --------------------------------------
                      deploykf_auth:
                        {} # <-- REMOVE THIS, IF YOU INCLUDE VALUES UNDER THIS SECTION!
        
                      ## --------------------------------------
                      ##        deploykf-istio-gateway
                      ## --------------------------------------
                      deploykf_istio_gateway:
                        {} # <-- REMOVE THIS, IF YOU INCLUDE VALUES UNDER THIS SECTION!
        
                      ## --------------------------------------
                      ##      deploykf-profiles-generator
                      ## --------------------------------------
                      deploykf_profiles_generator:
                        {} # <-- REMOVE THIS, IF YOU INCLUDE VALUES UNDER THIS SECTION!
        
                    ## --------------------------------------------------------------------------------
                    ##                                   deploykf-opt
                    ## --------------------------------------------------------------------------------
                    deploykf_opt:
        
                      ## --------------------------------------
                      ##            deploykf-minio
                      ## --------------------------------------
                      deploykf_minio:
                        {} # <-- REMOVE THIS, IF YOU INCLUDE VALUES UNDER THIS SECTION!
        
                      ## --------------------------------------
                      ##            deploykf-mysql
                      ## --------------------------------------
                      deploykf_mysql:
                        {} # <-- REMOVE THIS, IF YOU INCLUDE VALUES UNDER THIS SECTION!
        
                    ## --------------------------------------------------------------------------------
                    ##                                  kubeflow-tools
                    ## --------------------------------------------------------------------------------
                    kubeflow_tools:
        
                      ## --------------------------------------
                      ##                 katib
                      ## --------------------------------------
                      katib:
                        {} # <-- REMOVE THIS, IF YOU INCLUDE VALUES UNDER THIS SECTION!
        
                      ## --------------------------------------
                      ##               notebooks
                      ## --------------------------------------
                      notebooks:
                        {} # <-- REMOVE THIS, IF YOU INCLUDE VALUES UNDER THIS SECTION!
        
                      ## --------------------------------------
                      ##               pipelines
                      ## --------------------------------------
                      pipelines:
                        {} # <-- REMOVE THIS, IF YOU INCLUDE VALUES UNDER THIS SECTION!
        
          destination:
            server: "https://kubernetes.default.svc"
            namespace: "argocd"
        ```

    !!! step "Step 3 - Apply App-of-Apps Resource"

        Create a local file named `deploykf-app-of-apps.yaml` with the contents of the app-of-apps YAML above.

        Apply the resource to your cluster with the following command:

        ```bash
        kubectl apply -f ./deploykf-app-of-apps.yaml
        ```

        ---

        !!! tip "ArgoCD _Management Cluster_ Pattern"

            If you use a "management cluster" pattern, see the [off-cluster ArgoCD](./dependencies/argocd.md#can-i-use-an-off-cluster-argocd) guide.


=== "Manifests Repo Mode"

    !!! step "Step 1 - Install ArgoCD"

        If you have not already installed ArgoCD on your cluster, you will need to do so.

        Please see the [ArgoCD Getting Started Guide](https://argo-cd.readthedocs.io/en/stable/getting_started/) for instructions.
      
    !!! step "Step 2 - Install the deployKF CLI"

        If you have not already installed the `deploykf` CLI on your local machine, you will need to do so.

        Please see the [CLI Installation Guide](deploykf-cli.md#install-the-cli) for instructions.

    !!! step "Step 3 - Prepare a Git Repo"

        You will need to set up a git repo to store the generated manifests.
        If your repo is private (recommended), you will need to [configure ArgoCD with git credentials](https://argo-cd.readthedocs.io/en/stable/user-guide/private-repositories/) so it can access the repo.

        We recommend that you commit your values file(s) to the repo, so you can track changes over time.

    !!! step "Step 4 - Set Required Values"

        There are some values which must be set in your values file to tell ArgoCD where to find your generated manifests.
    
        <table markdown>
          <tr>
            <th>Value</th>
            <th>Description</th>
            <th>Example</th>
          </tr>
          <tr markdown>
            <td markdown>[`argocd.source.repo.url`](https://github.com/deployKF/deployKF/blob/v0.1.4/generator/default_values.yaml#L39-L43)</td>
            <td>the URL of the git repo where your generated manifests are stored</td>
            <td markdown>if you are using a GitHub repo named `deployKF/examples`, you might set this value to `"https://github.com/deployKF/examples"` or `"git@github.com:deployKF/examples.git"`</td>
          </tr>
          <tr markdown>
            <td markdown>[`argocd.source.repo.revision`](https://github.com/deployKF/deployKF/blob/v0.1.4/generator/default_values.yaml#L45-L48)</td>
            <td>is the git branch/tag/commit that ArgoCD should sync the manifests from</td>
            <td markdown>if you are using the `main` branch of your repo, you might set this value to `"main"`</td>
          </tr>
          <tr markdown>
            <td markdown>[`argocd.source.repo.path`](https://github.com/deployKF/deployKF/blob/v0.1.4/generator/default_values.yaml#L50-L54)</td>
            <td>is the folder path under the git repo where your generated manifests are stored</td>
            <td markdown>if you are using a folder named `GENERATOR_OUTPUT` at the root of your repo, you might set this value to `"./GENERATOR_OUTPUT/"`</td>
          </tr>
        </table>
    
        For example, the following values would tell ArgoCD to sync the manifests from a GitHub repo named `deployKF/examples`, using the `main` branch, and looking for the manifests in a folder named `./GENERATOR_OUTPUT`:
    
        ```yaml
        argocd:
          source:
            repo:
              url: "https://github.com/deployKF/examples.git"
              revision: "main"
              path: "./GENERATOR_OUTPUT/"
        ```

    !!! step "Step 5 - Generate Manifests"

        The `deploykf generate` command writes generated manifests into a folder, using one or more [values files](#about-values).

        If you want to customize the platform, see the [:star: __Configure deployKF__ :star:](./configs.md) guide.

        For example, this command will use deployKF `{{ latest_deploykf_version }}` to generate manifests under `GENERATOR_OUTPUT/`, from a values file named `custom-values.yaml`:
    
        ```shell
        deploykf generate \
            --source-version "{{ latest_deploykf_version }}" \
            --values ./custom-values.yaml \
            --output-dir ./GENERATOR_OUTPUT
        ```

        !!! warning "Avoid Manual Changes"
        
            Manual changes in the `--output-dir` will be __overwritten__ each time the `deploykf generate` command runs.
            If you find yourself needing to make manual changes, please [raise an issue](https://github.com/deployKF/deployKF/issues) so we may consider adding a new value to support your use-case.
    
        !!! info "Multiple Values Files"
            
            If you specify `--values` multiple times, they will be merged with later ones taking precedence.
            <br>
            Learn more in the [merging values](./values.md#merging-values) guide.

        !!! info "Required Arguments"

            The required arguments of the `deploykf generate` command are:
        
            Argument | Description
            --- | ---
            `--source-version` | the [version of deployKF](#deploykf-versions) to use
            `--values` | one or more values files to use for generating the manifests
            `--output-dir` | the directory where the generated manifests will be written

    !!! step "Step 6 - Commit Generated Manifests"

        After running `deploykf generate`, you will need to commit the manifests to your repo, so ArgoCD can apply them to your cluster:

        ```shell
        # for example, to directly commit changes to the 'main' branch of your repo
        git add GENERATOR_OUTPUT
        git commit -m "my commit message"
        git push origin main
        ```

    !!! step "Step 7 - Apply App-of-Apps Manifest"

        The only manifest you need to manually apply is the [app-of-apps](https://argo-cd.readthedocs.io/en/stable/operator-manual/cluster-bootstrapping/#app-of-apps-pattern), which creates all the other ArgoCD applications.

        The `app-of-apps.yaml` manifest is generated at the root of your `--output-dir` folder, so you can apply it with:
        
        ```shell
        kubectl apply --filename GENERATOR_OUTPUT/app-of-apps.yaml
        ```

        ---

        !!! tip "ArgoCD _Management Cluster_ Pattern"

            If you use a "management cluster" pattern, see the [off-cluster ArgoCD](./dependencies/argocd.md#can-i-use-an-off-cluster-argocd) guide.

### __:star: Sync ArgoCD Applications :star:__

Now that your deployKF app-of-apps has been applied, you must sync the ArgoCD applications to deploy your platform.
Syncing an application will cause ArgoCD to reconcile the actual state in the cluster, to match the state defined by the application resource.

!!! warning "Sync Order"

    The deployKF applications depend on each other, so you MUST sync them in the correct order to avoid errors.

There are a few ways to sync the applications, you only need to use ONE of them.
We recommend using the __automated sync script__.

=== ":star: Sync: Automated Script :star:"
    
    !!! step "Step - Sync with the Automated Script"

        We provide the [`sync_argocd_apps.sh`](https://github.com/deployKF/deployKF/blob/main/scripts/sync_argocd_apps.sh) script to automatically sync the applications that make up deployKF.
        Learn more about the automated sync script from the [`scripts` folder README](https://github.com/deployKF/deployKF/tree/main/scripts) .
    
        For example, to run the script, you might use the following commands:

        ```bash
        # clone the deploykf repo
        # NOTE: we use 'main', as the latest script always lives there
        git clone -b main https://github.com/deployKF/deployKF.git ./deploykf
        
        # ensure the script is executable
        chmod +x ./deploykf/scripts/sync_argocd_apps.sh
        
        # run the script
        bash ./deploykf/scripts/sync_argocd_apps.sh
        ```
    
    !!! note "About the sync script"
    
        - The script can take around 5-10 minutes to run on first install.
        - If the script fails or is interrupted, you can safely re-run it, and it will pick up where it left off.
        - There are a number of configuration variables at the top of the script which change the default behavior.
        - Learn more about the automated sync script from the [`scripts` folder README](https://github.com/deployKF/deployKF/tree/main/scripts) in the deployKF repo.

        Please be aware of the following issue when using the automated sync script:
        
        ??? bug "Bug in ArgoCD v2.9"
        
            There is a known issue ([`deploykf/deploykf#70`](https://github.com/deployKF/deployKF/issues/70), [`argoproj/argo-cd#16266`](https://github.com/argoproj/argo-cd/issues/16266)) with all `2.9.X` versions of the ArgoCD CLI that will cause the sync script to fail with the following error:
        
            ```text
            ==========================================================================================
            Logging in to ArgoCD...
            ==========================================================================================
            FATA[0000] cannot find pod with selector: [app.kubernetes.io/name=] - use the --{component}-name flag in this command or set the environmental variable (Refer to https://argo-cd.readthedocs.io/en/stable/user-guide/environment-variables), to change the Argo CD component name in the CLI
            ```
        
            Please upgrade your `argocd` CLI to at least version `2.10.0` to resolve this issue.

=== "Sync: ArgoCD Web UI"

    You can sync the applications using the ArgoCD Web UI.

    !!! step "Step 1 - Access the ArgoCD Web UI"

        For production usage, you may want to [expose ArgoCD with a `LoadBalancer` or `Ingress`](https://argo-cd.readthedocs.io/en/stable/getting_started/#3-access-the-argo-cd-api-server).

        For testing, you may use `kubectl` port-forwarding to expose the ArgoCD Web UI on your local machine:

        ```shell
        kubectl port-forward --namespace "argocd" svc/argocd-server 8090:https
        ```

        The ArgoCD Web UI should now be available at the following URL:

          :material-arrow-right-bold: [https://localhost:8090](https://localhost:8090)

        ---

        If this is the first time you are using ArgoCD, you will need to retrieve the initial password for the `admin` user:
        
        ```shell
        echo $(kubectl -n argocd get secret/argocd-initial-admin-secret \
          -o jsonpath="{.data.password}" | base64 -d)
        ```

        Once you log in with the `admin` user and above password, the Web UI should look like this:
    
        ![ArgoCD Web UI (Dark Mode)](../assets/images/argocd-ui-DARK.png#only-dark)
        ![ArgoCD Web UI (Light Mode)](../assets/images/argocd-ui-LIGHT.png#only-light)

    !!! step "Step 2 - Sync deployKF Applications"

        You MUST sync the deployKF applications in the correct order.
        For each application, click the `SYNC` button, and wait for the application to become "Healthy" before syncing the next.

        The applications are grouped and ordered as follows:
    
        !!! stack "Group 0: "app-of-apps""
        
            First, you must sync the app-of-apps application:
    
            1. `deploykf-app-of-apps`
            2. `deploykf-namespaces` (will only appear if using a remote destination)
    
        !!! stack "Group 1: "deploykf-dependencies""
        
            Second, you must sync the applications with the label `app.kubernetes.io/component=deploykf-dependencies`:
    
            1. `dkf-dep--cert-manager` (may fail on first attempt)
            2. `dkf-dep--istio`
            3. `dkf-dep--kyverno`
    
            __WARNING:__ for this group, each application MUST be synced INDIVIDUALLY and the preceding application MUST be "Healthy" before syncing the next.
    
        !!! stack "Group 2: "deploykf-core""
    
            Third, you must sync the applications with the label `app.kubernetes.io/component=deploykf-core`:
    
            1. `dkf-core--deploykf-istio-gateway`
            2. `dkf-core--deploykf-auth`
            3. `dkf-core--deploykf-dashboard`
            4. `dkf-core--deploykf-profiles-generator` (may fail on first attempt)
    
        !!! stack "Group 3: "deploykf-opt""
    
            Fourth, you must sync the applications with the label `app.kubernetes.io/component=deploykf-opt`:
    
            - `dkf-opt--deploykf-minio`
            - `dkf-opt--deploykf-mysql`
    
        !!! stack "Group 4: "deploykf-tools""
    
            Fifth, you must sync the applications with the label `app.kubernetes.io/component=deploykf-tools`:
    
            - (none yet)
    
        !!! stack "Group 5: "kubeflow-dependencies""
    
            Sixth, you must sync the applications with the label `app.kubernetes.io/component=kubeflow-dependencies`:
    
            - `kf-dep--argo-workflows`
    
        !!! stack "Group 6: "kubeflow-tools""
    
            Seventh, you must sync the applications with the label `app.kubernetes.io/component=kubeflow-tools`:
    
            - `kf-tools--katib`
            - `kf-tools--notebooks--jupyter-web-app`
            - `kf-tools--notebooks--notebook-controller`
            - `kf-tools--pipelines`
            - `kf-tools--poddefaults-webhook`
            - `kf-tools--tensorboards--tensorboard-controller`
            - `kf-tools--tensorboards--tensorboards-web-app`
            - `kf-tools--training-operator`
            - `kf-tools--volumes--volumes-web-app`

---

## 4. Use the Platform

Now that you have a working deployKF machine learning platform, here are some things to try out!

### __:star: Expose the deployKF Dashboard :star:__

The _deployKF dashboard_ is the web-based interface for deployKF, it gives users authenticated access to tools like [Kubeflow Pipelines](../reference/tools.md#kubeflow-pipelines), [Kubeflow Notebooks](../reference/tools.md#kubeflow-notebooks), and [Katib](../reference/tools.md#katib).

![deployKF Dashboard (Dark Mode)](../assets/images/deploykf-dashboard-DARK.png#only-dark)
![deployKF Dashboard (Light Mode)](../assets/images/deploykf-dashboard-LIGHT.png#only-light)

All public deployKF services (including the dashboard) are accessed via the deployKF Istio Gateway, you will need to expose its Kubernetes Service.

!!! step "Step 1 - Expose the Gateway"

    You may expose the deployKF Istio Gateway Service in a number of ways:
    
    - [Expose with: `kubectl port-forward`](./platform/deploykf-gateway.md#use-kubectl-port-forward) <small>(for local testing only)</small>
    - [Expose with: `LoadBalancer` Service](./platform/deploykf-gateway.md#use-a-loadbalancer-service)
    - [Expose with: `Ingress`](./platform/deploykf-gateway.md#use-a-kubernetes-ingress)

!!! step "Step 2 - Log in to the Dashboard"

    See the authentication guide to [define static credentials](./platform/deploykf-authentication.md#static-userpassword-combinations), or [connect deployKF to an external identity provider](#external-identity-providers) like Okta or Active Directory.

    There are a few default credentials set in the [`deploykf_core.deploykf_auth.dex.staticPasswords`](https://github.com/deployKF/deployKF/blob/v0.1.4/generator/default_values.yaml#L469-L492) value:

    ??? key "Credentials: Admin"

        __Username:__ `admin@example.com`
        <br>
        __Password:__ `admin`

        - This account is the [default "owner"](https://github.com/deployKF/deployKF/blob/v0.1.2/generator/default_values.yaml#L688-L694) of all profiles.
        - This account does NOT have access to "MinIO Console" or "Argo Server UI".
        - We recommend NOT using this account, and actually removing its [`staticPasswords` entry](https://github.com/deployKF/deployKF/blob/v0.1.2/generator/default_values.yaml#L394-L396).
        - We recommend leaving this account as the default "owner", even with `@example.com` as the domain (because profile owners can't be changed).

    ??? key "Credentials: User 1"

        __Username:__ `user1@example.com`
        <br>
        __Password:__ `user1`

        - This account has [write access to `team-1` profile](https://github.com/deployKF/deployKF/blob/v0.1.2/generator/default_values.yaml#L830-L833).
        - This account has [read access to `team-1-prod`](https://github.com/deployKF/deployKF/blob/v0.1.2/generator/default_values.yaml#L837-L840).

    ??? key "Credentials: User 2"

        __Username:__ `user2@example.com`
        <br>
        __Password:__ `user2`

        - This account has [write access to `team-1` profile](https://github.com/deployKF/deployKF/blob/v0.1.2/generator/default_values.yaml#L830-L833).
        - This account has [read access to `team-1-prod`](https://github.com/deployKF/deployKF/blob/v0.1.2/generator/default_values.yaml#L837-L840).

!!! step "Step 3 - Customize the Dashboard"

    If you would like to make changes to the _deployKF dashboard_, such as adding custom links to the sidebar or homepage, see the [dashboard customization guide](./platform/deploykf-dashboard.md).

### __Explore the Tools__

deployKF includes many [ML & Data tools](../reference/tools.md#tool-index) that address different stages of the machine learning lifecycle.
Here are a few popular tools to get started with:

- [Kubeflow Pipelines](../reference/tools.md#kubeflow-pipelines)
- [Kubeflow Notebooks](../reference/tools.md#kubeflow-notebooks)

!!! tip "User Guides"

    We provide a number of user-focused reference guides to help them deliver value with the platform faster.
    You should share these guides with your users.
  
    <table markdown="span">
      <tr>
        <th>User Guide</th>
        <th>Description</th>
      </tr>
      <tr markdown>
        <td markdown>[Access Kubeflow Pipelines API](../user-guides/access-kubeflow-pipelines-api.md)</td>
        <td>Learn how to access the Kubeflow Pipelines API from both inside and outside the cluster with the _Kubeflow Pipelines SDK_.</td>
      </tr>
      <tr markdown>
        <td markdown>[GitOps for Kubeflow Pipelines Schedules](../user-guides/gitops-for-kubeflow-pipelines.md)</td>
        <td>Learn how to use GitOps to manage Kubeflow Pipelines schedules (rather than manually creating them with the UI or Python SDK).</td>
      </tr>
    </table>

## Next Steps

- [:material-account-group: Join the deployKF community!](../about/community.md)
- [:star: Support us with a star on GitHub!](https://github.com/deployKF/deployKF)
- [<span style="color: #ff1f1f">:material-hospital-box:</span> Get support from our experts!](../about/support.md)