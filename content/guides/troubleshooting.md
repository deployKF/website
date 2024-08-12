---
icon: material/bug
description: >-
  Learn about common issues with deployKF and how to resolve them.
---

# Troubleshooting

Learn about common issues with deployKF and how to resolve them.

---

## Argo Server UI

??? bug "Cannot list resource "workflows" in API group "argoproj.io" at the cluster scope"

    Sometimes, users may open the "Argo Server" UI and see an error message like this:

    > {"code":7,"message":"workflows.argoproj.io is forbidden: User \"system:serviceaccount:kubeflow-argo-workflows:argo-server-user-b36a83701f1c3191e19722d6f90274bc1b5501fe69ebf33313e440fe4b0fe210\" cannot list resource \"workflows\" in API group \"argoproj.io\" at the cluster scope"}: workflows.argoproj.io is forbidden: User "system:serviceaccount:kubeflow-argo-workflows:argo-server-user-b36a83701f1c3191e19722d6f90274bc1b5501fe69ebf33313e440fe4b0fe210" cannot list resource "workflows" in API group "argoproj.io" at the cluster scope

    This error is actually telling you that you need to set a namespace filter, as the Argo Server UI is trying to list ALL workflows in the cluster (but no user has permission to do that).
    Each user's access in the Argo Server UI corresponds to their [profile memberships](./platform/deploykf-profiles.md#profile-definitions).

    ![Argo Server Error (Dark Mode)](../assets/images/argo-server-error-DARK.png#only-dark)
    ![Argo Server Error (Light Mode)](../assets/images/argo-server-error-LIGHT.png#only-light)

## Deployment Issues

??? bug "Pods fail with "too many open files" error"

    If your Kubernetes nodes are running __Linux__, you may need to increase the `fs.inotify.max_user_*` sysctl values or you may see errors like this in your Pod logs:

    > `too many open files`

    This error has been discussed in the upstream Kubeflow repo ([`kubeflow/manifests#2087`](https://github.com/kubeflow/manifests/issues/2087)), to resolve it, you will need to increase your system's open/watched file limits:

    1. Modify `/etc/sysctl.conf` to include the following lines:
        - `fs.inotify.max_user_instances = 1280`
        - `fs.inotify.max_user_watches = 655360`
    2. Reload sysctl configs by running `sudo sysctl -p`