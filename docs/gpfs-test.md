---
layout: article
title: GPFS Tests
permalink: /docs/gpfs-test.html
key: gpfs
aside:
  toc: true
---
## HW Configuration

|  18x |                  |
| :--- | :--- |
| CPU: | 2x AMD EPYC 7543 |
| :--- | :--- |
| Memory: | 512GB |
| :--- | :--- |
| Disk: | 2x 480GB SSD SATA<br/>8x 7.3TiB SSD NVME |
| :--- | :--- |
| GPU: | 2x NVIDIA A10 per node: kub-b1 -- kub-b3<br/>None: kub-b4 -- kub-b18|
| :--- | :--- |
| Network: | 2x 10Gbps NIC<br/>1x 100Gbps InfiniBand |
| :--- | :--- |

## GPFS Setup

Two volumes, Mirror as 4-way mirror configuration, RAID as 8+3 erasure coding. Pagepool limited to 32GB RAM only. All 144 NVME disks in, in case of 18 nodes.

## IOZone Testing

Iozone command: `iozone -Mce -t[number] -s256G -r256k -i0 -i1 -i2 -+m nodesiozone`

The iozone run on defined number of nodes.

### Local Test

Local test has been done on top of local RAID 0 of all 8 NVME disks

|---|---|---|---|---|---|---|
|Nodes|Threads|Type|Read Linear|Write Linear|Read Random|Write Random|
|---|---|---|---:|---:|---:|---:|
|1|4|Raid 0|9665804.50 kB/s|3226065.56 kB/s|3045126.25 kB/s|3046522.88 kB/s|
|2|8|Raid 0|18300435.75 kB/s|6375165.94 kB/s|6135955.69 kB/s|6329714.56 kB/s|
|4|16|Raid 0|38564588.25 kB/s|12869716.81 kB/s|12728638.88 kB/s|12715692.50 kB/s|
|8|32|Raid 0|75051993.50 kB/s|25754270.88 kB/s|25002526.31 kB/s|26225202.44 kB/s|
|18|72|Raid 0|169444818.12 kB/s|58596866.62 kB/s|56726668.94 kB/s|61578058.00 kB/s|

### GPFS Test All-to-All

`iozone` is running on all nodes in the table, i.e., 4, 8, and 18. The same number of nodes create the cluster.

|---|---|---|---|---|---|---|
|Nodes|Threads|Type|Read Linear|Write Linear|Read Random|Write Random|
|---|---|---|---:|---:|---:|---:|
|4|16|Mirror|15450073.88 kB/s|7066570.84 kB/s|4109981.08 kB/s|2769288.94 kB/s|
|4|16|Raid|15114023.75 kB/s|13591638.69 kB/s|4123895.00 kB/s|1776453.69 kB/s|
|8|32|Mirror|22505164.94 kB/s|9964138.91 kB/s|7655627.62 kB/s|4225650.12 kB/s|
|8|32|Raid|22116032.00 kB/s|18167540.00 kB/s|7675091.11 kB/s|2802509.34 kB/s|
|18|72|Mirror|47467272.62 kB/s|17169190.23 kB/s|16466901.61 kB/s|6712180.77 kB/s|
|18|72|Raid|43554656.69 kB/s|31707739.09 kB/s|15119176.98 kB/s|5047413.12 kB/s|

### GPFS Test Client-to-Server

`iozone` is running on dedicated nodes that do not export disks.

|---|---|---|---|---|---|---|---|
|Servers|Clients|Threads|Type|Read Linear|Write Linear|Read Random|Write Random|
|---|---|---|---|---:|---:|---:|---:|
|4|1|1|Mirror|9948759.00 kB/s|5433856.00 kB/s|168381.44 kB/s|1829260.00 kB/s|
|4|1|1|Raid|10624699.00 kB/s|8441799.00 kB/s|167091.83 kB/s|1579134.75 kB/s|
|4|1|4|Mirror|10317783.00 kB/s|6253592.38 kB/s|817474.12 kB/s|3148068.56 kB/s|
|4|1|4|Raid|11276012.50 kB/s|11567366.75 kB/s|810613.59 kB/s|1652378.53 kB/s|
|4|2|8|Mirror|20004521.00 kB/s|6486557.88 kB/s|1834332.94 kB/s|2445335.72 kB/s|
|4|2|8|Raid|19664908.75 kB/s|10777041.75 kB/s|1816458.12 kB/s|1730533.78 kB/s|
|4|4|16|Mirror|16559988.31 kB/s|6241745.75 kB/s|3459588.89 kB/s|1968840.45 kB/s|
|4|4|16|Raid|18028671.38 kB/s|10306010.19 kB/s|3444880.34 kB/s|1638063.06 kB/s|
|4|8|32|Mirror|19751287.19 kB/s|6334612.05 kB/s|7425030.20 kB/s||1925168.64 kB/s
|4|8|32|Raid|18493901.00 kB/s|10701033.97 kB/s|7453039.20 kB/s|1561307.49 kB/s|
|8|1|1|Mirror|9443386.00 kB/s|6528413.50 kB/s|160302.58 kB/s|2314426.25 kB/s|
|8|1|1|Raid|10207848.00 kB/s|8257618.00 kB/s|166649.08 kB/s|2235494.50 kB/s|
|8|1|4|Mirror|10596700.50 kB/s|6262270.12 kB/s|631479.34 kB/s|2536945.88 kB/s|
|8|1|4|Raid|8492436.25 kB/s|11965172.50 kB/s|638400.38 kB/s|2281125.56 kB/s|
|8|2|8|Mirror|7554419.44 kB/s|5552752.50 kB/s|1336451.75 kB/s|2878441.78 kB/s|
|8|2|8|Raid|10707949.25 kB/s|17209780.75 kB/s|1331589.69 kB/s|2458720.25 kB/s|
|8|4|16|Mirror|14730866.12 kB/s|5501406.62 kB/s|3186519.23 kB/s|3160925.27 kB/s|
|8|4|16|Raid|16840588.38 kB/s|17091926.38 kB/s|3165442.73 kB/s|2646366.28 kB/s|
|8|8|32|Mirror|27077112.50 kB/s|5531393.30 kB/s|6338315.22 kB/s|3640632.94 kB/s|
|8|8|32|Raid|25434443.62 kB/s|17126124.62 kB/s|6358202.62 kB/s|2595984.00 kB/s|

## FIO Test

FIO is single node test and has been focused on IOPS using random 4k reads and writes.

### Local NVME RAID 0

|---|---|---|
|Read|Write|
|---|---|---|
|131k|188k|

### GPFS

|---|---|---|
|Type|Read|Write|
|---|---|---|
|Mirror|21.1k|17.3k|
|Raid|23.4k|14.2k|

### NFS+GPFS+All-flash array

|---|---|---|
|Read|Write|
|---|---|---|
|30.7k|22.0k|

## Database Tests

|---|---|---|
|Type|Tool|Result|
|---|---|---|
|Local NVME|`pgbench -i -s 10000`|Duration: 14m25.6s|
|Local NVME|`pgbench -T 300 -c100 -j20 -r`|21199 TPS|
|GPFS RAID 4 Nodes|`pgbench -i -s 10000`|Duration: 147m54.1s|
|GPFS RAID 4 Nodes|`pgbench -T 300 -c100 -j20 -r`|2267 TPS|
|GPFS Mirror 4 Nodes|`pgbench -i -s 10000`|Duration: 187m49.7s|
|GPFS Mirror 4 Nodes|`pgbench -T 300 -c100 -j20 -r`|3535 TPS|
|GPFS RAID 18 Nodes|`pgbench -i -s 10000`|Duration: 151.56s|
|GPFS RAID 18 Nodes|`pgbench -T 300 -c100 -j20 -r`|2061 TPS|
|GPFS Mirror 18 Nodes|`pgbench -i -s 10000`|Duration: 115m0.5s|
|GPFS Mirror 18 Nodes|`pgbench -T 300 -c100 -j20 -r`|3164 TPS|
|NFS + GPFS + All-flash Array|`pgbench -i -s 10000`|Duration: 27m12s|
|NFS + GPFS + All-flash Array|`pgbench -T 300 -c100 -j20 -r`|5633 TPS|
