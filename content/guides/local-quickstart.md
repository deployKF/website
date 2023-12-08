---
icon: material/sprout
description: >-
  Learn how to quickly try deployKF on a local Kubernetes cluster.
  Test our powerful Helm-like interface for deploying Kubeflow and other MLOps tools.
---

# Local Quickstart

Learn how to __quickly try deployKF__ on a __local Kubernetes cluster__.
Test our powerful Helm-like interface for deploying Kubeflow and other MLOps tools.

!!! tip "Other Resources"

    - [__Getting Started__](getting-started.md) - start building your production-ready ML Platform on any Kubernetes cluster

---

## Introduction

To learn about deployKF and why you might want to use it, please see the [Introduction](../about/introduction.md).

[Read Introduction<br>:material-lightbulb-on:](../about/introduction.md#about-deploykf){ .md-button .md-button--primary }
[Watch Introduction<br>:material-youtube:](../about/introduction.md#video-introduction){ .md-button .md-button--primary }

## 1. Requirements

The requirements for this quickstart depend on your operating system.

=== "macOS"

    Requirement | Notes
    --- | ---
    Homebrew | [Install Guide](https://brew.sh/)
    Docker Desktop | [Install Guide](https://docs.docker.com/docker-for-mac/install/)
    Bash 4.2+ | RUN: `brew install bash`<br>*(macOS has bash `3.2` by default)*
    CLI: [`argocd`](https://argo-cd.readthedocs.io/en/stable/cli_installation/) | RUN: `brew install argocd`
    CLI: [`jq`](https://jqlang.github.io/jq/download/) | RUN: `brew install jq`
    CLI: [`k3d`](https://k3d.io/) | RUN: `brew install k3d`
    CLI: [`kubectl`](https://kubernetes.io/docs/tasks/tools/install-kubectl-macos/) | RUN: `brew install kubectl`

    !!! warning "Apple Silicon"

        deployKF does NOT currently support ARM clusters. 
        A small number of Kubeflow components do not support ARM just yet, we expect this to change after the release of Kubeflow 1.8 in October 2023.

    !!! warning "Resource Allocation"

        In Docker Desktop, you may need to increase the [resource allocation](https://docs.docker.com/desktop/settings/mac/#resources), we recommend allocating at least:
        
        - __4 CPU Cores__
        - __10 GB RAM__

    ??? question_secondary "Can I use Podman instead of Docker Desktop?"

        Yes. While we recommend using Docker Desktop, you may use [Podman](https://podman.io/) instead.
       
        Follow these steps to [configure `k3d` to use Podman](https://k3d.io/stable/usage/advanced/podman/):
        
        1. [Install Podman](https://podman.io/docs/installation#macos)
        2. Enable Podman socket: `sudo systemctl enable --now podman.socket`
        3. Link Docker socket to Podman: `sudo ln -s /run/podman/podman.sock /var/run/docker.sock`

=== "Linux"

    Requirement | Notes
    --- | ---
    Docker Engine | [Install Guide](https://docs.docker.com/engine/install/)
    CLI: `argocd` | [Install Guide](https://argo-cd.readthedocs.io/en/stable/cli_installation/) <sup>(also on Homebrew for Linux)</sup>
    CLI: `jq` | [Install Guide](https://jqlang.github.io/jq/download/) <sup>(also on Homebrew for Linux)</sup>
    CLI: `k3d` | [Install Guide](https://k3d.io/stable/#installation) <sup>(also on Homebrew for Linux)</sup>
    CLI: `kubectl` | [Install Guide](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/) <sup>(also on Homebrew for Linux)</sup>

    !!! warning "Inotify Limits"

        On __Linux__, you may need to increase your system's open/watched file limits.

        1. Modify `/etc/sysctl.conf` to include the following lines:
            - `fs.inotify.max_user_instances = 1280`
            - `fs.inotify.max_user_watches = 655360`
        2. Reload sysctl configs by running `sudo sysctl -p`

    ??? info "Homebrew for Linux"

        An easy way to install the requirements is with [Homebrew](https://brew.sh/), while traditionally a macOS tool, it supports linux as well.

        The following commands will install `brew` and add it to your PATH:
    
        ```bash
        # install Homebrew for Linux
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    
        # add 'brew' to your PATH
        # NOTE: reopen your shell for this to take effect
        (echo; echo 'eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"') >> ~/.profile
        ```

        After Homebrew is installed, you may use commands like:

        ```bash
        brew install argocd
        brew install jq
        brew install k3d
        brew install kubectl
        ```

=== "Windows"

    <h4>Step 1: Install Host Dependencies</h4>
    
    Install these dependencies on your __Windows host__:

    Requirement | Notes
    --- | ---
    Windows Subsystem for Linux (WSL 2) | [Install Guide](https://learn.microsoft.com/en-us/windows/wsl/install)
    Docker Desktop | [Install Guide](https://docs.docker.com/desktop/install/windows-install/)
    
    ---

    <h4>Step 2: Configure WSL</h4>

    Configure WSL to use our [__custom kernel__](https://github.com/deployKF/WSL2-Linux-Kernel) that properly supports Kubernetes (specifically Istio).

    ??? question_secondary "Why do we need a custom kernel?"
    
        - For context on why a custom kernel is needed, see [`deployKF/deployKF#41`](https://github.com/deployKF/deployKF/issues/41).
        - To see what changes we have made to the kernel, review [`deployKF/WSL2-Linux-Kernel`](https://github.com/deployKF/WSL2-Linux-Kernel).
        - Hopefully, once [`microsoft/WSL#8153`](https://github.com/microsoft/WSL/issues/8153) is resolved, we will no longer need a custom kernel.

    Run these commands in __PowerShell__ (search `PowerShell` in start menu):

    ```powershell
    # create a directory for custom kernels
    New-Item -Path "$env:USERPROFILE\WSL2Kernels" -ItemType Directory -Force | Out-Null

    # download our custom kernel
    $KERNEL_VERSION = "linux-deploykf-wsl-5.15.133.1"
    $KERNEL_URL = "https://github.com/deployKF/WSL2-Linux-Kernel/releases/download/${KERNEL_VERSION}/linux-deploykf-wsl"
    $KERNEL_PATH = "$env:USERPROFILE\WSL2Kernels\linux-deploykf-wsl"
    Invoke-WebRequest -Uri "${KERNEL_URL}" -OutFile "${KERNEL_PATH}"

    # set the custom kernel as the default
    # NOTE: this will overwrite any existing .wslconfig file
    $KERNEL_PATH_ESCAPED = ("$env:USERPROFILE\WSL2Kernels\linux-deploykf-wsl" -replace '\\', '\\')
    $WSLCONFIG_CONTENT = @"
    [wsl2]
    kernel="${KERNEL_PATH_ESCAPED}"
    "@
    Set-Content -Path "$env:USERPROFILE\.wslconfig" -Value "${WSLCONFIG_CONTENT}"

    # restart WSL
    wsl --shutdown
    ```

    !!! warning "Restart Docker Desktop"

        Now you must __restart Docker Desktop__ to ensure it is using the new kernel.

        Right-click the Docker Desktop icon in the system tray, then select `Restart`.

    ---

    <h4>Step 3: Install Homebrew</h4>

    Install Homebrew for Linux within your __WSL environment__.

    Run these commands in an Ubuntu shell (search `Ubuntu` in start menu):

    ```bash
    # install Homebrew for Linux
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

    # add 'brew' to your PATH
    # NOTE: reopen your shell for this to take effect
    (echo; echo 'eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"') >> ~/.profile
    ```

    ---

    <h4>Step 4: Install WSL Dependencies</h4>

    Install these dependencies within your Ubuntu shell (search `Ubuntu` in start menu):

    Requirement | Notes
    --- | ---
    CLI: [`argocd`](https://argo-cd.readthedocs.io/en/stable/cli_installation/) | RUN: `brew install argocd`
    CLI: [`jq`](https://jqlang.github.io/jq/download/) | RUN: `brew install jq`
    CLI: [`k3d`](https://k3d.io/) | RUN: `brew install k3d`
    CLI: [`kubectl`](https://kubernetes.io/docs/tasks/tools/install-kubectl-macos/) | RUN: `brew install kubectl`

    ---

    For the rest of the guide, unless otherwise instructed, run all commands in an Ubuntu shell.

## 2. Kubernetes

### About k3d

[K3d](https://k3d.io/) is a helpful command line tool which helps you spin up [k3s](https://k3s.io/) Kubernetes clusters running inside Docker containers.

K3s itself is an extremely lightweight Kubernetes distribution, which is fully compliant with the Kubernetes API, while being very similar to how cloud-based clusters are configured.

### Create Kubernetes Cluster

Run this command to create a local k3s cluster using `k3d`, named `deploykf`:

```bash
# NOTE: this will change your kubectl context to the new cluster
k3d cluster create "deploykf" \
  --image "rancher/k3s:v1.26.9-k3s1"
```

??? question_secondary "Can I use a different version of Kubernetes?"

    Yes. The `--image` flag allows you to specify the version of Kubernetes.
    You may use any version of the [`rancher/k3s`](https://hub.docker.com/r/rancher/k3s/tags) image which corresponds to a version of Kubernetes that is [supported by deployKF](../releases/version-matrix.md#deploykf-dependencies).

### Wait for Cluster to be Ready

Wait until the cluster is ready (all pods are in a `Running` or `Completed` state) before continuing.

??? steps "Get the state of Pods - _`k9s`_ :star:"

    We highly recommend [`k9s`](https://k9scli.io/), it makes interacting with Kubernetes much easier by providing a text-based management interface for any Kubernetes cluster.

    You may [install `k9s`](https://k9scli.io/topics/install/) with `brew install k9s` on macOS and Linux.

    __Get the status of all pods:__

    1. Run `k9s` in your terminal
    2. Presh `shift` + `:` to open the command prompt - _(tip: press `escape` to close any prompt)_
    3. Type `pods` and press `enter` - _(tip: press `tab` to autocomplete resource names)_
    4. Press `0` to show all namespaces
    5. Scroll through the list of pods and check the `STATUS` column

    __The resulting list of pods will look similar to this:__

    ```text
     Context: k3d-deploykf                             <0> all           <a>      Attach     <l>       Logs               <y> YAML                    ____  __.________        
     Cluster: k3d-deploykf                             <1> default       <ctrl-d> Delete     <p>       Logs Previous                                 |    |/ _/   __   \______ 
     User:    admin@k3d-deploykf                                         <d>      Describe   <shift-f> Port-Forward                                  |      < \____    /  ___/ 
     K9s Rev: v0.27.4                                                    <e>      Edit       <s>       Shell                                         |    |  \   /    /\___ \  
     K8s Rev: v1.26.4+k3s1                                               <?>      Help       <n>       Show Node                                     |____|__ \ /____//____  > 
     CPU:     0%                                                         <ctrl-k> Kill       <f>       Show PortForward                                      \/            \/  
     MEM:     22%                                                                                                                                                              
    ┌───────────────────────────────────────────────────────────────────────────── Pods(all)[7] ──────────────────────────────────────────────────────────────────────────────┐
    │ NAMESPACE↑               NAME                                                      PF READY RESTARTS STATUS     CPU  MEM %CPU/R %CPU/L %MEM/R %MEM/L IP           NODE  │
    │ kube-system              coredns-59b4f5bbd5-7vp9v                                  ●  1/1          0 Running      2   26      2    n/a     38     15 10.42.0.106  k3d-d │
    │ kube-system              helm-install-traefik-2h5mn                                ●  0/1          0 Completed    0    0    n/a    n/a    n/a    n/a 10.42.0.2    k3d-d │
    │ kube-system              helm-install-traefik-crd-q9mjn                            ●  0/1          0 Completed    0    0    n/a    n/a    n/a    n/a 10.42.0.5    k3d-d │
    │ kube-system              local-path-provisioner-76d776f6f9-pslbf                   ●  1/1          0 Running      1   16    n/a    n/a    n/a    n/a 10.42.0.92   k3d-d │
    │ kube-system              metrics-server-7b67f64457-qc5nt                           ●  1/1          0 Running     2↓  40↑     2↓    n/a    57↑    n/a 10.42.0.110  k3d-d │
    │ kube-system              svclb-traefik-1d8d8195-8j89l                              ●  2/2          0 Running      0    2    n/a    n/a    n/a    n/a 10.42.0.90   k3d-d │
    │ kube-system              traefik-56b8c5fb5c-q4hqp                                  ●  1/1          0 Running      1   69    n/a    n/a    n/a    n/a 10.42.0.133  k3d-d │
    └─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
    ```
    
    ---

    __Filtering by namespace:__

    1. Press `shift` + `:` to open the command prompt
    2. Type `ns` and press `enter`
    3. Select the namespace you want to view and press `enter` (will open list of pods in that namespace)
    4. Press `shift` + `:` to open the command prompt
    5. Type the name of a resource type (e.g. `service` or `secret`) and press `enter`
    
    Note, recently viewed namespaces are given a number (e.g. `1`, `2`, `3`), press that number to show all instances of the currently selected resource type in that namespace.

    ---

    __Other features:__

    - When viewing a list of resources, press `/` to open the search prompt - _(tip: press `escape` to close any prompt)_
    - When highlighting any resource, press `y` to view its YAML
    - When highlighting any resource, press `d` to describe it
    - When highlighting any resource, press `e` to open a `vim` editor for its YAML
    - When highlighting a pod, press `l` to view its logs
    - When highlighting a pod, press `s` to open an interactive shell
    - When highlighting a secret, press `x` to view its base64-decoded data

    For more information about the features of `k9s`, see the [k9s documentation](https://k9scli.io/), or press `?` to view the help menu.

??? steps "Get the state of Pods - _`kubectl`_"

    You can use `kubectl` to check the status of all pods, in all namespaces:

    ```bash
    kubectl get -A pods
    ```

    The list of pods will look similar to this:

    ```text
    NAMESPACE    NAME                                      READY   STATUS      RESTARTS         AGE
    kube-system  helm-install-traefik-crd-q9mjn            0/1     Completed   0                1h
    kube-system  helm-install-traefik-2h5mn                0/1     Completed   0                1h
    kube-system  svclb-traefik-1d8d8195-8j89l              2/2     Running     0                1h
    kube-system  local-path-provisioner-76d776f6f9-pslbf   1/1     Running     0                1h
    kube-system  coredns-59b4f5bbd5-7vp9v                  1/1     Running     0                1h
    kube-system  traefik-56b8c5fb5c-q4hqp                  1/1     Running     0                1h
    kube-system  metrics-server-7b67f64457-qc5nt           1/1     Running     0                1h
    ```

## 3. Prepare ArgoCD

### About ArgoCD

[ArgoCD](https://argo-cd.readthedocs.io/en/stable/) is an extremely widely-used tool that helps you programmatically manage the applications deployed on your cluster.

??? question_secondary "Why does deployKF use Argo CD?"

    We use [Argo CD](https://argo-cd.readthedocs.io/) to manage the state of the platform.

    ArgoCD gives us a pre-built system to determine the sync-state of the apps we deploy (if resources need to be updated), and also makes cleaning up old resources much easier.

    Argo CD is a great tool for this job given its [__widespread adoption__](https://github.com/argoproj/argo-cd/blob/master/USERS.md), and __well designed interface__ for visualizing and managing the current state of your cluster.

    In the future, we plan to support other Kubernetes GitOps tools (like [Flux CD](https://fluxcd.io/)), or even build a deployKF-specific solution, but we have initially chosen to use Argo CD due to its overwhelming popularity.

??? info "Argo CD vs Argo Workflows"

    It's important to note that _Argo CD_ is NOT the same as _Argo Workflows_, they just have similar names:
    
    - [__Argo CD__](https://argo-cd.readthedocs.io/en/stable/) is a __GitOps Tool__, it manages the state of Kubernetes resources
    - [__Argo Workflows__](https://argoproj.github.io/argo-workflows/) is a __Workflow Engine__, it defines and runs DAG workflows in Pods on Kubernetes

### About ArgoCD Applications

The main config for ArgoCD is the [`Application`](https://argo-cd.readthedocs.io/en/stable/user-guide/application-specification/), a Kubernetes [custom resource](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/) that specifies Kubernetes manifests that ArgoCD should deploy and manage (typically from a git repository).

An _"app of apps"_ is a pattern where a single ArgoCD `Application` contains other `Application` definitions, this is typically done to make bootstrapping large applications easier.

### About deployKF Plugin

We will be using the [deployKF ArgoCD Plugin](https://github.com/deployKF/deployKF/tree/main/argocd-plugin), which adds a special kind of ArgoCD `Application` that produces deployKF manifests.

The plugin removes the need to generate manifests, and instead allows you to define your platform using a single _"app of apps"_ `Application` whose specification only needs your [values](#about-values), and a specified [source version](#deploykf-versions) of deployKF.

### Install ArgoCD and deployKF Plugin

First, ensure that your current `kubectl` context is set to the new cluster.

??? question_secondary "How do I check my current kubectl context?"

    Run the following command, and ensure it prints `k3d-deploykf`:
    
    ```bash
    # get the name of the current kubectl context
    kubectl config current-context
    ```

??? question_secondary "How do I change my kubectl context?"

    We recommend using [__`kubectx`__](https://github.com/ahmetb/kubectx) to manage your `kubectl` contexts, which can be [__installed__](https://github.com/ahmetb/kubectx#installation) with `brew install kubectx` on macOS and Linux.

    To change your kubectl context with `kubectx`, run these commands:

    ```bash
    # list all contexts 
    # NOTE: this is interactive, if `fzf` is installed
    kubectx

    # set the current context to 'k3d-deploykf'
    kubectx "k3d-deploykf"
    ```

Now, run these commands to install [ArgoCD](https://argo-cd.readthedocs.io/) and the [deployKF ArgoCD Plugin](https://github.com/deployKF/deployKF/tree/main/argocd-plugin) into your cluster:

```bash
# clone the deploykf repo
# NOTE: we use 'main', as the latest plugin version always lives there
git clone -b main https://github.com/deployKF/deployKF.git ./deploykf

# ensure the script is executable
chmod +x ./deploykf/argocd-plugin/install_argocd.sh

# run the install script
# WARNING: this will install into your current kubectl context
bash ./deploykf/argocd-plugin/install_argocd.sh
```

After the script completes, wait for all pods in the `argocd` Namespace to be in a `Running` state ([using `k9s` or `kubectl` as described above](#wait-for-cluster-to-be-ready)).

## 4. Create ArgoCD Applications

### About Values

All aspects of your deployKF platform are configured with YAML-based configs named "values".
There are a very large number of values (more than 1500), but as deployKF supports _in-place upgrades_ you can start with a few important ones, and then grow your values file over time.

For this quickstart, will be using the [`sample-values.yaml`](https://github.com/deployKF/deployKF/blob/v{{ latest_deploykf_version }}/sample-values.yaml) file as our base.
These sample values (which are different for each deployKF version) have all ML & Data tools enabled, along with some sensible security defaults.

You may copy and make changes to the sample values, or directly use it as a base, and override specific values in a separate file.
We provide the [`sample-values-overrides.yaml`](https://github.com/deployKF/deployKF/blob/v{{ latest_deploykf_version }}/sample-values-overrides.yaml) file as an example of this approach.

!!! note "YAML Syntax"

    For a refresher on YAML syntax, we recommend the following resources:
    
    - [Learn YAML in Y minutes](https://learnxinyminutes.com/docs/yaml/)
    - [YAML Multiline Strings](https://yaml-multiline.info/)

### deployKF Versions

The "source version" chooses which version of the deployKF generator will be used.
Each version may include different tools, and may support different versions of external dependencies (like Kubernetes, Istio and cert-manager).

The [version matrix](../releases/version-matrix.md) lists which tools and dependency versions are supported by each deployKF release.
Specific information about each release (including important upgrade notes), can be found in the [deployKF generator changelog](../releases/changelog-deploykf.md).

### Create an App-of-Apps

To use deployKF, the only `Application` that you will need to manually create is the _"app of apps"_.

For example, the following _"app of apps"_ specification will use deployKF `{{ latest_deploykf_version }}` and read the [`sample-values.yaml`](https://github.com/deployKF/deployKF/blob/v{{ latest_deploykf_version }}/sample-values.yaml) (from the `v{{ latest_deploykf_version }}` tag of the `deploykf/deploykf` repo) while also showing how to set values with the `values` parameter:

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

You will need to apply this `Application` resource to your Kubernetes cluster.

??? steps "Apply the application - _CLI_ :star:"
    
    First, create a file named `deploykf-app-of-apps.yaml` with the contents of the application YAML above.

    Next, ensure your `kubectl` context is set to the `k3d-deploykf` cluster.

    Finally, run this command to apply the app-of-apps:

    ```bash
    kubectl apply -f ./deploykf-app-of-apps.yaml
    ```

??? steps "Apply the application - _ArgoCD Web UI_"

    You will need to retrieve the initial password for the `admin` user:
    
    ```shell
    echo $(kubectl -n argocd get secret/argocd-initial-admin-secret \
      -o jsonpath="{.data.password}" | base64 -d)
    ```
    
    Next, use `kubectl` port-forwarding to access the ArgoCD Web UI:

    ```shell
    kubectl port-forward --namespace "argocd" svc/argocd-server 8090:https
    ```

    You will now be able to access ArgoCD at [https://localhost:8090](https://localhost:8090) in your browser.

    Log in with the `admin` user, and the password you retrieved above.

    ---

    The ArgoCD Web UI will look like this (but without any applications):

    ![ArgoCD Web UI (Dark Mode)](../assets/images/argocd-ui-DARK.png#only-dark)
    ![ArgoCD Web UI (Light Mode)](../assets/images/argocd-ui-LIGHT.png#only-light)

    ---

    To create the app-of-apps, follow these steps:

    1. Click the `+ New App` button
    2. Click the `Edit as YAML` button
    3. Paste the application YAML into the editor
    4. Click the `Save` button
    5. Click the `Create` button

## 5. Sync ArgoCD Applications

Now that your deployKF app-of-apps has been applied, you must sync the ArgoCD applications to deploy your platform.
Syncing an application will cause ArgoCD to reconcile the actual state in the cluster, to match the state defined by the application resource.

ArgoCD supports syncing applications both _graphically (Web UI)_ and _programmatically (CLI)_.
For this quickstart, we will use the CLI via our automated [`sync_argocd_apps.sh`](https://github.com/deployKF/deployKF/blob/main/scripts/sync_argocd_apps.sh) script.

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

## 6. Try the Platform

Now that you have a local deployKF ML Platform, here are some things to try out!

### The Dashboard

The _deployKF dashboard_ is the web-based interface for deployKF, it gives users [authenticated access](./platform/deploykf-authentication.md) to tools like [Kubeflow Pipelines](../reference/tools.md#kubeflow-pipelines), [Kubeflow Notebooks](../reference/tools.md#kubeflow-notebooks), and [Katib](../reference/tools.md#katib).

![deployKF Dashboard (Dark Mode)](../assets/images/deploykf-dashboard-DARK.png#only-dark)
![deployKF Dashboard (Light Mode)](../assets/images/deploykf-dashboard-LIGHT.png#only-light)

### Access the Gateway

All public deployKF services (including the dashboard) are accessed via your _deployKF Istio Gateway_, to use the gateway, you will need to expose its Kubernetes Service.

For this quickstart, we will be using the port-forward feature of `kubectl` to expose the gateway locally on your machine.

=== "macOS"

    <h4>Step 1: Modify Hosts</h4>
  
    You will need to add the following lines to the END of your __local__ `/etc/hosts` file:

    ```text
    127.0.0.1 deploykf.example.com
    127.0.0.1 argo-server.deploykf.example.com
    127.0.0.1 minio-api.deploykf.example.com
    127.0.0.1 minio-console.deploykf.example.com
    ```

    !!! question_secondary "Why do I need these entries in my hosts file?"

        The _deployKF Istio Gateway_ uses the HTTP `Host` header to route requests to the correct internal service, meaning that using `localhost` or `127.0.0.1` will NOT work.


=== "Linux"

    <h4>Step 1: Modify Hosts</h4>

    You will need to add the following lines to the END of your __local__ `/etc/hosts` file:

    ```text
    127.0.0.1 deploykf.example.com
    127.0.0.1 argo-server.deploykf.example.com
    127.0.0.1 minio-api.deploykf.example.com
    127.0.0.1 minio-console.deploykf.example.com
    ```

    !!! question_secondary "Why do I need these entries in my hosts file?"

        The _deployKF Istio Gateway_ uses the HTTP `Host` header to route requests to the correct internal service, meaning that using `localhost` or `127.0.0.1` will NOT work.

=== "Windows"

    <h4>Step 1: Modify Hosts</h4>

    You will need to add the following lines to the END of your `C:\Windows\System32\drivers\etc\hosts` file:

    ```text
    127.0.0.1 deploykf.example.com
    127.0.0.1 argo-server.deploykf.example.com
    127.0.0.1 minio-api.deploykf.example.com
    127.0.0.1 minio-console.deploykf.example.com
    ```
  
    !!! warning "Edit hosts file as Administrator"

        The hosts file can ONLY be edited by the Windows _Administrator_ user.

        Run this PowerShell command to start an _Administrator_ Notepad, which can edit the hosts file:
    
        ```powershell
        Start-Process notepad.exe -ArgumentList "C:\Windows\System32\drivers\etc\hosts" -Verb RunAs
        ```

    !!! question_secondary "Why do I need these entries in my hosts file?"

        The _deployKF Istio Gateway_ uses the HTTP `Host` header to route requests to the correct internal service, meaning that using `localhost` or `127.0.0.1` will NOT work.

---

<h4>Step 2: Port-Forward Gateway</h4>

You may now port-forward the `deploykf-gateway` Service using this `kubectl` command:

```shell
kubectl port-forward \
  --namespace "deploykf-istio-gateway" \
  svc/deploykf-gateway 8080:http 8443:https
```

The deployKF dashboard should now be available on your local machine at:
    
  :material-arrow-right-bold: [https://deploykf.example.com:8443/](https://deploykf.example.com:8443/)

---

<h4>Step 3: Log in to Dashboard</h4>

The default values include [static user/password combinations](./platform/deploykf-authentication.md#static-userpassword-combinations) defined by the [`deploykf_core.deploykf_auth.dex.staticPasswords`](https://github.com/deployKF/deployKF/blob/v0.1.2/generator/default_values.yaml#L393-L402) value, which can be used for testing.

This table lists the default login credentials:

Username | Password | Notes
--- | --- | ---
`admin@example.com` | `admin` | The [default "owner"](https://github.com/deployKF/deployKF/blob/v0.1.2/generator/default_values.yaml#L688-L694) of all profiles, but a "member" of none, meaning it does NOT have access to "MinIO Console" or "Argo Workflows Server".<br><br>In production, we recommend leaving this account as the default "owner" but excluding its [`staticPasswords` entry](https://github.com/deployKF/deployKF/blob/v0.1.2/generator/default_values.yaml#L394-L396), so it can't be used to log in. 
`user1@example.com` | `user1` | Has [write access to `team-1` profile](https://github.com/deployKF/deployKF/blob/v0.1.2/generator/default_values.yaml#L830-L833), and [read access to `team-1-prod`](https://github.com/deployKF/deployKF/blob/v0.1.2/generator/default_values.yaml#L837-L840).
`user2@example.com` | `user2` | Has [write access to `team-1` profile](https://github.com/deployKF/deployKF/blob/v0.1.2/generator/default_values.yaml#L830-L833), and [read access to `team-1-prod`](https://github.com/deployKF/deployKF/blob/v0.1.2/generator/default_values.yaml#L837-L840).

### ML & Data Tools

deployKF includes [many tools](../reference/tools.md#tool-index) that address different stages of the ML & Data lifecycle.
The following links give more specific information about some of our most popular tools:

- [Kubeflow Pipelines](../reference/tools.md#kubeflow-pipelines)
- [Kubeflow Notebooks](../reference/tools.md#kubeflow-notebooks)

## Next Steps

- [:material-rocket-launch: Build a production-ready deployKF platform!](getting-started.md)
- [:material-account-group: Join the deployKF community!](../about/community.md)
- [:star: Support us with a star on GitHub!](https://github.com/deployKF/deployKF)
- [<span style="color: #ff1f1f">:material-hospital-box:</span> Get support from our experts!](../about/support.md)
