---
icon: custom/argocd
description: >-
  Learn how and why deployKF uses Argo CD.
  Learn how to use your existing Argo CD with deployKF and Kubeflow.
---

# Argo CD

Learn how and why deployKF uses Argo CD.
Learn how to use your existing Argo CD with deployKF and Kubeflow.

---

## __What is Argo CD?__

[:custom-argocd-color: __Argo CD__](https://argo-cd.readthedocs.io/en/stable/) is an extremely widely-used tool that helps you programmatically manage the applications deployed on a Kubernetes cluster.

!!! warning ""

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

The _Argo CD Web Interface_ lets you visually manage your cluster, allowing you to view and make changes to Kubernetes resources (including `Applications`).
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

### __What is the deployKF ArgoCD Plugin?__

The [deployKF ArgoCD Plugin](https://github.com/deployKF/deployKF/tree/main/argocd-plugin) is an optional part of deployKF which removes the need to commit manifests to a Git repository.
The plugin adds a special kind of Argo CD [`Application`](#argo-cd-applications) that produces deployKF manifests internally, similar to how Helm charts are used in Argo CD. 

With the plugin, you manage the whole platform from a single _"app of apps"_ `Application` whose specification only needs your [values](../values.md), and a specified _source version_ of deployKF.
For an example of this, see [__this section__](../local-quickstart.md#4-create-argocd-applications) of the local quickstart.

### __Can I use <small>_&lt;other tool&gt;_</small> instead of Argo CD?__
    
Not yet.

While we believe that Argo CD is currently the best in its category, we recognize that it's not the only option.
In the future, we may support other Kubernetes GitOps tools (like [Flux CD](https://fluxcd.io/)), or even build a deployKF-specific solution.

deployKF will make your MLOps life so much easier, that it's still worth using, even if you don't already love Argo CD.
If you want, you can largely treat Argo CD as a "black box" and just use the provided sync scripts to manage the platform.

!!! info

    To learn more about this decision, and participate in the discussion, see [`deployKF/deployKF#110`](https://github.com/deployKF/deployKF/issues/110).

---

## __Can I use my existing Argo CD?__

Yes, you must. 

See our [version matrix](../../releases/version-matrix.md#argo-cd) for a list of supported Argo CD versions, then follow the [Getting Started](../getting-started.md) guide to install deployKF with your existing Argo CD.

### __Can I use an off-cluster ArgoCD?__

Yes.
deployKF supports the Argo CD "management cluster" pattern, where multiple target clusters are managed by a single Argo CD.

??? step "Step 1 - Configure `destination` and `appNamePrefix`"

    When using an off-cluster ArgoCD, you must set the [`argocd.destination`](https://github.com/deployKF/deployKF/blob/v0.1.4/generator/default_values.yaml#L56-L61) value to target the correct cluster.
    
    You must also set the [`argocd.appNamePrefix`](https://github.com/deployKF/deployKF/blob/v0.1.4/generator/default_values.yaml#L8-L13) value to avoid conflicting ArgoCD application names (which is needed because multiple sets of them may exist in the management cluster).

    For example, say you have [defined a remote cluster](https://argo-cd.readthedocs.io/en/stable/operator-manual/declarative-setup/#clusters) named `"my-cluster1"` on your Argo CD management cluster.
    The following values will prefix all application names with `"cluster1-"` and target them to the named destination `"my-cluster1"`:

    ```yaml
    argocd:
      ## a prefix to use for argocd application names
      appNamePrefix: "cluster1-"
    
      ## the destination used for deployKF argocd applications
      destination:
        name: "my-cluster1"
    ```

    !!! warning "Destination MUST be remote"
    
        When the `argocd.appNamePrefix` value is non-empty, the `argocd.destination` MUST be a remote cluster (that is, you should not run deployKF on your management cluster).

??? step "Step 2 - Update App-of-Apps"

    Your app-of-apps `Application` MUST target the management cluster, NOT the remote cluster, only the internal `Applications` will target the remote cluster.

    Also, you must set the `app.kubernetes.io/part-of` label to `{argocd.appNamePrefix}deploykf`, so the sync script works correctly.

    For example, your app-of-apps `Application` might look like this:

    ```yaml
    apiVersion: argoproj.io/v1alpha1
    kind: Application
    metadata:
      name: {argocd.appNamePrefix}deploykf-app-of-apps
      namespace: argocd
      labels:
        app.kubernetes.io/name: deploykf-app-of-apps
        app.kubernetes.io/part-of: {argocd.appNamePrefix}deploykf
    spec:
      ## NOTE: This project ONLY applies to the app-of-apps itself, not the internal Applications.
      ##       It needs to create Applications in the management cluster and Namespaces in the target.
      ##       The project used by internal Applications is set by the `argocd.project` value.
      project: default

      source:
        ...
        ...
        ...

      destination:
        ## OPTION 1: target the management cluster with `server`
        server: "https://kubernetes.default.svc"

        ## OPTION 2: target the management cluster with `name`
        #name: "in-cluster"
    ```

??? step "Step 3 - Update Sync Script"

    By default, the [`sync_argocd_apps.sh`](https://github.com/deployKF/deployKF/blob/main/scripts/sync_argocd_apps.sh) script assumes that `argocd.appNamePrefix` is not set.

    Update the `ARGOCD_APP_NAME_PREFIX` variable at the top of the script to match your `argocd.appNamePrefix` value.

    ```bash
    ARGOCD_APP_NAME_PREFIX="cluster1-"
    ```

    __TIP:__ make sure you have your `kubectl` context set to the __management cluster__ (NOT your target cluster), before running the sync script.
