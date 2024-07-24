---
icon: custom/istio
description: >-
  Learn how and why deployKF uses Istio.
  Learn how to integrate your existing Istio with deployKF and Kubeflow.
---

# Istio

Learn how and why deployKF uses Istio.
Learn how to integrate your existing Istio with deployKF and Kubeflow.

---

## __What is Istio?__

[:custom-istio-color: __Istio__](https://istio.io/) is a service mesh for Kubernetes which is based around the [:custom-envoy-color: __Envoy__](https://www.envoyproxy.io/) proxy.
A service mesh is a dedicated infrastructure layer for managing service-to-service network communication.

Istio changes Kubernetes Pod definitions (dynamically at runtime) so they have a sidecar container (Envoy proxy) which is configured to intercept all network traffic to and from the Pod.
Together, these sidecars form a mesh network that can implement advanced networking features like [Traffic Management](https://istio.io/latest/docs/concepts/traffic-management/), [Security](https://istio.io/latest/docs/concepts/security/), and [Observability](https://istio.io/latest/docs/concepts/observability/) with minimal changes to the application code.

### __How is Istio configured?__

The Istio mesh is configured declaratively using Kubernetes [Custom Resources (CRDs)](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/), so you don't need to configure the Envoy proxies directly.
Some of the most important Istio CRDs are: [`Gateway`](https://istio.io/latest/docs/reference/config/networking/gateway/), [`VirtualService`](https://istio.io/latest/docs/reference/config/networking/virtual-service/), [`DestinationRule`](https://istio.io/latest/docs/reference/config/networking/destination-rule/), [`ServiceEntry`](https://istio.io/latest/docs/reference/config/networking/service-entry/), [`PeerAuthentication`](https://istio.io/latest/docs/reference/config/security/peer_authentication/), [`AuthorizationPolicy`](https://istio.io/latest/docs/reference/config/security/authorization-policy/) and [`EnvoyFilter`](https://istio.io/latest/docs/reference/config/networking/envoy-filter/).

### __How can external traffic access the mesh?__

#### Mutual TLS

The Envoy sidecar uses [Mutual TLS (mTLS)](https://www.cloudflare.com/learning/access-management/what-is-mutual-tls/) to verify if network traffic destined for the Pod is coming from within the mesh.
Based on the [`PeerAuthentication`](https://istio.io/latest/docs/reference/config/security/peer_authentication/) policy for the Pod, the Envoy sidecar will either allow or deny external traffic (not from within the mesh).

!!! info "Istio `PeerAuthentication` Policies"

    If external traffic is allowed to reach the Pod (like when `PeerAuthentication` has an `mtls.mode` of [`PERMISSIVE`](https://istio.io/latest/docs/reference/config/security/peer_authentication/#PeerAuthentication-MutualTLS-Mode)), it will be accessing the Pod directly, effectively bypassing the mesh.
    This means that `AuthorizationPolicy` and `EnvoyFilter` policies would not be applied to that traffic.

#### Gateways

To expose services in the mesh to external traffic (e.g. from the internet), Istio provides the concept of a "Gateway", which sits at the edge of the mesh and can route external traffic to virtual services defined in the mesh.

The idea of _"Gateways"_ is a common source of confusion for new Istio users because it refers to two different things.

Gateway Deployments | Gateway Resources
--- | ---
A Kubernetes [`Deployment` of special Envoy proxy `Pods`](https://istio.io/latest/docs/setup/additional-setup/gateway/) which act as an "entry point" to the mesh. | The [`Gateway`](https://istio.io/latest/docs/reference/config/networking/gateway/) is the CRD which configures the Envoy proxies of a "Gateway Deployment", and can be selected by [`VirtualServices`](https://istio.io/latest/docs/reference/config/networking/virtual-service/) to define routes to Pods in the mesh.

Here are examples of the two different types of "Gateway" in Istio:

??? code "Example - _Gateway Deployment_"

    The following `Deployment` will be automatically mutated by Istio to include an Envoy proxy sidecar container:

    ```yaml
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: my-gateway-deployment
      namespace: gateway-namespace
    spec:
      selector:
        matchLabels:
          istio: my-gateway-deployment
      template:
        metadata:
          annotations:
            ## this tells istio to inject using the "gateway" template,
            ## rather than the "sidecar" template (which is the default)
            inject.istio.io/templates: "gateway"
          labels:
            ## this ensures that the istio-proxy container is injected
            sidecar.istio.io/inject: "true"
            
            ## the pod label (same as any normal kubernetes deployment)
            ## but which is also used by Gateway resources to select these pods
            istio: my-gateway-deployment
        spec:
          ## allow binding to all ports (such as 80 and 443)
          securityContext:
            sysctls:
              - name: net.ipv4.ip_unprivileged_port_start
                value: "0"
          containers:
            - name: istio-proxy
              
              ## the image is automatically replaced by istio
              image: auto
              
              ## drop all privileges, allowing running as non-root
              securityContext:
                capabilities:
                  drop:
                    - ALL
                runAsUser: 1337
                runAsGroup: 1337
    ```
    
    The following `Service` exposes the "Gateway Deployment" from above with a `LoadBalancer` type so it can be accessed from outside the cluster:

    ```yaml
    apiVersion: v1
    kind: Service
    metadata:
      name: my-gateway-service
      namespace: gateway-namespace
    spec:
      type: LoadBalancer
      selector:
        istio: my-gateway-deployment
      ports:
        - port: 80
          name: http
        - port: 443
          name: https
    ```

??? code "Example - _Gateway Resource_"

    The following `Gateway` resource configures the "Gateway Deployment" from above:
    
    ```yaml
    apiVersion: networking.istio.io/v1beta1
    kind: Gateway
    metadata:
      name: my-gateway
      namespace: gateway-namespace
    spec:
      ## a selector for Pod labels, which selects the "Gateway Deployment"
      selector:
        istio: my-gateway-deployment
      servers:
        - port:
            number: 80
            name: http
            protocol: HTTP
          hosts:
            - "*"
        - port:
            number: 443
            name: https
            protocol: HTTPS
          hosts:
            - "*"
          tls:
            mode: SIMPLE
            ## the name of the Kubernetes Secret with a TLS certificate
            credentialName: my-gateway-certificate
    ```

    The following `VirtualService` selects the `Gateway` defined above, and routes traffic to an application `Service` named `my-service`:

    ```yaml
    apiVersion: networking.istio.io/v1beta1
    kind: VirtualService
    metadata:
      name: my-virtual-service
      ## virtual services can be in any namespace, not only the same as the gateway
      namespace: my-service-namespace
    spec:
      hosts:
        ## you could replace this with a specific hostname if you want
        ## to do Host-based routing, so multiple services can share the same gateway/port
        - "*"
      gateways:
        ## this selects the gateway defined above
        - some-namespace/my-gateway
      http:
        - route:
            ## this assumes there is a `Service` named `my-service` in `my-service-namespace`
            - destination:
                host: my-service.my-service-namespace.svc.cluster.local
                port:
                  number: 80
    ```

    !!! info "TLS Termination"

        In this example, the backend service listens for HTTP traffic (port 80).
        However, because the gateway is doing TLS termination, end-clients can access the service over HTTPS (port 443).

---

## __How does deployKF use Istio?__

deployKF uses Istio as a service mesh to provide advanced networking features.

Here are some of the ways deployKF itself uses Istio:

Feature | Implementation
--- | ---
External Traffic Routing | Services are exposed to non-mesh traffic via `Gateways` and `VirtualServices`.<br><br>_(Learn More: [Expose Gateway](../platform/deploykf-gateway.md))_
Authentication & Authorization | External traffic is authenticated using `EnvoyFilters`, then authorized with `AuthorizationPolicies`.<br><br>_(Learn More: [User Authentication](../platform/deploykf-authentication.md))_ 
Internal Service Communication | Internal services talk through the mesh, and service-to-service access controls are enforced with `AuthorizationPolicies` to restrict which services can talk to each other.

Additionally, some tools in deployKF make direct use of Istio:

Tool | How it uses Istio
--- | ---
[Kubeflow Notebooks](../../reference/tools.md#kubeflow-notebooks) | Manages `VirtualServices` for each `Notebook` Pod to make it accessible on the main Istio gateway.

---

## __Can I use my existing Istio?__

Yes.

By default, deployKF will _install Istio_ and create an _ingress gateway deployment_.
However, you may use your existing Istio installation and/or gateway deployment instead.

As the gateway deployment is separate from Istio itself, there are 3 common combinations of who manages what:

Configuration | [Istio Installation](#use-an-existing-istio-installation) | [Gateway Deployment](#use-an-existing-gateway-deployment) | [Gateway Resources](#use-custom-gateway-resources)
--- | --- | --- | ---
Default | deployKF | deployKF | Always by deployKF
Custom Istio, Managed Gateway | You | deployKF | Always by deployKF
Fully Custom | You | You  | Always by deployKF

### __Use an existing istio installation__

If you already have an Istio installation, you may use it instead of the deployKF-managed one by following these steps.
See the [version matrix](../../releases/version-matrix.md#istio) for which versions of Istio are supported by deployKF.

??? warning "Gateway Version Alignment"

    If you are NOT also bringing [your own gateway deployment](#use-an-existing-gateway-deployment), you MUST ensure that the deployKF-managed gateway matches your Istio version.
    The [`deploykf_core.deploykf_istio_gateway.charts.istioGateway.version`](https://github.com/deployKF/deployKF/blob/v0.1.4/generator/default_values.yaml#L699) value sets the version of the embedded gateway deployment.

    For example, the following deployKF values will deploy a gateway for Istio `1.19.6`:

    ```yaml
    deploykf_core:
      deploykf_istio_gateway:
        charts:
          istioGateway:
            name: gateway
            version: 1.19.6
            repository: https://istio-release.storage.googleapis.com/charts
    ```

??? step "Step 1 - Disable embedded Istio"

    Disable the embedded Istio installation by setting the [`deploykf_dependencies.istio.enabled`](https://github.com/deployKF/deployKF/blob/v0.1.3/generator/default_values.yaml#L194) value to `false`:
    
    ```yaml
    deploykf_dependencies:
      istio:
        enabled: false
    ```

??? step "Step 2 - Configure your Istio"

    deployKF requires some non-default [mesh configs](https://istio.io/latest/docs/reference/config/istio.mesh.v1alpha1) which you MUST set in your Istio installation:

    Mesh Config | Value | Purpose
    --- | --- | ---
    `defaultConfig.holdApplicationUntilProxyStarts` | `true` | Ensures the Istio sidecar is fully initialized before application containers start. Prevents race-conditions where application containers start before the sidecar is ready.
    `defaultConfig.proxyMetadata` | `{ "ISTIO_META_DNS_AUTO_ALLOCATE": "true", "ISTIO_META_DNS_CAPTURE": "true" }` | Enable [DNS Proxying](https://istio.io/latest/docs/ops/configuration/traffic-management/dns-proxy/), which deployKF requires.

    !!! warning "Default Namespace Injection"
    
        Ensure you do NOT have [`sidecarInjectorWebhook.enableNamespacesByDefault`](https://istio.io/latest/docs/setup/additional-setup/sidecar-injection/#controlling-the-injection-policy) set to `true`.
        <br>
        (In the Istio Helm Chart this [defaults to `false`](https://github.com/istio/istio/blob/1.19.6/manifests/charts/istio-control/istio-discovery/values.yaml#L101-L104), but you should check to be sure).

    For example, if you are using the [Istio Helm Chart](https://github.com/istio/istio/tree/1.19.6/manifests/charts/istio-control/istio-discovery) to install Istio, you may set these Helm values:
    
    ```yaml
    meshConfig:
      defaultConfig:
        holdApplicationUntilProxyStarts: true
        proxyMetadata:
          ISTIO_META_DNS_AUTO_ALLOCATE: "true"
          ISTIO_META_DNS_CAPTURE: "true"

    sidecarInjectorWebhook:
      enableNamespacesByDefault: false
    ```

### __Use an existing gateway deployment__

If you have an existing Istio [gateway deployment](#gateways), you can use it instead of the deployKF-managed one.
You may do this even when using the deployKF-managed Istio installation.

??? step "Step 1 - Disable embedded Gateway Deployment"

    Disable the embedded gateway deployment by setting the [`deploykf_core.deploykf_istio_gateway.charts.istioGateway.enabled`](https://github.com/deployKF/deployKF/blob/v0.1.4/generator/default_values.yaml#L696) value to `false`:
    
    ```yaml
    deploykf_core:
      deploykf_istio_gateway:

        ## disable the embedded gateway deployment
        charts:
          istioGateway:
            enabled: false
    ```

??? step "Step 2 - Configure deployKF"

    You must set the following deployKF values to match your existing gateway deployment:

    - [`deploykf_core.deploykf_istio_gateway.namespace`](https://github.com/deployKF/deployKF/blob/v0.1.4/generator/default_values.yaml#L673)
    - [`deploykf_core.deploykf_istio_gateway.gateway.ports`](https://github.com/deployKF/deployKF/blob/v0.1.4/generator/default_values.yaml#L715-L724)
    - [`deploykf_core.deploykf_istio_gateway.gateway.selectorLabels`](https://github.com/deployKF/deployKF/blob/v0.1.4/generator/default_values.yaml#L760-L764)
    - [`deploykf_core.deploykf_istio_gateway.gatewayDeployment.serviceAccount.name`](https://github.com/deployKF/deployKF/blob/v0.1.4/generator/default_values.yaml#L794)
    - [`deploykf_core.deploykf_istio_gateway.gatewayService.ports`](https://github.com/deployKF/deployKF/blob/v0.1.4/generator/default_values.yaml#L814-L823) (depending on your setup)

    For example, you might set the following values:    

    ```yaml
    deploykf_core:
      deploykf_istio_gateway:

        ## the namespace where your gateway deployment is running
        namespace: my-gateway-namespace
        
        gateway:
          ## the label selector for your gateway deployment pods
          selectorLabels:
            app: my-gateway-deployment
            istio: my-gateway-deployment

          ## the ports on your gateway deployment which deployKF should use
          ##  - the "internal" ports which deployKF will use on your gateway deployment
          ##  - they must be different from any existing services on this gateway deployment
          ##  - they may be different to the user-facing ports, as users might connect
          ##    to the gateway through a Service or Ingress (see `gatewayService.ports`)
          ports:
            http: 80
            https: 443

        gatewayDeployment:
          serviceAccount:
            ## the name of the SERVICE ACCOUNT used by the gateway deployment pods
            ##  - deployKF needs to know this so it can trust traffic from the gateway
            ##    check the `serviceAccountName` field in your gateway Pods
            name: my-gateway-service-account

        #gatewayService:
        #
        #  ## the ports which clients are actually using to connect to the gateway
        #  ##  - the "public" ports which clients are expected to connect to
        #  ##  - they can be different to the "internal" ports defined in `gateway.ports`
        #  ##  - these values affect the ports presented in user-facing HTTP links
        #  ##  - if unset, they default to the corresponding value of `gateway.ports`
        #  ports:
        #    http: 80
        #    https: 443
    ```

??? step "Step 3 - Expose your Gateway Deployment"
    
    If you havent already, you will need to create a `Service` (and possibly `Ingress`) that selects your gateway deployment to expose it to external traffic.

    !!! config "Service Health Checks"
    
        Many LoadBalancer Service implementations require a "health check" to pass before allowing traffic to flow (e.g. AWS NLB/ALB), and will send health-check requests to one or more ports on the Service.
    
        Istio gateway Pods will always return a [`200 OK` response on port `15021`, under the `/healthz/ready` HTTP path](https://istio.io/v1.22/docs/ops/deployment/application-requirements/#ports-used-by-istio) for this purpose.
        Therefore, you can expose the `15021` port on the Service, and configure the health-check path to `/healthz/ready`.
    
    !!! config "TLS Termination and SNI"
    
        If you put the Gateway behind a proxy which terminates TLS (like AWS ALB), you will probably need to disable _SNI Matching_.
        This is because most proxies don't forward the original request's [Server Name Indication (SNI)](https://en.wikipedia.org/wiki/Server_Name_Indication) to the backend service after TLS termination.

        To disable _SNI Matching_, set [`deploykf_core.deploykf_istio_gateway.gateway.tls.matchSNI`](https://github.com/deployKF/deployKF/blob/v0.1.4/generator/default_values.yaml#L741-L746) to `false`:

        ```yaml
        deploykf_core:
          deploykf_istio_gateway:

            gateway:
              tls:
                matchSNI: false
        ```

        Read more about this in the [Expose Gateway and configure HTTPS](../platform/deploykf-gateway.md#use-a-kubernetes-ingress) guide.

??? question_secondary "Can I have other services on the deployKF Gateway?"

    Yes. You may expose your non-deployKF `Gateway` and `VirtualService` resources on the same Gateway Deployment as deployKF, as long as the ports/hostnames are not incompatible with deployKF's configuration.
    
    ??? warning "Limitations in deployKF `0.1.3` and earlier"
    
        In deployKF `0.1.3` and earlier, you MUST use a DEDICATED gateway deployment for deployKF.
        That is, you can't expose non-deployKF services on the same gateway deployment as deployKF.

        This limitation was [removed in deployKF `0.1.4`](https://github.com/deployKF/deployKF/pull/66).

    ??? config "Using non-standard ports"
    
        If you already have Istio `VirtualServices` on your gateway deployment using ports `80` and `443`, you will need to use non-standard ports (like `18080` and `18443`) for deployKF.
    
        For example, you might set the following values to use non-standard ports:
    
        ```yaml
        deploykf_core:
          deploykf_istio_gateway:

            ## the ports on your gateway deployment which deployKF should use
            gateway:
              ports:
                http: 18080
                https: 18443
    
            ## the ports which clients are actually using to connect to the gateway
            gatewayService:
              ports:
                http: 80
                https: 443
        ```

        You will probably also want to [use an Ingress](../platform/deploykf-gateway.md#use-a-kubernetes-ingress) which listens on standard ports, and routes traffic to the correct gateway port based on the hostname.
        This will prevent users from seeing the non-standard ports in their URLs like `https://deploykf.example.com:18443`.

        For example, your Ingress could route traffic like this:
    
        - `other-service.example.com` → gateway port `443`
        - `deploykf.example.com` → gateway port `18443`
        - `*.deploykf.example.com` → gateway port `18443`



### __Use custom gateway resources__

You are NOT able to use your own `Gateway` and `VirtualService` resources for deployKF.

While you may [attach deployKF to an existing Gateway Deployment](#use-an-existing-gateway-deployment) (Pods + Service), ALL virtual `Gateway` and `VirtualService` resources are managed by deployKF, this is a result of how deployKF implements features like authentication.

For reference, here are some gateway resources that deployKF creates:

Resources | Purpose
--- | ---
[`Gateway/deploykf-istio-gateway`](https://github.com/deployKF/deployKF/blob/v0.1.4/generator/templates/manifests/deploykf-core/deploykf-istio-gateway/templates/gateway/Gateway.yaml) | The main gateway that [exposes the platform](../platform/deploykf-gateway.md) to external traffic.
[`Gateway/deploykf-istio-gateway-https-redirect`](https://github.com/deployKF/deployKF/blob/v0.1.4/generator/templates/manifests/deploykf-core/deploykf-istio-gateway/templates/gateway/Gateway-https-redirect.yaml) | A special gateway for HTTP to HTTPS redirects.
[`VirtualService/https-redirect`](https://github.com/deployKF/deployKF/blob/v0.1.4/generator/templates/manifests/deploykf-core/deploykf-istio-gateway/templates/gateway/VirtualService-https-redirect.yaml) | Redirects HTTP traffic to HTTPS, connected to `Gateway/deploykf-istio-gateway-https-redirect`.
[`VirtualService/deploykf-istio-gateway`](https://github.com/deployKF/deployKF/blob/v0.1.4/generator/templates/manifests/deploykf-core/deploykf-dashboard/templates/central-dashboard/VirtualService.yaml) | Routes for the [central dashboard](../platform/deploykf-dashboard.md).
