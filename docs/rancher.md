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

## Rancher

_Rancher_ instance is available on [rancher.cloud.e-infra.cz](https://rancher.cloud.e-infra.cz). Please login via CESNET or ELIXIR (EGI is not approved yet).
After logging in, you shall see default dashboard. You should see default cluster as shown below. If none cluster is shown, please, realod the page after few seconds.

World of Rancher and Kuberntes is organized into *clusters*, *projects*, and *namespaces*.

You can find assigned clusters which you are allowed to access either in upper left corner:

![clusters](cluster1.jpg)

or just in the list on home page:

![home page](cluster2.jpg)

When you select a cluster, you can display your *projects and namespaces*

![projects and namespaces](projects.jpg)

It is possible to work to certain extent only with Rancher. However, command line tool `kubectl` allows more actions. You can utilize both ways but we do not recommend `kubectl` for users inexperienced with working in terminal.
