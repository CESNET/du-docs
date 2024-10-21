---
languages:
  - en
  - cs
---

# S3 Browser

[S3 Browser](https://s3browser.com/) is a freeware powerful and easy-to-use Windows client for S3 storage. You can manage up to two S3 accounts for free.

For installation please use the official package on the S3 [Browser webpages](https://s3browser.com/download.aspx).

## Basic configuration

Storage settings are made via the **Accounts** button in the left part of the program window.

![](s3browser-screenshots/s3browser1.png){ style="display: block; margin: 0 auto" }

Then select **Add new account**

![](s3browser-screenshots/s3browser2.png){ style="display: block; margin: 0 auto" }

In the following window, select **S3 Compatible Storage**

![](s3browser-screenshots/s3browser3.png){ style="display: block; margin: 0 auto" }

Then fill in **Display name** which is your connection name for better orientation, if you have multiple accounts. Then the **server s3.clX.du.cesnet.cz (clX - X according to the provided storage)** And keys: **Access Key ID = acces_key** and **Secret Access Key = secret_key by**. By clicking on **Add new account** the settings will be saved.

![](s3browser-screenshots/s3browser4.png){ style="display: block; margin: 0 auto" }

## Multipart upload/download configuration

If you need to upload and download large objects (typically larger than 5GB) you need to configure so-called multipart uploads/downloads. A large object is divided into multiple parts and then uploaded/downloaded. This functionality can also optimize the data throughput. On the data storage system are the objects represented as one object again.

Open the tool S3 Browser and then click in the main menu on **1. Tools** and then on **2. Options**.

![](s3browser-screenshots/s3b-multipart1.png){ style="display: block; margin: 0 auto" }

Then click on the bookmark **1. General**. Then tick the box **2. Enable multipart uploads** and define the `part` size for upload. Then tick the box **3. Enable multipart downloads** and define the `part` size for download. In the end, click on the button **4. Save changes**.

![](s3browser-screenshots/s3b-multipart2.png){ style="display: block; margin: 0 auto" }




