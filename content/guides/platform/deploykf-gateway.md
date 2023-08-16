# Expose deployKF Gateway and configure HTTPS

This guide explains how to expose the deployKF Gateway Service and configure HTTPS.

## Overview

The "deployKF Gateway Service" is the main network entry point to deployKF. 
By default, it is a [Kubernetes Service](https://kubernetes.io/docs/concepts/services-networking/service/) named `deploykf-gateway` pointing to our [Istio Ingress Gateway](https://istio.io/latest/docs/tasks/traffic-management/ingress/ingress-control/) pods.

!!! contribute "Help Improve this Guide"

    This guide covers an incredibly broad topic with near limitless possible implementations.
    As a result, it is likely to be missing some important details for your specific use case.
    If you see anything that is incorrect or missing, please help us by [raising an issue](https://github.com/deployKF/website/issues/new/?title=[Feedback]+{{ page.title }})!

## 1. Expose the Gateway Service

The first step is to expose the deployKF Gateway Service on an IP address that is accessible from outside the cluster.

There are two main options to expose the deployKF Gateway Service:

1. Use a [`LoadBalancer`](https://kubernetes.io/docs/concepts/services-networking/service/#loadbalancer) type Service (recommended)
2. Configure an [`Ingress`](https://kubernetes.io/docs/concepts/services-networking/ingress/#terminology)

!!! danger "Public Internet"

    You should seriously consider the security implications of exposing the deployKF Gateway to the public internet.
    Given the nature of ML Platforms, most companies choose to expose the gateway on their private network, and then use a VPN or other secure connection to access it.

### Expose with LoadBalancer Service

??? steps "Steps to Expose with LoadBalancer Service"

    Most Kubernetes platforms provide a LoadBalancer service that can expose on a public/private IP address.
    
    To use this option, you will generally need to do the following:

    1. Set the [`deploykf_core.deploykf_istio_gateway.gatewayService.type`](https://github.com/deployKF/deployKF/blob/v0.1.1/generator/default_values.yaml#L653) value to `"LoadBalancer"` (the default)
    2. Use the [`deploykf_core.deploykf_istio_gateway.gatewayService.annotations`](https://github.com/deployKF/deployKF/blob/v0.1.1/generator/default_values.yaml#L654C7-L654C18) value to configure the Service

    ---

    ??? config "Amazon Web Services (EKS)"

        The [AWS Load Balancer Controller](https://kubernetes-sigs.github.io/aws-load-balancer-controller/) is commonly used to configure LoadBalancer services on EKS.
    
        For example, you might set the following values to use a [Network Load Balancer (NLB)](https://docs.aws.amazon.com/elasticloadbalancing/latest/network/introduction.html):
    
        ```yaml
        deploykf_core:
          deploykf_istio_gateway:

            ## these values are used to configure the deployKF Gateway Service
            ##
            gatewayService:
              name: "deploykf-gateway"
              type: "LoadBalancer"
              annotations:
                service.beta.kubernetes.io/aws-load-balancer-type: "external"
                service.beta.kubernetes.io/aws-load-balancer-nlb-target-type: "ip"
                service.beta.kubernetes.io/aws-load-balancer-scheme: "internal"
    
                ## for external-dns integration (if not `--source=istio-gateway` config)
                #external-dns.alpha.kubernetes.io/hostname: "deploykf.example.com, *.deploykf.example.com"

                ## for static private IP addresses
                #service.beta.kubernetes.io/aws-load-balancer-private-ipv4-addresses: "192.168.XXX.XXX, 192.168.YYY.YYY"
                #service.beta.kubernetes.io/aws-load-balancer-subnets: "subnet-XXX, subnet-YYY"
    
                ## for static public IP addresses
                #service.beta.kubernetes.io/aws-load-balancer-eip-allocations: "eipalloc-XXX, eipalloc-YYY"
                #service.beta.kubernetes.io/aws-load-balancer-subnets: "subnet-XXX, subnet-YYY"
        ```
    
    ??? config "Google Cloud (GKE)"

        GKE, has a LoadBalancer Service type, which is configured with annotations like [`networking.gke.io/load-balancer-type`](https://cloud.google.com/kubernetes-engine/docs/concepts/service-load-balancer-parameters). 

        For example, you might set the following values to use an [INTERNAL Passthrough Network Load Balancer](https://cloud.google.com/kubernetes-engine/docs/concepts/service-load-balancer):
    
        ```yaml
        deploykf_core:
          deploykf_istio_gateway:

            ## these values are used to configure the deployKF Gateway Service
            ##
            gatewayService:
              name: "deploykf-gateway"
              type: "LoadBalancer"
              annotations:
                networking.gke.io/load-balancer-type: "Internal"

                ## for external-dns integration (if not `--source=istio-gateway` config)
                #external-dns.alpha.kubernetes.io/hostname: "deploykf.example.com, *.deploykf.example.com"
    
              ## for static IP addresses
              #loadBalancerIP: "192.168.XXX.XXX"
              #loadBalancerSourceRanges: ["192.168.XXX.XXX/32"]
        ```

### Expose with Ingress

??? steps "Steps to Expose with Ingress"

    Most Kubernetes platforms provide an Ingress class that can expose on a public/private IP address.
    
    To use this option, you will generally need to do the following:

    1. Set the [`deploykf_core.deploykf_istio_gateway.gatewayService.type`](https://github.com/deployKF/deployKF/blob/v0.1.1/generator/default_values.yaml#L653) value to `"NodePort"` or `"ClusterIP"`
    2. Use the [`deploykf_core.deploykf_istio_gateway.gatewayService.annotations`](https://github.com/deployKF/deployKF/blob/v0.1.1/generator/default_values.yaml#L654C7-L654C18) value to configure the Service
    3. Create an `Ingress` resource that points to the `deploykf-gateway` Service

    !!! note "Extra Manifests Values"

        deployKF provides an `extraManifests` value for each component which allows arbitrary YAML manifests to be added to the generated output.
        For example, [`deploykf_core.deploykf_istio_gateway.extraManifests`](https://github.com/deployKF/deployKF/blob/v0.1.1/generator/default_values.yaml#L575-L579) may be used to add an Ingress resource to the generated output.

    ---

    ??? config "Amazon Web Services (EKS)"

        The [AWS Load Balancer Controller](https://kubernetes-sigs.github.io/aws-load-balancer-controller/) is commonly used to configure Ingress resources on EKS.

        !!! warning "TLS Certificates"
    
            Because ALB does NOT support TLS-passthrough, you must manually create an [AWS Certificate Manager (ACM)](https://aws.amazon.com/certificate-manager/) wildcard certificate for your domain.
            The `alb.ingress.kubernetes.io/certificate-arn` Ingress annotation will be used to select the certificate and allow the Ingress to terminate TLS before forwarding to the Gateway Service.

            Hostname | Certificate Field
            --- | ---
            `*.deploykf.example.com` | CN, SAN
            `deploykf.example.com` | SAN

        For example, you might set the following values to use an [Application Load Balancer (ALB)](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/introduction.html):
    
        ```yaml
        deploykf_core:
          deploykf_istio_gateway:

            ## this value is used to add arbitrary manifests to the generated output
            ##
            extraManifests:
              - |
                apiVersion: extensions/v1beta1
                kind: Ingress
                metadata:
                  name: deploykf-gateway
                  annotations:
                    alb.ingress.kubernetes.io/scheme: internal
                    alb.ingress.kubernetes.io/target-type: ip
                    alb.ingress.kubernetes.io/listen-ports: '[{"HTTP": 80}, {"HTTPS": 443}]'
                    alb.ingress.kubernetes.io/ssl-redirect: '443'
                    alb.ingress.kubernetes.io/certificate-arn: "arn:aws:acm:REGION_NAME:ACCOUNT_ID:certificate/CERTIFICATE_ID"
                    alb.ingress.kubernetes.io/backend-protocol: HTTPS
                spec:
                  ingressClassName: alb                  
                  rules:
                    - host: "deploykf.example.com"
                      http:
                        paths:
                          - path: "/*"
                            backend:
                              service:
                                name: "deploykf-gateway"
                                port:
                                  name: https
                    - host: "*.deploykf.example.com"
                      http:
                        paths:
                          - path: "/*"
                            backend:
                              service:
                                name: "deploykf-gateway"
                                port:
                                  name: https

            ## these values are used to configure the deployKF Gateway Service
            ##
            gatewayService:
              name: "deploykf-gateway"
              type: "NodePort"
              annotations: {}
        ```

    ??? config "Google Cloud (GKE)"

        GKE, has an Ingress class that can be used to configure Ingress resources for external or internal access. 

        !!! warning "TLS Certificates"
    
            In the following example, we are configuring the GKE Ingress to use the same TLS certificate as the deployKF Gateway Service (found in `Secret/deploykf-istio-gateway-cert`).
            Later in this guide you will learn how to make this certificate valid, and not self-signed.

        For example, you might set the following values to use an [INTERNAL Application Load Balancer](https://cloud.google.com/kubernetes-engine/docs/concepts/ingress):
    
        ```yaml
        deploykf_core:
          deploykf_istio_gateway:
  
              ## this value is used to add arbitrary manifests to the generated output
              ##
              extraManifests:
                - |
                  apiVersion: networking.k8s.io/v1
                  kind: Ingress
                  metadata:
                    name: deploykf-gateway
                    annotations:
                      kubernetes.io/ingress.class: "gce-internal"
                      kubernetes.io/ingress.allow-http: "false"
                  spec:
                    tls:
                      ## NOTE: this secret is created as part of the deployKF installation
                      - secretName: "deploykf-istio-gateway-cert"
                    rules:
                      - host: "deploykf.example.com"
                        http:
                          paths:
                            - path: "/*"
                              pathType: ImplementationSpecific
                              backend:
                                service:
                                  name: "deploykf-gateway"
                                  port:
                                    name: https
                      - host: "*.deploykf.example.com"
                        http:
                          paths:
                            - path: "/*"
                              pathType: ImplementationSpecific
                              backend:
                                service:
                                  name: "deploykf-gateway"
                                  port:
                                    name: https
  
              ## these values are used to configure the deployKF Gateway Service
              ##
              gatewayService:
                name: "deploykf-gateway"
                type: "NodePort"
                annotations:
                  cloud.google.com/app-protocols: '{"https":"HTTPS","http":"HTTP"}'
                  
                  ## this annotation may be required if you are using a Shared VPC
                  ##  https://cloud.google.com/kubernetes-engine/docs/how-to/internal-load-balance-ingress#shared_vpc
                  #cloud.google.com/neg: '{"ingress": true}'
        ```

??? warning "Ingress Considerations"

    In most cases, using a LoadBalancer Service is the preferred option for the following reasons:

    1. __Faster__: less hops between the client and the gateway
    2. __Future-proof__: deployKF might expose non-HTTP services in the future
    3. __Simpler TLS__: many Ingress controllers don't support TLS passthrough

## 2. Configure DNS

Now that the deployKF Gateway Service has an IP address, you must configure DNS records which point to it.

There are two main options to configure DNS records:

1. Automatically with [External-DNS](https://github.com/kubernetes-sigs/external-dns) (recommended)
2. Manually with your DNS provider

Depending on which components of deployKF are used, the following hostnames may be served by the deployKF Gateway Service:

Hostname | Description | Required By
--- | --- | ---
`deploykf.example.com` | the deployKF Gateway | ALL
`argo-server.deploykf.example.com` | the Argo Server UI | Argo Server (Kubeflow Pipelines)
`minio-api.deploykf.example.com` | the MinIO API | MinIO
`minio-console.deploykf.example.com` | the MinIO UI | MinIO

!!! config "Base Domain"

    The "base domain" is defined by [`deploykf_core.deploykf_istio_gateway.gateway.hostname`](https://github.com/deployKF/deployKF/blob/v0.1.1/generator/default_values.yaml#L600), which has a default value of `"deploykf.example.com"`.

### Configure records with External-DNS

??? steps "Steps to configure records with External-DNS"

    [External-DNS](https://github.com/kubernetes-sigs/external-dns) is a Kubernetes controller that automatically configures DNS records for Kubernetes resources.

    To use this option, you will generally need to do the following:

    1. Install External-DNS and connect it to your DNS provider
    2. Configure External-DNS to set DNS records for the deployKF Gateway Service
    ---

    __Step 1:__ Install External-DNS

    The External-DNS documentation provides instructions for [installing External-DNS on various platforms](https://github.com/kubernetes-sigs/external-dns#running-externaldns).

    Here are some popular platforms:

    Cloud Platform | DNS Provider
    --- | ---
    Amazon Web Services | [Route53](https://github.com/kubernetes-sigs/external-dns/blob/master/docs/tutorials/aws.md)
    Google Cloud | [Cloud DNS](https://github.com/kubernetes-sigs/external-dns/blob/master/docs/tutorials/gke.md)
    Microsoft Azure | [Azure DNS](https://github.com/kubernetes-sigs/external-dns/blob/master/docs/tutorials/azure.md), [Azure Private DNS](https://github.com/kubernetes-sigs/external-dns/blob/master/docs/tutorials/azure-private-dns.md)
    Any | [Cloudflare](https://github.com/kubernetes-sigs/external-dns/blob/master/docs/tutorials/cloudflare.md), [Akamai Edge DNS](https://github.com/kubernetes-sigs/external-dns/blob/master/docs/tutorials/akamai-edgedns.md)

    ---

    __Step 2:__ Configure External-DNS

    There are two main ways to configure External-DNS so that it sets DNS records for the deployKF Gateway Service:

    1. Use the [`--source=istio-gateway`](https://github.com/kubernetes-sigs/external-dns/blob/master/docs/tutorials/istio.md) config:
        - _In this case, a separate DNS record is created for [each domain selected by the Istio `Gateway`](https://github.com/deployKF/deployKF/blob/v0.1.1/generator/templates/manifests/deploykf-core/deploykf-istio-gateway/templates/gateway/Gateway.yaml#L14-L25)_
    2. Annotate the Service or Ingress with [`external-dns.alpha.kubernetes.io/hostname`](https://github.com/kubernetes-sigs/external-dns/blob/master/docs/faq.md#how-do-i-specify-a-dns-name-for-my-kubernetes-objects):
        - _In this case, you may use a wildcard DNS record, or a separate record for each domain_
        - _You may use the [`deploykf_core.deploykf_istio_gateway.gatewayService.annotations`](https://github.com/deployKF/deployKF/blob/v0.1.1/generator/default_values.yaml#L654) value to annotate the Service (or if using an Ingress, you will need to set the annotations yourself)_


### Configure records manually

??? steps "Steps to configure records manually"

    You can manually configure DNS records with your DNS provider that target your deployKF Gateway Service.

    To use this option, you will generally need to do the following:

    1. Ensure the deployKF Gateway has a static IP address (or hostname, in some cases)
    2. Configure DNS records with your DNS provider

    ---

    __Step 1:__ Static IP Addresses

    Each type of LoadBalancer Service (or Ingress controller) has different ways to configure static IP addresses or hostnames.
    Please refer to the documentation for your platform.

    ---

    __Step 2:__ Configure DNS Records

    See the previous section for information about which DNS records to configure.

    !!! tip "Wildcard DNS Records"
    
        If possible, we recommend using a [wildcard DNS record](https://en.wikipedia.org/wiki/Wildcard_DNS_record) to account for any future subdomains that may be added to the deployKF Gateway Service.
    
        For example, you might set the following DNS records:
    
        - `*.deploykf.example.com`
        - `deploykf.example.com`

## 3. Configure HTTPS/TLS

Now that the deployKF Gateway Service has a DNS pointing to it, to prevent self-signed certificate errors, you must configure a way to make the TLS certificates valid.

- If you are exposing the deployKF Gateway [with a LoadBalancer Service](#expose-with-loadbalancer-service), then ONLY the Istio Gateway will need to be configured with valid TLS certificates.
- If you are exposing the deployKF Gateway [with an Ingress](#expose-with-ingress), then BOTH the Istio Gateway and the Ingress will need to be configured with valid TLS certificates (unless your Ingress supports TLS passthrough, which most do not).

### Configure TLS for Istio Gateway

deployKF includes [cert-manager](https://cert-manager.io/) to automatically generate TLS certificates for the Istio Gateway.

By default, the Istio Gateway uses a self-signed certificate generated by [this `ClusterIssuer`](https://github.com/deployKF/deployKF/blob/v0.1.1/generator/templates/manifests/deploykf-dependencies/cert-manager/templates/ClusterIssuer-kubeflow-gateway-issuer.yaml), which is fine for testing (especially if you don't own the domain you are using), but not recommended for production usage.

To have cert-manager generate valid TLS certificates for the Istio Gateway, you will need to:

1. Connect cert-manager to your DNS provider
2. Create a `ClusterIssuer` resource that can generate certificates for your domain
3. Configure the Istio Gateway to use your `ClusterIssuer` to generate certificates

!!! info "Custom Deployment"

    deployKF includes an embedded version of cert-manager, if you wish to use your own, you may set the [`deploykf_dependencies.cert_manager.enabled`](https://github.com/deployKF/deployKF/blob/v0.1.1/generator/default_values.yaml#L75) value to `false`.
    If you do this, the [`deploykf_dependencies.cert_manager.clusterIssuer`](https://github.com/deployKF/deployKF/blob/v0.1.1/generator/default_values.yaml#L164-L171) values will still control which `ClusterIssuer` is used to generate certificates for the Istio Gateway.

#### STEP 1: Connect cert-manager to DNS Provider

For almost everyone, the best Certificate Authority (CA) is [Let's Encrypt](https://letsencrypt.org/).

Because deployKF uses a [wildcard `Certificate`](https://github.com/deployKF/deployKF/blob/v0.1.1/generator/templates/manifests/deploykf-core/deploykf-istio-gateway/templates/gateway/Certificate.yaml#L16), you MUST use the [`DNS-01`](https://letsencrypt.org/docs/challenge-types/#dns-01-challenge) challenge to verify domain ownership rather than [`HTTP-01`](https://letsencrypt.org/docs/challenge-types/#http-01-challenge).
This requires you to configure cert-manager so that it is able to create DNS records.

The cert-manager documentation provides [instructions for configuring `DNS-01` challenges](https://cert-manager.io/docs/configuration/acme/dns01/) for various DNS providers.
The following table lists some popular DNS providers:

Cloud Platform | DNS Provider
--- | ---
Amazon Web Services | [Route53](https://cert-manager.io/docs/configuration/acme/dns01/route53/)
Google Cloud | [Cloud DNS](https://cert-manager.io/docs/configuration/acme/dns01/google/)
Microsoft Azure | [Azure DNS](https://cert-manager.io/docs/configuration/acme/dns01/azuredns/)
Any | [Cloudflare](https://cert-manager.io/docs/configuration/acme/dns01/cloudflare/), [Akamai Edge DNS](https://cert-manager.io/docs/configuration/acme/dns01/akamai/)

!!! info "Pod ServiceAccount Annotations"

    To use Pod-based authentication with your DNS Provider, you may need to annotate the cert-manager ServiceAccount.
    Custom ServiceAccount annotations can be applied with the [`deploykf_dependencies.cert_manager.controller.serviceAccount.annotations`](https://github.com/deployKF/deployKF/blob/v0.1.1/generator/default_values.yaml#L155) value.

#### STEP 2: Create a ClusterIssuer

Once cert-manager is connected to your DNS provider, you must create a `ClusterIssuer` resource that can generate certificates for your domain from [Let's Encrypt](https://letsencrypt.org/).

For example, you may create a `ClusterIssuer` resource like this when using Google Cloud DNS:

```yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: my-cluster-issuer
spec:
  acme:
    server: https://acme-staging-v02.api.letsencrypt.org/directory
    email: user@example.com
    privateKeySecretRef:
      name: letsencrypt-staging
      key: tls.key
    solvers:
      - dns01:
          cloudDNS:
            project: my-project-id
            serviceAccountSecretRef:
              name: my-service-account-secret
              key: service-account.json
        selector:
          dnsNames:
            - "*.deploykf.example.com"
            - "deploykf.example.com"
```

!!! tip "Issuer Kind"

    Many cert-manager examples show an `Issuer` resource. 
    Note that any issuer may be converted to its equivalent cluster version by changing the `kind` field from `"Issuer"` to `"ClusterIssuer"` and removing the `metadata.namespace` field.

#### STEP 3: Configure the Istio Gateway

Once you have a `ClusterIssuer` resource that can generate certificates for your domain, you must configure the deployKF Istio Gateway to use it.

This is done by using the [`deploykf_dependencies.cert_manager.clusterIssuer`](https://github.com/deployKF/deployKF/blob/v0.1.1/generator/default_values.yaml#L164-L171) values.
For example, if you created a `ClusterIssuer` named `my-cluster-issuer`, you would set the following values:

```yaml
deploykf_dependencies:
  cert_manager:
    clusterIssuer:
      ## this tells deployKF that you have created a ClusterIssuer
      enabled: false
      
      ## this value should match the name of your ClusterIssuer
      issuerName: "my-cluster-issuer"
```

### Configure TLS for Ingress

How you configure TLS for your Ingress will depend on which Ingress controller you are using.
Please refer to the documentation for your platform.

!!! tip "Share Certificate with Istio Gateway"

    In some cases, your Ingress can use the same TLS certificate as the Istio Gateway.
    By default, a Kubernetes `Secret` named `deploykf-istio-gateway-cert` which contains the certificate is found in the `deploykf-istio-gateway` namespace, managed by [this `Certificate`](https://github.com/deployKF/deployKF/blob/v0.1.1/generator/templates/manifests/deploykf-core/deploykf-istio-gateway/templates/gateway/Certificate.yaml) resource.

??? warning "Ingress Considerations"
    Pods which are in the [Istio mesh](https://istio.io/latest/about/service-mesh/) use hairpinning (via [this Istio `ServiceEntry`](https://github.com/deployKF/deployKF/blob/v0.1.1/generator/templates/manifests/deploykf-core/deploykf-istio-gateway/templates/gateway/ServiceEntry-gateway.yaml)) to access the gateway without leaving the cluster.
    This means that even if your Ingress has a valid TLS certificate, if you do not [Configure TLS for the Istio Gateway](#configure-tls-for-istio-gateway), you may see certificate errors when accessing services from within the cluster.
