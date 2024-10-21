---
languages:
  - en
  - cs
---

# CyberDuck tool

[CyberDuck](https://cyberduck.io/) is a swiss knife tool for various cloud storage providers. It supports FTP, SFTP, WebDAV, OpenStack, OneDrive, Google Drive, Dropbox, etc. 

## Installation
You can download the exe installer from the [CybeDuck webpage](https://cyberduck.io/) and follow the installation steps.

## Configuration

Setup of new storage can be done via button **New connection** in the left menu.

![](cyberduck-screenshots/cyberduck1en.png){ style="display: block; margin: 0 auto" }

In the following window you can select **Amazon S3** and then insert the URL of the server s3.clX.du.cesnet.cz, where `X` is number asociated with your S3 account (e.g. `cl4`). Then please insert the `acces_key` and `secret_key`. Then you can click on the **Connection** button.

![](cyberduck-screenshots/cyberduck2en.png){ style="display: block; margin: 0 auto" }

The you can create a bucket - in the main directory can be only directories (buckets).

![](cyberduck-screenshots/cyberduck3en.png){ style="display: block; margin: 0 auto" }

While creating the bucket keep default region.

![](cyberduck-screenshots/cyberduck4en.png){ style="display: block; margin: 0 auto" }
