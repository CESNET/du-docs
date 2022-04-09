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

**Question:** Every Pod, Job, Deployment, and any other kind that runs a container needs *resources* attribute to be set otherwise deploy is rejected with similar error:
```
Pods "master-685f855ff-gg9sr" is forbidden: failed quota: default-w2qv7: must specify limits.cpu,limits.memory,requests.cpu,requests.memory:Deployment does not have minimum availability.
```

**Answer:** Pod, Job, Deployement is missing the following resource section with appropriate values:
```yaml
resources:
  requests:
    cpu: 1
    memory: 512Mi
  limits:
    cpu: 1
    memory: 512Mi

```

**Question:** Deployment returns message simmilar to:
```
pods cz-iocb-nextprot-loader-loaderspark-1649322652207-driver" is forbidden: 
exceeded quota: default-sq5kt, requested: limits.cpu=1,limits.memory=2432Mi,requests.cpu=1,requests.memory=2432Mi, 
used: limits.cpu=0,limits.memory=0,requests.cpu=0,requests.memory=0,
limited:limits.cpu=0,limits.memory=0,requests.cpu=0,requests.memory=0.
```

**Answer:** Deployment is done to a *Namespace* that is running out of quotas or even has quota set to zero. You need to increase *Namespace* quota which may need to decrease your other *Namespaces* quotas or request explicit *Project*. See [Projects, Namespaces, and Quotas](/docs/quotas.html).

**Question:** No GPU found, `nvidia-smi` returns `command not found`.

**Answer:** Deployment is missing request for GPU like:
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
