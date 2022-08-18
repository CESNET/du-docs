---
layout: article
title: Desktop
permalink: /docs/desktop.html
key: desktop
aside:
  toc: true
sidebar:
  nav: docs
---

## Running Desktop

If not already logged, log to [rancher.cloud.e-infra.cz](https://rancher.cloud.e-infra.cz), see [Rancher](https://cerit-sc.githu
b.io/kube-docs/docs/rancher.html) section.

Following the steps below, you can run Desktop application. This application can have persistent home directory, it means, that if you delete the application and later install the application again preserving its name, content of home directory will be preserved. It also possible to connect some storage from e-infra.

### Notes

* Default project had quota limit for 12 guaranteed CPUs and quota for 16 CPUs limit. Do not select more than 10 guaranteed CPUs and more than 14 CPUs limit. If needed more just [ask](mailto:k8s@ics.muni.cz). This may be increased in future so request for more CPUs can be made.

### Select Application to Run

Ensure, you did not select any namespace and see `Only User Namespaces` (1) at the top of the Rancher page.

Navigate through `App & Marketplace` (2), `Charts` (3), limit charts only to `cerit-sc` (4) and select `desktop` (5). See screenshot below.

![selectapp](desktop/selectapp.png)

### Select Version of the Application

When you click on the chart, you can select version of application as shown below. Chart versions can vary in time. Hit `Install` to continue.

![selectversion](desktop/selectversion.png)

### Install the Application

Now you can install the Desktop application. In most cases, keep both `Namespace` (1) and `Name` (2) intact, however, you can select namespace as desired except `default`. The `default` namespace is available but it is not meant to be used. The `Name` will be in URL to access the application. The `Name` must be unique in the `Namespace`, i.e., you cannot run two or more instances with the same `Name` in the same `Namespace`. If you delete the application and later install the application again preserving its `Name`, content of home directory will be preserved if enabled.

![appinst](desktop/appinst.png)

In the first part of the form, you select `Desktop` `Image`, currently, LTS Ubuntu 18, 20, 22 ara available, but images can vary in time.

![appform1](desktop/appform1.png)

In the second part of the form, you select access display method. [VNC]((https://cs.wikipedia.org/wiki/Virtual_Network_Computing) method is default. You will need some vncview program [realvnc](https://www.realvnc.com/en/connect/download/viewer/) or `vncviewer` on most Linux distribution. On MacOS, just type `vnc://host` into the Safari browser, replace `host` according to instructions below. Do not hit `Install` until the form is completed. Using *VNC*, only software drawing is available, no 3D acceleration is possible.

If VNC is not selected, *WEBRTC* method is used. This option is still in beta version, however, full 3D OpenGL acceleration is available.

#### Note

*WEBRTC* method is available in chromium-based web browsers  such as `google-chrome`, Microsoft Edge; or in Apple Safari. Especially, it does not work in Mozilla Firefox.

![appform2](desktop/appform2.png)

In the third part of the form, you select `password`. This password is used to login through VNC. If VNC is not selected, you need to fill also `username`, these credentials will be used in the browser to attach to the *WEBRTC* session.

#### For VNC
![appform3](desktop/appform3.png)

#### For WEBRTC
![appform3-rtc](desktop/appform3-rtc.png)

In the fourth part of the form, you select if you desire persistent home, i.e., home that will be preserved even if you uninstall the application. Note: persistent home is bound with application name from the very beginning of install form. It means, if you set name to `desktop`, persistent home will be bound with name `desktop`. If you select the name `desktop-0` next time, you get new home that is bound with the name `desktop-0`.

In this part, you can select **e-infra** storage to connect to the application. If you check `External Storage`, few more options appear. You can select storage and access credentials. Currently, only `storage-brno12-cerit.metacentrum.cz` is supported. Username is e-infra ([metacentrum](https://metavo.metacentrum.cz/)) login and password **is not** Metacentrum password, but different set by administrator, [ask](mailto:k8s@ics.muni.cz) if you need to set. We are preparing more convenient way. This storage is mounted to `/storage` directory.

![appform3](desktop/appform4.png)

In the fifth part  of the form, you can select requested resources. This step is optional. `Minimum` CPU or RAM is guaranteed amount of CPU and RAM, system reserves these resources for the application. However, the application can exceed guaranteed resources up to `Maximum`. However, in this case, resources are not exclusive and can be shared among other applications. If the application exceeds `Maximum` CPU, it gets limited, if it exceeds `Maximum` RAM, it gets terminated (you will see OOMKill report) and restarted. See note above about maximum values.

![appform4](desktop/appform5.png)

### Wait for Application to Start

When you hit `Install`, you will see installation log. Once you see `SUCCESS` (1) (see screenshot below), the application is running. In case of `VNC` version, you can see URL what shall be passed into VNC viewer (2) or in case of WebRTC version into the browser (2).

#### Notes

* If filled password for storage was not correct, it will be pending indefinitely. In such a case, delete application and start over.

#### VNC

![apphelm](desktop/apphelm.png)

#### WebRTC

![apphelm](desktop/apphelm-rtc.png)

### Connect to the Running Instance

Once the application is running, for *VNC* version, navigate through `Service Discovery` (1) and `Services` (2), hover with mouse over `Target` (3) and depending on used browser, you should see target URL (4). Chrome browser shows it in the lower left corner. This is IP and port you need to pass to your `vncviewer` application or fill into the Safari navigation bar, e.g., `vnc://147.251.253.246`. Or just use displayer URL from the screenshots above.

In case of *WEBRTC*, instead of `Services`, navigate to `Ingresses` (5) and you will see full URL to click on to start the *WEBRTC* connection.

*VNC* client will ask for the password. Type the password from the form. *WEBRTC* connection will ask for the username and password, those **are not** metacentrum username and password but the ones from the beginning of the form.

![apphelm](desktop/appservice.png)

## Desktop

On the first login, desktop will look like this depending on selected version:

![appdesktop](desktop/ubuntu18.png)

## Delete Running Instance

If you feel you do not need the application anymore, you can delete it. Just navigate to `App & Marketplace` (1), `Installed Apps` (2), select the application (3) and hit `Delete` (4). The data in home directory is not deleted in case you check persistent home. Running the application again with the same `Name` restores access to the home directory folder.

![appdel](desktop/appdel.png)

## Install Additional Software

It is possible to install additional software into running desktop either using system install or `conda` system.

### System Install

`apt-get install`, `apt install`, or `dpkg -i` commands can be used to install any package into the running desktop. However, if the desktop is restarted, all installed packages are lost and have to be installed again. All mentioned commands are shell aliases using `fakeroot` and those aliases are working in `bash` only, if using different shell, it might be needed to use e.g.: `fakeroot apt-get install [package]`.

### Conda

We strongly recommend to use `mamba` tool in favor of `conda` as it is faster. If you setup virtual conda environment into home directory, everything installed using `conda` or `mamba` will be persistent. For more information [see official conda documentation](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#managing-environments), specifically `Specifying a location for an environment`.
