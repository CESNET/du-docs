---
languages:
  - en
  - cs
---

# CloudBerry Explorer for Amazon S3

[CloudBerry Explorer](https://cloudberry-explorer-for-amazon-s3.en.softonic.com/) is an intuitive file explorer that helps you manage your S3 account as if it were another folder on your local drive. The program has a double-pane interface and acts as an FTP client, with each window dedicated to a single folder. These locations are not fixed and can be switched to suit your current task: a local computer and a remote S3 server, two local folders, or even two S3 accounts. 

## Cloudberry Installation
You can use exe installer from [the oficial websites of Cloudberry](https://cloudberry-explorer-for-amazon-s3.en.softonic.com/). When you start the program, it will be always informed about the registration options. Registration is free. Then you receive the key via e-mail and then all pop-ups are avoided.

!!! warning
    CloudBerry in the FREE version does not support Multipart Upload and Multithreading, which means that it cannot work with files larger than 5GB. Encryption and compression is also enabled in the PRO version.

## Cloudberry Configuration
Storage configuration can be done via **1. File** menu, where you select **2 Add New Account**. Do not select the Amazon S3 Accounts option, as it does not have the option of entering a service point etc.!

![](cloudberry-screenshots/cloudberry1.png){ style="display: block; margin: 0 auto" }

In the next window Select Cloud Storage - **1. S3 Compatible** option.

![](cloudberry-screenshots/cloudberry2.png){ style="display: block; margin: 0 auto" } 

In the next step you have to fill in S3 credentials including the S3 endpoint.

![](cloudberry-screenshots/cloudberry3.png){ style="display: block; margin: 0 auto" }

Then you can start to upload your data. From the **1. Source selector** you will select your **2. S3 account**, which has been previously configured.

![](cloudberry-screenshots/cloudberry4.png){ style="display: block; margin: 0 auto" }

First you need to **1. Create new bucket** and then you can upload your data into it.

![](cloudberry-screenshots/cloudberry5.png){ style="display: block; margin: 0 auto" }

