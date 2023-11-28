---
description: >-
  A detailed look at the architecture of deployKF and its components.

# disable the mkdocs-macros-plugin for this page
ignore_macros: true
---

# Architecture of deployKF

This document takes a detailed look at the __architecture of deployKF__ and its components.

---

## Overview

deployKF has two user-facing components:

- [__deployKF CLI:__](#deploykf-cli) a command line program who's primary purpose is to generate a set of folders containing GitOps-ready Kubernetes manifests, from configs provided in one or more values files
- [__deployKF Generator:__](#deploykf-generator) a versioned `.zip` package which contains all the templates and helpers needed to generate the output folders

## deployKF CLI

The __deployKF CLI__ is a command line program written in Go, it is
developed in the [`deployKF/cli` GitHub repo](https://github.com/deploykf/cli).

### Steps of the `deploykf generate` command

1. Locate the [deployKF Generator](#deploykf-generator) to use, depending on which arguments were provided:
    - `--source-version`: download a generator ZIP from the [releases of `deploykf/deploykf` GitHub repo](https://github.com/deploykf/deploykf/releases)
    - `--source-path`: use a local generator ZIP or folder with unzipped generator files
2. Unzip or copy the generator into a temporary folder:
    - The folder is automatically deleted after the command is run, or if the command fails
3. Read the `.deploykf_generator` marker file from the root of the generator:
    - The `.deploykf_generator` file contains JSON data with information like the `generator_schema` version
    - If the CLI does not support the encountered `generator_schema` version, the CLI will exit with an error
4. Clean the folder currently at the `--outut-dir` target:
    - The CLI will only remove the contents of a non-empty target if there is a `.deploykf_output` marker file at its root
5. Render the manifests into `--outut-dir` in two phases, using the provided `--values` files:
    1. PHASE 1: render the `.gomplateignore_template` files into `.gomplateignore` files (still in the temporary folder)
        - Note, these files behave like `.gitignore` files, and are used to exclude files from the output in the second phase
    2. PHASE 2: render the templates from the `templates` folder into the `--output-dir`
        - Note, the resulting output folder will be structured identically to the `templates` folder (subject to the `.gomplateignore` files)

### Notes about the `deploykf generate` command

- The generator templates are rendered using a version of [gomplate](https://docs.gomplate.ca/) that is embedded in the deployKF CLI:
    - The template delimiters are set to `{{<` and `>}}` as to avoid conflicts with Helm and other Go-like templates
- The output folder will contain a `.deploykf_output` marker file which contains the following information in JSON format:
    - `generated_at`: the time the generator was run
    - `source_version`: the source version that was used (if `--source-version` was provided)
    - `source_path`: the path of the source artifact that was used 
    - `source_hash`: the SHA256 hash of the source artifact that was used
    - `cli_version`: the version of the deployKF CLI that was used

## deployKF Generator

The __deployKF Generator__ is a versioned ZIP package which contains all the templates and helpers needed to generate the output folders,
it is developed in the [`deployKF/deployKF` GitHub repo](https://github.com/deploykf/deploykf).

### Structure of generator ZIP

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
    │   ├── deploykf-core/
    │   ├── deploykf-dependencies/
    │   ├── deploykf-opt/
    │   ├── deploykf-tools/
    │   ├── kubeflow-dependencies/
    │   ├── kubeflow-tools/
    │   └── namespaces/
    └── manifests/
        ├── deploykf-core/
        ├── deploykf-dependencies/
        ├── deploykf-opt/
        ├── deploykf-tools/
        ├── kubeflow-dependencies/
        └── kubeflow-tools/
```

### Purpose of each item under `.`

- `.deploykf_generator` a file with metadata about the generator, in JSON format, including the `generator_schema` version
- `default_values.yaml` a file with the default values for this generator version
- `helpers/` a folder with helpers that are used in the `templates/`
- `templates/` a folder with templates that are used to generate the output

### Purpose of each item under `templates/`

- `.gomplateignore_template` is used to generate the `.gomplateignore` files in the first phase of the `deploykf generate` command
- `app-of-apps.yaml` a template for an Argo CD [app of apps](https://argo-cd.readthedocs.io/en/stable/operator-manual/cluster-bootstrapping/#app-of-apps-pattern), which points to `./argocd/kustomization.yaml` (this is the only manifest which is manually applied by the user)
- `argocd/` a folder with templates of Argo CD applications
- `manifests/` a folder with templates of Kubernetes manifests

### Purpose of each item under `templates/argocd/`

- `kustomization.yaml` a [Kustomize](https://kustomize.io/) file pointing to the other Argo CD applications and namespaces (this is the target of the `app-of-apps.yaml`)
- `deploykf-core/` a folder with templates of Argo CD applications for "core components of deployKF"
- `deploykf-dependencies/` a folder with templates of Argo CD applications for "dependencies of deployKF"
- `deploykf-opt/` a folder with templates of Argo CD applications for "optional embedded applications that are used when external alternatives are not configured"
- `deploykf-tools/` a folder with templates of Argo CD applications for "MLOps tools from the deployKF ecosystem"
- `kubeflow-dependencies/` a folder with templates of Argo CD applications for "dependencies of Kubeflow's MLOps tools"
- `kubeflow-tools/` a folder with templates of Argo CD applications for "MLOps tools from the Kubeflow ecosystem"
- `namespaces/` a folder with the templates for Kubernetes Namespaces

### Purpose of each item under `templates/manifests/`

- `deploykf-core/` a folder with templates of Kubernetes manifests for "core components of deployKF"
- `deploykf-dependencies/` a folder with templates of Kubernetes manifests for "dependencies of deployKF"
- `deploykf-opt/` a folder with templates of Kubernetes manifests for "optional embedded applications that are used when external alternatives are not configured"
- `deploykf-tools/` a folder with templates of Kubernetes manifests for "MLOps tools from the deployKF ecosystem"
- `kubeflow-dependencies/` a folder with templates of Kubernetes manifests for "dependencies of Kubeflow's MLOps tools"
- `kubeflow-tools/` a folder with templates of Kubernetes manifests for "MLOps tools from the Kubeflow ecosystem"