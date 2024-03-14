---
icon: material/monitor-dashboard
description: >-
  Learn how to customize the deployKF Dashboard.
---

# Customize the Dashboard

Learn how to __customize__ the __deployKF Dashboard__.

---

## Overview

The [deployKF Dashboard](https://github.com/deployKF/dashboard) is the web-based interface for deployKF, and is the primary way that users interact with the platform.

The dashboard includes navigation menus with links to various tools and documentation which can be customized.

![deployKF Dashboard (Dark Mode)](../../assets/images/deploykf-dashboard-DARK.png#only-dark)
![deployKF Dashboard (Light Mode)](../../assets/images/deploykf-dashboard-LIGHT.png#only-light)

## Sidebar Links

Extra links may be added to the sidebar navigation menu with the [`deploykf_core.deploykf_dashboard.navigation.externalLinks`](https://github.com/deployKF/deployKF/blob/v0.1.1/generator/default_values.yaml#L538-L547) value.

For example, you may use the following values to add a link to the deployKF website:

```yaml
deploykf_core:
  deploykf_dashboard:
    navigation:
      externalLinks:
        - name: "deployKF Website"
          url: "https://deployKF.org"
          icon: "launch"
```

## Documentation Links

Extra links may be added to the "documentation" section of the home page with the [`deploykf_core.deploykf_dashboard.navigation.documentationItems`](https://github.com/deployKF/deployKF/blob/v0.1.1/generator/default_values.yaml#L549-L559) value.

For example, you may use the following values to add a link to the deployKF website:

```yaml
deploykf_core:
  deploykf_dashboard:
    navigation:
      documentationItems:
        - text: "deployKF Website"
          desc: "The tool that deployed your ML platform!"
          link: "https://github.com/deployKF/deployKF"
```