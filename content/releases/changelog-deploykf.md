---
icon: material/script-text
---

# Changelog - deployKF

This changelog lists releases of __deployKF__ that are found in the [`deployKF/deployKF`](https://github.com/deployKF/deployKF/releases) repository.

!!! info "Pre-releases"

    For a changelog that shows pre-releases, see [the full-changelog](./full-changelog-deploykf.md) page.

---

## [0.1.2](https://github.com/deployKF/deployKF/releases/tag/v0.1.2) - 2023-09-22

### Significant Changes
* docs: add reference `sync_argocd_apps.sh` script by [@thesuperzapper](https://github.com/thesuperzapper) in [#38](https://github.com/deployKF/deployKF/pull/38)

### Bug Fixes
* fix: set kyverno webhook failure policy to ignore (fix uninstall deadlock) by [@thesuperzapper](https://github.com/thesuperzapper) in [#26](https://github.com/deployKF/deployKF/pull/26)
* fix: resolve cert-manager race conditions by [@thesuperzapper](https://github.com/thesuperzapper) in [#28](https://github.com/deployKF/deployKF/pull/28)
* fix: argocd plugin with "file://" dependencies (needed for helm forks) by [@thesuperzapper](https://github.com/thesuperzapper) in [#29](https://github.com/deployKF/deployKF/pull/29)
* fix: create separate namespaces app, if destination is remote by [@thesuperzapper](https://github.com/thesuperzapper) in [#30](https://github.com/deployKF/deployKF/pull/30)
* fix: ensure namespaces are never deleted or pruned by [@thesuperzapper](https://github.com/thesuperzapper) in [#31](https://github.com/deployKF/deployKF/pull/31)
* fix: add sync waves to argocd apps (fix deletion) by [@thesuperzapper](https://github.com/thesuperzapper) in [#32](https://github.com/deployKF/deployKF/pull/32)
* fix: resolve profile generator race condition by [@thesuperzapper](https://github.com/thesuperzapper) in [#33](https://github.com/deployKF/deployKF/pull/33)
* fix: resolve race conditions with cloned secrets by [@thesuperzapper](https://github.com/thesuperzapper) in [#34](https://github.com/deployKF/deployKF/pull/34)
* fix: app-of-apps should always target argocd cluster by [@thesuperzapper](https://github.com/thesuperzapper) in [#35](https://github.com/deployKF/deployKF/pull/35)

### Documentation
* docs: move guides to website by [@thesuperzapper](https://github.com/thesuperzapper) in [#20](https://github.com/deployKF/deployKF/pull/20)
* docs: improve example app-of-apps for plugin by [@thesuperzapper](https://github.com/thesuperzapper) in [#37](https://github.com/deployKF/deployKF/pull/37)
* docs: improve sample values, add reference overrides by [@thesuperzapper](https://github.com/thesuperzapper) in [#36](https://github.com/deployKF/deployKF/pull/36)


## [0.1.1](https://github.com/deployKF/deployKF/releases/tag/v0.1.1) - 2023-08-08

### Significant Changes
* feat: create argocd plugin by [@thesuperzapper](https://github.com/thesuperzapper) in [#16](https://github.com/deployKF/deployKF/pull/16)

### New Features
* feat: allow custom documentation links in dashboard by [@yankcrime](https://github.com/yankcrime) in [#12](https://github.com/deployKF/deployKF/pull/12)
* feat: allow a single ArgoCD to manage deployKF across multiple clusters by [@thesuperzapper](https://github.com/thesuperzapper) in [#17](https://github.com/deployKF/deployKF/pull/17)

### Bug Fixes
* fix: set `securityContext.fsGroup` on minio pods by [@thesuperzapper](https://github.com/thesuperzapper) in [#14](https://github.com/deployKF/deployKF/pull/14)
* fix: minio-console user permissions (update minio) by [@thesuperzapper](https://github.com/thesuperzapper) in [#18](https://github.com/deployKF/deployKF/pull/18)

### Documentation
* docs: improve getting started formatting by [@thesuperzapper](https://github.com/thesuperzapper) in [#8](https://github.com/deployKF/deployKF/pull/8)
* docs: add links to important values in readme by [@thesuperzapper](https://github.com/thesuperzapper) in [#9](https://github.com/deployKF/deployKF/pull/9)
* docs: improve getting started guide by [@thesuperzapper](https://github.com/thesuperzapper) in [#11](https://github.com/deployKF/deployKF/pull/11)
* docs: add link to youtube demo by [@thesuperzapper](https://github.com/thesuperzapper) in [#13](https://github.com/deployKF/deployKF/pull/13)


## [0.1.0](https://github.com/deployKF/deployKF/releases/tag/v0.1.0) - 2023-07-10

### Significant Changes
* initial release 🎉 🎉 🎉 

