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

_Rancher_ instance is available on [rancher.cerit-sc.cz](https://rancher.cerit-sc.cz). Please login via CESNET or ELIXIR (EGI is not approved yet).
After logging in, you shall see default dashboard. Right now, you do not have any default project but after 5 minutes, one will be assigned to you. Please refresh the page after such time. 

You can find assigned project in the upper left corner of the page under tab `Global` &rarr; `hdhu-cluster` &rarr; `Default project (your name)`

![default project](https://github.com/CERIT-SC/kube-docs/blob/gh-pages/default.png?raw=true)

It is possible to work to certain extent only with Rancher. However, command line tool `kubectl` allows more actions. You can utilize both ways but we do not recommend `kubectl` for users inexperienced with working in terminal.
