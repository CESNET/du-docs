---
layout: article
title: Kubectl
permalink: /docs/kubectl-expose.html
key: kubectl-expose
aside:
  toc: true
sidebar:
  nav: docs
---
## Exposing Applications

Basically, there are two types of exposable applications: *web-based* applications, *other* applications. The difference between these types is the required IP address. The web-based application shares IP address with other web-based applications, while the other applications need new IP address for each service. The number of IP addresses is limited, so use the web-based approach if possible.

In the following documentation there are YAML fragments, they are meant to be deployed using the `kubectl` like this: `kubectl create -f file.yaml -n namespace` where `file.yaml` contains the YAMLs below and `namespace` is the namespace containing the application. Also, this part of the documentation assumes that the application (deployment) already exists. If you are not sure, read [hello example](kubectl-helloworld.html) again.

### Web-based Applications

Web-based applications are those that communicate using the `HTTP' protocol. These applications are exposed using `Ingress` rules.

This type of application requires a service that binds a port to an application and ingress rules that expose the service to the Internet.

Suppose we have an application that is ready to run on port 8080. We create a service:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: application-svc
spec:
  type: ClusterIP
  ports:
  - name: application-port
    port: 80
    targetPort: 8080
  selector:
    app: application
```

Where `selector:` `app: application` must match the application name in the deployment and `application-svc` and `application-port` are arbitrary names.

Once we have a service, we create an ingress:

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: application-ingress
  annotations:
    kubernetes.io/ingress.class: "nginx"
    kubernetes.io/tls-acme: "true"
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
spec:
  tls:
    - hosts:
        - "application.dyn.cloud.e-infra.cz"
      secretName: application-dyn-clout-e-infra-cz-tls
  rules:
  - host: "application.dyn.cloud.e-infra.cz"
    http:
      paths:
      - backend:
          service:
            name: application-svc
            port:
              number: 80
        pathType: ImplementationSpecific
```

Where `service` `name: application-svc` must match the metadata name of the *Service*. This *Ingress* exposes the application to the web URL `application.dyn.cloud.e-infra.cz`. Note: the domain name will be registered automatically if it is in the `dyn.cloud.e-infra.cz` domain. The `tls` section creates Lets Encrypt certificate, no need to maintain it.

If `tls` section is used, TLS will be terminated at NGINX Ingress. The application must be set to communicate over `HTTP`. Communication between Kubernetes and a user is over `HTTPS`.

*IMPORTANT
TLS is terminated at the cluster boundary in NGINX Ingress. Communication within the cluster is not encrypted, especially within a single cluster node. If this is a problem, the user must omit the `tls` and `anotations` sections and provide a certificate and key to the Pod itself.

*IMPORTANT
Some applications are confused by being configured as `HTTP` but exposed as `HTTPS`. If an application generates absolute URLs, it must generate `HTTPS` URLs, not `HTTP`. Kubernetes Ingress sets the `HTTP_X_SCHEME` header to `HTTPS` if it is TLS terminated. For example, for *django*, the user must set SECURE_PROXY_SSL_HEADER = ("HTTP_X_SCHEME", "https")`. A common header used for this situation is `X_FORWARDED_PROTO`, but this is not set by Kubernetes NGINX. It is also possible to expose `HTTPS' configured applications. See *HTTPS target* below.

#### Custom Domain Name (FQDN)

It is also possible to use custom domain name (basically any name).

1. DNS record `CNAME` is required. For `kuba-cluster`, `CNAME` target is `kuba-pub.cerit-sc.cz`.
2. Ingress object is in the form:
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: application-ingress
  annotations:
    kubernetes.io/ingress.class: "nginx"
    kubernetes.io/tls-acme: "true"
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
spec:
  tls:
    - hosts:
        - "my-name"
      secretName: my-name-tls
  rules:
  - host: "my-name"
    http:
      paths:
      - backend:
          service:
            name: application-svc
            port:
              number: 80
        pathType: ImplementationSpecific
```

##### Note

`CNAME` must be pre-set and propagated so that the Let's Encrypt service can verify the domain when TLS is requested. This means that seamless migration from any system to our infrastructure is not easily possible.

#### Authentication

`Ingress` can require user authentication to provide restricted access to the `Service`. Authentication can be set using a `Secret` and annotations.

First setup a secret:
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: secretref
type: Opaque
data:
   auth: password
```
Where `secretref` is an arbitrary name and password is a `base64` encoded `htpasswd`. The password can be generated with this command: `htpasswd -n username | base64 -w0` where `username` is the desired login username. It will return text like `Zm9vOiRhcHIxJGhOZVRzdngvJEkyVk9NbEhHZDE1N1gvYTN2aktYSDEKCg==`, which will be used instead of the `password` in the secret above.

The following two annotations are required in the `Ingress`.

```yaml
    nginx.ingress.kubernetes.io/auth-type: basic
    nginx.ingress.kubernetes.io/auth-secret: secretref
```

The `secretref' must match the metadata name of the `Secret'.

*IMPORTANT
The password protection is only applied to external traffic, i.e. the user will be prompted for a password. However, traffic from other pods will bypass authentication if it communicates directly with the `Service` IP. This can be mitigated by using `Network Policy'. See [Security](/docs/security.html).

#### Large Data Upload

If a large data upload is expected, the following two `Ingress` annotations may be required to deal with the upload size limit.
```yaml
nginx.ingress.kubernetes.io/proxy-body-size: "600m"
nginx.org/client-max-body-size: "600m"
```

Replace the `600m` value with the desired maximum upload size.

#### HTTPS Target

The Ingress object can expose applications that use HTTPS protocol instead of HTTP, i.e. the communication between the ingress and the application is also encrypted. In this case, you need to add `nginx.ingress.kubernetes.io/backend-protocol: "HTTPS"` annotation to the ingress object.

#### Limiting Access

It is possible to restrict access to a web application at the ingress level by limiting access from a specific IP range. This is done using the `Ingress` annotation `nginx.ingress.kubernetes.io/whitelist-source-range`, the following example restricts access only from the MUNI network.

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: application-ingress
  annotations:
    kubernetes.io/ingress.class: "nginx"
    kubernetes.io/tls-acme: "true"
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
    nginx.ingress.kubernetes.io/whitelist-source-range: 147.251.0.0/16
spec:
  tls:
    - hosts:
        - "my-name"
      secretName: my-name-tls
  rules:
  - host: "my-name"
    http:
      paths
      - backend:
          service:
            name: application-svc
            port:
              number: 80
        pathType: ImplementationSpecific

```

### Other Applications

Applications that to not use the `HTTP` protocol are exposed directly via `Service`.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: application-svc
  annotations:
    external-dns.alpha.kubernetes.io/hostname: application.dyn.cloud.e-infra.cz
spec:
  type: LoadBalancer
  ports:
  - port: 22
    targetPort: 2222
  selector:
    app: application
```

Where `selector:` `app: application` must match the application name in the deployment and `application-svc` is any name. If annotation `external-dns.alpha.kubernetes.io/hostname` is provided and value i in domain `dyn.cloud.e-infra.cz`, the name will be registered in DNS.

Deploying this *Service* exposes the application on a public IP. You can check the IP with `kubectl get svc -n namespace`, where `namespace` is the namespace of the Service and the application.

It is also possible to expose the application on a private MUNI IP. In this case the application will be reachable from MUNI network or using MUNI VPN. This type of exposing is selected using the annotation `metallb.universe.tf/address-pool: privmuni`. This case is preferred because it does not use public IP. Full example is below.
```yaml
apiVersion: v1
kind: Service
metadata:
  name: application-svc
  annotations:
    metallb.universe.tf/address-pool: privmuni
    external-dns.alpha.kubernetes.io/hostname: application.dyn.cloud.e-infra.cz
spec:
  type: LoadBalancer
  ports:
  - port: 22
    targetPort: 2222
  selector:
    app: application
```

