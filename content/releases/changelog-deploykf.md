---
icon: material/script-text
description: >-
  The main changelog for deployKF.
---

# Changelog - deployKF

This changelog lists releases of __deployKF__ that are found in the [`deployKF/deployKF`](https://github.com/deployKF/deployKF/releases) repository.

---

!!! warning "Upgrade Steps"

    Please review the _"Upgrade Notes"_ and/or _"Important Notes"_ __before__ upgrading deployKF.<br>For more information about upgrading, see the [upgrade guide](../guides/upgrade.md).

!!! question_secondary "How can I get notified about new releases?"

    Watch the [`deployKF/deployKF`](https://github.com/deployKF/deployKF) repo on GitHub.<br>At the top right, click `Watch` → `Custom` → `Releases` then confirm by selecting `Apply`.

!!! info "Pre-releases"

    For a changelog that includes pre-releases, see the [full-changelog](./full-changelog-deploykf.md).


## [0.1.4](https://github.com/deployKF/deployKF/releases/tag/v0.1.4) - 2024-02-16
### Upgrade Notes

- There will be some downtime for Kubeflow Pipelines and users will be forced to re-authenticate.
- You __MUST sync with pruning enabled__, as we have changed a number of resources.
- If you are using our automated ArgoCD Sync Script:
    - Update to the latest script version, [found in the `main` branch](https://github.com/deployKF/deployKF/blob/main/scripts/sync_argocd_apps.sh).
    - Ensure you respond "yes" to all "Do you want to sync with PRUNING enabled?" prompts.
    - To prevent the need to sync twice, please manually delete this `ClusterPolicy` using the following command BEFORE syncing: `kubectl delete clusterpolicy "kubeflow-pipelines--generate-profile-resources"`
    - (otherwise, the first sync will time-out waiting for `kf-tools--pipelines` to be healthy)

### Important Notes

- We no longer use Kyverno to generate resources in each profile for Kubeflow Pipelines, we now include these resources directly based on your profile values, this is due to Kyverno not scaling well for large numbers of profiles. However, we still use Kyverno for cloning Secrets across namespaces, triggering restarts of Deployments, and a few other things.
- We have resolved the compatibility issues with __Azure AKS__. To enable the Azure-specific fixes, please set the `kubernetes.azure.admissionsEnforcerFix` value to `true`.
- There have been significant changes to how authentication is implemented. These changes should allow you to bring your own Istio Gateway Deployment (Pods) without having other services end up behind deployKF's authentication system. However, please note that deployKF still manages its own Gateway Resource (CRD).
- For those experiencing "route not found" issues when using an external proxy to terminate TLS, you can now disable "SNI Matching" on the Istio Gateway by setting the `deploykf_core.deploykf_istio_gateway.gateway.tls.matchSNI` value to `false`.

### What's Changed
#### Significant Changes
* feat: allow other istio gateways on ingress deployment by [@thesuperzapper](https://github.com/thesuperzapper) in [#66](https://github.com/deployKF/deployKF/pull/66)
* feat: allow disabling SNI matching on gateway by [@thesuperzapper](https://github.com/thesuperzapper) in [#83](https://github.com/deployKF/deployKF/pull/83)
* fix: issues preventing deployment on Azure AKS by [@thesuperzapper](https://github.com/thesuperzapper) in [#85](https://github.com/deployKF/deployKF/pull/85)
* improve: stop using kyverno to provision kfp profile resources by [@thesuperzapper](https://github.com/thesuperzapper) in [#102](https://github.com/deployKF/deployKF/pull/102)
#### New Features
* feat: disable default plugins and resource-quotas in specific profiles by [@thesuperzapper](https://github.com/thesuperzapper) in [#67](https://github.com/deployKF/deployKF/pull/67)
* feat: allow custom external service ports by [@thesuperzapper](https://github.com/thesuperzapper) in [#82](https://github.com/deployKF/deployKF/pull/82)
* feat: allow disabling HTTPS redirect by [@thesuperzapper](https://github.com/thesuperzapper) in [#86](https://github.com/deployKF/deployKF/pull/86)
* feat: add pod-labels value for cert-manager controller by [@thesuperzapper](https://github.com/thesuperzapper) in [#88](https://github.com/deployKF/deployKF/pull/88)
* feat: optional sign-in page to stop background request CSRF accumulation by [@thesuperzapper](https://github.com/thesuperzapper) in [#100](https://github.com/deployKF/deployKF/pull/100)
#### Improvements
* improve: use `__Secure-` cookie prefix and remove domains config by [@thesuperzapper](https://github.com/thesuperzapper) in [#87](https://github.com/deployKF/deployKF/pull/87)
* improve: increase kyverno resource limits and add values by [@thesuperzapper](https://github.com/thesuperzapper) in [#93](https://github.com/deployKF/deployKF/pull/93)
* improve: use CRD-level "replace" for kyverno ArgoCD app by [@thesuperzapper](https://github.com/thesuperzapper) in [#94](https://github.com/deployKF/deployKF/pull/94)
* improve: argocd sync script should only wait for app health once by [@thesuperzapper](https://github.com/thesuperzapper) in [#104](https://github.com/deployKF/deployKF/pull/104)
#### Bug Fixes
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
#### Documentation
* docs: update example ArgoCD to 2.9.6 by [@thesuperzapper](https://github.com/thesuperzapper) in [#91](https://github.com/deployKF/deployKF/pull/91)


---

## [0.1.3](https://github.com/deployKF/deployKF/releases/tag/v0.1.3) - 2023-10-31
### Important Notes

- For more information about using the new "browser login flow" with _Kubeflow Pipelines SDK_, please see the updated [Access Kubeflow Pipelines API](https://www.deploykf.org/user-guides/access-kubeflow-pipelines-api/) guide.

### What's Changed
#### Significant Changes
* feat: browser-based KFP SDK auth by [@thesuperzapper](https://github.com/thesuperzapper) in [#45](https://github.com/deployKF/deployKF/pull/45)
#### New Features
* feat: update oauth2-proxy to 7.5.1 by [@thesuperzapper](https://github.com/thesuperzapper) in [#44](https://github.com/deployKF/deployKF/pull/44)
* feat: kyverno policy for image-pull-secrets by [@thesuperzapper](https://github.com/thesuperzapper) in [#47](https://github.com/deployKF/deployKF/pull/47)
* feat: add values for kyverno replicas by [@thesuperzapper](https://github.com/thesuperzapper) in [#50](https://github.com/deployKF/deployKF/pull/50)
#### Improvements
* improve: limit trigger operations for kyverno policies by [@thesuperzapper](https://github.com/thesuperzapper) in [#49](https://github.com/deployKF/deployKF/pull/49)
#### Bug Fixes
* fix: don't mount trust bundles with own cert-manager by [@thesuperzapper](https://github.com/thesuperzapper) in [#46](https://github.com/deployKF/deployKF/pull/46)
* fix: ensure kyverno has permission to manage PodDefaults by [@thesuperzapper](https://github.com/thesuperzapper) in [#51](https://github.com/deployKF/deployKF/pull/51)
#### Documentation
* docs: update sync script to force update kyverno policies by [@thesuperzapper](https://github.com/thesuperzapper) in [#40](https://github.com/deployKF/deployKF/pull/40)
* docs: add requirement checks to argocd sync script by [@thesuperzapper](https://github.com/thesuperzapper) in [#42](https://github.com/deployKF/deployKF/pull/42)
* docs: update reference argocd version to 2.8.5 by [@thesuperzapper](https://github.com/thesuperzapper) in [#52](https://github.com/deployKF/deployKF/pull/52)
#### Miscellaneous
* refactor: always use `v1` kyverno resources by [@thesuperzapper](https://github.com/thesuperzapper) in [#48](https://github.com/deployKF/deployKF/pull/48)


---

## [0.1.2](https://github.com/deployKF/deployKF/releases/tag/v0.1.2) - 2023-09-22
### Important Notes

- If you are using the [`deployKF ArgoCD Plugin`](https://github.com/deployKF/deployKF/tree/main/argocd-plugin), you MUST update to the latest version of the plugin BEFORE upgrading to this version (see: [#29](https://github.com/deployKF/deployKF/pull/29)).

### What's Changed
#### Significant Changes
* docs: add reference `sync_argocd_apps.sh` script by [@thesuperzapper](https://github.com/thesuperzapper) in [#38](https://github.com/deployKF/deployKF/pull/38)
#### Bug Fixes
* fix: set kyverno webhook failure policy to ignore (fix uninstall deadlock) by [@thesuperzapper](https://github.com/thesuperzapper) in [#26](https://github.com/deployKF/deployKF/pull/26)
* fix: resolve cert-manager race conditions by [@thesuperzapper](https://github.com/thesuperzapper) in [#28](https://github.com/deployKF/deployKF/pull/28)
* fix: argocd plugin with "file://" dependencies (needed for helm forks) by [@thesuperzapper](https://github.com/thesuperzapper) in [#29](https://github.com/deployKF/deployKF/pull/29)
* fix: create separate namespaces app, if destination is remote by [@thesuperzapper](https://github.com/thesuperzapper) in [#30](https://github.com/deployKF/deployKF/pull/30)
* fix: ensure namespaces are never deleted or pruned by [@thesuperzapper](https://github.com/thesuperzapper) in [#31](https://github.com/deployKF/deployKF/pull/31)
* fix: add sync waves to argocd apps (fix deletion) by [@thesuperzapper](https://github.com/thesuperzapper) in [#32](https://github.com/deployKF/deployKF/pull/32)
* fix: resolve profile generator race condition by [@thesuperzapper](https://github.com/thesuperzapper) in [#33](https://github.com/deployKF/deployKF/pull/33)
* fix: resolve race conditions with cloned secrets by [@thesuperzapper](https://github.com/thesuperzapper) in [#34](https://github.com/deployKF/deployKF/pull/34)
* fix: app-of-apps should always target argocd cluster by [@thesuperzapper](https://github.com/thesuperzapper) in [#35](https://github.com/deployKF/deployKF/pull/35)
#### Documentation
* docs: move guides to website by [@thesuperzapper](https://github.com/thesuperzapper) in [#20](https://github.com/deployKF/deployKF/pull/20)
* docs: improve example app-of-apps for plugin by [@thesuperzapper](https://github.com/thesuperzapper) in [#37](https://github.com/deployKF/deployKF/pull/37)
* docs: improve sample values, add reference overrides by [@thesuperzapper](https://github.com/thesuperzapper) in [#36](https://github.com/deployKF/deployKF/pull/36)


---

## [0.1.1](https://github.com/deployKF/deployKF/releases/tag/v0.1.1) - 2023-08-08
### What's Changed
#### Significant Changes
* feat: create argocd plugin by [@thesuperzapper](https://github.com/thesuperzapper) in [#16](https://github.com/deployKF/deployKF/pull/16)
#### New Features
* feat: allow custom documentation links in dashboard by [@yankcrime](https://github.com/yankcrime) in [#12](https://github.com/deployKF/deployKF/pull/12)
* feat: allow a single ArgoCD to manage deployKF across multiple clusters by [@thesuperzapper](https://github.com/thesuperzapper) in [#17](https://github.com/deployKF/deployKF/pull/17)
#### Bug Fixes
* fix: set `securityContext.fsGroup` on minio pods by [@thesuperzapper](https://github.com/thesuperzapper) in [#14](https://github.com/deployKF/deployKF/pull/14)
* fix: minio-console user permissions (update minio) by [@thesuperzapper](https://github.com/thesuperzapper) in [#18](https://github.com/deployKF/deployKF/pull/18)
#### Documentation
* docs: improve getting started formatting by [@thesuperzapper](https://github.com/thesuperzapper) in [#8](https://github.com/deployKF/deployKF/pull/8)
* docs: add links to important values in readme by [@thesuperzapper](https://github.com/thesuperzapper) in [#9](https://github.com/deployKF/deployKF/pull/9)
* docs: improve getting started guide by [@thesuperzapper](https://github.com/thesuperzapper) in [#11](https://github.com/deployKF/deployKF/pull/11)
* docs: add link to youtube demo by [@thesuperzapper](https://github.com/thesuperzapper) in [#13](https://github.com/deployKF/deployKF/pull/13)


---

## [0.1.0](https://github.com/deployKF/deployKF/releases/tag/v0.1.0) - 2023-07-10
### What's Changed
#### Significant Changes
* initial release 🎉 🎉 🎉 

