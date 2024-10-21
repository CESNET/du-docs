---
languages:
  - en
  - cs
---

# WinSCP - S3 usage

[WinSCP](https://winscp.net/eng/index.php) is the popular SFTP client and FTP client for Microsoft Windows! Transfer files between your local computer and remote servers using FTP, FTPS, SCP, SFTP, WebDAV or S3 file transfer protocols.

## WinSCP installation
Please use the package directly from [WinSCP](https://winscp.net/eng/download.php) for installation. Installation is common and no special settings are required.

## WinSCP configuration

Run the tool.

![](winscp-screenshots/winscp_setup1en.png){ style="display: block; margin: 0 auto" }

The storage connection is made via **Session** from the main menu and the **New session**.

![](winscp-screenshots/winscp_setup2en.png){ style="display: block; margin: 0 auto" }

In the drop-down menu **File protocol** select **Amazon S3**.

![](winscp-screenshots/winscp_setup3en.png){ style="display: block; margin: 0 auto" }

Then insert **Host name** `s3.clX.du.cesnet.cz` where replace **X** with the number of the cluster associated with your S3 account. Port `443` will be pre-filled automatically. Copy `access_key` into the field Access key ID and `secret_key` into the Secret access key - you received both of these keys encrypted from the administrators.

![](winscp-screenshots/winscp_setup4en.png){ style="display: block; margin: 0 auto" }

Select **Advanced** settings.

![](winscp-screenshots/winscp_setup5en.png){ style="display: block; margin: 0 auto" }

The field `Default region` leave blank! A Style URL **Path** and confirm OK. Then click **Connect**.

![](winscp-screenshots/winscp_setup6en.png){ style="display: block; margin: 0 auto" }

Then the storage is connected and you will see a list of your buckets on the right side. Or you can start to create own buckets.
