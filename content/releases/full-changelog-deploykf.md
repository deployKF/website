---
icon: material/script-text
description: >-
  Changelog for deployKF, including pre-releases.

hide:
  - navigation
---

# Changelog (all releases) - deployKF

This changelog lists ALL releases of __deployKF__ (including pre-releases) that are found in the [`deployKF/deployKF`](https://github.com/deployKF/deployKF/releases) repository.

!!! info "Main Changelog"

    For a changelog that hides pre-releases, see [the main changelog](./changelog-deploykf.md) page.

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


## [0.1.0](https://github.com/deployKF/deployKF/releases/tag/v0.1.0) - 2023-07-10
### What's Changed
#### Significant Changes
* initial release 🎉 🎉 🎉 

