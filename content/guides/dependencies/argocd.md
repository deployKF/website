---
icon: custom/argocd
description: >-
  Learn how and why deployKF uses Argo CD.
---

# Argo CD

Learn how and why deployKF uses Argo CD.

---

## __What is Argo CD?__

[:custom-argocd-color: __Argo CD__](https://argo-cd.readthedocs.io/en/stable/) is an extremely widely-used tool that helps you programmatically manage the applications deployed on a Kubernetes cluster.

!!! warning "Argo CD vs Argo Workflows"

    Please note that _Argo CD_ is a __completely different tool__ from _Argo Workflows_, they just have similar names.
    
    <table markdown="span">
      <tr markdown>
        <th markdown>[__Argo CD__](https://argo-cd.readthedocs.io/en/stable/)</th>
        <td markdown>Manages the state of Kubernetes resources.</td>
      </tr>
      <tr markdown>
        <th markdown>[__Argo Workflows__](https://argoproj.github.io/argo-workflows/)</th>
        <td markdown>Runs DAG workflows in Pods on Kubernetes.<br><small>(Used by [Kubeflow Pipelines](../../reference/tools.md#kubeflow-pipelines))</small></td>
      </tr>
    </table>

### Argo CD Applications

The main config for Argo CD is the [`Application`](https://argo-cd.readthedocs.io/en/stable/user-guide/application-specification/), a Kubernetes [custom resource](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/) that specifies Kubernetes manifests for Argo CD to deploy and manage (typically from a git repository).

An _"app of apps"_ is a pattern where a single Argo CD `Application` contains other `Application` definitions, this is typically done to make bootstrapping large applications easier.

### Argo CD Interfaces

The _Argo CD Web Interface_ lets you visually manage your cluster, allowing you to view and make changes to Kubernetes resources (including [`Applications`](#argo-cd-applications)).
While the [CLI](https://argo-cd.readthedocs.io/en/stable/user-guide/commands/argocd/) and [REST API](https://cd.apps.argoproj.io/swagger-ui) allow you to manage everything programmatically.

!!! image ""

    <div class="image-wrapper">
    ![Argo CD Web UI (Dark Mode)](../../assets/images/argocd-ui-DARK.png#only-dark)
    ![Argo CD Web UI (Light Mode)](../../assets/images/argocd-ui-LIGHT.png#only-light)
    </div>

    <div class="image-caption">
    The __ArgoCD Web UI__ allows you to view and manage your cluster.
    </div>

---

## __How does deployKF use Argo CD?__

Argo CD is a core part of deployKF, it helps us manage the lifecycle and state of all components in the platform.
For example, we use Argo CD for:

- __Applying__ manifests to the cluster, in a defined order
- __Detecting__ when applications are out-of-sync
- __Syncing__ applications to their desired state
- __Pruning__ old manifests which are no longer needed
- __Programmatically__ managing all of the above

### __Can I use my existing Argo CD?__

Yes, you must.
See our [version matrix](../../releases/version-matrix.md#deploykf-dependencies) for a list of supported Argo CD versions and the [getting started](../getting-started.md#argocd-configuration) guide for configuration details.

### __Can I use <small>_&lt;other tool&gt;_</small> instead of Argo CD?__
    
No, not yet. 
While we believe that Argo CD is currently the best in its category, we recognize that it's not the only option.
In the future, we may support other Kubernetes GitOps tools (like [Flux CD](https://fluxcd.io/)), or even build a deployKF-specific solution.

We think deployKF is good enough to try, even if you don't love Argo CD!

!!! info

    To learn more about this decision, and participate in the discussion, see [`deployKF/deployKF#110`](https://github.com/deployKF/deployKF/issues/110).

### __Can a single Argo CD deploy multiple clusters?__

Yes.
However, as Argo CD `Applications` must have unique names, we provide the [`argocd.appNamePrefix`](https://github.com/deployKF/deployKF/blob/v0.1.4/generator/default_values.yaml#L8-L13) value to prefix all Application names.

For example, to set a prefix of `"cluster1-"`, you might use the following values:

```yaml
argocd:
  appNamePrefix: "cluster1-"
```

When `argocd.appNamePrefix` is non-empty, the [`argocd.destination`](https://github.com/deployKF/deployKF/blob/v0.1.4/generator/default_values.yaml#L56-L61) MUST be a remote cluster (note, the [default is "in-cluster"](https://github.com/deployKF/deployKF/blob/v0.1.4/generator/default_values.yaml#L60)).
For example, if you have [defined an Argo CD cluster](https://argo-cd.readthedocs.io/en/stable/operator-manual/declarative-setup/#clusters) named `"my-cluster1"`, you might use the following values:

```yaml
argocd:
  destination:
    name: "my-cluster1"
```

!!! warning "Sync Script"

    By default, the [`sync_argocd_apps.sh`](https://github.com/deployKF/deployKF/blob/main/scripts/sync_argocd_apps.sh) script assumes that `argocd.appNamePrefix` is not set.
    Update the `ARGOCD_APP_NAME_PREFIX` variable at the top of the script to match your `argocd.appNamePrefix` value.

    ```bash
    ARGOCD_APP_NAME_PREFIX="cluster1-"
    ```

---

## __What is the _deployKF ArgoCD Plugin_?__

The [deployKF ArgoCD Plugin](https://github.com/deployKF/deployKF/tree/main/argocd-plugin) is an optional part of deployKF which removes the need to commit manifests to a Git repository.
The plugin adds a special kind of Argo CD `Application` that produces deployKF manifests internally, similar to how Helm charts are used in Argo CD. 

With the plugin, you manage the whole platform from a single _"app of apps"_ `Application` whose specification only needs your [values](../getting-started.md#2-platform-configuration), and a specified [source version](../getting-started.md#deploykf-versions) of deployKF.
For an example of this, see [__this section__](../local-quickstart.md#create-an-app-of-apps) of the local quickstart.