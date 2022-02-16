---
layout: article
title: Rancher
permalink: /docs/rancher.html
key: rancher
aside:
  toc: true
sidebar:
  nav: docs
---

_Rancher_ instance is available on [rancher.cloud.e-infra.cz](https://rancher.cloud.e-infra.cz). Please login via CESNET, ELIXIR or EGI.
After logging in, you shall see default dashboard. You should see default cluster as shown below. If none cluster is shown, please, realod the page after few seconds.

World of Rancher and Kuberntes is organized into *clusters*, *projects*, and *namespaces*. *Clusters* correspond to sets of physical nodes. *Projects* are created within the *cluster* and *namespaces* are created within the *Projects*. Each user is given a *Default Project* with name and surname and default *namespace* called `surname-ns`. The *Default Project* and default *namespace* is created automatically on the first login to Rancher dashboard.

You can find assigned clusters which you are allowed to access either in upper left corner:

![clusters](cluster1.jpg)

or just in the list on home page:

![home page](cluster2.jpg)

When you select a cluster, you can display your *projects and namespaces*

![projects and namespaces](projects.jpg)

It is possible to work to certain extent only with Rancher. However, command line tool `kubectl` allows more actions. You can utilize both ways but we do not recommend `kubectl` for users inexperienced with working in terminal.
