# Manage Profiles and Assigning Users

This guide explains how to __manage profiles__ and __assign users__ to them in deployKF.

---

## Overview

A deployKF profile has a 1:1 relationship with a Kubernetes namespace.
The profiles which a user is a member of determines their level of access to resources/tools in the cluster.

!!! info "No Profile = No Access"

    If a user is not a member of any profiles, they will NOT have any access, even though they may be able to log in.

!!! warning "Use Profile Generator Only"

    You must ONLY use the `deploykf_core.deploykf_profiles_generator` values to manage profile definitions or user assignments.
    Any manual changes using the UI or other manifests will result in undefined behaviour.
    

### User Entities

The [`deploykf_core.deploykf_profiles_generator.users`](https://github.com/deployKF/deployKF/blob/v0.1.1/generator/default_values.yaml#L776-L786) value defines "user" entities.

For example, you might use the following values to define three users:

```yaml
deploykf_core:
  deploykf_profiles_generator:
    users:
      - id: user-1
        email: "user1@example.com"

      - id: user-2
        email: "user2@example.com"

      - id: user-3
        email: "user3@example.com"
```

!!! info "User Identifiers"

    Users are identified by email address, which is provided from the identity provider or static accounts, this means that each `email` must be unique.

### Group Entities

The [`deploykf_core.deploykf_profiles_generator.groups`](https://github.com/deployKF/deployKF/blob/v0.1.1/generator/default_values.yaml#L788-L798) value defines "group" entities, which are __logical__ collections of "user" entities.

For example, you might use the following values to define two groups:

```yaml
deploykf_core:
  deploykf_profiles_generator:
    groups:
      - id: team-1--admins
        users:
          - user-1

      - id: team-1--users
        users:
          - user-1
          - user-2
          - user-3
```

!!! warning "Syncing External Groups"

    Currently, groups must be __manually defined__ in the values, and can NOT be synced from an external identity provider.

### Profile Definitions

The [`deploykf_core.deploykf_profiles_generator.profiles`](https://github.com/deployKF/deployKF/blob/v0.1.1/generator/default_values.yaml#L800-L839) value defines the profiles (namespaces) to create, and the groups/users to assign to them.

For example, you might use the following values to define two profiles:

```yaml
deploykf_core:
  deploykf_profiles_generator:
    profiles:
      - name: team-1
        members:
          - group: team-1--users
            access:
              role: edit
              notebooksAccess: true

      - name: team-1-prod
        members:
          - group: team-1--admins
            access:
              role: edit
              notebooksAccess: true

          - group: team-1--users
            access:
              role: view
              notebooksAccess: false
```

!!! info "Highest Level of Access"

    If a user has multiple memberships in the same profile, the highest level of access will be used.

!!! danger "Default Profile Owner"
    
    By default, [`"admin@example.com"` is the "owner" of all profiles](https://github.com/deployKF/deployKF/blob/v0.1.1/generator/default_values.yaml#L687-L693), but is not a "member" of any.
    This means that it does not have access to the "MinIO Console" or "Argo Workflows Server" interfaces.

    ---

    Because it is NOT possible to change the owner of a profile ([`kubeflow/kubeflow#6576`](https://github.com/kubeflow/kubeflow/issues/6576)), we recommend that you leave the default owner as `admin@example.com`, and never log into that account.

    For additional security, remove the `staticPasswords` entry for that email, so it can never be used to log in.