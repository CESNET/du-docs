---
layout: article
title: Postgres Operator Cloudnative-PG
permalink: /docs/operators/postgres-cnpg.html
key: postgrescnpg
aside:
  toc: true
sidebar:
  nav: docs
---

The [Postgres Operator](https://cloudnative-pg.io/documentation/1.18/) provides easy to run PostgreSQL cluster on Kubernetes. We have provided cluster-wide Postgres Operator for easy deployment of Postgres SQL database servers. The Postgres Operator defines a kind of `Cluster` that ensures the existence of a database or database cluster, full documentation about its structure is available [here](https://cloudnative-pg.io/documentation/1.18/). The official manual for creating a minimal PostgreSQL cluster can be found [here](https://cloudnative-pg.io/documentation/1.18/quickstart/). For your convenience, we provide some working examples below, divided into sections. We have also added a comparison of deployments that use different underlying storage.

## Deploying a single instance

You can start with a minimal instance, which is suitable for testing only, it uses NFS storage as backend and consumes limited resources, but also performance is low. You can download the [minimal manifest](/docs/postgres/minimal-cn.yaml).

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

It is possible to use local storage (SSD) instead of NFS or any network supported PVC. While it is not possible to directly request local storage in the `volume` section, it is still possible to use local storage. You can download the [single instance manifest](/docs/postgres/minimal-local-cn.yaml) which can also be used for the cluster instance (set the desired `numberOfInstances`).

Basically, the `zfs-csi` storage class can be used to use local storage. Special care must be taken when setting the limit. It cannot be increased in the future and the limit is enforced, however, it is fasted storage that is offered.

## Database Access 

Database can be accessed (connected) from the same namespace, different namespace, or from outside of the Kubernetes cluster. Databases commonly use read-only connections (targeting usually replicas) and read-write connections (targeting master instance).

### Authentication

Username and password are based on the cluster instance, if you created the instance including username and password, use these credentials to connect. 

### Access from the same Namespace

If the cluster has been created with the name `test-cluster`:

```yaml
kind: Cluster
metadata:
  name: test-cluster
...
```

The hostname of read-only replica is `test-cluster-ro` and the hostname of writable master is `test-cluster-rw`. If not explicitly set otherwise, port is default `5432`.

### Access from a different Namespace

This case is similar to the case of access from the same namespace. Assuming the database name is the same `test-cluster, the read-only hostname is `test-cluster-ro.[namespace].svc.cluster.local` and writable master is `test-cluster-rw.[namespace].svc.cluster.local`, replace `[namespace]` with name of the namespace where the database is deployed.


### Access from outside of the Kubernetes Cluster

To access the database from outside of the Kubernetes Cluster, a new service object of type LoadBalancer must be created. If both types of access are required -- read-only and writable, two LoadBalancers must be created, one for each type. In this case, it is strongly recommended to distinguish between read-only and writable access by different ports rather than different IP addresses as those are scare resources. 

Assuming the database name is again `test-cluster`, you can find example of both objects [here](/docs/postgres/expose-cn.yaml). The annotation `metallb.universe.tf/allow-shared-ip` ensures that both LoadBalancers share the same IP address and are distinguished by port: `5433` port is for read-only replicas and `5432` is writable. This example assigns IP addresses that are reachable only from internal network from Masaryk University or via VPN service of Masaryk University. While this is recommended setup for users of Masaryk University, it will not work for the others. Other users must remove the annotation `metallb.universe.tf/address-pool: privmuni` and the IP addresses will be allocated from public IP pool. 

### Network Policy

To increase security, a *network policy* can be used to allow network access to the database only from certain pods. The network policy is recommended in all cases mentioned above and strongly recommended, if access from oside of the Kubernetes cluster has been set up. See [Network Policy](/docs/security.html) for general concepts.

You should restrict access from either a particular Pod or a particular external IP address. However, access from `cloudnativegp` namespace must be allowed as well so that the operator can control the instance. If your network policy contains also `Egress` rules, keep in mind to allow access to S3 backup address so that backups are working.

Example for access from the Kubernetes cluster is [here](/docs/postgres/netpolicy-internal.yaml), example for access from external IP adress is [here](/docs/postgres/netpolicy-external.yaml). In both casese, replace `[namespace]` with your namespace and for the external case, replace `IP/32` with your external IP `/32` (this slash 32 must be the trailing part of the address).

## Variants Comparison

For variants comparison, see [zalando operator](/docs/operators/postgres.html#variants-comparison).

## Data Backups

Operator offers automatic backups to S3 storage implemented via periodic wal streaming and regular backups (basically `pgdump` equivalent) using `CronJobs`.

First you need to get an S3 storage account, e.g. at [DU Cesnet](https://du.cesnet.cz/en/navody/object_storage/cesnet_s3/start), mainly `KEY-ID` and `SECRET-ID` are needed. Using these two IDs, you can create a `Secret` object via [template](/docs/postgres/secret-cn.yaml), replacing `KEY-ID` and `SECRET-ID` with real values.

Next, deploy the DB cluster via [template](/docs/postgres/minimal-cn-backup.yaml). Replace `BUCKET` and `S3URL` with real values. **Do not replace `ACCESS_KEY_ID` and `ACCESS_SECRET_KEY`, they need to match the Secret key names.**

### Full Backups

For full backups, additional resource needs to be created. 

```yaml
apiVersion: postgresql.cnpg.io/v1
kind: ScheduledBackup
metadata:
  name: [backup-name]
spec:
  schedule: "0 0 0 * * *"
  backupOwnerReference: self
  cluster:
    name: [db-name]
```

Replace `[backup-name]` with appropriate name of the resource (must be unique within a namespace), and `[db-name]` with the name of the database cluster from the main manifest, these two names must match. E.g., cluster manifest beginning with:
```yaml
apiVersion: postgresql.cnpg.io/v1
kind: Cluster
metadata:
  name: test-cluster
```

Needs backup manifest:
```yaml
apiVersion: postgresql.cnpg.io/v1
kind: ScheduledBackup
metadata:
  name: backup
spec:
  schedule: "0 0 0 * * *"
  backupOwnerReference: self
  cluster:
    name: test-cluster
```

Schedule is standard `cron` schedule. 

## High Availability

Replicated cluster is usable for high availability cases. Starting from Postgres version 11, operator supports some additional settings to increase high availability. 

1. Increase wal segments history using the following snippeet. Change the `wal_keep_size` value as appropriate. Default value is about 500MB which can be small. However, this value is allocated from the underlaying storage. If `zfs-csi` is used, it enforces disk size and DB wals can easily consume all disk space.
```yaml
postgresql:
    parameters:
      wal_keep_size: 64GB
```

2. Enable high availability option:
```yaml
replicationSlots:
    highAvailability:
      enabled: true
```

Please, keep in mind, that these options work for Postgres 11 and later only. Full cluster example with the HA options:
```yaml
apiVersion: postgresql.cnpg.io/v1
kind: Cluster
metadata:
  name: test-cluster
spec:
  instances: 3

  imageName: 'ghcr.io/cloudnative-pg/postgresql:14.7-3'

  primaryUpdateStrategy: unsupervised

  bootstrap:
    initdb:
      database: dbname
      owner: dbowner

  postgresql:
    parameters:
      wal_keep_size: 64GB

  replicationSlots:
    highAvailability:
      enabled: true

  resources:
    requests:
      memory: "4096Mi"
      cpu: 1
    limits:
      memory: "4096Mi"
      cpu: 1

  storage:
    size: 10Gi
    storageClass: zfs-csi
```

## Caveats

### Deploy Errors

1. If you encounter a deployment error and want to delete and recreate, **you must** make sure that the running instance is deleted before recreating. If you create a new instance too early, the instance will never be created and you will have to use a different name.

2. If you run out of quotas during the *cluster* deployment, only instances within quotas will be deployed. Unfortunately, even in this case, you cannot remove/redeploy a database using these deployments.

3. Local SSD variant is not resilient to cluster failure. Data may be lost in this case (e.g. if cluster is restored from backup, local data may not be available). Regular backups are strongly recommended.

4. It may happen that a replica fails and cannot join the cluster, in which case the replica and PVC must be removed at once using kubectl delete pod/test-cluster-1 pvc/test-cluster-1 -n [namespace]` if the failed replica is `test-cluster-1`. The replica will be rebuilt and synchronized with the rest of the cluster. However, its number will be increased.

### Images

Currently, cloudnative-pg docker images do not contain `cs_CZ` locale, so Czech collate cannot be used. For this reason, we have created two local images: `cerit.io/cloudnative-pg/postgresql:10.23-3` and `cerit.io/cloudnative-pg/postgresql:15.0` which contain Czech locales.

List of public images is available [here](https://github.com/cloudnative-pg/postgres-containers/pkgs/container/postgresql).

## Network Policy

To increase security, a *network policy* can be used to allow network access to the database only from certain pods. See [Network Policy](/docs/security.html) for more information. External access, i.e. access from the public Internet, is disabled by default. However, it is possible to expose the database via [Load Balancer](/docs/kubectl-expose.html#other-applications).

The following example shows a simple NetworkPolicy applied to the Postgres operator. You can download this example [here](postgres-cnpg-minimal-postgres-np.yaml). **Please note that if you want to use the data backups and also restrict the egress communication, you may need to add an egress rule enabling the communication to the backup server!** If ingress only restriction is suitable for you, you can remove the egress rules.

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: postgres-cnpg-np
spec:
  podSelector:
    matchLabels:
      # This Network Policy is applied to our Postgres CNPG Cluster resource named "test-cluster"
      cnpg.io/cluster: test-cluster
  policyTypes:
  - Ingress
  - Egress # <---
  ingress:
    # Enables ingress Postgres port for all Pods
  - ports:
    - port: 5432
      protocol: TCP
    from:
    - podSelector: {}
    # Enables ingress communication from the Postgres CNPG Operator installed in the Kubernetes
  - ports:
    - port: 8000
      protocol: TCP
    from:
    - namespaceSelector:
        matchLabels:
          kubernetes.io/metadata.name: cloudnativepg
      podSelector:
        matchLabels:
          app.kubernetes.io/name: cloudnative-pg
  egress: # <---
    # Enables egress communication to the Postgres CNPG Operator installed in the Kubernetes
  - ports:
    - port: 6443
      protocol: TCP
    to:
    - ipBlock:
        cidr: 10.43.0.1/32
    - ipBlock:
        cidr: 10.16.62.14/32
    - ipBlock:
        cidr: 10.16.62.15/32
    - ipBlock:
        cidr: 10.16.62.16/32
    - ipBlock:
        cidr: 10.16.62.17/32
    - ipBlock:
        cidr: 10.16.62.18/32
```
