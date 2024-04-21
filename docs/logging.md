---
layout: article
title: Logging
permalink: /docs/logging.html
key: logging
aside:
  toc: true
sidebar:
  nav: docs
---
## Logging

Logging in the Kubernetes cluster is handled by a [Logging operator](https://kube-logging.dev/). This tool allows the creation of customised logging pipelines that meet user requirements.

The logging pipeline consists of two components, `SyslogNGFlow` and `SyslogNGOutput`. `SyslogNGFlow` specifies the log selection and log filters. `SyslogNGOutput` specifies the output destination of the logs.

### SyslogNGFlow

The `SyslogNGFlow` specifies what logs should be sent to the final output destination. For that, it uses `match` statements that support logical operator `and`, `or` and `not`. `SyslogNGFlow` must have at least one `match` statement to transfer any logs.

#### Example
You might use the example configuration below to collect all pod logs from a namespace. Specify the namespace and the name of the related `SyslogNGOutput` resource.

```yaml
apiVersion: logging.banzaicloud.io/v1beta1
kind: SyslogNGFlow
metadata:
  name: syslog-flow
  namespace: [your_namespace]
spec:
  match:
    regexp:
      value: json.kubernetes.labels.app.kubernetes.io/instance
      pattern: "*"
      type: glob
  localOutputRefs:
    - [output_resource_name]
```

If a related Logging resource specifies the `loggingRef` value, add this to the `SyslogNGFlow` specification.
```yaml
spec:
  loggingRef: [value]
```

To see all routing options, see [official documentation](https://kube-logging.dev/docs/configuration/log-routing-syslog-ng/).

### SyslogNGOutput

`SyslogNGOutput` configures the output destination of the logs. `SyslogNGOutput` can configure only one output plugin within the specification.

#### Example
You might use the example configuration below to transfer logs using the Syslog protocol. Specify the resource name, namespace, IP address and port. Make sure you use the same name as in `localOutputRefs`.

```yaml
apiVersion: logging.banzaicloud.io/v1beta1
kind: SyslogNGOutput
metadata:
  name: [output_resource_name]
  namespace: [your_namespace]
spec:
  syslog:
      host: [ip_address]
      port: [port]
```

If a related Logging resource specifies the `loggingRef` value, add this to the `SyslogNGFlow` specification.
```yaml
spec:
  loggingRef: [value]
```

To see full list of available output plugins, see [official documentation](https://kube-logging.dev/docs/configuration/plugins/syslog-ng-outputs/).

### Logging pipeline deployment
To create a new logging pipeline, apply the resource configurations from a YAML file.

    kubectl apply -f [path_to_yaml_file]
