---
icon: material/view-list
description: >-
  Learn deployKF values (configs) and how to configure them.
---

# Values

Learn deployKF values (configs) and how to configure them.

---

## Overview

All aspects of your deployKF platform are configured with YAML-based configs named __"values"__.
There are a very large number of values (more than 1500), but as deployKF supports [_in-place upgrades_](./upgrade.md) you can start with a few important ones, and then grow your values file over time.

See the [configuring deployKF](./configs.md) page for guides that explain common configuration tasks.

## Custom Values

When you set a value, you are overriding its default.
The defaults may vary between deployKF versions, and are found in the corresponding [`default_values.yaml`](https://github.com/deployKF/deployKF/blob/v{{ latest_deploykf_version }}/generator/default_values.yaml) file.

For example, to connect Kubeflow Pipelines to an external MySQL database, you might set the following values in your `custom-values.yaml` file:

```yaml
kubeflow_tools:
  pipelines:
    mysql:
      useExternal: true
      host: "mysql.example.com"
      port: 3306
      auth:
        ## WARNING: in the real world, read the credentials from a secret
        ##          see https://www.deploykf.org/guides/external/mysql/
        username: my-username
        password: my-password
```

!!! tip "YAML Syntax"

    For a refresher on YAML syntax, we recommend the following resources:
    
    - [Learn YAML in Y minutes](https://learnxinyminutes.com/docs/yaml/)
    - [YAML Multiline Strings](https://yaml-multiline.info/)

## Sample Values

We recommend using the [`sample-values.yaml`](https://github.com/deployKF/deployKF/blob/v{{ latest_deploykf_version }}/sample-values.yaml) file as a starting point for your custom values.
Each version of deployKF has a corresponding `sample-values.yaml` file with all supported [ML & Data tools](../reference/tools.md#tool-index) enabled, along with some sensible security defaults.

There are two main ways to use the sample values file:

1. __Directly:__ Copy the `sample-values.yaml` file and make changes directly to that file.
2. __Overrides:__ Include the `sample-values.yaml` file first, and then override specific values in later files.
   We provide the [`sample-values-overrides.yaml`](https://github.com/deployKF/deployKF/blob/v{{ latest_deploykf_version }}/sample-values-overrides.yaml) file as an example of this approach.

The following commands will download the sample files for the latest deployKF version:

```bash
# download the `sample-values.yaml` file
curl -fL -o "sample-values-{{ latest_deploykf_version }}.yaml" \
  "https://raw.githubusercontent.com/deployKF/deployKF/v{{ latest_deploykf_version }}/sample-values.yaml"
  
# download the `sample-values-overrides.yaml` file
curl -fL -o "sample-values-overrides-{{ latest_deploykf_version }}.yaml" \
  "https://raw.githubusercontent.com/deployKF/deployKF/v{{ latest_deploykf_version }}/sample-values-overrides.yaml"
```

!!! info "All Values"

    The `sample-values.yaml` file is a great starting point, but it does NOT include all possible values.

    For your reference, ALL values and their defaults are listed on the [values reference](../reference/deploykf-values.md) page, 
    which is generated from the full [`default_values.yaml`](https://github.com/deployKF/deployKF/blob/v{{ latest_deploykf_version }}/generator/default_values.yaml) file of the latest deployKF version.

## Merging Values

You may define your custom values in __one or more files__, which together form the complete "desired state" of your deployKF platform.

When multiple values files are used, they are merged together __in the order they are passed__ to the `deploykf` command or plugin.
This means that if a value is defined in multiple files, the last one wins.

!!! warning "Merging Lists"

    List values are NOT merged.
    If a list is redefined, the new list will replace the old one in full.

### Example

This example will demonstrate how values are merged together.
Including both map-type and list-type values.
In this example, we have two values files:

??? code "values-1.yaml"

    ```yaml
    deploykf_core:
      deploykf_auth:
        dex:
          staticPasswords:
            - email: "user1@example.com"
              password:
                value: "password1"

            - email: "user2@example.com"
              password:
                value: "password2"
    
    kubeflow_tools:
      pipelines:
        mysql:
          host: "mysql_OLD.example.com"
    ```

??? code "values-2.yaml"

    ```yaml
    deploykf_core:
      deploykf_auth:
        dex:
          staticPasswords:
            - email: "user3@example.com"
              password:
                value: "password3"

    kubeflow_tools:
      pipelines:
        mysql:
          host: "mysql_NEW.example.com"
    ```

=== "Manifests Repo Mode"

    In [manifests repo mode](./modes.md), if you pass these files to the `deploykf` command in the following order:
    
    ```bash
    deploykf generate \
      --source-version "{{ latest_deploykf_version }}" \
      --values ./values-1.yaml \
      --values ./values-2.yaml \
      --output-dir ./GENERATOR_OUTPUT
    ```

=== "ArgoCD Plugin Mode"

    In [ArgoCD plugin mode](./modes.md), if you pass these files under `values_files` in the following order:

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
        ##  - assuming you have committed the following files:
        ##    sample-values-{{ latest_deploykf_version }}.yaml, values-1.yaml, values-2.yaml
        ##
        repoURL: "https://github.com/<EXAMPLE_ORG>/<EXAMPLE_REPO>.git"
        targetRevision: "main"
        path: "."
    
        ## plugin configuration
        ##
        plugin:
          name: "deploykf"
          parameters:
    
            ## the deployKF generator version
            ##
            - name: "source_version"
              string: "{{ latest_deploykf_version }}"
    
            ## paths to values files within the `repoURL` repository
            ##
            - name: "values_files"
              array:
                - "./sample-values-{{ latest_deploykf_version }}.yaml"
                - "./values-1.yaml"
                - "./values-2.yaml"

            ## a string containing the contents of a values file
            ##  - we are not using this in this example
            ##  - values defined here have the highest precedence
            ##
            #- name: "values"
            #  string: |
            #    ...
            #    values file contents
            #    ...
    ```

The resulting "merged" values will be as follows (with the default values omitted for brevity):

```yaml
deploykf_core:
  deploykf_auth:
    dex:
      ## NOTE: list values are NOT merged, they are replaced in full
      staticPasswords:
        - email: "user3@example.com"
          password:
            value: "password3"

kubeflow_tools:
  pipelines:
    mysql:
      ## NOTE: for map values, the last one wins
      host: "mysql_NEW.example.com"
```