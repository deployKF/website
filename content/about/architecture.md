---
description: >-
  A detailed look at the architecture of deployKF and its components.

# disable the mkdocs-macros-plugin for this page
render_macros: false
---

# Architecture of deployKF

This document takes a detailed look at the __architecture of deployKF__ and its components.

---

## Overview

deployKF has three user-facing components:

Component<br><small>(Click for Details)</small> | Description
--- | ---
[__deployKF ArgoCD Plugin__](#deploykf-argocd-plugin) | A plugin for ArgoCD which allows you to use deployKF without rendering manifests into a git repo
[__deployKF CLI__](#deploykf-cli) | A command line program to generate a the Kubernetes manifests, from configs provided in one or more values files
[__deployKF Generator__](#deploykf-generator) | A versioned `.zip` package with the templates and helpers needed to generate the manifests

## deployKF ArgoCD Plugin

The __deployKF ArgoCD Plugin__ is a plugin for ArgoCD which allows you to deploy deployKF without rendering manifests into a git repo, it is developed in the [`deployKF/deployKF`](https://github.com/deployKF/deployKF/tree/main/argocd-plugin) GitHub repo.

## deployKF CLI

The __deployKF CLI__ is a command line program written in Go, it is developed in the [`deployKF/cli`](https://github.com/deploykf/cli) GitHub repo.

### `deploykf generate`

!!! value "Code"

    The code which defines the `deploykf generate` command is found in [`cmd/deploykf/generate.go`](https://github.com/deployKF/cli/blob/main/cmd/deploykf/generate.go).

!!! value "Implementation"

    The `deploykf generate` command is implemented as follows:

    1. Locate the [deployKF Generator](#deploykf-generator) to use, depending on which arguments were provided:
        - `--source-version`: download a generator ZIP from the [GitHub releases of `deploykf/deploykf`](https://github.com/deploykf/deploykf/releases)
        - `--source-path`: use a local generator ZIP or folder with unzipped generator files
    2. Unzip or copy the generator into a temporary folder:
        - The folder is automatically deleted after the command is run, or if the command fails
    3. Read the `.deploykf_generator` marker file from the root of the generator:
        - The `.deploykf_generator` file contains JSON data with information like the `generator_schema` version
        - If the CLI does not support the encountered `generator_schema` version, the CLI will exit with an error
    4. Clean the folder currently at the `--output-dir` target:
        - The CLI will only remove the contents of a non-empty target if there is a `.deploykf_output` marker file at its root
    5. Render the manifests into `--output-dir` in two phases, using the provided `--values` files:
        1. PHASE 1: render the `.gomplateignore_template` files into `.gomplateignore` files (still in the temporary folder)
            - Note, these files behave like `.gitignore` files, and are used to exclude files from the output in the second phase
        2. PHASE 2: render the templates from the `templates` folder into the `--output-dir`
            - Note, the resulting output folder will be structured identically to the `templates` folder (subject to the `.gomplateignore` files)

    The output folder will contain a `.deploykf_output` marker file with the following information in JSON format:

    - `generated_at`: the time the generator was run
    - `source_version`: the source version that was used (if `--source-version` was provided)
    - `source_path`: the path of the source artifact that was used 
    - `source_hash`: the SHA256 hash of the source artifact that was used
    - `cli_version`: the version of the deployKF CLI that was used

## deployKF Generator

The __deployKF Generator__ is a versioned ZIP package which contains all the templates and helpers needed to generate the output folders, it is developed in the [`deployKF/deployKF` ](https://github.com/deploykf/deploykf) GitHub repo.

### Generator Templates

!!! value ""

    The generator templates are rendered using a version of [gomplate](https://docs.gomplate.ca/) that is embedded in the deployKF CLI.
    
    Note, the template delimiters are set to `{{<` and `>}}` as to avoid conflicts with Helm and other Go-like templates.

### Generator ZIP Structure

#### Tree View

```
.
├── .deploykf_generator
├── default_values.yaml
├── helpers/
└── templates/
    ├── .gomplateignore_template
    ├── app-of-apps.yaml
    ├── argocd/
    │   ├── kustomization.yaml
    │   ├── applications/
    │   │   ├── kustomization.yaml
    │   │   ├── namespaces.yaml
    │   │   ├── deploykf-core/
    │   │   ├── deploykf-dependencies/
    │   │   ├── deploykf-opt/
    │   │   ├── deploykf-tools/
    │   │   ├── kubeflow-dependencies/
    │   │   └── kubeflow-tools/
    │   └── namespaces/
    │       ├── kustomization.yaml
    │       ├── deploykf-core/
    │       ├── deploykf-dependencies/
    │       ├── deploykf-opt/
    │       ├── deploykf-tools/
    │       ├── kubeflow-dependencies/
    │       └── kubeflow-tools/
    └── manifests/
        ├── deploykf-core/
        ├── deploykf-dependencies/
        ├── deploykf-opt/
        ├── deploykf-tools/
        ├── kubeflow-dependencies/
        └── kubeflow-tools/
```

#### [`./`](https://github.com/deployKF/deployKF/tree/main/generator)

!!! value ""

    - [`.deploykf_generator`](https://github.com/deployKF/deployKF/blob/main/generator/.deploykf_generator) metadata about the generator:
        - _(JSON format, includes the `generator_schema` version to ensure compatibility with the CLI)_
    - [`default_values.yaml`](https://github.com/deployKF/deployKF/blob/main/generator/default_values.yaml) default [values](../reference/deploykf-values.md) for the generator
    - [`helpers/`](https://github.com/deployKF/deployKF/tree/main/generator/helpers) helpers that are used in the `templates/`
    - [`templates/`](https://github.com/deployKF/deployKF/tree/main/generator/templates) templates that are used to generate the output

#### [`./templates/`](https://github.com/deployKF/deployKF/tree/main/generator/templates)

!!! value ""

    - `.gomplateignore_template` template of a `.gomplateignore` file
    - `app-of-apps.yaml` an [Argo CD app-of-apps](../guides/dependencies/argocd.md) (points to `./argocd/kustomization.yaml`)
    - `argocd/` templates for Argo CD applications and namespaces
    - `manifests/` templates for Helm & Kustomize apps

#### [`./templates/argocd/`](https://github.com/deployKF/deployKF/tree/main/generator/templates/argocd)

!!! value ""

    - `kustomization.yaml` a Kustomize file pointing to `applications/` and `namespaces/`
    - `applications/` templates for Argo CD Applications
    - `namespaces/` templates for Kubernetes Namespaces

#### [`./templates/argocd/applications/`](https://github.com/deployKF/deployKF/tree/main/generator/templates/argocd/applications)

!!! value ""

    - `kustomization.yaml` a Kustomize file pointing to the Argo CD applications
    - `deploykf-core/` Argo CD applications for [`deploykf-core`](../reference/deploykf-values.md#deploykf-core)
    - `deploykf-dependencies/` Argo CD applications for [`deploykf-dependencies`](../reference/deploykf-values.md#deploykf-dependencies)
    - `deploykf-opt/`Argo CD applications for [`deploykf-opt`](../reference/deploykf-values.md#deploykf-opt)
    - `deploykf-tools/` Argo CD applications for [`deploykf-tools`](../reference/deploykf-values.md#deploykf-tools)
    - `kubeflow-dependencies/` Argo CD applications for [`kubeflow-dependencies`](../reference/deploykf-values.md#kubeflow-dependencies)
    - `kubeflow-tools/` Argo CD applications for [`kubeflow-tools`](../reference/deploykf-values.md#kubeflow-tools)

#### [`./templates/argocd/namespaces/`](https://github.com/deployKF/deployKF/tree/main/generator/templates/argocd/namespaces)

!!! value ""

    - `kustomization.yaml` a Kustomize file pointing to the Kubernetes Namespaces
    - `deploykf-core/` Kubernetes Namespaces for [`deploykf-core`](../reference/deploykf-values.md#deploykf-core)
    - `deploykf-dependencies/` Kubernetes Namespaces for [`deploykf-dependencies`](../reference/deploykf-values.md#deploykf-dependencies)
    - `deploykf-opt/` Kubernetes Namespaces for [`deploykf-opt`](../reference/deploykf-values.md#deploykf-opt)
    - `deploykf-tools/` Kubernetes Namespaces for [`deploykf-tools`](../reference/deploykf-values.md#deploykf-tools)
    - `kubeflow-dependencies/` Kubernetes Namespaces for [`kubeflow-dependencies`](../reference/deploykf-values.md#kubeflow-dependencies)
    - `kubeflow-tools/` Kubernetes Namespaces for [`kubeflow-tools`](../reference/deploykf-values.md#kubeflow-tools)

#### [`./templates/manifests/`](https://github.com/deployKF/deployKF/tree/main/generator/templates/manifests)

!!! value ""

    - `kustomization.yaml` a Kustomize file pointing to the Helm & Kustomize apps
    - `deploykf-core/` templated Helm & Kustomize apps for [`deploykf-core`](../reference/deploykf-values.md#deploykf-core)
    - `deploykf-dependencies/` templated Helm & Kustomize apps for [`deploykf-dependencies`](../reference/deploykf-values.md#deploykf-dependencies)
    - `deploykf-opt/` templated Helm & Kustomize apps for [`deploykf-opt`](../reference/deploykf-values.md#deploykf-opt)
    - `deploykf-tools/` templated Helm & Kustomize apps for [`deploykf-tools`](../reference/deploykf-values.md#deploykf-tools)
    - `kubeflow-dependencies/` templated Helm & Kustomize apps for [`kubeflow-dependencies`](../reference/deploykf-values.md#kubeflow-dependencies)
    - `kubeflow-tools/` templated Helm & Kustomize apps for [`kubeflow-tools`](../reference/deploykf-values.md#kubeflow-tools)
