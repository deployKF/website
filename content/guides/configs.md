---
icon: material/cog
description: >-
  Learn how to configure deployKF to meet your organization's needs.
---

# Configure deployKF

Learn how to configure deployKF to meet your organization's needs.

---

## Configuration Guides

deployKF is incredibly configurable via its centralized [values system](#about-values).
To help you get started with common configuration tasks, we have created the following guides.

### __Platform Configuration__

The following guides help you configure the deployKF platform itself, including user authentication, authorization, and branding.

<table markdown="span">
  <tr>
    <th>Guide<br><small>(Click for Details)</small></th>
    <th>Description</th>
  </tr>
  <tr markdown>
    <td markdown>[User Authentication](./platform/deploykf-authentication.md)</td>
    <td>Integrate with your existing user authentication system (GitHub, Google, Okta, etc.) and define static user accounts.</td>
  </tr>
  <tr markdown>
    <td markdown>[User Authorization and Profile Management](./platform/deploykf-profiles.md)</td>
    <td>Manage user permissions by defining profiles and assigning users to them.</td>
  </tr>
  <tr markdown>
    <td markdown>[Expose Gateway and configure HTTPS](./platform/deploykf-gateway.md)</td>
    <td>Make deployKF available publicly and configure valid HTTPS certificates.</td>
  </tr>
  <tr markdown>
    <td markdown>[Customize the Dashboard](./platform/deploykf-dashboard.md)</td>
    <td>Customize the deployKF dashboard with your own branding and links.</td>
  </tr>
</table>

### __Tool Configuration__

The following guides help you configure the [ML & Data tools](../reference/tools.md#tool-index) which are part of the deployKF platform.

<table markdown="span">
  <tr>
    <th>Guide<br><small>(Click for Details)</small></th>
    <th>Description</th>
  </tr>
  <tr markdown>
    <td markdown>[Configure Kubeflow Notebooks](./tools/kubeflow-notebooks.md)</td>
    <td>Configure Kubeflow Notebooks with custom server images and compute resources, including GPUs.</td>
  </tr>
</table>

---

## About Values

All aspects of your deployKF platform are configured with YAML-based configs named "values".
There are a very large number of values (more than 1500), but as deployKF supports _in-place upgrades_ you can start with a few important ones, and then grow your values file over time.

### __Defining Values__

We recommend using the [`sample-values.yaml`](https://github.com/deployKF/deployKF/blob/v{{ latest_deploykf_version }}/sample-values.yaml) file as the base of your values.
These sample values have all supported [ML & Data tools](../reference/tools.md#tool-index) enabled, along with some sensible security defaults.

You may copy and make changes to the sample values, or directly use it as a base, and override specific values in a separate file.
We provide the [`sample-values-overrides.yaml`](https://github.com/deployKF/deployKF/blob/v{{ latest_deploykf_version }}/sample-values-overrides.yaml) file as an example of this approach.

!!! warning "deployKF Version"

    Each `sample-values.yaml` is specific to a deployKF version, be sure to use the correct version!

!!! info "Values Reference"

    deployKF has many additional values not found in the sample files.
    For your reference, ALL values and their defaults are listed on the [values reference](../reference/deploykf-values.md) page, which is generated from the full [`default_values.yaml`](https://github.com/deployKF/deployKF/blob/v{{ latest_deploykf_version }}/generator/default_values.yaml) file.

!!! info "YAML Syntax"

    For a refresher on YAML syntax, we recommend the following resources:
    
    - [Learn YAML in Y minutes](https://learnxinyminutes.com/docs/yaml/)
    - [YAML Multiline Strings](https://yaml-multiline.info/)
