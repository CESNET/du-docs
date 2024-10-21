---
languages:
  - en
  - cs
---
# RBD Service

The Rados Block Device **RBD** is a block device that you can connect into your infrastructure. The connection must be done using a **Linux machine** (RBD connection to Windows is not yet implemented in reliable manner). Subsequently, you can re-export the connected block device anywhere within your systems (samba remount to your network). RBD is particularly suitable for use in centralized backup systems. RBD is a very specialized service that requires the user to have extensive experience in managing Linux devices. The service is intended for larger volumes of data - hundreds of TB. The block device can also be encrypted on your side (client side) using LUKS. Client-side encryption also means that the transmission of data over the network is encrypted, and in case of eavesdropping during transmission, the data cannot be decrypted. Access to the service is controlled by virtual organizations and coresponding groups.

!!! warning
    RBD connection is only possible from dedicated IPv4 addresses that are enabled on the firewall in our Data Centers. An RBD image can only be subsequently mounted on **ONE** machine, it is not possible for each of your users to mount the same RBD on their workstation - having said that the RBD is not used as clustered file system. Usage of clustered file systems over RBD must first be consulted with Data Care support.

???+ note "How to get RBD service?"
    To connect to RBD service you have to contact support at:
    `support@cesnet.cz`

----
## RBD elementary use cases
In the following section you can find the description of elementary use cases related to RBD service.

### Large dataset backups requiring local filesystem
If you have a centralized backup system (script suite, bacula, BackupPC…) requiring local file system, then we recommend you to use [RBD service](rbd-setup.md), see the figure  below. The RBD image can be connected directly to the machine where the central backup system is running, as a block device. RBD can then be equipped with snapshots, see service description, as protection against unwanted overwriting or ransomware attacks.

![](rbd-service-screenshots/central_backup.png){ style="display: block; margin: 0 auto" }

### Centralized shared storage for internal redistribution
If you need to store live data and need to provide the storage for individual user, then you can use [RBD](rbd-setup.md) service which you can connect to you infrastructure using a Linux machine. You can create a file system on the connected block device, or equip it with encryption, and then re-export them inside your infrastructure using, for example, samba, NFS, ftp, ssh, etc. (also in the form of containers ensuring the distribution of protocols to your internal network). Client-side encryption also means that the data transmission over the network is encrypted and the data cannot be decrypted once the transmission is sent. The advantage is that you can create groups and manage rights according to your preferences, or use your local database of users and groups. The RBD block device can also be equipped with snapshots at the RBD level, so if data is accidentally deleted, it is possible to return to a snapshot from the previous day, for example.

![](rbd-service-screenshots/shared_distribution.png){ style="display: block; margin: 0 auto" }

## RBD Data Reliability (Data Redundancy) - replicated vs erasure coding
In the section below are described additional aproaches for data redundancy applied to the object storage pool. RBD service can be equipped with **replicated** or **erasure code (EC)** redundancy or with **synchronous/asynchronous geographical repliacation**.

### Replicated
Your data is stored in three copies in the data center. In case one copy is corrupted, the original data is still readable in an undamaged form, and the damaged data is restored in the background. Using a service with the replicated flag also allows for faster reads, as it is possible to read from all replicas at the same time. Using a service with the replicated flag reduces write speed because the write operation waits for write confirmation from all three replicas.

???+ note "Suitable for?"
    Suitable for smaller volumes of live data with a preference for reading speed (not very suitable for large data volumes).

### Erasure Coding (EC)
Erasure coding (EC) is a data protection method. It is similar to the dynamic RAID known from disk arrays. Erasure coding (EC) is a method where data is divided into individual fragments, which are then stored with some redundancy across the data storage. Therefore, if some disks (or the entire storage server) fail, the data is still accessible and will be restored in the background. So it is not possible for your data to be on one disk that gets damaged and you lose your data.

???+ note "Suitable for?"
    Suitable, for example, for storing large data volumes.

### RBD snapshots 
Snapshots can be used at the RBD (replicated/erasure coding) level. Snapshots are controlled from the client side. [RBD snapshotting](rbd-setup.md) is one of the replacement options for the `tape_tape` policy - snapshots mirrored to another geographic location, see below.

### Synchronous geographical replication
Synchronous geographical replication protects against data center failure. Synchronous geographical replication degrades write speed because the system waits for a successful write confirmation at both geographic locations. If you feel that you need this service, please contact us.

### Asynchronous geographical replication
Asynchronous geographical replication partially protects against data center failure (certain data may be lost between individual asynchronous synchronizations due to time lag). However, with an asynchronous geographical replication, in case of data corruption (ransomware), you can disrupt the replication and safe your data. If you feel that you need this service, please contact us.
