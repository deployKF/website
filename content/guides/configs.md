---
icon: material/cog
description: >-
  Learn how to configure deployKF to meet your organization's needs.
---

# Configuration

Learn how to configure deployKF to meet your organization's needs.

---

## Overview

deployKF is incredibly configurable via its centralized [values system](./values.md), which allows you to define all aspects of the platform in a single YAML file (or multiple, if you prefer).

## Configuration Guides

To help you get started with common configuration tasks, we have created the following guides.

### __Platform Configuration Guides__

The following guides help you configure the deployKF platform itself, including user authentication, authorization, and branding.

<table markdown="span">
  <tr>
    <th>Guide<br><small>(Click for Details)</small></th>
    <th>Description</th>
  </tr>
  <tr markdown>
    <td markdown>[User Authentication and External Identity Providers](./platform/deploykf-authentication.md)</td>
    <td>Integrate with an existing user authentication system (GitHub, Google, Okta, etc.) or define static user accounts.</td>
  </tr>
  <tr markdown>
    <td markdown>[User Authorization and Profile Management](./platform/deploykf-profiles.md)</td>
    <td>Define profiles (namespaces) and assign users to them.</td>
  </tr>
  <tr markdown>
    <td markdown>[Expose Gateway and configure HTTPS](./platform/deploykf-gateway.md)</td>
    <td>Expose the deployKF gateway with a LoadBalancer or Ingress, and configure valid HTTPS certificates.</td>
  </tr>
  <tr markdown>
    <td markdown>[Customize the Dashboard](./platform/deploykf-dashboard.md)</td>
    <td>Customize the deployKF dashboard with your own branding and links.</td>
  </tr>
  <tr markdown>
    <td markdown>[Image Pull Secrets and Private Registries](./platform/image-pull-secrets.md)</td>
    <td>Configure image pull secrets, avoid Docker Hub rate limits, or use a private container registry.</td>
  </tr>
</table>

### __Tool Configuration Guides__

The following guides help you configure the [ML & Data tools](../reference/tools.md#tool-index) which are part of the deployKF platform.

<table markdown="span">
  <tr>
    <th>Guide<br><small>(Click for Details)</small></th>
    <th>Description</th>
  </tr>
  <tr markdown>
    <td markdown>[Configure Kubeflow Notebooks](./tools/kubeflow-notebooks.md)</td>
    <td>Configure Kubeflow Notebooks with custom server images and compute resources (including GPUs).</td>
  </tr>
</table>
