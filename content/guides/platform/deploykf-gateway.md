---
description: >-
  Learn how to make deployKF accessible to your users, and how to configure HTTPS/TLS.

# TODO: remove status, after a while
status: new
---

# Expose Gateway and configure HTTPS

Learn how to __make deployKF accessible__ to your users, and how to __configure HTTPS/TLS__.

!!! contribute ""

    This guide covers an incredibly broad topic with near limitless possible implementations.
    If you see anything incorrect or missing, please help us by [raising an issue](https://github.com/deployKF/website/issues/new/?title=[Feedback]+{{ page.title }})!

---

## Expose the Gateway Service

deployKF uses [ :custom-istio-color: __Istio__](../dependencies/istio.md#what-is-istio) for networking.
Clients access deployKF through the Pods of an [Istio Gateway Deployment](../dependencies/istio.md#gateways) via a Kubernetes `Service` named `deploykf-gateway`.
This Service needs to be accessible from outside the cluster to allow users to access the deployKF dashboard and other tools.

!!! danger "Public Internet"

    The default Service type is `LoadBalancer`, this may expose your deployKF Gateway to the public internet (depending on how your Kubernetes cluster is configured).

    You should seriously consider the security implications of exposing the deployKF Gateway to the public internet.
    Most organizations choose to expose the gateway on a private network, and then use a VPN or other secure connection to access it.


You can expose the `deploykf-gateway` Service in a few different ways, depending on your platform and requirements:

### __Use kubectl port-forward__

If you are just testing the platform, you may use [`kubectl port-forward`](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_port-forward/) to access a Service from your local machine.

??? steps "Step 1 - Modify Hosts"
    
    The _deployKF Istio Gateway_ uses the HTTP `Host` header to route requests to the correct internal service.
    This means that using `localhost` or `127.0.0.1` will NOT work.
    
    === "macOS"
    
        You will need to add the following lines to the END of your __local__ `/etc/hosts` file:
    
        ```text
        127.0.0.1 deploykf.example.com
        127.0.0.1 argo-server.deploykf.example.com
        127.0.0.1 minio-api.deploykf.example.com
        127.0.0.1 minio-console.deploykf.example.com
        ```
    
    === "Linux"
    
        You will need to add the following lines to the END of your __local__ `/etc/hosts` file:
    
        ```text
        127.0.0.1 deploykf.example.com
        127.0.0.1 argo-server.deploykf.example.com
        127.0.0.1 minio-api.deploykf.example.com
        127.0.0.1 minio-console.deploykf.example.com
        ```
    
    === "Windows"
    
        You will need to add the following lines to the END of your `C:\Windows\System32\drivers\etc\hosts` file:
    
        ```text
        127.0.0.1 deploykf.example.com
        127.0.0.1 argo-server.deploykf.example.com
        127.0.0.1 minio-api.deploykf.example.com
        127.0.0.1 minio-console.deploykf.example.com
        ```
      
        !!! warning "Edit hosts file as Administrator"
    
            The hosts file can ONLY be edited by the Windows _Administrator_ user.
    
            Run this PowerShell command to start an _Administrator_ Notepad, which can edit the hosts file:
        
            ```powershell
            Start-Process notepad.exe -ArgumentList "C:\Windows\System32\drivers\etc\hosts" -Verb RunAs
            ```

??? steps "Step 2 - Port-Forward the Gateway"
    
    You may now port-forward the `deploykf-gateway` Service using this `kubectl` command:
    
    ```shell
    kubectl port-forward \
      --namespace "deploykf-istio-gateway" \
      svc/deploykf-gateway 8080:http 8443:https
    ```
    
    The deployKF dashboard should now be available on your local machine at:
        
      :material-arrow-right-bold: [https://deploykf.example.com:8443/](https://deploykf.example.com:8443/)
    
    ---

    !!! warning "Port-Forwards Known Issues"
    
        There are upstream issues which can cause you to need to restart the port-forward, see [`kubernetes/kubernetes#74551`](https://github.com/kubernetes/kubernetes/issues/74551) for more information.

### __Use a LoadBalancer Service__

Most Kubernetes platforms provide a [LoadBalancer](https://kubernetes.io/docs/concepts/services-networking/service/#loadbalancer)-type Service that can be used to expose Pods on a private or public IP address.
How you configure a LoadBalancer Service will depend on the platform you are using, for example:

??? config "AWS - Network Load Balancer"

    The [AWS Load Balancer Controller](https://kubernetes-sigs.github.io/aws-load-balancer-controller/) is commonly used to configure LoadBalancer services on EKS.

    For example, you might set the following values to use a [Network Load Balancer (NLB)](https://docs.aws.amazon.com/elasticloadbalancing/latest/network/introduction.html):

    ```yaml
    deploykf_core:
      deploykf_istio_gateway:

        ## these values configure the deployKF Gateway Service
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

          ## the ports the gateway Service listens on
          ##  - defaults to the corresponding port under `gateway.ports`
          ##  - these are the "public" ports which clients will connect to
          ##    (they impact the user-facing HTTP links)
          ##
          ports:
            http: 80
            https: 443
    ```

??? config "Google Cloud - Network Load Balancer"

    GKE, has a LoadBalancer Service type, which is configured with annotations like [`networking.gke.io/load-balancer-type`](https://cloud.google.com/kubernetes-engine/docs/concepts/service-load-balancer-parameters). 

    For example, you might set the following values to use an [INTERNAL Passthrough Network Load Balancer](https://cloud.google.com/kubernetes-engine/docs/concepts/service-load-balancer):

    ```yaml
    deploykf_core:
      deploykf_istio_gateway:

        ## these values configure the deployKF Gateway Service
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

          ## the ports the gateway Service listens on
          ##  - defaults to the corresponding port under `gateway.ports`
          ##  - these are the "public" ports which clients will connect to
          ##    (they impact the user-facing HTTP links)
          ##
          ports:
            http: 80
            https: 443
    ```

### __Use a Kubernetes Ingress__

Most Kubernetes platforms provide an [Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/) class that can expose cluster services behind an application-layer load balancer.
How you configure an Ingress will depend on the platform you are using, for example:

??? config "AWS - Application Load Balancer"

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

        ## this value adds arbitrary manifests to the generated output
        ##
        extraManifests:
          - |
            apiVersion: networking.k8s.io/v1
            kind: Ingress
            metadata:
              name: deploykf-gateway
              annotations:
                alb.ingress.kubernetes.io/scheme: internal
                alb.ingress.kubernetes.io/target-type: ip
                alb.ingress.kubernetes.io/backend-protocol: HTTPS

                ## the 'deploykf-gateway' service has a named "status-port" pointing to Istio's 15021 health port
                ## see: https://istio.io/latest/docs/ops/deployment/requirements/#ports-used-by-istio
                alb.ingress.kubernetes.io/healthcheck-port: "status-port"
                alb.ingress.kubernetes.io/healthcheck-path: "/healthz/ready"

                alb.ingress.kubernetes.io/listen-ports: '[{"HTTP": 80}, {"HTTPS": 443}]'
                alb.ingress.kubernetes.io/ssl-redirect: "443"
                alb.ingress.kubernetes.io/certificate-arn: |
                  arn:aws:acm:REGION_NAME:ACCOUNT_ID:certificate/CERTIFICATE_ID
            spec:
              ingressClassName: alb                  
              rules:
                - host: "deploykf.example.com"
                  http:
                    paths:
                      - path: "/"
                        pathType: Prefix
                        backend:
                          service:
                            name: "deploykf-gateway"
                            port:
                              name: https
                - host: "*.deploykf.example.com"
                  http:
                    paths:
                      - path: "/"
                        pathType: Prefix
                        backend:
                          service:
                            name: "deploykf-gateway"
                            port:
                              name: https

        ## these values configure the deployKF Istio Gateway
        ##
        gateway:
          ## when using an ingress, standard ports are required
          ## (the default in 'sample-values.yaml' are 8080/8443)
          ports:
            http: 80
            https: 443

          ## these values configure TLS
          ##
          tls:
            ## ALB does NOT forward the SNI after TLS termination, 
            ## so we must disable SNI matching in the gateway
            matchSNI: false

        ## these values configure the deployKF Gateway Service
        ##
        gatewayService:
          name: "deploykf-gateway"
          ## WARNING: must be "NodePort" if "alb.ingress.kubernetes.io/target-type" is "instance"
          type: "ClusterIP"
          annotations: {}
    ```

??? config "Google Cloud - Application Load Balancer"

    GKE, has an Ingress class that can be used to configure Ingress resources for external or internal access. 

    In the following example, we are configuring the GKE Ingress to use the same TLS certificate as the deployKF Gateway Service (found in `Secret/deploykf-istio-gateway-cert`).
    Later in this guide you will learn how to [make this certificate valid](#configure-tls-certificates), and not self-signed.

    !!! warning "Google Managed Certificates"

        _Google Managed Certificates_ are [only supported](https://cloud.google.com/kubernetes-engine/docs/how-to/managed-certs#prerequisites) by EXTERNAL Application Load Balancers (ALB).
        Because using an EXTERNAL ALB would expose deployKF to the public internet, we instead strongly recommend [configuring cert-manager](#configure-tls-certificates) to generate a valid certificate.

    For example, you might set the following values to use an [INTERNAL Application Load Balancer](https://cloud.google.com/kubernetes-engine/docs/concepts/ingress):

    ```yaml
    deploykf_core:
      deploykf_istio_gateway:

        ## this value adds arbitrary manifests to the generated output
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

        ## these values configure the deployKF Istio Gateway
        ##
        gateway:
          ## when using an ingress, standard ports are required
          ## (the default in 'sample-values.yaml' are 8080/8443)
          ports:
            http: 80
            https: 443

        ## these values configure the deployKF Gateway Service
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

??? config "Nginx Ingress"

    Many clusters are configured with the [Nginx Ingress Controller](https://kubernetes.github.io/ingress-nginx/).

    In the following example, we are configuring the Nginx Ingress to use the same TLS certificate as the deployKF Gateway Service (found in `Secret/deploykf-istio-gateway-cert`).
    Later in this guide you will learn how to [make this certificate valid](#configure-tls-certificates), and not self-signed.

    For example, you might set the following values:

    ```yaml
    deploykf_core:
      deploykf_istio_gateway:

        ## this value adds arbitrary manifests to the generated output
        ##
        extraManifests:
          - |
            apiVersion: networking.k8s.io/v1
            kind: Ingress
            metadata:
              name: deploykf-gateway
              annotations:
                nginx.ingress.kubernetes.io/backend-protocol: HTTPS

                ## nginx wil NOT proxy the SNI by default
                ## see: https://kubernetes.github.io/ingress-nginx/user-guide/nginx-configuration/annotations/#backend-certificate-authentication
                nginx.ingress.kubernetes.io/proxy-ssl-name: "deploykf.example.com"
                nginx.ingress.kubernetes.io/proxy-ssl-server-name: "on"

                ## this config is needed due to a bug in ingress-nginx
                ## see: https://github.com/kubernetes/ingress-nginx/issues/6728
                nginx.ingress.kubernetes.io/proxy-ssl-secret: "deploykf-istio-gateway/deploykf-istio-gateway-cert"
            spec:
              ingressClassName: nginx
              tls:
                ## NOTE: this secret is created as part of the deployKF installation
                - secretName: "deploykf-istio-gateway-cert"
              rules:
                - host: "deploykf.example.com"
                  http:
                    paths:
                      - path: "/"
                        pathType: Prefix
                        backend:
                          service:
                            name: "deploykf-gateway"
                            port:
                              name: https
                - host: "*.deploykf.example.com"
                  http:
                    paths:
                      - path: "/"
                        pathType: Prefix
                        backend:
                          service:
                            name: "deploykf-gateway"
                            port:
                              name: https

        ## these values configure the deployKF Istio Gateway
        ##
        gateway:
          ## when using an ingress, standard ports are required
          ## (the default in 'sample-values.yaml' are 8080/8443)
          ports:
            http: 80
            https: 443

        ## these values configure the deployKF Gateway Service
        ##
        gatewayService:
          name: "deploykf-gateway"
          type: "ClusterIP"
          annotations: {}
    ```

There are a few important things to note when using an Ingress:

??? warning "Ingress TLS Termination / SNI Matching"

    If you put the deployKF Gateway behind a proxy which terminates TLS (like AWS ALB), you will probably need to disable _SNI Matching_.
    This is because most proxies don't forward the original request's [Server Name Indication (SNI)](https://en.wikipedia.org/wiki/Server_Name_Indication) to the backend service after TLS termination.

    To disable _SNI Matching_, set [`deploykf_core.deploykf_istio_gateway.gateway.tls.matchSNI`](https://github.com/deployKF/deployKF/blob/v0.1.4/generator/default_values.yaml#L741-L746) to `false`:

    ```yaml
    deploykf_core:
      deploykf_istio_gateway:
        gateway:
          tls:
            matchSNI: false
    ```

??? warning "HTTPS Redirection"

    By default, the deployKF Gateway redirects all HTTP requests to HTTPS.
    This means any proxy you place in front of the gateway will need to talk to the gateway over HTTPS.

    ---

    By default, the deployKF Istio Gateway uses a self-signed certificate, to make your proxy trust this certificate you will probably need to do ONE of the following:

    1. [Configure a valid certificate for the gateway](#configure-tls-certificates)
    2. Trust the certificate in `Secret/deploykf-istio-gateway-cert` (Namespace: `deploykf-istio-gateway`)
    3. Trust the CA found in `Secret/selfsigned-ca-issuer-root-cert` (Namespace: `cert-manager`)
    4. Disable backend certificate validation in your proxy

    ---

    If your proxy is simply unable to use HTTPS backends, and you don't require end-to-end encryption, you may disable the automatic redirection by setting [`deploykf_core.deploykf_istio_gateway.gateway.tls.redirect`](https://github.com/deployKF/deployKF/blob/v0.1.4/generator/default_values.yaml#L748-L758) to `false`:

    ```yaml
    deploykf_core:
      deploykf_istio_gateway:
        gateway:
          tls:
            redirect: false
    ```

---

## Configure DNS Records

Now that the deployKF Gateway Service has an IP address, you must configure DNS records which point to it.

!!! warning "Virtual Hostname Routing"

    You can't access deployKF using the IP address alone.
    This is because deployKF hosts multiple services on the same IP address using [virtual hostname routing](https://en.wikipedia.org/wiki/Virtual_hosting#Name-based).

### __Hostname and Ports__

deployKF uses a combination of _hostnames_, _http paths_, and _ports_ to route requests to the correct internal service.
Depending on which tools you have enabled, the gateway may serve the following hostnames:

Hostname | Description
--- | ---
`deploykf.example.com` | Base Domain (dashboard and other apps)
`argo-server.deploykf.example.com` | Argo Server
`minio-api.deploykf.example.com` | MinIO API
`minio-console.deploykf.example.com` | MinIO Console

These values set the base domain to `deploykf.example.com`, and the ports to `80` and `443`:

```yaml
deploykf_core:
  deploykf_istio_gateway:
    gateway:
      ## the "base domain" for deployKF
      ##  - this domain and its subdomains should be dedicated to deployKF
      ##
      hostname: deploykf.example.com
      
      ## the ports that gateway Pods listen on
      ##  - 80/443 are the defaults, but if you are using 'sample-values.yaml' 
      ##    as a base, the defaults are 8080/8443, so you will need to 
      ##    override them to use the standard ports
      ##
      ports:
        http: 80
        https: 443

    #gatewayService:
      
      ## the ports the gateway Service listens on
      ##  - defaults to the corresponding port under `gateway.ports`
      ##  - these are the "public" ports which clients will connect to
      ##    (they impact the user-facing HTTP links)
      ##
      #ports:
      #  http: ~
      #  https: ~
```

### __Use External-DNS__

[External-DNS](https://github.com/kubernetes-sigs/external-dns) is a Kubernetes controller that automatically configures DNS records for Kubernetes resources.
The following steps explain how to install and configure External-DNS to set DNS records for the deployKF Gateway Service.

??? steps "Step 1 - Install External-DNS"

    The External-DNS documentation provides instructions for [installing External-DNS on various platforms](https://kubernetes-sigs.github.io/external-dns/latest/#deploying-to-a-cluster).

    The following table links to the documentation for some popular DNS providers:

    Cloud Platform | DNS Provider Documentation
    --- | ---
    Amazon Web Services | [Route53](https://kubernetes-sigs.github.io/external-dns/latest/tutorials/aws/)
    Google Cloud | [Cloud DNS](https://kubernetes-sigs.github.io/external-dns/latest/tutorials/gke/)
    Microsoft Azure | [Azure DNS](https://kubernetes-sigs.github.io/external-dns/latest/tutorials/azure/), [Azure Private DNS](https://kubernetes-sigs.github.io/external-dns/latest/tutorials/azure-private-dns/)
    Any | [Cloudflare](https://kubernetes-sigs.github.io/external-dns/latest/tutorials/cloudflare/), [Akamai Edge DNS](https://kubernetes-sigs.github.io/external-dns/latest/tutorials/akamai-edgedns/)

    !!! danger "Deletion of DNS Records"
    
        Unless the `--policy=upsert-only` argument is used, external-dns will __delete DNS records__ when a resource is deleted (or changed in a way that would affect the records).
        Records take time to propagate, so you may experience downtime if you delete resources and then recreate them.

??? steps "Step 2 - Configure External-DNS"

    There are a few ways to configure External-DNS so that it sets DNS records for the deployKF Gateway Service.

    ---

    <h3>Option 1 - Istio Gateway Source: :star:</h3>

    You may configure External-DNS to [extract hostnames names from Istio `Gateway` resources](https://kubernetes-sigs.github.io/external-dns/latest/tutorials/istio/).
    If you do this, a separate DNS record is created for each domain selected by [our Istio `Gateway`](https://github.com/deployKF/deployKF/blob/v0.1.4/generator/templates/manifests/deploykf-core/deploykf-istio-gateway/templates/gateway/Gateway.yaml#L2-L13).

    To connect External-DNS with Istio, you will need to:

    1. Update your `Deployment/external-dns` to include the `--source=istio-gateway` start argument
    2. Update your `ClusterRole/external-dns` to allow access to Istio `Gateway` and `VirtualService` resources

    ---

    <h3>Option 2 - Ingress Source:</h3>

    You may configure External-DNS to automatically extract the domain names from Kubernetes `Ingress` resources.
    If you do this, a separate DNS record is created for each hostname in the Ingress.

    To connect External-DNS with Ingress, you will need to:

    1. Update your `Deployment/external-dns` to include the `--source=ingress` start argument
    2. Update your `ClusterRole/external-dns` to allow access to Kubernetes `Ingress` resources

    ---

    <h3>Option 3 - Manual Annotation:</h3>

    You can manually configure External-DNS by annotating the `Service` or `Ingress` resource with the [`external-dns.alpha.kubernetes.io/hostname`](https://kubernetes-sigs.github.io/external-dns/latest/faq/#how-do-i-specify-a-dns-name-for-my-kubernetes-objects) annotation.
    Multiple hostnames can be specified in a single annotation using a __comma-separated__ list.
    
    The annotation can be set in one of the following ways:

    - __Service__: setting the [`deploykf_core.deploykf_istio_gateway.gatewayService.annotations`](https://github.com/deployKF/deployKF/blob/v0.1.4/generator/default_values.yaml#L809) value
    - __Ingress__: manually annotating your Ingress resource

    See the [manually create DNS records](#manually-create-dns-records) section for information about which records to create.

### __Manually Create DNS Records__

This section explains how to manually configure DNS records with your DNS provider.

??? steps "Step 1 - Get Service IP"

    You will need to find the IP address of the deployKF Gateway Service, this can be done by running the following command:

    ```shell
    kubectl get service deploykf-gateway --namespace deploykf-istio-gateway
    ```

    The `EXTERNAL-IP` field will contain the IP address of the deployKF Gateway Service.

    ```text
    NAME               TYPE           CLUSTER-IP     EXTERNAL-IP   PORT(S)                                         AGE
    deploykf-gateway   LoadBalancer   10.43.24.148   172.23.0.2    15021:30XXXX/TCP,80:30XXXX/TCP,443:30XXXX/TCP   1d
    ```

??? steps "Step 2 - Configure DNS Records"

    You can now configure DNS records with your DNS provider that target the IP address of the deployKF Gateway Service.

    You need to create records for BOTH the __base domain__ AND __subdomains__.
    You can avoid the need to specify each subdomain by using a [wildcard DNS record](https://en.wikipedia.org/wiki/Wildcard_DNS_record), but you will still need to specify the base domain.

    For example, you might set the following DNS records:

    [Type](https://en.wikipedia.org/wiki/List_of_DNS_record_types) | Name | Value
    --- | --- | ---
    A | `*.deploykf.example.com` | IP Address of the deployKF Gateway Service
    A | `deploykf.example.com` | IP Address of the deployKF Gateway Service

    !!! warning "Propagation Time"

        DNS records can take time to propagate, so you may experience downtime if you delete records and then recreate them.

---

## Configure TLS Certificates

deployKF uses [:custom-cert-manager-color: __cert-manager__](../dependencies/cert-manager.md#what-is-cert-manager) to manage TLS certificates.

By default, we use a self-signed certificate for the deployKF Gateway.
Therefore, if you are not using an external proxy to terminate TLS (like AWS ALB), you will likely want to configure a valid TLS certificate for the deployKF Gateway.

!!! info "Existing cert-manager Installation"

    If your cluster already has a cert-manager installation, you should follow [these instructions](../dependencies/cert-manager.md#can-i-use-my-existing-cert-manager) to disable the deployKF cert-manager installation and use your own.

!!! info "In-Mesh Traffic to Gateway"

    When Pods inside the Istio mesh make requests to the gateway [hostname/ports](#hostname-and-ports), this traffic bypasses your public LoadBalancer/Ingress and goes directly to the Gateway Deployment Pods (through the mesh).

    Therefore, even if your Ingress has its own valid TLS termination (e.g. from AWS ALB), in-mesh Pods will see the certificate of the Istio Gateway itself (which by default is self-signed).

    ??? question_secondary "Why does this happen?"

        Traffic from in-mesh Pods gets intercepted by the Istio sidecar because of [this `ServiceEntry`](https://github.com/deployKF/deployKF/blob/v0.1.4/generator/templates/manifests/deploykf-core/deploykf-istio-gateway/templates/gateway/ServiceEntry-gateway.yaml), and because we enable Istio's [DNS Proxying](https://istio.io/latest/docs/ops/configuration/traffic-management/dns-proxy/) feature by setting `ISTIO_META_DNS_CAPTURE` and `ISTIO_META_DNS_AUTO_ALLOCATE` to `true`.

    ??? question_secondary "How can I prevent these TLS errors?"

        All core deployKF apps are configured to trust the default self-signed certificate (e.g. [oauth2-proxy](https://github.com/deployKF/deployKF/blob/v0.1.3/generator/templates/manifests/deploykf-core/deploykf-auth/templates/oauth2-proxy/Deployment.yaml#L69-L70)).
        However, your own in-mesh apps will need to do ONE of the following (unless you use a valid certificate):

        1. Disable _Istio DNS Proxying_ on your app's Pods:
            - Set the `proxy.istio.io/config` Pod annotation to `{"proxyMetadata": {"ISTIO_META_DNS_CAPTURE": "false", "ISTIO_META_DNS_AUTO_ALLOCATE": "false"}}`
        2. Disable certificate validation in your app:
            - _See your app's documentation for information on how to do this._
        3. Trust the CA found in `Secret/selfsigned-ca-issuer-root-cert` (Namespace: `cert-manager`):
            - _See your app's documentation for information on how to do this._
            - Note, we create a [trust-manager `Bundle`](https://github.com/deployKF/deployKF/blob/v0.1.3/generator/templates/manifests/deploykf-dependencies/cert-manager/templates/selfsigned-ca-issuer/Bundle.yaml) for this CA by default;
              All Namespaces with the label `deploykf.github.io/inject-root-ca-cert: "enabled"` will have a `ConfigMap` named `deploykf-gateway-issuer-root-ca-cert` with a key named `root-cert.pem` containing the CA certificate.

### __Use Let's Encrypt with Cert-Manager__

For almost everyone, the best Certificate Authority (CA) is [Let's Encrypt](https://letsencrypt.org/).
The following steps explain how to use Let's Encrypt with cert-manager to generate a valid TLS certificate for the deployKF Gateway.

??? steps "Step 1 - Connect Cert-Manager to DNS Provider"

    Because deployKF uses a [wildcard `Certificate`](https://github.com/deployKF/deployKF/blob/v0.1.4/generator/templates/manifests/deploykf-core/deploykf-istio-gateway/templates/gateway/Certificate.yaml#L16), you MUST use the [`DNS-01`](https://letsencrypt.org/docs/challenge-types/#dns-01-challenge) challenge to verify domain ownership (rather than [`HTTP-01`](https://letsencrypt.org/docs/challenge-types/#http-01-challenge)).
    This requires you to configure cert-manager so that it is able to create DNS records.

    The cert-manager documentation provides [instructions for configuring `DNS-01` challenges](https://cert-manager.io/docs/configuration/acme/dns01/) for various DNS providers.
    The following table links to the documentation for some popular DNS providers:

    Cloud Platform | DNS Provider Documentation
    --- | ---
    Amazon Web Services | [Route53](https://cert-manager.io/docs/configuration/acme/dns01/route53/)
    Google Cloud | [Cloud DNS](https://cert-manager.io/docs/configuration/acme/dns01/google/)
    Microsoft Azure | [Azure DNS](https://cert-manager.io/docs/configuration/acme/dns01/azuredns/)
    Any | [Cloudflare](https://cert-manager.io/docs/configuration/acme/dns01/cloudflare/), [Akamai Edge DNS](https://cert-manager.io/docs/configuration/acme/dns01/akamai/)

    !!! info "ServiceAccount Annotations"
    
        To use Pod-based authentication with your DNS Provider (for example, to use IRSA on EKS), you may need to annotate the cert-manager ServiceAccount.
        
        Custom ServiceAccount annotations may be applied to the embedded cert-manager with the [`deploykf_dependencies.cert_manager.controller.serviceAccount.annotations`](https://github.com/deployKF/deployKF/blob/v0.1.4/generator/default_values.yaml#L177) value:

        ```yaml
        deploykf_dependencies:
          cert_manager:
            controller:

              ## EXAMPLE: for Azure AD Workload Identity
              #podLabels:
              #  azure.workload.identity/use: "true"

              serviceAccount:
                annotations: 
                  ## EXAMPLE: for AWS IRSA
                  #eks.amazonaws.com/role-arn: "arn:aws:iam::MY_ACCOUNT_ID:role/MY_ROLE_NAME"

                  ## EXAMPLE: for GCP Workload Identity
                  #iam.gke.io/gcp-service-account=GSA_NAME@GSA_PROJECT.iam.gserviceaccount.com

                  ## EXAMPLE: for Azure AD Workload Identity
                  #azure.workload.identity/client-id: "00000000-0000-0000-0000-000000000000"
                  #azure.workload.identity/tenant-id: "00000000-0000-0000-0000-000000000000"
        ```

??? steps "Step 2 - Create a ClusterIssuer"

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

        Most cert-manager examples show an `Issuer` resource. 
        Note that any issuer may be converted to its equivalent cluster version by changing the `kind` field from `"Issuer"` to `"ClusterIssuer"` and removing the `metadata.namespace` field.

??? steps "Step 3 - Configure the Istio Gateway"

    Once you have a `ClusterIssuer` resource that can generate certificates for your domain, you must configure the deployKF Istio Gateway to use it.
    This is done by using the [`deploykf_dependencies.cert_manager.clusterIssuer`](https://github.com/deployKF/deployKF/blob/v0.1.4/generator/default_values.yaml#L186-L193) values.

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