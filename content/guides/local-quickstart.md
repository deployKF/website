---
icon: material/sprout
description: >-
  Quickly try deployKF on a local Kubernetes cluster.
  Easily try out Kubeflow and other MLOps tools!
---

# Local Quickstart

Learn how to quickly try <strong><span class="deploykf-orange">deploy</span><span class="deploykf-blue">KF</span></strong> on a __local__ Kubernetes cluster.

---

## Introduction

This quickstart will guide you through setting up a local `k3d` Kubernetes cluster, installing ArgoCD, and running deployKF on top of it.

!!! warning "Not for Production Use"

    This quickstart is for __testing__ purposes only.
    For production use, please see the [Getting Started](./getting-started.md) guide.

## 1. Requirements

The requirements for this quickstart depend on your operating system.

=== "macOS"

    !!! danger "Apple Silicon"

        Currently, deployKF does NOT support `arm64` clusters like Apple Silicon.
        Furthermore, some core components don't work under rosetta emulation.
        Please use an `x86_64` machine or cloud-instance to run this quickstart.

    !!! step "Step 1 - Install Core Dependencies"

        First, install these core dependencies on your __macOS host__:

        Requirement | Notes
        --- | ---
        Homebrew | [Install Guide](https://brew.sh/)
        Docker Desktop | [Install Guide](https://docs.docker.com/docker-for-mac/install/)

        !!! warning "Resource Allocation"
    
            In Docker Desktop, you may need to increase the [resource allocation](https://docs.docker.com/desktop/settings/mac/#resources).
            We recommend allocating at least the following resources:
            
            - __4 CPU Cores__
            - __10 GB RAM__

        ??? question_secondary "Can I use Podman instead of Docker Desktop?"
    
            Yes. While we recommend using Docker Desktop, you may use [Podman](https://podman.io/) instead.
           
            Follow these steps to [configure `k3d` to use Podman](https://k3d.io/stable/usage/advanced/podman/):
            
            1. [Install Podman](https://podman.io/docs/installation#macos)
            2. Enable Podman socket: `sudo systemctl enable --now podman.socket`
            3. Link Docker socket to Podman: `sudo ln -s /run/podman/podman.sock /var/run/docker.sock`

    !!! step "Step 2 - Install CLI Tools"

        Next, install these CLI tools on your __macOS host__:

        Requirement | Notes
        --- | ---
        Bash 4.2+ | RUN: `brew install bash`<br>*(macOS has bash `3.2` by default)*
        CLI: [`argocd`](https://argo-cd.readthedocs.io/en/stable/cli_installation/) | RUN: `brew install argocd`
        CLI: [`jq`](https://jqlang.github.io/jq/download/) | RUN: `brew install jq`
        CLI: [`k3d`](https://k3d.io/) | RUN: `brew install k3d`
        CLI: [`kubectl`](https://kubernetes.io/docs/tasks/tools/install-kubectl-macos/) | RUN: `brew install kubectl`

=== "Linux"

    !!! step "Step 1 - Install Core Dependencies"

        First, install these core dependencies on your __Linux host__:

        Requirement | Notes
        --- | ---
        Docker Engine | [Install Guide](https://docs.docker.com/engine/install/)<br><small>Note, you do not need to use Docker Desktop, Docker Engine is sufficient.</small>
    
    !!! step "Step 2 - Install CLI Tools"

        Next, install these CLI tools on your __Linux host__:

        Requirement | Notes
        --- | ---
        CLI: `argocd` | [Install Guide](https://argo-cd.readthedocs.io/en/stable/cli_installation/) <sup>(also on Homebrew for Linux)</sup>
        CLI: `jq` | [Install Guide](https://jqlang.github.io/jq/download/) <sup>(also on Homebrew for Linux)</sup>
        CLI: `k3d` | [Install Guide](https://k3d.io/stable/#installation) <sup>(also on Homebrew for Linux)</sup>
        CLI: `kubectl` | [Install Guide](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/) <sup>(also on Homebrew for Linux)</sup>

        ??? question_secondary "How do I use Homebrew for Linux?"
    
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
    !!! step "Step 3 - Inotify Limits"
    
        On __Linux__, you may need to increase your system's open/watched file limits.

        1. Modify `/etc/sysctl.conf` to include the following lines:
            - `fs.inotify.max_user_instances = 1280`
            - `fs.inotify.max_user_watches = 655360`
        2. Reload sysctl configs by running `sudo sysctl -p`

=== "Windows"

    !!! step "Step 1 - Install Host Dependencies"
    
        Install these dependencies on your __Windows host__:
        
        Requirement | Notes
        --- | ---
        Windows Subsystem for Linux (WSL 2) | [Install Guide](https://learn.microsoft.com/en-us/windows/wsl/install)
        Docker Desktop | [Install Guide](https://docs.docker.com/desktop/install/windows-install/)
    
    !!! step "Step 2 - Configure WSL"

        Configure WSL to use our [__custom kernel__](https://github.com/deployKF/WSL2-Linux-Kernel) that properly supports Kubernetes (specifically Istio).

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

        !!! question_secondary "Why do we need a custom kernel?"
        
            - For context on why a custom kernel is needed, see [`deployKF/deployKF#41`](https://github.com/deployKF/deployKF/issues/41).
            - To see what changes we have made to the kernel, review [`deployKF/WSL2-Linux-Kernel`](https://github.com/deployKF/WSL2-Linux-Kernel).
            - Hopefully, once [`microsoft/WSL#8153`](https://github.com/microsoft/WSL/issues/8153) is resolved, we will no longer need a custom kernel.

    !!! step "Step 3 - Install Homebrew"

        Install Homebrew for Linux within your __WSL environment__.
        
        Run these commands in an Ubuntu shell (search `Ubuntu` in start menu):
        
        ```bash
        # install Homebrew for Linux
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        
        # add 'brew' to your PATH
        # NOTE: reopen your shell for this to take effect
        (echo; echo 'eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"') >> ~/.profile
        ```

    !!! step "Step 4 - Install WSL Dependencies"

        Install these dependencies within your Ubuntu shell (search `Ubuntu` in start menu):
        
        Requirement | Notes
        --- | ---
        CLI: [`argocd`](https://argo-cd.readthedocs.io/en/stable/cli_installation/) | RUN: `brew install argocd`
        CLI: [`jq`](https://jqlang.github.io/jq/download/) | RUN: `brew install jq`
        CLI: [`k3d`](https://k3d.io/) | RUN: `brew install k3d`
        CLI: [`kubectl`](https://kubernetes.io/docs/tasks/tools/install-kubectl-macos/) | RUN: `brew install kubectl`

        For the rest of the guide, unless otherwise instructed, run all commands in an Ubuntu shell.

## 2. Prepare Kubernetes

deployKF can run on any [:custom-kubernetes-color: __Kubernetes__](https://kubernetes.io/) cluster, in any cloud or local environment.

For this quickstart, we will be using the [`k3d`](https://k3d.io/) command line tool which runs [K3s Clusters](https://k3s.io/) inside Docker.
K3s is an extremely lightweight Kubernetes distribution that is fully compliant with the Kubernetes API, while also being very similar to a cloud-based cluster.


!!! step "Step 1 - Create a k3d Cluster"

    Run this command to create a local `k3d` cluster named `deploykf`:
    
    ```bash
    # NOTE: this will change your kubectl context to the new cluster
    k3d cluster create "deploykf" \
      --image "rancher/k3s:v1.27.10-k3s2"
    ```

    ??? question_secondary "Can I use a different version of Kubernetes?"
    
        Yes. The `--image` flag allows you to specify the version of Kubernetes.
        You may use any version of the [`rancher/k3s`](https://hub.docker.com/r/rancher/k3s/tags) image which corresponds to a version of Kubernetes that is [supported by deployKF](../releases/version-matrix.md#deploykf-dependencies).

!!! step "Step 2 - Wait for Cluster to be Ready"

    Wait until the cluster is ready before continuing, ensure all Pods are in a `Running` or `Completed` state.

    Here are some ways to check the status of Pods, we highly recommend trying `k9s`!

    === "Get Pods Status: `kubectl`"

        You can use `kubectl` to check the status of all pods, in all namespaces:
    
        ```bash
        kubectl get -A pods
        ```
    
        The list of pods will look similar to this (see the `STATUS` column):
    
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

    === ":star: Get Pods Status: `k9s` :star:"
    
        [`k9s`](https://k9scli.io/) makes interacting with Kubernetes much easier by providing a text-based management interface for any Kubernetes cluster.
        You can [install `k9s`](https://k9scli.io/topics/install/) from Homebrew on macOS or Linux:

        ```bash
        brew install k9s
        ```
        
        ---

        To check the status of all pods in all namespaces:

        1. Run `k9s` in your terminal
        1. Presh `shift` + `:` to open the command prompt - _(tip: press `escape` to close any prompt)_
        1. Type `pods` and press `enter` - _(tip: press `tab` to autocomplete resource names)_
        1. Press `0` to show all namespaces
        1. Scroll through the list of pods and check the `STATUS` column
        1. Quit `k9s` by pressing `ctrl` + `c`

        The resulting list of pods will look similar to this (see the `STATUS` column):

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

        ??? question_secondary "What else can `k9s` do?"

            For more information about the features of `k9s`, see the [k9s documentation](https://k9scli.io/), or press `?` to view the help menu.

            __Some useful features:__

            - When viewing a list of resources, press `/` to open the search prompt - _(tip: press `escape` to close any prompt)_
            - When highlighting any resource, press `y` to view its YAML
            - When highlighting any resource, press `d` to describe it
            - When highlighting any resource, press `e` to open a `vim` editor for its YAML
            - When highlighting a pod, press `l` to view its logs
            - When highlighting a pod, press `s` to open an interactive shell
            - When highlighting a secret, press `x` to view its base64-decoded data

            __Filtering by namespace:__

            1. Press `shift` + `:` to open the command prompt
            2. Type `ns` and press `enter`
            3. Select the namespace you want to view and press `enter` (will open list of pods in that namespace)
            4. Press `shift` + `:` to open the command prompt
            5. Type the name of a resource type (e.g. `service` or `secret`) and press `enter`
            
            Note, recently viewed namespaces are given a number (e.g. `1`, `2`, `3`), press that number to show all instances of the currently selected resource type in that namespace.

## 3. Prepare ArgoCD

deployKF uses [:custom-argocd-color: __ArgoCD__](./dependencies/argocd.md#what-is-argo-cd) to apply manifests to your Kubernetes cluster.

For this quickstart, we will use the [deployKF ArgoCD Plugin](https://github.com/deployKF/deployKF/tree/main/argocd-plugin) which adds a special kind of ArgoCD `Application` that produces deployKF manifests.
This allows us to define the platform using a single app-of-apps which only needs your [values](#about-values), and a [deployKF version](#deploykf-versions).

!!! step "Step 1 - Verify kubectl Context"

    We need to ensure that our `kubectl` context is set to the new `k3d` cluster.
    This is so we don't accidentally install ArgoCD into the wrong cluster.

    Run this command and ensure the output is `k3d-deploykf` (or the name of your cluster):
    
    ```bash
    # get the name of the current kubectl context
    kubectl config current-context
    ```
    
    ---

    ??? question_secondary "How do I change my kubectl context?"
    
        We recommend using [`kubectx`](https://github.com/ahmetb/kubectx) to manage your `kubectl` contexts.
        
        You may install `kubectx` from Homebrew on macOS or Linux:

        ```bash
        brew install kubectx
        ```
        
        To change your context with `kubectx`, run these commands:
    
        ```bash
        # list all contexts
        kubectx
    
        # set the current context to 'k3d-deploykf'
        kubectx "k3d-deploykf"
        ```
  
        ---

        Note, the `kubectx` command will be interactive if you install `fzf`:

        ```bash
        brew install fzf
        ```

!!! step "Step 2 - Install ArgoCD"

    We will now install ArgoCD (and the deployKF ArgoCD Plugin) by running a script from the deployKF repo:

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
    
!!! step "Step 3 - Wait for ArgoCD to be Ready"

    After the script completes, wait for all pods in the `argocd` Namespace to be in a `Running` state.

    See how to do this with `k9s` or `kubectl` in the [previous section](#2-prepare-kubernetes).

## 4. Create ArgoCD Applications

### __deployKF Versions__

Each deployKF version may include different [ML & Data tools](../reference/tools.md) or support different versions of cluster dependencies.
See the [version matrix](../releases/version-matrix.md) for an overview, and the [changelog](../releases/changelog-deploykf.md) for detailed information about what changed in each release (including important tips for upgrading).

!!! step ""
    
    For this quickstart, we will be using deployKF [`{{ latest_deploykf_version }}`](https://github.com/deployKF/deployKF/releases/tag/v{{ latest_deploykf_version }}).

### __About Values__

All aspects of deployKF are configured via a centralized set of YAML-based configs named "values".
Learn more about creating your own values files on the [values](./values.md) page.

!!! step ""

    For this quickstart, we will be using the [`sample-values.yaml`](https://github.com/deployKF/deployKF/blob/v{{ latest_deploykf_version }}/sample-values.yaml) file as our base.
    These sample values have all supported [ML & Data tools](../reference/tools.md#tool-index) enabled, along with some sensible security defaults.

### __Create an App-of-Apps__

The only resource you manually create is the `deploykf-app-of-apps`, this resource generates all the other `Application` resources.
Think of it as a _"single source of truth"_ for the desired state of your platform.

!!! step "Step 1 - Define App-of-Apps Resource" 

    Use the following sample as a starting point for your `deploykf-app-of-apps` resource.
    If you want to customize the platform, see the [configure deployKF](./configs.md) guide.

    ---

    This app-of-apps will use deployKF [version](#deploykf-versions) `{{ latest_deploykf_version }}`, 
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

!!! step "Step 2 - Apply App-of-Apps Resource"

    You will need to apply the `deploykf-app-of-apps` resource to your Kubernetes cluster.

    You can apply the resource using either the CLI or the ArgoCD Web UI:

    === ":star: Apply: `kubectl` :star:"
    
        Create a local file named `deploykf-app-of-apps.yaml` with the contents of the app-of-apps YAML above.

        Next, ensure your `kubectl` context is set to the `k3d-deploykf` cluster.

        Finally, apply the resource to your cluster with the following command:

        ```bash
        kubectl apply -f ./deploykf-app-of-apps.yaml
        ```

    === "Apply: ArgoCD Web UI"

        Use `kubectl` port-forwarding to expose the ArgoCD Web UI on your local machine:
    
        ```shell
        kubectl port-forward --namespace "argocd" svc/argocd-server 8090:https
        ```
    
        The ArgoCD Web UI should now be available at the following URL:

          :material-arrow-right-bold: [https://localhost:8090](https://localhost:8090)
    
        ---

        Retrieve the initial password for the `admin` user:
        
        ```shell
        echo $(kubectl -n argocd get secret/argocd-initial-admin-secret \
          -o jsonpath="{.data.password}" | base64 -d)
        ```

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

!!! step "Step - Sync ArgoCD Applications"

    For this quickstart, we will use the ArgoCD CLI via our automated [`sync_argocd_apps.sh`](https://github.com/deployKF/deployKF/blob/main/scripts/sync_argocd_apps.sh) script.

    Run the following commands to use the sync script:
    
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

## 6. Try the Platform

The _deployKF dashboard_ is the web-based interface for deployKF, it gives users authenticated access to tools like [Kubeflow Pipelines](../reference/tools.md#kubeflow-pipelines), [Kubeflow Notebooks](../reference/tools.md#kubeflow-notebooks), and [Katib](../reference/tools.md#katib).

![deployKF Dashboard (Dark Mode)](../assets/images/deploykf-dashboard-DARK.png#only-dark)
![deployKF Dashboard (Light Mode)](../assets/images/deploykf-dashboard-LIGHT.png#only-light)

All public deployKF services (including the dashboard) are accessed via your _deployKF Istio Gateway_, to use the gateway, you will need to expose its Kubernetes Service.

For this quickstart, we will be using the port-forward feature of `kubectl` to expose the gateway locally on your machine:

!!! step "Step 1 - Modify Hosts"

    The _deployKF Istio Gateway_ uses the HTTP `Host` header to route requests to the correct internal service.
    This means that using `localhost` or `127.0.0.1` will NOT work.

    We must add a host entry so that `deploykf.example.com` resolves to `127.0.0.1`:
    
    === "macOS"
    
        You will need to add the following lines to the END of your __local__ `/etc/hosts` file:
    
        ```text
        127.0.0.1 deploykf.example.com
        127.0.0.1 argo-server.deploykf.example.com
        127.0.0.1 minio-api.deploykf.example.com
        127.0.0.1 minio-console.deploykf.example.com
        ```
    
    === "Linux"
    
        You will need to add the following lines to the END of your __local__ `/etc/hosts` file:
    
        ```text
        127.0.0.1 deploykf.example.com
        127.0.0.1 argo-server.deploykf.example.com
        127.0.0.1 minio-api.deploykf.example.com
        127.0.0.1 minio-console.deploykf.example.com
        ```
    
    === "Windows"
    
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

!!! step "Step 2 - Port-Forward the Gateway"
    
    You may now port-forward the `deploykf-gateway` Service using this `kubectl` command:
    
    ```shell
    kubectl port-forward \
      --namespace "deploykf-istio-gateway" \
      svc/deploykf-gateway 8080:http 8443:https
    ```
    
    The deployKF dashboard should now be available on your local machine at:
        
      :material-arrow-right-bold: [https://deploykf.example.com:8443/](https://deploykf.example.com:8443/)

    ---

    !!! warning "Port-Forwards Known Issues"
    
        There are upstream issues which can cause you to need to __restart the port-forward__, see [`kubernetes/kubernetes#74551`](https://github.com/kubernetes/kubernetes/issues/74551) for more information.

!!! step "Step 3 - Log in to the Dashboard"

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

## Next Steps

- [:material-rocket-launch: Build a production-ready deployKF platform!](getting-started.md)
- [:material-account-group: Join the deployKF community!](../about/community.md)
- [:star: Support us with a star on GitHub!](https://github.com/deployKF/deployKF)
- [<span style="color: #ff1f1f">:material-hospital-box:</span> Get support from our experts!](../about/support.md)
