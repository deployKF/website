# Install the deployKF CLI

The deployKF command line tool (CLI) is used to generate GitOps-ready Kubernetes manifests from one or more [values files](../reference/deploykf-values.md).
The CLI binaries are distributed via [GitHub releases](https://github.com/deployKF/cli/releases), you will need to download the appropriate binary for your operating system.

=== "macOS"

    !!! warning "macOS Security"
        
        MacOS has security features that will prevent you running the CLI if you downloaded it via a web browser.
        However, if you download it from the command line (for example, using `curl` or `wget`) it should be allowed to run.
        
        Either way, if you encounter a "this app is from an unidentified developer" error you can go to `System Preferences > Privacy & Security` and click `Open Anyway` to allow the CLI to run.

    !!! tip "Latest Version"
        
        You can find the latest version number by visiting the [GitHub releases page](https://github.com/deployKF/cli/releases).

    The following commands will download the CLI for macOS and place it in `/usr/local/bin`:

    ```bash
    DKF_CLI_VERSION="{{ latest_deploykf_cli_version }}"
    DKF_CLI_ARCH="$(uname -m)"
    DFK_CLI_DEST=/usr/local/bin/deploykf
    
    # download the binary
    sudo curl -L "https://github.com/deploykf/cli/releases/download/v${DKF_CLI_VERSION}/deploykf-darwin-${DKF_CLI_ARCH}" -o "${DFK_CLI_DEST}"
    
    # make the binary executable
    sudo chmod +x "${DFK_CLI_DEST}"
    
    # test the binary
    deploykf version
    ```

    Alternatively, you can manually download the latest `deploykf-darwin-{ARCH}` binary from the [GitHub releases page](https://github.com/deployKF/cli/releases), and place it in a directory on your `PATH` environment variable.

    !!! info "Apple Silicon"
       
        If you have a Mac with an Apple Silicon processor (M1, M2, etc), you will need to download the `deploykf-darwin-arm64` binary.
        If you have a Mac with an Intel processor, you will need to download the `deploykf-darwin-amd64` binary.

=== "Linux"

    !!! tip "Latest Version"
        
        You can find the latest version number by visiting the [GitHub releases page](https://github.com/deployKF/cli/releases).

    The following commands will download the CLI for Linux and place it in `/usr/local/bin`:

    ```bash
    DKF_CLI_VERSION="{{ latest_deploykf_cli_version }}"
    DKF_CLI_ARCH="$(uname -m)"
    DFK_CLI_DEST=/usr/local/bin/deploykf

    # download the binary
    sudo curl -L "https://github.com/deploykf/cli/releases/download/v${DKF_CLI_VERSION}/deploykf-linux-${DKF_CLI_ARCH}" -o "${DFK_CLI_DEST}"

    # make the binary executable
    sudo chmod +x "${DFK_CLI_DEST}"

    # test the binary
    deploykf version
    ```

    Alternatively, you can manually download the latest `deploykf-linux-{ARCH}` binary from the [GitHub releases page](https://github.com/deployKF/cli/releases) and place it in a directory on your `PATH` environment variable.

    !!! info "Processor Architecture"
    
        If you are using a Linux machine with an ARM64 processor, you will need to download the `deploykf-linux-arm64` binary.
        If you are using a Linux machine with an X86/AMD64 processor, you will need to download the `deploykf-linux-amd64` binary.

=== "Windows"

    !!! warning "Windows Security"
    
        Windows has security features that may prevent you from running the CLI.
        If you encounter a "Windows protected your PC" error you can click `More info` and then `Run anyway` to allow the CLI to run.

    !!! warning "Elevated PowerShell Prompt"
        
        You will need to run the following commands in an elevated PowerShell prompt (right-click and select `Run as administrator`).

    !!! tip "Latest Version"
        
        You can find the latest version number by visiting the [GitHub releases page](https://github.com/deployKF/cli/releases).

    The following PowerShell commands will download the CLI for Windows and place it in `C:\Windows\System32`:

    ```powershell 
    $DKF_CLI_VERSION="{{ latest_deploykf_cli_version }}"
    $DFK_CLI_DEST="C:\Windows\System32\deploykf.exe"
    
    # download the binary
    Invoke-WebRequest -Uri "https://github.com/deploykf/cli/releases/download/v${DKF_CLI_VERSION}/deploykf-windows-amd64.exe" -OutFile "${DFK_CLI_DEST}"

    # test the binary
    deploykf version
    ```

    Alternatively, you can manually download the latest `deploykf-windows-amd64.exe` binary from the [GitHub releases page](https://github.com/deployKF/cli/releases) and place it in a directory on your `PATH` environment variable.
