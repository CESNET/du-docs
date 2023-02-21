---
layout: article
title: Container Platform Overview
permalink: /index.html
key: index
aside:
  toc: true
sidebar:
  nav: docs
---

Our container platform is based on [Kubernetes orchestrator](https://kubernetes.io/) and [docker](https://hub.docker.com/) container images. We have adopted [rancher](https://rancher.com) Kubernetes distribution, so our platform UI is available through [Rancher dashboard](https://rancher.cloud.e-infra.cz). Currently, the platform is built on Linux and x86\_64 binary architecture (no Arm or Microsoft Windows is possible), we provide GPU accelerators (currently only NVIDIA), and SSD storage. We also provide InfiniBand 100Gbps interconnect fabrics between selected nodes.

In general, this platform can be used for almost anything, starting with a simple web application, see the [hello world](/docs/kubectl-helloworld.html) example, to running a full remote desktop, see the [ansys](/docs/ansys.html) application, or running a complex workflow pipeline, see the [nextflow](/docs/nextflow.html) example.

This platform offers users to focus solely on their applications, so that required knowledge comprises of using the application or containerizing the application only. In the latter case, knowledge of creating dockerfiles is required (see [dockerfile](/docs/dockerfile.html) section). However, almost no knowledge of infrastructure is needed such as mounting `NFS` and so on.

Academic affiliation or sponsored account is required to use this platform. Users can log in via CESNET AAI, Elixir AAI or EGI AAI. No additional membership is required for a *standard* project with limited resources.

End user can use this platform in the following three ways:

1. Use pre-built applications through the infrastructure, see [Rancher Applications](/docs/rancher-applications.html) in the navigation on the left.

2. Leverage existing Docker images from around the world hosted on a *registry* such as [hub.docker.com](https://hub.docker.com), in this case see [limitations](/docs/limitations.html).

3. Advanced users can also create their own application, see [dockerfile](/docs/dockerfile.html) section.
