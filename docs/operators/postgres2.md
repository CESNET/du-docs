---
layout: article
title: Postgres Operator Cloudnative-PG
permalink: /docs/operators/postgres2.html
key: postgres2
aside:
  toc: true
sidebar:
  nav: docs
---

The [Postgres Operator](https://cloudnative-pg.io/documentation/1.18/) provides easy to run PostgreSQL cluster on Kubernetes. We have provided cluster-wide Postgres Operator for easy deployment of Postgres SQL database servers. The Postgres Operator defines a kind of `Cluster` that ensures the existence of a database or database cluster, full documentation about its structure is available [here](https://cloudnative-pg.io/documentation/1.18/). The official manual for creating a minimal PostgreSQL cluster can be found [here](https://cloudnative-pg.io/documentation/1.18/quickstart/). For your convenience, we provide some working examples below, divided into sections. We have also added a comparison of deployments that use different underlying storage.

## Deploying a single instance

You can start with a minimal instance, which is suitable for testing only, it uses NFS storage as backend and consumes limited resources, but also performance is low. You can download the [minimal manifest] (/docs/postgres/minimal-cn.yaml).

```yaml
apiVersion: postgresql.cnpg.io/v1
kind: Cluster
metadata:
  name: test-cluster
spec:
  instances: 1             # single instance

  imageName: 'cerit.io/cloudnative-pg/postgresql:15.0' #image to use

  primaryUpdateStrategy: unsupervised

  bootstrap:
   initdb:
     database: mydb        # db to create
     owner: myowner        # user to create

  storage:
    size: 10Gi
    storageClass: nfs-csi  # storage class to use
```

Run `kubectl create -f minimal-cn.yaml -n [namespace]`, you should see a pod named `test-cluster-1` (if `metadata.name` has not been changed from the example) running in your namespace.

### Account Password

To reveal the password of the create user, simply issue
```shell
kubectl get secret test-cluster-app -n [namespace] -o 'jsonpath={.data.pgpass}' | base64 -d
```

It will show the string in the form: `dbhost:port:dbname:dbuser:password`. For example:
```
test-cluster-rw:5432:mydb:myowner:uLUmkvAMwR0lJtw5ksUVKihd5OvCrD28RFH1JTLbbzO6BhEAtnWJr1L0nWpTi3GL
```

This type of setup is resilient to node failure --- if a node running this instance fails, the database is recreated on another node, data is reconnected from NFS storage, and operations resume. On the other hand, this setup is not speed superior even when resources are added.

## Deploying Cluster Instance

For better availability, cluster deployment can be used. In this case, multiple instances run in the cluster where one of them is a leader and others follow and sync data from the leader.

To deploy cluster version, you can download [cluster manifest](/docs/postgres/cluster-cn.yaml). The only difference is on line:

```yaml
numberOfInstances: 3
```

That requests 3 node cluster.

Note: Cluster instances consume more resources and you must consider how much resources you have available. Cluster instance consumes `numberOfInstances * limits` of resources.

## Utilizing Local Storage

It is possible to use local storage (SSD) instead of NFS or any network supported PVC. While it is not possible to directly request local storage in the `volume' section, it is still possible to use local storage. You can download the [single instance manifest](/docs/postgres/minimal-local-cn.yaml) which can also be used for the cluster instance (set the desired `numberOfInstances`).

Basically, the `zfs-csi` storage class can be used to use local storage. Special care must be taken when setting the limit. It cannot be increased in the future and the limit is enforced.

## Database Access 

To access the database from other Pods, you can use `test-cluster-rw` as host (based on `metadata.name` from the deployment) within the same namespace, port is default `5432`. Username and password are based on the above deployment. There is a `test-cluster-ro` name available to access read-only replicas. If exposure to another namespace is required, use the full name: `test-cluster-rw.[namespace].svc.cluster.local`.

To increase security, a *network policy* can be used to allow network access to the database only from certain pods. See [Network Policy](/docs/security.html). External access, i.e. access from the public Internet, is disabled by default. However, it is possible to expose the database via [Load Balancer](/docs/kubectl-expose.html#other-applications).

An example of exposing the database outside of the Kubernetes cluster can be found [here](/docs/postgres/expose-cn.yaml). This example exposes the DB on private MUNI addresses. If you need to expose to the internet, remove the `metallb.universe.tf/address-pool: privmuni` annotations, especially in this case, be sure to specify `loadBalancerSourceRanges` which restricts access only from these IPs. Note: The `/32` suffix is required. This example exposes both read-only and read-write services, read-write is on port `5432` while read-only is on port `5433`. In order for the two ports to share the same IP address, the `metallb.universe.tf/allow-shared-ip' annotation must be unique and have the same value for both services.

## Variants Comparison

For variants comparison, see [zalando operator](/docs/operators/postgres.html#variants-comparison).

## Data Backups

Operator offers automatic backups to S3 storage implemented via cronjobs.

First you need to get an S3 storage account, e.g. at [DU Cesnet](https://du.cesnet.cz/en/navody/object_storage/cesnet_s3/start), mainly `KEY-ID` and `SECRET-ID` are needed. Using these two IDs, you can create a `Secret` object via [template](/docs/postgres/secret-cn.yaml), replacing `KEY-ID` and `SECRET-ID` with real values.

Next, deploy the DB cluster via [template](/docs/postgres/minimal-cn-backup.yaml). Replace `BUCKET` and `S3URL` with real values. **Do not replace `ACCESS_KEY_ID` and `ACCESS_SECRET_KEY`, they need to match the Secret key names.**

## Caveats

### Deploy Errors

1. If you encounter a deployment error and want to delete and recreate, **you must** make sure that the running instance is deleted before recreating. If you create a new instance too early, the instance will never be created and you will have to use a different name.

2. If you run out of quotas during the *cluster* deployment, only instances within quotas will be deployed. Unfortunately, even in this case, you cannot remove/redeploy a database using these deployments.

3. Local SSD variant is not resilient to cluster failure. Data may be lost in this case (e.g. if cluster is restored from backup, local data may not be available). Regular backups are strongly recommended.

4. It may happen that a replica fails and cannot join the cluster, in which case the replica and PVC must be removed at once using kubectl delete pod/test-cluster-1 pvc/test-cluster-1 -n [namespace]` if the failed replica is `test-cluster-1`. The replica will be rebuilt and synchronized with the rest of the cluster. However, its number will be increased.

### Images

Currently, cloudnative-pg docker images do not contain `cs_CZ` locale, so Czech collate cannot be used. For this reason, we have created two local images: `cerit.io/cloudnative-pg/postgresql:10.23-3` and `cerit.io/cloudnative-pg/postgresql:15.0` which contain Czech locales.
