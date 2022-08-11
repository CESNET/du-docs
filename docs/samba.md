---                                                                                                                                                                                                        
layout: article                                                                 
title: Samba Server
permalink: /docs/samba.html                                                     
key: samba                                                          
aside:                                                                          
  toc: true                                                                     
sidebar:                                                                        
  nav: docs                                                                     
---  

## Samba Server
Samba server can be used to expose Persistent Volume Claim via CIFS/SMB protocol as a network drive reachable at specified **URL** in the form of `\\[namespace]-[samba_name].dyn.cloud.e-infra.cz\data` . Persistent Volume Claim (PVC) is used as a storage for running applications in Kubernetes. If you want to upload/download data to/from PVC using GUI, Samba server is a convenient way to do so.

### Prerequisities
Samba server works only when you want to expose already existing PVC! Therefore, make sure your PVC already exists.

### Installation
1. In the Rancher GUI, check the name of the PVC you would like to expose. In the example, we are going to expose PVC with name `matlab-home` in namespace `spisakova-ns`.

![pvcs](samba-images/pvc.png) 

2. Navigate to all available applications and select `samba`, then click on install button in the top right corner.

![samba](samba-images/charts.png) 

3. Select the namespace, where application will be deployed. You must choose **the same** namespace as the namespace of the PVC you want to expose. Therefore, in the example we select namespace `spisakova-ns`. Select a name for your samba application that will form a part of the final url; the name must be unique in the namespace. In the example, we will use `samba-matlab`.

![samba-basic](samba-images/basic.png) 

4. In the server settings, set password for the samba server. Username is always **user**. Select the PVC you want to expose, in the example we select `matlab-home`.

![samba-server-settings](samba-images/serversettings.png)

4.1. Your network drive will be available only in MUNI network or after connecting to MUNI VPN. If you want to access the network drive from elsewhere, select public exposure in the second tab `Expose type`. 

![samba-public-expose](samba-images/expose.png)

5. Wait, until samba server is installed, it should take a couple of seconds. 

### Connection
The final URL is composed of selected namespaces and samba application name. In our case, we can see name (samba-matlab) and namespace (spisakova-ns) next to green `Deployed` (which is a sign of successfull installation together with SUCCESS message in the logs boxs at the bottom of the page). The final url therefore looks like `spisakova-ns-samba-matlab.dyn.cloud.e-infra.cz`. 


1. Linux ---

2. Windows ---

3. MacOS --- open Safari and provide url in the form of `smb://[namespace]-[samba_name].dyn.cloud.e-infra.cz\data`. Click on `Allow`, provide the credentials as registered user (username is user, password is the one you set). Connect and nework drive will be available in the Finder. You can later unmount the drive using unmount button. 


![samba-mac-allow](samba-images/mac-allow.png)
![samba-mac-connect](samba-images/mac-connect.png)
![samba-mac-unmount](samba-images/mac-unmount.png)

