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

Basically, there are two kinds of exposable applications: *web-based* applications, *other* applications. The difference between these types is in required IP address. The Web-based application shares IP address with other Web-based applications while the other applications require new IP address for each service. Number of IP addresses is limited so if possible, use the Web-based approach.

In the following documentation, there are YAML fragments, they are meant to be deployed using the `kubectl` like this: `kubectl create -f file.yaml -n namespace` where `file.yaml` contains those YAMLs below and `namespace` is the namespace with the application. Furthermore, this part of documentation suppose, that the application (deployment) already exists. If not sure, read again [hello example](kubectl-helloworld.html).

### Web-based Applications

Web-based applications are those that communicate via `HTTP` protocol. These applications are exposed using `Ingress` rules. 

This kind of applications require a service that binds a port with application and ingress rules that expose the service to the Internet.

Suppose, we have an application that is ready to serve on port 8080. We create a service:

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

Where `selector:` `app: application` must match application name in deployment and `application-svc` and `application-port` are arbitrary names.

Once we have a service, we create ingress:

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
      secretName: applicatoin-dyn-clout-e-infra-cz-tls
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

Where `service` `name: application-svc` must match metadata name from the *Service*. This *Ingress* exposes the application on web URL `application.dyn.cloud.e-infra.cz`. Note: domain name is automatically registered if it is in `dyn.cloud.e-infra.cz` domain. The `tls` section creates Lets Encrypt certificate, no need to maintain it. 

If `tls` section is used, TLS is terminated at system NGINX Ingress. Application must be set to communicate via `HTTP`. Communication between Kubernetes and a user is via `HTTPS`.

*IMPORTANT* 
TLS is terminated in NGINX Ingress at cluster boundary. Communication inside cluster is not encrypted, mainly not inside a single cluster node. If this is a problem, user needs to omit `tls` section and `anotations` section and provide a certificate and key on his/her own to the Pod. 

*IMPORTANT*
Some applications are confused that they are configured as `HTTP` but exposed as `HTTPS`. If an application generates absolute URLs, it must generate `HTTPS` URLs and not `HTTP`. Kubernetes Ingress sets `HTTP_X_SCHEME` header to `HTTPS` if it is TLS terminated. E.g., for *diango*, user must set: `SECURE_PROXY_SSL_HEADER = ("HTTP_X_SCHEME", "https")`. Common header used for this situation is `X_FORWARDED_PROTO` but this is not set by Kubernetes NGINX.

### Other Applications

Applications that to not use `HTTP` protocol are exposed directly via `Service`.

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

Where `selector:` `app: application` must match application name in deployment and `application-svc` is arbitrary name. If annotation `external-dns.alpha.kubernetes.io/hostname` is provided and value i in domain `dyn.cloud.e-infra.cz`, the name is registered in DNS. 

Deploying this *Service* exposes the application on a public IP. One can check the IP with `kubectl get svc -n namespace` where `namespace` is namespace of the Service and application.
