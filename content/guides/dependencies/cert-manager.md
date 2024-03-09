---
icon: custom/cert-manager
description: >-
  Learn how deployKF uses cert-manager and how to integrate your existing cert-manager with deployKF.
---

# Cert Manager

Learn how deployKF uses cert-manager and how to integrate your existing cert-manager with deployKF.

---

## __What is cert-manager?__

[:custom-cert-manager-color: __Cert-Manager__](https://cert-manager.io/docs/) is a widely-used Kubernetes operator that declaratively manages TLS certificates using Kubernetes resources.

The core resource of cert-manager is the [`Certificate`](https://cert-manager.io/docs/concepts/certificate/), which is a Kubernetes [custom resource](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/) that specifies the details of a TLS certificate (e.g. domain name).
Each `Certificate` references an [`Issuer`](https://cert-manager.io/docs/concepts/issuer/) (or `ClusterIssuer`) which tells cert-manager how to provision the certificate (e.g. using [Let's Encrypt](https://letsencrypt.org/) or self-signing).
Cert-Manager can store provisioned certificates in Kubernetes [`Secrets`](https://kubernetes.io/docs/concepts/configuration/secret/) so they can be used by Pods, and will automatically renew the certificate when it is about to expire.

### __What is trust-manager?__

[__Trust-Manager__](https://cert-manager.io/docs/trust/trust-manager/) is a Kubernetes operator that declaratively manages trust bundles using Kubernetes resources.
deployKF uses trust-manager when self-signed certificates are configured (the default) because it allows us to distribute the root CA certificate (via our [root CA `Bundle`](https://github.com/deployKF/deployKF/blob/v0.1.3/generator/templates/manifests/deploykf-dependencies/cert-manager/templates/selfsigned-ca-issuer/Bundle.yaml)) to all services in the platform.

---

## __How does deployKF use cert-manager?__

deployKF uses cert-manager to provision TLS certificates for the Istio Ingress Gateway.
Furthermore, many tools in the platform use cert-manager to provision TLS certificates for internal webhooks and APIs.

See the [Expose Gateway and Configure TLS](../platform/deploykf-gateway.md#configure-tls-certificates) guide for more details.

---

## __Can I use my existing cert-manager?__

Yes.

If you want to bring your own cert-manager deployment, you may set the [`deploykf_dependencies.cert_manager.enabled`](https://github.com/deployKF/deployKF/blob/v0.1.3/generator/default_values.yaml#L75) value to `false` to disable the deployKF-managed one:

```yaml
deploykf_dependencies:
  cert_manager:
    enabled: false
```
        
When you do this, the [`deploykf_dependencies.cert_manager.clusterIssuer`](https://github.com/deployKF/deployKF/blob/v0.1.3/generator/default_values.yaml#L172) value still selects the `ClusterIssuer` (which must be provisioned by you) that is used to [generate certificates for the Istio Gateway](../platform/deploykf-gateway.md#configure-tls-certificates):

```yaml
deploykf_dependencies:
  cert_manager:
    enabled: false
    
    clusterIssuer:
      ## NOTE: when `cert_manager.enabled` is false, 
      ##       all other `cert_manager` values have NO effect
      issuerName: my-cluster-issuer
```
