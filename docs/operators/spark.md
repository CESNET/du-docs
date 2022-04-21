---
layout: article
title: Spark Operator
permalink: /docs/operators/spark.html
key: spark
aside:
  toc: true
sidebar:
  nav: docs
---

The [Spark Operator](https://github.com/GoogleCloudPlatform/spark-on-k8s-operator) aims to make specifying and running Spark applications as easy and idiomatic as running other workloads on Kubernetes. We have deployed cluster-wide Spark Operator that defines kinds `ScheduledSparkApplication` and `SparkApplication`, full documentation on kinds' structure is available [here](https://github.com/GoogleCloudPlatform/spark-on-k8s-operator/blob/master/docs/api-docs.md). The official and detailed user guide is available [here](https://github.com/GoogleCloudPlatform/spark-on-k8s-operator/blob/master/docs/user-guide.md).

## Important Configuration
You have to set `spec.driver.serviceAccount` to  `default`, otherwise your spark application will fail on permission issues. The Spark example feature `hostPath` as volume source but this won't work in the cluster since host mounts are forbidden. Please use `persistentVolumeClaim` instead ([examples](https://github.com/GoogleCloudPlatform/spark-on-k8s-operator/blob/master/docs/user-guide.md#mounting-volumes)) and don't forget to create [PVC](https://docs.cerit.io/docs/pvc.html#pvc).

## Other Configuration

### Spark UI

If you want to use Spark UI, you have to include following code snippet in spark application YAML. 

```
  sparkUIOptions:
    ingressAnnotations:
      cert-manager.io/cluster-issuer: letsencrypt-prod
      kubernetes.io/ingress.class: nginx
      kubernetes.io/tls-acme: 'true'
    ingressTLS:
      - hosts:
          - spark.cloud.e-infra.cz
        secretName: spark-cloud-e-infra-cz-tls
```

The snippet ensures application will be reachable (while running) on `spark.cloud.e-infra.cz/<namespace-of-spark-application>/<spark-application-name>`. The address is also visible in Rancher UI, follow the steps to see its final form. When you copy the address into the browser, omit the last character group `(/|$)(.*)` (a Rancher related issue). 

![sparkaddress](sparkaddress.png)  

When you access the path, you should be presented with dashboard similar to

![sparkdashboard](sparkdashboard.png)  


