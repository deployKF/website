---
description: >-
  Learn how to install the deployKF CLI.
---
# Install deployKF CLI

Learn how to install the deployKF CLI (command line interface).

---

## About the CLI

The deployKF CLI is used to generate GitOps-ready Kubernetes manifests from one or more [values files](../reference/deploykf-values.md).
This example generates manifests under the `./GENERATOR_OUTPUT` directory from the `{{ latest_deploykf_version }}` source version with the values specified in the `./custom-values.yaml` file.

```bash
deploykf generate \
  --source-version "{{ latest_deploykf_version }}" \
  --values ./custom-values.yaml \
  --output-dir ./GENERATOR_OUTPUT
```

!!! info "Source Version"

    The `--source-version` is a tagged release of the [deployKF generator](https://github.com/deployKF/deployKF/releases), without the "v" prefix.

    The version of the CLI does NOT need to match the `--source-version`. 
    If a breaking change is ever needed, the CLI will fail to generate with newer source versions, and will print message telling you to upgrade the CLI.

!!! note "deployKF ArgoCD Plugin"

    If you are using the [deployKF ArgoCD Plugin](https://github.com/deployKF/deployKF/tree/main/argocd-plugin), it is NOT necessary to install the deployKF CLI,
    this is because the manifests generation will happen inside the ArgoCD plugin, rather than on your local machine.

---

## Install the CLI

You can install the CLI on your local machine by following the instructions below that are appropriate for your operating system.

!!! info "Latest Version"
    
    You can find the latest version of the CLI on the [GitHub releases page](https://github.com/deployKF/cli/releases), which is currently [`v{{ latest_deploykf_cli_version }}`](https://github.com/deployKF/cli/releases/tag/v{{ latest_deploykf_cli_version }}).

=== "macOS"

    !!! warning "macOS Security"
        
        macOS has security features that will prevent you running the CLI if you downloaded it via a web browser.
        However, if you download it from the command line (for example, using `curl` or `wget`) it should be allowed to run.
        
        Either way, if you encounter a "this app is from an unidentified developer" error you can go to `System Preferences > Privacy & Security` and click `Open Anyway` to allow the CLI to run.

    The following commands will download the CLI for macOS and place it in `/usr/local/bin`:

    ```bash
    DKF_CLI_VERSION="{{ latest_deploykf_cli_version }}"
    DKF_CLI_ARCH=$(uname -m | sed -e 's/x86_64/amd64/')
    DFK_CLI_DEST=/usr/local/bin/deploykf
    
    # download the binary
    sudo curl -fL "https://github.com/deploykf/cli/releases/download/v${DKF_CLI_VERSION}/deploykf-darwin-${DKF_CLI_ARCH}" -o "${DFK_CLI_DEST}"
    
    # make the binary executable
    sudo chmod +x "${DFK_CLI_DEST}"
    
    # test the binary
    deploykf version
    ```

    Alternatively, you can manually download the latest `deploykf-darwin-{ARCH}` binary from the [`v{{ latest_deploykf_cli_version }}` GitHub Release](https://github.com/deployKF/cli/releases/tag/v{{ latest_deploykf_cli_version }}) and place it in a directory on your `PATH` environment variable.

    !!! info "Apple Silicon"
       
        If you have a Mac with an Apple Silicon processor (M1, M2, etc), you will need to download the `deploykf-darwin-arm64` binary.
        If you have a Mac with an Intel processor, you will need to download the `deploykf-darwin-amd64` binary.

=== "Linux"

    The following commands will download the CLI for Linux and place it in `/usr/local/bin`:

    ```bash
    DKF_CLI_VERSION="{{ latest_deploykf_cli_version }}"
    DKF_CLI_ARCH=$(uname -m | sed -e 's/x86_64/amd64/' -e 's/aarch64/arm64/')
    DFK_CLI_DEST=/usr/local/bin/deploykf

    # download the binary
    sudo curl -fL "https://github.com/deploykf/cli/releases/download/v${DKF_CLI_VERSION}/deploykf-linux-${DKF_CLI_ARCH}" -o "${DFK_CLI_DEST}"

    # make the binary executable
    sudo chmod +x "${DFK_CLI_DEST}"

    # test the binary
    deploykf version
    ```

    Alternatively, you can manually download the latest `deploykf-linux-{ARCH}` binary from the [`v{{ latest_deploykf_cli_version }}` GitHub Release](https://github.com/deployKF/cli/releases/tag/v{{ latest_deploykf_cli_version }}) and place it in a directory on your `PATH` environment variable.

    !!! info "Processor Architecture"
    
        If you are using a Linux machine with an ARM64 processor, you will need to download the `deploykf-linux-arm64` binary.
        If you are using a Linux machine with an X86/AMD64 processor, you will need to download the `deploykf-linux-amd64` binary.

=== "Windows"

    !!! warning "Elevated PowerShell Prompt"
        
        You will need to run the following commands in an elevated PowerShell prompt (right-click and select `Run as administrator`).

    !!! warning "Windows Security"
    
        Windows has security features that may prevent you from running the CLI.
        If you encounter a "Windows protected your PC" error you can click `More info` and then `Run anyway` to allow the CLI to run.

    The following PowerShell commands will download the CLI for Windows and place it in `C:\Windows\System32`:

    ```powershell 
    $DKF_CLI_VERSION="{{ latest_deploykf_cli_version }}"
    $DFK_CLI_DEST="C:\Windows\System32\deploykf.exe"
    
    # download the binary
    Invoke-WebRequest -Uri "https://github.com/deploykf/cli/releases/download/v${DKF_CLI_VERSION}/deploykf-windows-amd64.exe" -OutFile "${DFK_CLI_DEST}"

    # test the binary
    deploykf version
    ```

    Alternatively, you can manually download the latest `deploykf-windows-amd64.exe` binary from the [`v{{ latest_deploykf_cli_version }}` GitHub Release](https://github.com/deployKF/cli/releases/tag/v{{ latest_deploykf_cli_version }}) and place it in a directory on your `PATH` environment variable.
