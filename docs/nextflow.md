---
layout: article
title: Running Nextflow Pipelines in Kubernetes
permalink: /docs/nextflow.html
key: nextflow
aside:
  toc: true
sidebar:
  nav: docs
---

The following text describes how to run Nextflow pipelines in CERIT-SC Kubernetes cluster.

## Nextflow Installation

To install nextflow enter this command in your terminal:
```
curl -s https://get.nextflow.io | bash
```
You can install specific Nextflow version exporting NXF_VER environment
variable before running the install command, e.g.:
```
export NXF_VER=20.10.0
curl -s https://get.nextflow.io | bash
```

## Architecture of Nextflow 

The Nextflow pipeline starts running the `nextflow` command, e.g.:

```
nextflow run hello
```

which starts running hello pipeline. The pipeline run consists of two parts:
*workflow controller* and *workers*.

Nextflow engine expects that the *workflow controller* and the *workers* have
access to some shared storage. On a local computer, this is usually just a
particular directory, in case of distributed computing, this has to be a
network storage such as NFS mount. User needs to specify what storage can be
used when running the Nextflow.

## Runing Nextflow in Kubernetes

In case of K8s, *workflow controller* is run as a
[Pod](https://kubernetes.io/docs/concepts/workloads/pods/) in Kubernetes
cluster. Its task is to run *worker* pods according to pipeline definition.

### Requirements

* Installed [`kubectl`](https://cerit-sc.github.io/kube-docs/docs/kubectl.html) with configuration file.
* Created [PVC](https://kubernetes.io/docs/concepts/storage/persistent-volumes/) (see below how to do it).

### PVC

The PVC represents some kind of persistent storage that can be mounted into
a *pod*. PVCs are usually network volumes, e.g., NFS or CIFS/SMB. These kind
of PVCs can be mounted to many pods simultaneously thus making it a shared
storage among pods.

* User can create an ad-hoc PVC using [pvc.yaml](https://github.com/CERIT-SC/example-deployments/blob/master/pvc/pvc.yaml)
   template. Downloading it and filling proper `name` and `storage` size and
   issuing command:
    ```
kubectl create -f pvc.yaml -n namespace
    ```

    where `namespace` is user namespace as can be seen in rancher GUI, usually
    *surname-ns*. The ad-hoc pod does not contain any data in advance, the user
    needs to populate the data on his/her own. PVC name is the exactly the
    same you fill in the `name` value.
    TODO: how to populate data.

* Another option is to create PVC as CIFS storage from CERIT-SC. In such a case,
    user needs to download [secret.yaml](https://github.com/CERIT-SC/example-deployments/blob/master/pvc/secret.yaml),
    fill in proper `name` and the following two annotations: `cerit.io/storage`,
    `cerit.io/share`. Those values from the example work for *storage-brno12-cerit* as
    they are. User also needs to fill in `mount_flags`. The `mount_flags` is
    base64 encoded string that can be obtained using the following command:
    ```
echo -n "username=USER,password=PASS,uid=1000,gid=1000,nosetuids,vers=3.11,noserverino" | base64
    ```
    where `USER` and `PASS` are username and password accessing
    *storage-brno12-cerit*, resp. In case the `USER` is UČO, `domain=UCN` needs to
    be added into the `echo` command as another comma separated value, i.e.,
    ```
echo -n "username=USER,password=PASS,uid=1000,gid=1000,nosetuids,vers=3.11,noserverino,domain=UCN" | base64
    ```

    In case, you do not know CIFS password for CERIT-SC storage, just ask for one
    on support@cerit-sc.cz. It is **not** the same password you use for logging
    into infrastructure!

    Be aware that the base64 encoded string is not encrypted, so keep it secret!

    Once the user created secret.yaml file, it needs to be uploaded into
    Kubernetes via the following command:
    ```
kubectel create -f secret.yaml -n namespace
    ```
    The `namespace` is the same as in the previous case. PVC name is derived
    from the `name` value and will be: `pvc-name`. In this case, PVC will not
    be empty, it contains data from your home from storage-brno12-cerit.

* The last option is to request admins to create special PVC for you according
to your needs. You can request it at k8s@ics.muni.cz.

### Running Nextflow

Running the Nextflow in Kubernetes requires local configuration. You can
download
[nextflow.config](https://github.com/CERIT-SC/example-deployments/blob/master/nextflow/nextflow.config)
which can be used as is in the case, you change `namespace` to correct value
and specify `launchDir` and `workDir` to point somewhere on the PVC. Take
care, if running Nextflow in parallel, always use different `launchDir` and
`workDir` for the parallel runs.

You need to keep the file in the current directory where the `nextflow`
command is run.

To instruct the Nextflow to run the pipeline in Kubernetes, you can run the
following command:
```
nextflow kuberun hello -pod-image 'cerit.io/nextflow:21.09.1' -v PVC:/mnt 
```
where PVC is name of the PVC as discussed above. It will be mounted as /mnt.
You should use this mount point as some pipelines expect this location.

If everything was correct then you should see output like this:
```
Pod started: naughty-williams
N E X T F L O W  ~  version 21.09.0-SNAPSHOT
Launching `nextflow-io/hello` [naughty-williams] - revision: e6d9427e5b [master]
[f0/ce818c] Submitted process > sayHello (2)
[8a/8b278f] Submitted process > sayHello (1)
[5f/a4395f] Submitted process > sayHello (3)
[97/71a2e0] Submitted process > sayHello (4)
Ciao world!
Hola world!
Bonjour world!
Hello world!
```

## nf-core/sarek pipeline
## vib-singlecell-nf/vsn-pipelines pipeline
