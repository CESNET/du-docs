---
languages:
  - en
  - cs
---
# Favorite S3 service clients
In the following section you can find recommended S3 clients. For all S3 clients are necessary S3 credentials `access_key` and `secret_key` and the S3 endpoint address, see below.

???+ note "Available S3 endpoints"
    cl1 - https://s3.cl1.du.cesnet.cz<br/>
    cl2 - https://s3.cl2.du.cesnet.cz<br/>
    cl3 - https://s3.cl3.du.cesnet.cz<br/>
    cl4 - https://s3.cl4.du.cesnet.cz<br/>

## S3 Browser (GUI Windows)
[S3 Browser](https://s3browser.com/) is a freeware tool for Windows to manage your S3 storage, upload and download data. You can manage up to two user accounts (S3 account) for free. [The Guide for S3 Browser](s3browser.md).

## CloudBerry Explorer for Amazon S3 (GUI Windows)
[CloudBerry Explorer](https://cloudberry-explorer-for-amazon-s3.en.softonic.com/) is an intuitive file browser for your S3 storage. It has two windows so in one you can see the local disk and in the second you can see the remote S3 storage. Between these two windows, you can drag and drop your files. [The guide for CloudBerry explorer](cloudberry.md).

## AWS-CLI (command line, Linux, Windows)
[AWS CLI](https://aws.amazon.com/cli/) - Amazon Web Services Command Line Interface - is standardized too; supporting S3 interface. Using this tool you can handle your data and set up your S3 data storage. You can used the command line control or you can incorporate AWS CLI into your automated scripts. [The guide for AWS-CLI](aws-cli.md).

## Rclone (command line + GUI, Linux, Windows)
The tool [Rclone](https://rclone.org/downloads/) is suitable for data synchronization and data migration between more endpoints (even between different data storage providers). Rclone preserves the time stamps and checks the checksums. It is written in Go language. Rclone is available for multiple platforms (GNU/Linux, Windows, macOS, BSD and Solaris). In the following guide, we will demonstrate the usage in Linux and Windows systems. [The guide for rclone](rclone.md).

## s3cmd (command line Linux)
[S3cmd](https://s3tools.org/download) is a free command line tool to upload and download your data. You can also control the setup of your S3 storage via this tool. S3cmd is written in python. It goes about open-source project available under GNU Public License v2 (GPLv2) for personal either or commercial usage. [The guide for s3cmd](s3cmd.md).

## s5cmd for very fast transfers (command line Linux)
In case you have a connection between 1-2Gbps and you wish to optimize the transfer throughput you can use s5cmd tool. S5cmd is available in the form of precompiled binaries for Windows, Linux and macOS. It is also available in form of source code or docker images. The final solution always depends on the system where you wish to use s5cmd. A complete overview can be found at [Github project](https://github.com/peak/s5cmd). [The guide for s5cmd](s5cmd.md).

## WinSCP (GUI Windows)
[WinSCP](https://winscp.net/eng/index.php) is the popular SFTP client and FTP client for Microsoft Windows! Transfer files between your local computer and remote servers using FTP, FTPS, SCP, SFTP, WebDAV or S3 file transfer protocols. [The guide for WinSCP](winscp.md)

## CyberDuck (GUI Windows)
[CyberDuck](https://cyberduck.io/s3/) is a multifunctional tool for various types of data storage (FTP, SFTP, WebDAV, OpenStack, OneDrive, Google Drive, Dropbox, etc.). Cyberduck provides only elementary functionalities, most of the advanced functions are paid. [The guide for CyberDuck](cyberduck.md)







