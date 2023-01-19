---
layout: article
title: Available Hardware
permalink: /docs/hw.html
key: matlab
aside:
  toc: true
sidebar:
  nav: docs
---

## kuba-cluster

This cluster comprises 4992 *hyperthreaded* CPU cores, 3456 currently available to users, 19.5TB RAM, 13TB currently available to users, and 22 NVIDIA A40, 6 NVIDIA A10 and 12 NVIDIA A100 (80GB variant) GPU accelerators. Four A100 cards are configured as MIGs in 12x 10GB + 8 20GB variants. It consists of 39 nodes (31 currently available) with the following configuration:

|  39x |                  |
| :--- | :--- |
| CPU: | 2x AMD EPYC 7543 |
| :--- | :--- |
| Memory: | 512GB |
| :--- | :--- |
| Disk: | 2x 3.5TB SSD SATA: kub-a5 -- kub-a25<br/> 8x 8TB NVME SSD: kub-b1 -- kub-b18 |
| :--- | :--- |
| GPU: | None: kub-a5 -- kub-a9<br/>2x NVIDIA A40 per node: kub-a10 -- kub-a14<br/>1x NVIDIA A40 per node: kub-a15 -- kub-a24 <br/> 2x NVIDIA A10 per node: kub-b1 -- kub-b3<br>2x NVIDIA A100 (80GB) per node: kub-b4 -- kub-b9|
| :--- | :--- |
| Network: | 2x 10Gbps NIC<br/>1x 100Gbps Infiniband: kub-b1 -- kub-b18 |
| :--- | :--- |

## Storage

Primary network storage consists of four head nodes each equipped with AMD EPYC 7302P, 256GB RAM, 2x 10Gbps NIC (failover only). It offers 500TB all-flash capacity of SSD drives only in RAID 6 equivalent configuration. Used filesystem is IBM Spectrum Scale that is exported via NFS version 3 to the kubernetes cluster.

### Data Backup

Storage is not backed up to another location, however, file system snapshots are made on daily basis, 14 snapshosts are kept. I.e., up to 14 days to the past, we are able to restore deleted/overwritten data.
