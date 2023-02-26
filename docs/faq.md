---
layout: article
title: FAQ
permalink: /docs/faq.html
key: FAQ
aside:
  toc: true
sidebar:
  nav: docs
---

**Question:** Every Pod, Job, Deployment, and any other type that runs a container must have the *resources* attribute set, otherwise the deploy will fail with a similar error:
```
Pods "master-685f855ff-gg9sr" is forbidden: failed quota: default-w2qv7: must specify limits.cpu,limits.memory,requests.cpu,requests.memory:Deployment does not have minimum availability.
```

**Answer:** Pod, Job, Deployment is missing the following resource section with appropriate values:
```yaml
resources:
  requests:
    cpu: 1
    memory: 512Mi
  limits:
    cpu: 1
    memory: 512Mi

```

---

**Question:** Deployment returns message simmilar to:
```
pods cz-iocb-nextprot-loader-loaderspark-1649322652207-driver" is forbidden: 
exceeded quota: default-sq5kt, requested: limits.cpu=1,limits.memory=2432Mi,requests.cpu=1,requests.memory=2432Mi, 
used: limits.cpu=0,limits.memory=0,requests.cpu=0,requests.memory=0,
limited:limits.cpu=0,limits.memory=0,requests.cpu=0,requests.memory=0.
```

**Answer:** The deployment is being made to a *Namespace* that is running out of quota or even has quota set to zero. You need to increase the *Namespace* quota, which may require decreasing the quotas of your other *Namespaces* or requesting an explicit *Project*. See [Projects, Namespaces, and Quotas](/docs/quotas.html).
---

**Question:** No GPU found, `nvidia-smi` returns `command not found`.

**Answer:** The deployment is missing request for GPU like:
```yaml
resources:
  limits:
    nvidia.com/gpu: 1
```
or
```yaml
resources:   
  limits:
    cerit.io/gpu-mem: 1
```

---

**Question:** Deployment returns message similar to:
```
CreateContainerConfigError (container has runAsNonRoot and image will run as root (pod: "mongo-db-846b7bfc7-qrlqt_namespace-ns(5d3538ab-7493-41ab-bd94-a4256c236f6f)", container: mongo-db-test))
```

**Answer:** The deployment is missing the `securityContext` section and the container image (in this case `mongo`) does not contain **numeric** `USER`. To fix this, just extend the deployment definition like this:
```yaml
image: cerit.io/nextflowproxy:v1.2
imagePullPolicy: Always
securityContext:
  runAsUser: 1000
  runAsGroup: 1000
resources:
  limits:
    cpu: 4
    memory: 8192Mi
```

The `runAsUser` and `runAsGroup` lines are important.
