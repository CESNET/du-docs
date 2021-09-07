---
layout: article
title: BinderHub
permalink: /docs/binderhub.html
key: binderhub
aside:
  toc: true
sidebar:
  nav: docs
---
# BinderHub

BinderHub is a Binder instance working on Kubernetes located on [binderhub.cerit-sc.cz](https://binderhub.cerit-sc.cz). Binder turns a Git repo into collection of interactive notebooks. It is enough to fill the git repository name (optionally specific notebook or branch) and binderhub will turn it into a web notebook. 

The notebook runs under anonymous user and if you close browser tab, you won't be able to run the same notebook (if you don't save the url). Furthermore, inactive (closed tab) notebooks are removed after 10 minutes of inactivity which is checked every 10 minutes. Currently, every notebook is assigned `0.2 CPU` and `512 MiB` of memory. 

## Custom Dockerfile

The hub spawns notebook instances with default image not conatining any special libraries. However, you can create custom `Dockerfile` with all dependencies and it will be used as base image. The `Dockerfile` must be located in the repository you are going to launch in Binder. 

When creating the `Dockerfile` bear in mind it has to be runnable under *user*. Furthermore, it is important to `chown` all used directories to user, e.g. :
```
RUN chown -R 1000:1000 /work /home/jovyan
```

