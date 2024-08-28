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

## Istio

??? bug "Istio sidecars crash with `iptables-restore: unable to initialize table 'nat'` error"

    If you experience crashes in your Istio sidecars with an error message like this:

    ```bash
    2024-08-25T10:50:29.229925Z	info	Running command: iptables-restore --noflush
    2024-08-25T10:50:29.240073Z	error	Command error output: xtables parameter problem: iptables-restore: unable to initialize table 'nat'
    ```

    Then your nodes are likely missing some __Linux kernel modules__ required by Istio.
    This error has been discussed in the upstream Istio repo ([`istio#23009`](https://github.com/istio/istio/issues/23009), [`istio#44118`](https://github.com/istio/istio/issues/44118)).

    1. Get a list of the currently loaded kernel modules by running `lsmod`:

        ```bash
        lsmod | awk '{print $1}' | sort
        ```

    2. At the time of writing, the following command will enable the [required kernel modules](https://istio.io/latest/docs/ops/deployment/platform-requirements/) on boot:

        ```bash
        ## NOTE: if you are using Istio ambient mode, there are additional modules required
        cat <<EOF | sudo tee /etc/modules-load.d/99-istio-modules.conf
        br_netfilter
        ip_tables
        iptable_filter
        iptable_mangle
        iptable_nat
        iptable_raw
        nf_nat
        x_tables
        xt_REDIRECT
        xt_conntrack
        xt_multiport
        xt_owner
        xt_tcpudp
        EOF
        ```

    3. Now, either reboot your nodes or immediately load the modules with the following commands (which will also indicate if any modules are missing):

        ```bash
        sudo modprobe br_netfilter
        sudo modprobe ip_tables
        sudo modprobe iptable_filter
        sudo modprobe iptable_mangle
        sudo modprobe iptable_nat
        sudo modprobe iptable_raw
        sudo modprobe nf_nat
        sudo modprobe x_tables
        sudo modprobe xt_REDIRECT
        sudo modprobe xt_conntrack
        sudo modprobe xt_multiport
        sudo modprobe xt_owner
        sudo modprobe xt_tcpudp
        ```

## Kubeflow

??? bug "Pods crash with `too many open files` error"

    If you experience pods crashing with an error message like this:

    ```bash
    too many open files
    ```

    You may need to increase the `fs.inotify.max_user_*` sysctl values on your nodes (only for Linux nodes).
    This error has been discussed in the upstream Kubeflow repo ([`kubeflow/manifests#2087`](https://github.com/kubeflow/manifests/issues/2087))

    To resolve it, you will need to increase your system's open/watched file limits:

    1. Modify `/etc/sysctl.conf` to include the following lines:

        ```bash
        fs.inotify.max_user_instances = 1280
        fs.inotify.max_user_watches = 655360
        ```

    2. Now, apply immediately the changes with the following command:

        ```bash
        sudo sysctl -p
        ```