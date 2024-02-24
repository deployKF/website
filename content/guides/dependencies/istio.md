---
icon: custom/istio
description: >-
  Learn how deployKF uses Istio and how to integrate your existing Istio with deployKF.
---

# Istio

Learn how deployKF uses Istio and how to integrate your existing Istio with deployKF.

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
However, you may also configure deployKF to use your existing Istio installation and/or gateway deployment.

As the gateway deployment is separate from Istio itself, there are 4 possible combinations of who manages what:

Configuration | [Istio Installation](#use-an-existing-istio-installation) | [Gateway Deployment](#use-an-existing-gateway-deployment) | [Gateway Resources](#use-custom-gateway-resources)
--- | --- | --- | ---
Default | deployKF | deployKF | Always by deployKF
Custom Istio Installation | You | deployKF | Always by deployKF
Custom Gateway Deployment | deployKF | You  | Always by deployKF
Fully Custom | You | You  | Always by deployKF

### __Use an existing istio installation__

If you already have an Istio installation, you may use it instead of the deployKF-managed one.

deployKF uses an unmodified version of Istio with a few non-default mesh configs.
See the [version matrix](../../releases/version-matrix.md#deploykf-dependencies) for information about which versions of Istio are supported by deployKF.

!!! danger "Namespace Injection"

    Ensure that your Istio installation does NOT have [`sidecarInjectorWebhook.enableNamespacesByDefault`](https://istio.io/latest/docs/setup/additional-setup/sidecar-injection/#controlling-the-injection-policy) set to `true` (note, [the Istio Helm Chart defaults to `false`](https://github.com/istio/istio/blob/1.19.6/manifests/charts/istio-control/istio-discovery/values.yaml#L101-L104)).

First, disable the embedded Istio installation by setting the [`deploykf_dependencies.istio.enabled`](https://github.com/deployKF/deployKF/blob/v0.1.3/generator/default_values.yaml#L194) value to `false`:

```yaml
deploykf_dependencies:
  istio:
    enabled: false
```

Second, there are a number of [mesh configs](https://istio.io/latest/docs/reference/config/istio.mesh.v1alpha1/) which you MUST set in your Istio installation to ensure compatibility with deployKF:

Mesh Config | Value | Purpose
--- | --- | ---
`defaultConfig.holdApplicationUntilProxyStarts` | `true` | Ensures the Istio sidecar is fully initialized before application containers start. Prevents race-conditions where application containers start before the sidecar is ready.
`defaultConfig.proxyMetadata` | `{"ISTIO_META_DNS_AUTO_ALLOCATE": "true", "ISTIO_META_DNS_CAPTURE": "true"}` | Enable [DNS Proxying](https://istio.io/latest/docs/ops/configuration/traffic-management/dns-proxy/), which deployKF requires.

For example, if you are using the [Istio Helm Chart](https://github.com/istio/istio/tree/1.19.6/manifests/charts/istio-control/istio-discovery) to install Istio, you may set these Helm values:

```yaml
meshConfig:
  defaultConfig:
    holdApplicationUntilProxyStarts: true
    proxyMetadata:
      ISTIO_META_DNS_AUTO_ALLOCATE: "true"
      ISTIO_META_DNS_CAPTURE: "true"
```

!!! warning "Gateway Version Alignment"

    If you are not also bringing [your own gateway deployment](#use-an-existing-gateway-deployment), you MUST ensure that the deployKF-managed gateway matches your Istio version.
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

### __Use an existing gateway deployment__

If you already have an Istio [gateway deployment](#gateways), you can use it instead of the deployKF-managed one.
The minimum configuration is to create a gateway `Deployment` and an associated `Service` pointing to those Pods.

!!! danger "Dedicated Gateway Deployment"

    In deployKF `0.1.3` and earlier, you MUST use a dedicated gateway deployment for deployKF.
    This is because these versions apply [deployKF Authentication](../platform/deploykf-authentication.md) to all paths by default, so would block access to other services exposed on the gateway.
    This limitation was removed in deployKF `0.1.4` (see: [`PR #66`](https://github.com/deployKF/deployKF/pull/66)).

First, disable the embedded gateway deployment by setting the [`deploykf_core.deploykf_istio_gateway.charts.istioGateway.enabled`](https://github.com/deployKF/deployKF/blob/v0.1.4/generator/default_values.yaml#L696) value to `false`:

```yaml
deploykf_core:
  deploykf_istio_gateway:
    charts:
      istioGateway:
        enabled: false
```

Ensure your gateway deployment pods have unique labels which can be used to select them, then update [`deploykf_core.deploykf_istio_gateway.gateway.selectorLabels`](https://github.com/deployKF/deployKF/blob/v0.1.4/generator/default_values.yaml#L760-L764) to match those labels:

```yaml
deploykf_core:
  deploykf_istio_gateway:
    gateway:
      selectorLabels:
        app: my-gateway-deployment
        istio: my-gateway-deployment
```

The ports which the gateway will listen on for each protocol are defined by the [`deploykf_core.deploykf_istio_gateway.gateway.ports`](https://github.com/deployKF/deployKF/blob/v0.1.4/generator/default_values.yaml#L715-L724) values:

```yaml
deploykf_core:
  deploykf_istio_gateway:
    gateway:
      ## TIPS:
      ##  - these are the "internal" ports which the gateway use, and can be different
      ##    to the user-facing ports which the service listens on, see `gatewayService.ports`
      ##  - if you have other Gateway resources which select this gateway deployment,
      ##    they must use different server ports to avoid conflicts
      ##  - when exposing a shared gateway deployment behind a single Ingress, you may need to
      ##    use host-based routing to ensure that traffic is routed to the correct gateway port
      ports:
        http: 80
        https: 443
```

If clients will connect over different ports, you can set the [`deploykf_core.deploykf_istio_gateway.gatewayService.ports`](https://github.com/deployKF/deployKF/blob/v0.1.4/generator/default_values.yaml#L814-L823) value to match your `Service` ports:

```yaml
deploykf_core:
  deploykf_istio_gateway:
    gatewayService:
      ## TIPS:
      ##  - if unset, they default to their corresponding port under `gateway.ports`
      ##  - these are the "public" ports which clients are expected to connect to,
      ##    and can be different to the "internal" ports defined in `gateway.ports`
      ##  - when using your own gateway service, these values still affect the ports 
      ##    presented in user-facing HTTP links
      ports:
        http: ~
        https: ~
```

!!! info "Service Health Checks"

    Many LoadBalancer Service implementations check the health of the service before allowing traffic to flow (e.g. AWS NLB/ALB), and will send health-check requests to one or more ports on the Service.

    Istio gateway Pods will always return a [`200 OK` response on port `15021`, under the `/healthz/ready` HTTP path](https://istio.io/latest/docs/ops/deployment/requirements/#ports-used-by-istio) for this purpose.
    So if you are using a custom LoadBalancer Service, you may need to expose the `15021` port on the Service, and configure the health-check path to `/healthz/ready`.

!!! info "TLS Termination and SNI"

    If you have an outer proxy which terminates TLS for users (e.g. an AWS ALB), you will likely need to disable `deploykf_core.deploykf_istio_gateway.gateway.tls.matchSNI`, as most proxies will not send the correct SNI header.
    Read more about this in the [Expose Gateway and configure HTTPS](../platform/deploykf-gateway.md#2-expose-the-gateway-service) guide.

    ```yaml
    deploykf_core:
      deploykf_istio_gateway:
        gateway:
          tls:
            matchSNI: false
    ```

### __Use custom gateway resources__

You are NOT able to use your own `Gateway` and `VirtualService` resources for deployKF.

While you may [attach deployKF to an existing Gateway Deployment](#use-an-existing-gateway-deployment) (Pods + Service), ALL virtual `Gateway` and `VirtualService` resources are managed by deployKF, this is a result of how deployKF implements features like authentication.

However, you may expose your non-deployKF `Gateway` and `VirtualService` resources on the same Gateway Deployment as deployKF, as long as the ports/hostnames are not incompatible with deployKF's configuration.

For reference, here are some gateway resources that deployKF creates:

Resources | Purpose
--- | ---
[`Gateway/deploykf-istio-gateway`](https://github.com/deployKF/deployKF/blob/v0.1.4/generator/templates/manifests/deploykf-core/deploykf-istio-gateway/templates/gateway/Gateway.yaml) | The main gateway that [exposes the platform](../platform/deploykf-gateway.md) to external traffic.
[`Gateway/deploykf-istio-gateway-https-redirect`](https://github.com/deployKF/deployKF/blob/v0.1.4/generator/templates/manifests/deploykf-core/deploykf-istio-gateway/templates/gateway/Gateway-https-redirect.yaml) | A special gateway for HTTP to HTTPS redirects.
[`VirtualService/https-redirect`](https://github.com/deployKF/deployKF/blob/v0.1.4/generator/templates/manifests/deploykf-core/deploykf-istio-gateway/templates/gateway/VirtualService-https-redirect.yaml) | Redirects HTTP traffic to HTTPS, connected to `Gateway/deploykf-istio-gateway-https-redirect`.
[`VirtualService/deploykf-istio-gateway`](https://github.com/deployKF/deployKF/blob/v0.1.4/generator/templates/manifests/deploykf-core/deploykf-dashboard/templates/central-dashboard/VirtualService.yaml) | Routes for the [central dashboard](../platform/deploykf-dashboard.md).
