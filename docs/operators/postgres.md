---
layout: article
title: Postgres Operator
permalink: /docs/operators/postgres.html
key: postgres
aside:
  toc: true
sidebar:
  nav: docs
---

The [Postgres Operator](https://opensource.zalando.com/postgres-operator/) delivers easy to run PostgreSQL cluster on Kubernetes. We have deployed cluster-wide Postgres operator for easy deployment of Postgres SQL database servers. The Postgres Operator defines kind `postgresql` that ensures existence of databse or database cluster, full documentation on kind's structure is available [here](https://postgres-operator.readthedocs.io/en/latest/reference/cluster_manifest/). The official user guide to creating a minimal PostgreSQl cluster can be found [here](https://postgres-operator.readthedocs.io/en/latest/user/). For convenience, we provide some working examples below divided into sections. Furthermore, we added comparison of deployments that used different underlying storage.

## Deploying Single Instance 

You can start with minimal instance suitable for testing only, it uses NFS storage as backend and uses only limited resources, but also performance is low. You can download [minimal manifest](postgres/minimal-nfs-postgres-manifest.yaml). 

```yaml
apiVersion: "acid.zalan.do/v1"
kind: postgresql
metadata:
  name: acid-test-cluster  ## name of our cluster
spec:
  teamId: "acid-test"
  numberOfInstances: 1     ## single instance
  users:
    zalando:               ## create user to db
    - superuser
    - createdb
  databases:            
    testdb: zalando        ## create db 'testdb' and add access to 'zalando' user
  postgresql:
    version: "13"          ## deploy postgres version 13
  volume:
    size: 1Gi            
    storageClass: nfs-csi  ## use nfs-csi class for backend storage
  spiloRunAsUser: 101      ## security context for db deployment
  spiloRunAsGroup: 103
  spiloFSGroup: 103
  resources:               ## give some resources
    requests:
      cpu: 10m
      memory: 100Mi
    limits:
      cpu: 500m
      memory: 500Mi
  patroni:
    initdb:                ## setup db for utf-8
      encoding: "UTF8"
      locale: "en_US.UTF-8"
      data-checksums: "true"
```

Issue `kubectl create -f minimal-nfs-postgres-manifest.yaml -n [namespace]` to run, you should see pod called `acid-test-cluster1-0` (if `metadata.name` has not been changed from the example) running in your namespace.

TBD: password for zalando user

This kind of setup is resilient to node failure --- if a node running this instance fails, database is recreated on a different node, data is attached again from NFS storage and operations are resumed. On the other hand, this setup is not speed superior even if resources are added.

## Deploying Cluster Instance

For better availability, cluster deployment can be used. In this case, multiple instances run in the cluster where one of them is a leader and others follow and sync data from the leader.

To deploy cluster version, you can download [cluster manifest](postgres/cluster-nfs-postgres-manifest.yaml). The only difference is on line:

```yaml
numberOfInstances: 3
```

That requests 3 node cluster.

Note: Cluster instances consume more resources and you must conside how much resources you have available. Cluster instance consumes `numberOfInstances * limits` of resources.

## Utilizing Local Storage

It is possible to use a local storage (SSD) instead of NFS or any network-backed PVC. While it is not possible to directly request local storage in `volume` section, it is still possible to use local storage. You can download [single instance manifest](postgres/minimal-local-postgres-manifest.yaml) which can be used for the cluster instance as well (setting desired `numberOfInstances`).

```yaml
volume:
  size: 1Gi
  storageClass: nfs-csi
additionalVolumes:
- name: data
  mountPath: /home/postgres/pgdata/pgroot
  targetContainers:
  - all
  volumeSource:
    emptyDir:
      sizeLimit: 10Gi
```

You need to add the `additionalVolumes` that mounts to `/home/postgres/pgdata/pgroot` and use `emptyDir` as backend storage. The `sizeLimit` value is very important in this case, if database storage exceeds this value, database Pod will be evicted. `size` for `volume` is not enforced like this.

## Database Access 

To access the database from other Pods, you can use `acid-test-cluster1` as host (following `metadata.name` from the deployment) within the same namespace, port is standard `5432`. Username and password is based on the deployment above. 

To increase security, one can deploy *Network policy* to allow network access to database from particular pods only. See [Network Policy](/docs/security.html). External access, i.e., access from public internet, is disabled by default. It is possible to expose the database via [Load Balancer](/docs/kubectl-expose.html#other-applications) though.

## Variants Comparison

We did some benchmarks utilizing standard `pgbench` tool. There were two benchmarks, `pgbench -i -s 1000` (**Create** column) which creates a table with 100M rows -- lower value is better, the second `pgbench -T 300 -c10 -j20 -r` (**TPS** column) which runs for 5 minutes and result is number of transactions per second -- higher value is better. 

Low resources means Limits: CPU 0.5, Memory 500MB, Requests: CPU 0.01, Memory 100MB. High resources means Limits: CPU 8, Memory 5000MB, Requests: CPU 1, Memory 1000MB. Extreme resources means Limits and Requests: CPU 16, Memory 32GB.

**Fail Safe** column denotes whether deployment is resilient to a single node failure meaning data loss will occur if a node fails.

### Single Instance

|---|---|---|---|---|
|Storage|Resources|Create|TPS|Fail Safe|
|---|---|---:|---:|:---:|
|Local SSD|Low|628 sec|561|No|
|Local SSD|High|263 sec|6745|No|
|Local SSD|Extreme|244 sec|10567|No|
|NFS|Low|586 sec|602|Yes|
|NFS|High|314 sec|4432|Yes|
|Ceph RBD|Low|2457 sec|142|Yes|

### Cluster Instances

|---|---|---|---|---|
|Storage|Resources|Create|TPS|Fail Safe|
|---|---|---:|---:|:---:|
|Local SSD|Low|704 sec|460|Yes|
|Local SSD|High|277 sec|6550|Yes|
|Local SSD|Extreme|246 sec|10447|Yes|
|NFS|Low|1027 sec|347|Yes|
|NFS|High|389 sec|2310|Yes|

## Data Backups

Operator offers automatic backups to S3 storage implemented via cronjobs.

TBD

## Caveats

### Deploy Errors

1. If you encounter an error in deployment and want to delete and create again, **you must** ensure that running instance is deleted before creating again. If you create a new instance too early, the instance will not be ever created and you need to use a different name. 

2. If starting instance encounters error in `initContainer` (which is disabled by default, so no error should be here), it cannot be deleted via removing the deployment above. You must delete the `StatefulSet` manually. Also in this case, new deployment with the same name will not be possible most probably. We recommend to use some testing names such as `test1`, `test2` for test deployments to mitigate this issue.

3. If you run out of quotas during the *Cluster* deployment, only instances within quotas are deployed. Unfortunately, also in this case you cannot remove/redeploy database using these deployments.

4. If you run out of `sizeLimit`, Pods will be evicted, i.e., terminated. TBD: what to do? Update specs?

5. Local SSD variant is not resilient to whole cluster failure. Data can be lost in this case (e.g., if cluster is restored from backup, local data might not be available). It is strongly recommended to backup regularly.
