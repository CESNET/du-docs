---
layout: article
title: PVC
permalink: /docs/pvc.html
key: pvc
aside:
  toc: true
sidebar:
  nav: docs
---

The PVC represents some kind of persistent storage that can be mounted into
a *pod*. PVCs are usually network volumes, e.g., NFS or CIFS/SMB. These kind
of PVCs can be mounted to many pods simultaneously thus making it a shared
storage among pods.

* User can create an ad-hoc PVC using [pvc.yaml](deployments/pvc.yaml)
   template. Downloading it and filling proper `name` and `storage` size and
   issuing command:
    ```
kubectl create -f pvc.yaml -n namespace
    ```

    where `namespace` is user namespace as can be seen in Rancher GUI, usually
    *surname-ns*. The ad-hoc pod does not contain any data in advance, the user
    needs to populate the data on his/her own. PVC name is the exactly the
    same you fill in the `name` value.
    TODO: how to populate data.

* Another option is to create PVC as CIFS storage from CERIT-SC. In such a case,
    user needs to download [secret.yaml](deployments/secret.yaml),
    fill in proper `name` and the following two annotations: `cerit.io/storage`,
    `cerit.io/share`. Those values from the example work for *storage-brno12-cerit* as
    they are, they make access to users home directory. For share `project` folders, `cerit.io/share` has to be set to: `cerit.io/share: 'export/nfs4/projects/project_name'`.
    User also needs to fill in `mount_flags`. The `mount_flags` is
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
    on [support@cerit-sc.cz](mailto: support@cerit-sc.cz). It is **not** the same password you use for logging
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
to your needs. You can request it at [k8s@ics.muni.cz](mailto: k8s@ics.muni.cz).

You see your PVCs in Rancher GUI in `Storage` &rarr; `PersistentVolumeClaims` ![Volumes](pvc.jpg)
