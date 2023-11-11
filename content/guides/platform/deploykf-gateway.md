# Expose Gateway and configure HTTPS

This guide explains how to __expose__ the deployKF Gateway and __configure HTTPS__.

!!! contribute "Help Improve this Guide"

    This guide covers an incredibly broad topic with near limitless possible implementations.
    If you see anything incorrect or missing, please help us by [raising an issue](https://github.com/deployKF/website/issues/new/?title=[Feedback]+{{ page.title }})!

---

## Overview

The "deployKF Gateway Service" is the main network entry point to deployKF. 
By default, it is a [Kubernetes Service](https://kubernetes.io/docs/concepts/services-networking/service/) named `deploykf-gateway` pointing to our [Istio Ingress Gateway](https://istio.io/latest/docs/tasks/traffic-management/ingress/ingress-control/) pods.

## 1. Set Hostname and Ports

The hostnames and ports on which the deployKF Gateway listens are configured with these values:

Value | Purpose
--- | ---
[`deploykf_core.deploykf_istio_gateway.gateway.hostname`](https://github.com/deployKF/deployKF/blob/v0.1.3/generator/default_values.yaml#L653) | base domain name
[`deploykf_core.deploykf_istio_gateway.gateway.ports`](https://github.com/deployKF/deployKF/blob/v0.1.3/generator/default_values.yaml#L654) | ports for HTTP/HTTPS

For example, the following values will use `deploykf.example.com` on port `80` and `443`:

```yaml
deploykf_core:
  deploykf_istio_gateway:
    gateway:
      ## NOTE: this domain and its subdomains must be dedicated to deployKF
      hostname: deploykf.example.com
      
      ## NOTE: these are the defaults, but if you are using 'sample-values.yaml' 
      ##       as a base, the defaults are 8080/8443, so you will need to 
      ##       override them to use the standard ports 
      ports:
        http: 80
        https: 443
```

Depending on which tools you have enabled, the gateway may serve the following hostnames:

Hostname | Description
--- | ---
`deploykf.example.com` | the deployKF Gateway
`argo-server.deploykf.example.com` | the Argo Server UI
`minio-api.deploykf.example.com` | the MinIO API
`minio-console.deploykf.example.com` | the MinIO UI

## 2. Expose the Gateway Service

So your users can access deployKF, the deployKF Gateway Service will need to be accessible from outside the cluster.
There are two main options to expose the deployKF Gateway Service:

1. Use a [LoadBalancer](https://kubernetes.io/docs/concepts/services-networking/service/#loadbalancer) type `Service` (recommended)
2. Configure an [`Ingress`](https://kubernetes.io/docs/concepts/services-networking/ingress/#what-is-ingress)

??? steps "Expose Gateway Service - _LoadBalancer Service_ :star:"

    Most Kubernetes platforms provide a LoadBalancer Service that can expose on a public/private IP address.
    
    To use this option, you will generally need to do the following:

    1. Set the [`deploykf_core.deploykf_istio_gateway.gatewayService.type`](https://github.com/deployKF/deployKF/blob/v0.1.1/generator/default_values.yaml#L653) value to `"LoadBalancer"` (the default)
    2. Use the [`deploykf_core.deploykf_istio_gateway.gatewayService.annotations`](https://github.com/deployKF/deployKF/blob/v0.1.1/generator/default_values.yaml#L654C7-L654C18) value to configure the Service

    ---

    How you configure a LoadBalancer Service will depend on the platform you are using, for example:

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

??? steps "Expose Gateway Service - _Ingress_"

    Most Kubernetes platforms provide an Ingress class that can expose on a public/private IP address.
    
    To use this option, you will generally need to do the following:

    1. Set the [`deploykf_core.deploykf_istio_gateway.gatewayService.type`](https://github.com/deployKF/deployKF/blob/v0.1.1/generator/default_values.yaml#L653) value to `"NodePort"` or `"ClusterIP"`
    2. Use the [`deploykf_core.deploykf_istio_gateway.gatewayService.annotations`](https://github.com/deployKF/deployKF/blob/v0.1.1/generator/default_values.yaml#L654C7-L654C18) value to configure the Service
    3. Create an `Ingress` resource that points to the `deploykf-gateway` Service

    ---

    How you configure an Ingress will depend on the platform you are using, for example:

    ??? config "Amazon Web Services (EKS)"

        The [AWS Load Balancer Controller](https://kubernetes-sigs.github.io/aws-load-balancer-controller/) is commonly used to configure Ingress resources on EKS.

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

!!! danger "Public Internet"

    You should seriously consider the security implications of exposing the deployKF Gateway to the public internet.
    Given the nature of ML Platforms, most organizations choose to expose the gateway on their private network, and then use a VPN or other secure connection to access it.

!!! warning "Ingress vs LoadBalancer"

    In most cases, using a LoadBalancer Service rather than an Ingress is preferred for the following reasons:

    1. __Faster__: less hops between the client and the gateway
    2. __Future-proof__: deployKF might expose non-HTTP services in the future
    3. __Simpler TLS__: many Ingress controllers don't support TLS passthrough

!!! info "Including Arbitrary Manifests"

    deployKF provides an `extraManifests` value for each component which allows arbitrary YAML manifests to be added to the generated output.
    
    For example, [`deploykf_core.deploykf_istio_gateway.extraManifests`](https://github.com/deployKF/deployKF/blob/v0.1.1/generator/default_values.yaml#L575-L579) may be used to add a custom Ingress or Secret resource to the generated output of the `deploykf-istio-gateway` component.

## 3. Configure DNS

Now that the deployKF Gateway Service has an IP address, you must configure DNS records which point to it.
There are two main options to provision DNS records:

1. Automatically with [External-DNS](https://github.com/kubernetes-sigs/external-dns) (recommended)
2. Manually with your DNS provider

??? steps "Configure DNS - _External-DNS_ :star:"

    [External-DNS](https://github.com/kubernetes-sigs/external-dns) is a Kubernetes controller that automatically configures DNS records for Kubernetes resources.

    To use this option, you will generally need to do the following:

    1. Install External-DNS and connect it to your DNS provider
    2. Configure External-DNS to set DNS records for the deployKF Gateway Service
    ---

    __Step 1:__ Install External-DNS

    The External-DNS documentation provides instructions for [installing External-DNS on various platforms](https://kubernetes-sigs.github.io/external-dns/latest/#deploying-to-a-cluster).

    Here are some popular platforms:

    Cloud Platform | DNS Provider
    --- | ---
    Amazon Web Services | [Route53](https://kubernetes-sigs.github.io/external-dns/latest/tutorials/aws/)
    Google Cloud | [Cloud DNS](https://kubernetes-sigs.github.io/external-dns/latest/tutorials/gke/)
    Microsoft Azure | [Azure DNS](https://kubernetes-sigs.github.io/external-dns/latest/tutorials/azure/), [Azure Private DNS](https://kubernetes-sigs.github.io/external-dns/latest/tutorials/azure-private-dns/)
    Any | [Cloudflare](https://kubernetes-sigs.github.io/external-dns/latest/tutorials/cloudflare/), [Akamai Edge DNS](https://kubernetes-sigs.github.io/external-dns/latest/tutorials/akamai-edgedns/)

    ---

    __Step 2:__ Configure External-DNS

    There are a few ways to configure External-DNS so that it sets DNS records for the deployKF Gateway Service.

    ??? config "Configure External-DNS - _Automatically from Istio Gateway_ :star:"

        You may configure External-DNS to automatically extract the domain names from Istio `Gateway` resources.
       
        If you do this, a separate DNS record is created for each [domain selected by our Istio `Gateway`](https://github.com/deployKF/deployKF/blob/v0.1.1/generator/templates/manifests/deploykf-core/deploykf-istio-gateway/templates/gateway/Gateway.yaml#L14-L25).

        To [connect External-DNS with Istio](https://kubernetes-sigs.github.io/external-dns/latest/tutorials/istio/), you will need to:

        1. Update your `Deployment/external-dns` to set the `--source=istio-gateway` start argument
        2. Update your `ClusterRole/external-dns` to allow access to Istio `Gateway` and `VirtualService` resources

    ??? config "Configure External-DNS - _Manual Annotations_"

        You can manually configure External-DNS by annotating the `Service` or `Ingress` resource with the [`external-dns.alpha.kubernetes.io/hostname`](https://kubernetes-sigs.github.io/external-dns/latest/faq/#how-do-i-specify-a-dns-name-for-my-kubernetes-objects) annotation.
        
        If you do this, you need to add BOTH the __base domain__ AND __subdomains__.
        You can avoid the need to specify each subdomain by using a wildcard DNS record, but you will still need to specify the base domain.
        Multiple hostnames can be specified in a single annotation using a comma-separated list.

        Depending on if you are using a Service or Ingress, you will set the `external-dns.alpha.kubernetes.io/hostname` annotation by:

        - __Service__: setting the [`deploykf_core.deploykf_istio_gateway.gatewayService.annotations`](https://github.com/deployKF/deployKF/blob/v0.1.1/generator/default_values.yaml#L654) value
        - __Ingress__: manually annotating your Ingress resource

    ---

    !!! danger "Deletion of DNS Records"

        Be aware that External-DNS will __delete__ the DNS records associated with resources when they are deleted:

        - When using the annotation method, deleting the `Service` or `Ingress` resource will delete the associated DNS records.
        - When using `--source=istio-gateway`, deleting the Istio `Gateway` or `VirtualService` will delete the associated DNS records.

        Remember that DNS records take time to propagate, so you may experience downtime if you delete resources and then recreate them.

??? steps "Configure DNS - _Manual_"

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

    You need to create records for BOTH the __base domain__ AND __subdomains__.
    You can avoid the need to specify each subdomain by using a wildcard DNS record, but you will still need to specify the base domain.

!!! info "Wildcard DNS Records"

    If you plan to manually create the records (either via External-DNS annotations or manual record creation), we recommend using a [wildcard DNS record](https://en.wikipedia.org/wiki/Wildcard_DNS_record) to account for any future subdomains that may be added to the deployKF Gateway Service.

    For example, you might set BOTH the following DNS records:

    - `*.deploykf.example.com`
    - `deploykf.example.com`

## 4. Configure HTTPS/TLS

Now that the deployKF Gateway Service has a DNS pointing to it, to prevent self-signed certificate errors, you must configure a way to make the TLS certificates valid.

- If you are exposing the Gateway with a __LoadBalancer type Service__, then ONLY the Istio Gateway will need to be configured with valid TLS certificates.
- If you are exposing the Gateway with an __Ingress__, then BOTH the Istio Gateway and the Ingress will need to be configured with valid TLS certificates (unless your Ingress supports TLS passthrough, which most do not).

The following sections explain how to configure TLS at the _Istio Gateway_ and _Ingress_ levels.

??? steps "Configure TLS - _Istio Gateway_ :star:"

    This section explains how to configure TLS for the Istio Gateway (which you will always need to do).

    ---

    deployKF includes [cert-manager](https://cert-manager.io/) to automatically generate TLS certificates for the Istio Gateway.
    
    By default, the Istio Gateway uses a self-signed certificate generated by [this `ClusterIssuer`](https://github.com/deployKF/deployKF/blob/v0.1.1/generator/templates/manifests/deploykf-dependencies/cert-manager/templates/ClusterIssuer-kubeflow-gateway-issuer.yaml), which is fine for testing (especially if you don't own the domain you are using), but not recommended for production usage.
    
    To have cert-manager generate valid TLS certificates for the Istio Gateway, you will need to:
    
    1. Connect cert-manager to your DNS provider
    2. Create a `ClusterIssuer` resource that can generate certificates for your domain
    3. Configure the Istio Gateway to use your `ClusterIssuer` to generate certificates
    
    ---

    !!! question_secondary "Can I bring my own cert-manager?"
    
        Yes. deployKF includes an embedded version of cert-manager, but if you want to bring your own, you may set the [`deploykf_dependencies.cert_manager.enabled`](https://github.com/deployKF/deployKF/blob/v0.1.1/generator/default_values.yaml#L75) value to `false`.
        
        Note, if you do this, the [`deploykf_dependencies.cert_manager.clusterIssuer`](https://github.com/deployKF/deployKF/blob/v0.1.1/generator/default_values.yaml#L164-L171) values are still used to select the `ClusterIssuer` (provisioned by you), which is used to generate certificates for the Istio Gateway.

    !!! info "ServiceAccount Annotations"
    
        To use Pod-based authentication with your DNS Provider (for example, to use IRSA on EKS), you may need to annotate the cert-manager ServiceAccount.
        
        Custom ServiceAccount annotations may be applied to the embedded cert-manager with the [`deploykf_dependencies.cert_manager.controller.serviceAccount.annotations`](https://github.com/deployKF/deployKF/blob/v0.1.1/generator/default_values.yaml#L155) value.

    ---    

    <h4> STEP 1: Connect cert-manager to DNS Provider</h4>
    
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
    
    !!! tip "Issuer Kind"
    
        Most cert-manager examples show an `Issuer` resource. 
        Note that any issuer may be converted to its equivalent cluster version by changing the `kind` field from `"Issuer"` to `"ClusterIssuer"` and removing the `metadata.namespace` field.

    ---

    <h4>STEP 2: Create a ClusterIssuer</h4>
    
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

    ---

    <h4>STEP 3: Configure the Istio Gateway</h4>
    
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

??? steps "Configure TLS - _Ingress_"

    This section explains how to configure TLS for your Ingress (if you are using one).

    !!! warning "Both Istio Gateway and Ingress need valid TLS"

        Pods which are in the [Istio mesh](https://istio.io/latest/about/service-mesh/) use hairpinning (via [this Istio `ServiceEntry`](https://github.com/deployKF/deployKF/blob/v0.1.1/generator/templates/manifests/deploykf-core/deploykf-istio-gateway/templates/gateway/ServiceEntry-gateway.yaml)) to access the gateway without leaving the cluster.
        This means that even if your Ingress has a valid TLS certificate, if you do not _Configure TLS for the Istio Gateway_, you may see certificate errors when accessing services from within the cluster.

    ---

    How you configure TLS for your Ingress will depend on which Ingress controller you are using.
    Please refer to the documentation for your platform.

    !!! tip "Share Certificate with Istio Gateway"

        In some cases, your Ingress can use the same TLS certificate as the Istio Gateway.

        By default, a Kubernetes `Secret` named `deploykf-istio-gateway-cert` which contains the certificate is found in the `deploykf-istio-gateway` namespace, managed by [this `Certificate`](https://github.com/deployKF/deployKF/blob/v0.1.1/generator/templates/manifests/deploykf-core/deploykf-istio-gateway/templates/gateway/Certificate.yaml) resource.
        If your Ingress controller supports referencing a Kubernetes `Secret` for TLS certificates, you can use this `Secret` to share the certificate with your Ingress.