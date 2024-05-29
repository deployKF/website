---
icon: material/script-text
description: >-
  The main changelog for deployKF.
---

# Changelog - deployKF

This changelog lists releases of __deployKF__ that are found in the [`deployKF/deployKF`](https://github.com/deployKF/deployKF/releases) repository.

---

!!! danger

    Carefully review the ___"Upgrade Notes"___ and ___"Important Notes"___ before [upgrading deployKF](../guides/upgrade.md) to a new version.<br><br>Also review the [tool versions](./tool-versions.md) and [version matrix](./version-matrix.md) pages.

??? question_secondary "Can I be notified of new releases?"

    Yes. Watch the [`deployKF/deployKF`](https://github.com/deployKF/deployKF) repo on GitHub.<br>At the top right, click `Watch` → `Custom` → `Releases` then confirm by selecting `Apply`.

??? question_secondary "What about pre-releases?"

    For a changelog that includes pre-releases, see the [full-changelog](./full-changelog-deploykf.md).


---

## [__0.1.5__](https://github.com/deployKF/deployKF/releases/tag/v0.1.5) (2024-05-28) { #0.1.5 }

??? warning "Upgrade Notes"

    
    - We strongly recommend updating to this version for security reasons.
    - As always, if your deployKF platform is critical to your organization, you should test this upgrade in a non-production cluster. We have done extensive testing, but you could encounter unexpected issues.
    - Please update your [`sync_argocd_apps.sh`](https://github.com/deployKF/deployKF/blob/main/scripts/sync_argocd_apps.sh) script version BEFORE SYNCING 0.1.5.
    - The sample values for 0.1.4 had some values that will conflict with 0.1.5, __YOU MUST REMOVE THEM__ from your custom values when upgrading:
         - `kubeflow_tools.pipelines.kfpV2.defaultPipelineRoot`
         - `kubeflow_tools.pipelines.kfpV2.minioFix`
         - `kubeflow_tools.pipelines.kfpV2.launcherImage`
    - We have updated the default embedded Istio version to 1.17.8. To make the process of updating the sidecar images easier, we now provide the [`update_istio_sidecars.sh`](https://github.com/deployKF/deployKF/blob/main/scripts/update_istio_sidecars.sh) script to restart pods with incorrect istio sidecar container versions. Warning, running this script will cause DISRUPTION, especially to Notebooks, so ensure your users have saved their work!
    - If you have followed the [Air-Gapped Clusters](https://www.deploykf.org/guides/platform/offline/) guide, you must mirror the new images/charts used in 0.1.5, and update the corresponding values. For an overview of which images have changed, see the [diff of `default_values.yaml`](https://gist.github.com/thesuperzapper/68094346da699f91b5e0c6fb9eb2b17f/revisions?diff=split) from 0.1.4 to 0.1.5. Warning, DO NOT continue using the old images/charts with 0.1.5, as this will not work.
    

??? info "Important Notes"

    
    - __deployKF Dashboard:__
        - We have grouped the sidebar links from Kubeflow Pipelines into their own section.
        - Users can now see their profiles with "view" and "edit" access on the "Manage Contributors" page.
    - __Kubeflow Pipelines:__
         - This release includes a [patched version](https://github.com/deployKF/kubeflow-pipelines) of Kubeflow Pipelines 2.1.0 which is specially designed to be backward compatible with all V1 and V2-compatible pipelines.
         - When doing an in-place upgrade, you will not automatically have the V2 tutorial pipelines added to your cluster. You may want to upload them manually as "shared" pipeline definitions (find the YAML files attached to the GitHub release).
    - __Kubeflow Notebooks:__
         - We have updated the default Kubeflow Notebooks images to the ones shipped with upstream 1.8.0, these provide significant version bumps for all packages, including TensorFlow 2.13.0 and PyTorch 2.1.0. These images will be updated further in the next release.
         - Please note, we have only updated the DEFAULT IMAGES, which will not affect any existing notebooks. To update existing Notebooks, you must delete and recreate them (data stored in the home directory PVC will be persisted, and you can re-attach it to the new notebooks).
    - __ARM Support:__
         - For those waiting on full ARM64 support, there are now only two remaining components preventing this. The Kubeflow Notebooks backend (which will be updated in the next release), and Kubeflow Pipelines (which needs some help upstream, see [#10309](https://github.com/kubeflow/pipelines/issues/10309) to help).
    - __Istio:__
         - While the default version of Istio (`1.17.8`) is very old, you can easily update to a newer version that is [supported by deployKF](https://www.deploykf.org/releases/version-matrix/#istio) by updating the [`deploykf_dependencies.istio.charts`](https://github.com/deployKF/deployKF/blob/v0.1.5/generator/default_values.yaml#L233-L244) and [`deploykf_core.deploykf_istio_gateway.charts.istioGateway`](https://github.com/deployKF/deployKF/blob/v0.1.5/generator/default_values.yaml#L691-L700) values.
         - We provide the [`update_istio_sidecars.sh`](https://github.com/deployKF/deployKF/blob/main/scripts/update_istio_sidecars.sh) script to restart pods with incorrect Istio sidecar container versions. Warning, running this script will cause DISRUPTION, especially to Notebooks, so ensure your users have saved their work!
         - In the next minor release, we will do a significant update to the default Istio version, and drop out-of-the-box support for very old Kubernetes versions.
    - __Kyverno:__
         - We still have a [hard dependency](https://www.deploykf.org/releases/version-matrix/#kyverno) on Kyverno 1.10.0 due to issues upstream. Hopefully, this will change in the next deployKF version as we test and implement support for the recently released Kyverno 1.12 (which is NOT supported in deployKF 0.1.5).
         - This means that you are still unable to bring your own Kyverno deployment (unless it happens to be the 1.10.0 version). Once this is not the case, we will release a proper "use existing Kyverno" guide like we have [for Istio](https://www.deploykf.org/guides/dependencies/istio/#can-i-use-my-existing-istio).
    

??? abstract "What's Changed"


    <h4>Significant Changes</h4>

    * docs: add `update_istio_sidecars.sh` script by [@thesuperzapper](https://github.com/thesuperzapper) in [#132](https://github.com/deployKF/deployKF/pull/132)
    * feat: update to Kubeflow Pipelines 2.1.0 by [@thesuperzapper](https://github.com/thesuperzapper) in [#122](https://github.com/deployKF/deployKF/pull/122)
    * feat: update dashboard to 0.1.1 + update sidebar links by [@thesuperzapper](https://github.com/thesuperzapper) in [#163](https://github.com/deployKF/deployKF/pull/163)
    * feat: update default notebook images to 1.8.0 by [@thesuperzapper](https://github.com/thesuperzapper) in [#164](https://github.com/deployKF/deployKF/pull/164)

    <h4>New Features</h4>

    * feat: update oauth2-proxy to 7.6.0 by [@thesuperzapper](https://github.com/thesuperzapper) in [#152](https://github.com/deployKF/deployKF/pull/152)
    * feat: update cert-manager to 1.12.10 by [@thesuperzapper](https://github.com/thesuperzapper) in [#153](https://github.com/deployKF/deployKF/pull/153)
    * feat: update dex to 2.39.1 by [@thesuperzapper](https://github.com/thesuperzapper) in [#155](https://github.com/deployKF/deployKF/pull/155)
    * feat: update kubectl container to 1.26.15 by [@thesuperzapper](https://github.com/thesuperzapper) in [#156](https://github.com/deployKF/deployKF/pull/156)
    * feat: update default istio to 1.17.8 by [@thesuperzapper](https://github.com/thesuperzapper) in [#157](https://github.com/deployKF/deployKF/pull/157)
    * feat: update default minio to `RELEASE.2024-05-10T01-41-38Z` by [@thesuperzapper](https://github.com/thesuperzapper) in [#158](https://github.com/deployKF/deployKF/pull/158)
    * feat: update default mysql to 8.0.37 by [@thesuperzapper](https://github.com/thesuperzapper) in [#159](https://github.com/deployKF/deployKF/pull/159)
    * feat: update profile-controller and kfam to 1.8.0 by [@thesuperzapper](https://github.com/thesuperzapper) in [#162](https://github.com/deployKF/deployKF/pull/162)
    * feat: update trust-manager to 0.9.2 by [@thesuperzapper](https://github.com/thesuperzapper) in [#154](https://github.com/deployKF/deployKF/pull/154)

    <h4>Improvements</h4>

    * improve: support `argocd.appNamePrefix` in argocd sync script by [@thesuperzapper](https://github.com/thesuperzapper) in [#108](https://github.com/deployKF/deployKF/pull/108)
    * improve: add robots.txt to deny all user-agents by [@thesuperzapper](https://github.com/thesuperzapper) in [#106](https://github.com/deployKF/deployKF/pull/106)

    <h4>Bug Fixes</h4>

    * fix: argocd sync script only seeing first app in each group by [@thesuperzapper](https://github.com/thesuperzapper) in [#109](https://github.com/deployKF/deployKF/pull/109)
    * fix: require pruning in sync script by [@thesuperzapper](https://github.com/thesuperzapper) in [#123](https://github.com/deployKF/deployKF/pull/123)
    * fix: require bash 4.4+ for sync script by [@thesuperzapper](https://github.com/thesuperzapper) in [#126](https://github.com/deployKF/deployKF/pull/126)
    * fix: script should sync apps that failed their last sync by [@thesuperzapper](https://github.com/thesuperzapper) in [#151](https://github.com/deployKF/deployKF/pull/151)
    * fix: minio not starting, upstream removed curl by [@thesuperzapper](https://github.com/thesuperzapper) in [#165](https://github.com/deployKF/deployKF/pull/165)
    * fix: stop embedded mysql log spam about `mysql_native_password` by [@thesuperzapper](https://github.com/thesuperzapper) in [#167](https://github.com/deployKF/deployKF/pull/167)

    <h4>Documentation</h4>

    * docs: update default argocd to 2.10.4 by [@thesuperzapper](https://github.com/thesuperzapper) in [#114](https://github.com/deployKF/deployKF/pull/114)
    * docs: add argocd helm example for plugin by [@thesuperzapper](https://github.com/thesuperzapper) in [#121](https://github.com/deployKF/deployKF/pull/121)
    * docs: remove confusing sample values by [@thesuperzapper](https://github.com/thesuperzapper) in [#160](https://github.com/deployKF/deployKF/pull/160)
    * docs: update default argocd to 2.10.11 by [@thesuperzapper](https://github.com/thesuperzapper) in [#166](https://github.com/deployKF/deployKF/pull/166)
    

---

## [__0.1.4__](https://github.com/deployKF/deployKF/releases/tag/v0.1.4) (2024-02-16) { #0.1.4 }

??? warning "Upgrade Notes"

    
    - There will be some downtime for Kubeflow Pipelines and users will be forced to re-authenticate.
    - You __MUST sync with pruning enabled__, as we have changed a number of resources.
    - If you are using our automated ArgoCD Sync Script:
        - Update to the latest script version, [found in the `main` branch](https://github.com/deployKF/deployKF/blob/main/scripts/sync_argocd_apps.sh).
        - Ensure you respond "yes" to all "Do you want to sync with PRUNING enabled?" prompts.
        - To prevent the need to sync twice, please manually delete this `ClusterPolicy` using the following command BEFORE syncing: `kubectl delete clusterpolicy "kubeflow-pipelines--generate-profile-resources"`
        - (otherwise, the first sync will time-out waiting for `kf-tools--pipelines` to be healthy)
    

??? info "Important Notes"

    
    - We no longer use Kyverno to generate resources in each profile for Kubeflow Pipelines, we now include these resources directly based on your profile values, this is due to Kyverno not scaling well for large numbers of profiles. However, we still use Kyverno for cloning Secrets across namespaces, triggering restarts of Deployments, and a few other things.
    - We have resolved the compatibility issues with __Azure AKS__. To enable the Azure-specific fixes, please set the `kubernetes.azure.admissionsEnforcerFix` value to `true`.
    - There have been significant changes to how authentication is implemented. These changes should allow you to bring your own Istio Gateway Deployment (Pods) without having other services end up behind deployKF's authentication system. However, please note that deployKF still manages its own Gateway Resource (CRD).
    - For those experiencing "route not found" issues when using an external proxy to terminate TLS, you can now disable "SNI Matching" on the Istio Gateway by setting the `deploykf_core.deploykf_istio_gateway.gateway.tls.matchSNI` value to `false`.
    

??? abstract "What's Changed"


    <h4>Significant Changes</h4>

    * feat: allow other istio gateways on ingress deployment by [@thesuperzapper](https://github.com/thesuperzapper) in [#66](https://github.com/deployKF/deployKF/pull/66)
    * feat: allow disabling SNI matching on gateway by [@thesuperzapper](https://github.com/thesuperzapper) in [#83](https://github.com/deployKF/deployKF/pull/83)
    * fix: issues preventing deployment on Azure AKS by [@thesuperzapper](https://github.com/thesuperzapper) in [#85](https://github.com/deployKF/deployKF/pull/85)
    * improve: stop using kyverno to provision kfp profile resources by [@thesuperzapper](https://github.com/thesuperzapper) in [#102](https://github.com/deployKF/deployKF/pull/102)

    <h4>New Features</h4>

    * feat: disable default plugins and resource-quotas in specific profiles by [@thesuperzapper](https://github.com/thesuperzapper) in [#67](https://github.com/deployKF/deployKF/pull/67)
    * feat: allow custom external service ports by [@thesuperzapper](https://github.com/thesuperzapper) in [#82](https://github.com/deployKF/deployKF/pull/82)
    * feat: allow disabling HTTPS redirect by [@thesuperzapper](https://github.com/thesuperzapper) in [#86](https://github.com/deployKF/deployKF/pull/86)
    * feat: add pod-labels value for cert-manager controller by [@thesuperzapper](https://github.com/thesuperzapper) in [#88](https://github.com/deployKF/deployKF/pull/88)
    * feat: optional sign-in page to stop background request CSRF accumulation by [@thesuperzapper](https://github.com/thesuperzapper) in [#100](https://github.com/deployKF/deployKF/pull/100)

    <h4>Improvements</h4>

    * improve: use `__Secure-` cookie prefix and remove domains config by [@thesuperzapper](https://github.com/thesuperzapper) in [#87](https://github.com/deployKF/deployKF/pull/87)
    * improve: increase kyverno resource limits and add values by [@thesuperzapper](https://github.com/thesuperzapper) in [#93](https://github.com/deployKF/deployKF/pull/93)
    * improve: use CRD-level "replace" for kyverno ArgoCD app by [@thesuperzapper](https://github.com/thesuperzapper) in [#94](https://github.com/deployKF/deployKF/pull/94)
    * improve: argocd sync script should only wait for app health once by [@thesuperzapper](https://github.com/thesuperzapper) in [#104](https://github.com/deployKF/deployKF/pull/104)

    <h4>Bug Fixes</h4>

    * fix: prevent kyverno log spam on missing generate context by [@thesuperzapper](https://github.com/thesuperzapper) in [#54](https://github.com/deployKF/deployKF/pull/54)
    * fix: rstudio logo format for non-chrome browsers by [@thesuperzapper](https://github.com/thesuperzapper) in [#56](https://github.com/deployKF/deployKF/pull/56)
    * fix: using AWS IRSA with Kubeflow Pipelines by [@thesuperzapper](https://github.com/thesuperzapper) in [#79](https://github.com/deployKF/deployKF/pull/79)
    * fix: use 307 status for HTTP redirects by [@thesuperzapper](https://github.com/thesuperzapper) in [#81](https://github.com/deployKF/deployKF/pull/81)
    * fix: proxy protocol envoyfilter for istio gateway by [@thesuperzapper](https://github.com/thesuperzapper) in [#80](https://github.com/deployKF/deployKF/pull/80)
    * fix: disallow out-of-band KFP audience when disabled by [@thesuperzapper](https://github.com/thesuperzapper) in [#89](https://github.com/deployKF/deployKF/pull/89)
    * fix: support kyverno chart changes (but keep kyverno version) by [@thesuperzapper](https://github.com/thesuperzapper) in [#92](https://github.com/deployKF/deployKF/pull/92)
    * fix: annotate cloned imagePullSecrets to be ignored by ArgoCD by [@dkhachyan](https://github.com/dkhachyan) in [#90](https://github.com/deployKF/deployKF/pull/90)
    * fix: add background filter to restart trigger policies by [@thesuperzapper](https://github.com/thesuperzapper) in [#95](https://github.com/deployKF/deployKF/pull/95)
    * fix: prevent CSRF cookie accumulation on auth expiry by [@thesuperzapper](https://github.com/thesuperzapper) in [#99](https://github.com/deployKF/deployKF/pull/99)

    <h4>Documentation</h4>

    * docs: update example ArgoCD to 2.9.6 by [@thesuperzapper](https://github.com/thesuperzapper) in [#91](https://github.com/deployKF/deployKF/pull/91)
    

---

## [__0.1.3__](https://github.com/deployKF/deployKF/releases/tag/v0.1.3) (2023-10-31) { #0.1.3 }

??? info "Important Notes"

    
    - For more information about using the new "browser login flow" with _Kubeflow Pipelines SDK_, please see the updated [Access Kubeflow Pipelines API](https://www.deploykf.org/user-guides/access-kubeflow-pipelines-api/) guide.
    

??? abstract "What's Changed"


    <h4>Significant Changes</h4>

    * feat: browser-based KFP SDK auth by [@thesuperzapper](https://github.com/thesuperzapper) in [#45](https://github.com/deployKF/deployKF/pull/45)

    <h4>New Features</h4>

    * feat: update oauth2-proxy to 7.5.1 by [@thesuperzapper](https://github.com/thesuperzapper) in [#44](https://github.com/deployKF/deployKF/pull/44)
    * feat: kyverno policy for image-pull-secrets by [@thesuperzapper](https://github.com/thesuperzapper) in [#47](https://github.com/deployKF/deployKF/pull/47)
    * feat: add values for kyverno replicas by [@thesuperzapper](https://github.com/thesuperzapper) in [#50](https://github.com/deployKF/deployKF/pull/50)

    <h4>Improvements</h4>

    * improve: limit trigger operations for kyverno policies by [@thesuperzapper](https://github.com/thesuperzapper) in [#49](https://github.com/deployKF/deployKF/pull/49)

    <h4>Bug Fixes</h4>

    * fix: don't mount trust bundles with own cert-manager by [@thesuperzapper](https://github.com/thesuperzapper) in [#46](https://github.com/deployKF/deployKF/pull/46)
    * fix: ensure kyverno has permission to manage PodDefaults by [@thesuperzapper](https://github.com/thesuperzapper) in [#51](https://github.com/deployKF/deployKF/pull/51)

    <h4>Documentation</h4>

    * docs: update sync script to force update kyverno policies by [@thesuperzapper](https://github.com/thesuperzapper) in [#40](https://github.com/deployKF/deployKF/pull/40)
    * docs: add requirement checks to argocd sync script by [@thesuperzapper](https://github.com/thesuperzapper) in [#42](https://github.com/deployKF/deployKF/pull/42)
    * docs: update reference argocd version to 2.8.5 by [@thesuperzapper](https://github.com/thesuperzapper) in [#52](https://github.com/deployKF/deployKF/pull/52)

    <h4>Miscellaneous</h4>

    * refactor: always use `v1` kyverno resources by [@thesuperzapper](https://github.com/thesuperzapper) in [#48](https://github.com/deployKF/deployKF/pull/48)
    

---

## [__0.1.2__](https://github.com/deployKF/deployKF/releases/tag/v0.1.2) (2023-09-22) { #0.1.2 }

??? info "Important Notes"

    
    - If you are using the [`deployKF ArgoCD Plugin`](https://github.com/deployKF/deployKF/tree/main/argocd-plugin), you MUST update to the latest version of the plugin BEFORE upgrading to this version (see: [#29](https://github.com/deployKF/deployKF/pull/29)).
    

??? abstract "What's Changed"


    <h4>Significant Changes</h4>

    * docs: add reference `sync_argocd_apps.sh` script by [@thesuperzapper](https://github.com/thesuperzapper) in [#38](https://github.com/deployKF/deployKF/pull/38)

    <h4>Bug Fixes</h4>

    * fix: set kyverno webhook failure policy to ignore (fix uninstall deadlock) by [@thesuperzapper](https://github.com/thesuperzapper) in [#26](https://github.com/deployKF/deployKF/pull/26)
    * fix: resolve cert-manager race conditions by [@thesuperzapper](https://github.com/thesuperzapper) in [#28](https://github.com/deployKF/deployKF/pull/28)
    * fix: argocd plugin with "file://" dependencies (needed for helm forks) by [@thesuperzapper](https://github.com/thesuperzapper) in [#29](https://github.com/deployKF/deployKF/pull/29)
    * fix: create separate namespaces app, if destination is remote by [@thesuperzapper](https://github.com/thesuperzapper) in [#30](https://github.com/deployKF/deployKF/pull/30)
    * fix: ensure namespaces are never deleted or pruned by [@thesuperzapper](https://github.com/thesuperzapper) in [#31](https://github.com/deployKF/deployKF/pull/31)
    * fix: add sync waves to argocd apps (fix deletion) by [@thesuperzapper](https://github.com/thesuperzapper) in [#32](https://github.com/deployKF/deployKF/pull/32)
    * fix: resolve profile generator race condition by [@thesuperzapper](https://github.com/thesuperzapper) in [#33](https://github.com/deployKF/deployKF/pull/33)
    * fix: resolve race conditions with cloned secrets by [@thesuperzapper](https://github.com/thesuperzapper) in [#34](https://github.com/deployKF/deployKF/pull/34)
    * fix: app-of-apps should always target argocd cluster by [@thesuperzapper](https://github.com/thesuperzapper) in [#35](https://github.com/deployKF/deployKF/pull/35)

    <h4>Documentation</h4>

    * docs: move guides to website by [@thesuperzapper](https://github.com/thesuperzapper) in [#20](https://github.com/deployKF/deployKF/pull/20)
    * docs: improve example app-of-apps for plugin by [@thesuperzapper](https://github.com/thesuperzapper) in [#37](https://github.com/deployKF/deployKF/pull/37)
    * docs: improve sample values, add reference overrides by [@thesuperzapper](https://github.com/thesuperzapper) in [#36](https://github.com/deployKF/deployKF/pull/36)
    

---

## [__0.1.1__](https://github.com/deployKF/deployKF/releases/tag/v0.1.1) (2023-08-08) { #0.1.1 }

??? abstract "What's Changed"


    <h4>Significant Changes</h4>

    * feat: create argocd plugin by [@thesuperzapper](https://github.com/thesuperzapper) in [#16](https://github.com/deployKF/deployKF/pull/16)

    <h4>New Features</h4>

    * feat: allow custom documentation links in dashboard by [@yankcrime](https://github.com/yankcrime) in [#12](https://github.com/deployKF/deployKF/pull/12)
    * feat: allow a single ArgoCD to manage deployKF across multiple clusters by [@thesuperzapper](https://github.com/thesuperzapper) in [#17](https://github.com/deployKF/deployKF/pull/17)

    <h4>Bug Fixes</h4>

    * fix: set `securityContext.fsGroup` on minio pods by [@thesuperzapper](https://github.com/thesuperzapper) in [#14](https://github.com/deployKF/deployKF/pull/14)
    * fix: minio-console user permissions (update minio) by [@thesuperzapper](https://github.com/thesuperzapper) in [#18](https://github.com/deployKF/deployKF/pull/18)

    <h4>Documentation</h4>

    * docs: improve getting started formatting by [@thesuperzapper](https://github.com/thesuperzapper) in [#8](https://github.com/deployKF/deployKF/pull/8)
    * docs: add links to important values in readme by [@thesuperzapper](https://github.com/thesuperzapper) in [#9](https://github.com/deployKF/deployKF/pull/9)
    * docs: improve getting started guide by [@thesuperzapper](https://github.com/thesuperzapper) in [#11](https://github.com/deployKF/deployKF/pull/11)
    * docs: add link to youtube demo by [@thesuperzapper](https://github.com/thesuperzapper) in [#13](https://github.com/deployKF/deployKF/pull/13)
    

---

## [__0.1.0__](https://github.com/deployKF/deployKF/releases/tag/v0.1.0) (2023-07-10) { #0.1.0 }

??? abstract "What's Changed"


    <h4>Significant Changes</h4>

    * initial release 🎉 🎉 🎉 
    
