---
layout: article
title: Running Virtual Machine
permalink: /docs/vm.html
key: vm
aside:
  toc: true
sidebar:
  nav: docs
---
## Prerequisites

1. Visited [https://rancher.cloud.e-infra.cz](https://rancher.cloud.e-infra.cz) and remember your [namespace](/docs/quotas.html).
2. Configured `kubectl` tool, see [kubectl](/docs/kubectl.html) section.
3. Computer with installed `ssh` command.

## Running Simple Virtual Machine

Running true virtual machine is of course not possible in containerized infrastructure. However following steps show how to run something very close to a virtual machine.

Running VM consists of several steps:

1. Generate [ssh key](https://www.ssh.com/academy/ssh/key)
2. Create a `secret` with public ssh key. 
3. Choose ssh compatible docker image
4. Create and run manifest

### SSH Keys

In the following, prefer RSA key type for maximum compatibility.

#### Generate SSH key -- Linux/MacOS

Ssh keys are usually located in home directory in `.ssh` sub directory and named like `id_rsa.pub`. If there is no such directory of files, you can generate new keys using `ssh-keygen` command that generates secret and public key. Names of the files are print out during key generation, e.g.:
```
$ ssh-keygen 
Generating public/private rsa key pair.
Enter file in which to save the key (/home/user/.ssh/id_rsa): 
Enter passphrase (empty for no passphrase): 
Enter same passphrase again: 
Your identification has been saved in /home/user/.ssh/id_rsa.
Your public key has been saved in /home/user/.ssh/id_rsa.pub.
```
In this case, `id_rsa` is a private key (keep it secretly and never send), `id_rsa.pub` is a public key. Passphrase is not required but recommended.

#### Generate SSH key -- Microsoft Windows

In this case, follow [guide here](https://www.puttygen.com/).

#### Create Secret

For this step, the `kubectl` needs to be installed and configured. Create the secret issuing:
```
kubectl create secret generic ssh-publickey --from-file=ssh-publickey=~/.ssh/id_rsa.pub -n [namespace]
```
Replace `[namespace]` with name of your *namespace* from Rancher. If you generated or are using different key type than *RSA*, replace `id_rsa.pub` with correct public key location.

### Docker Image

We created 4 base images for public use:
1. `cerit.io/pub/ssh-base:d10` -- Debian 10 (Buster) based image
2. `cerit.io/pub/ssh-base:d11` -- Debian 11 (Bullseye) based image
3. `cerit.io/pub/ssh-base:ubuntu20.04` -- Ubuntu 20.04 (Focal) based image
4. `cerit.io/pub/ssh-base:ubuntu22.04` -- Ubuntu 22.04 (Jellyfish) based image

These images can be directly used or can be used as base images for creating own more advanced images, see below.

### Manifest

[Download](/docs/deployments/vm-simple.yaml) manifest. Edit line 6:
```yaml
annotations:
  external-dns.alpha.kubernetes.io/hostname: vm-[namespace].dyn.cloud.e-infra.cz
```
and replace `[namespace]` with your *namespace*. This *namespace* must be the same as the *namespace* used for the secret.

If desired, replace `image` name on line 34:
```yaml
image: cerit.io/pub/ssh-base:d10
```
with any other image mentioned above like `cerit.io/pub/ssh-base:ubuntu22.04`. Save the file and run the manifest:
```
kubectl create -f vm-simple.yaml -n [namespace]
```
We suppose that the downloaded and edited file has name `vm-simple.yaml`. Replace again `[namespace]` with your *namespace* from Rancher. This command run the manifest. You can check `Workload` -> `Pods` in Rancher to see your manifest is running:
![vm-ssh-simple](/docs/vm/vm-ssh.png)

### Logging In

If manifest is running, you can log in using ssh command:
```
ssh user@vm-[namespace].dyn.cloud.e-infra.cz
```
Again, replace `[namespace]` with your *namespace* from Rancher and you should see something like this:
```
anubis: ~ $ ssh user@vm-hejtmanek1-ns.dyn.cloud.e-infra.cz
Warning: Permanently added 'vm-hejtmanek1-ns.dyn.cloud.e-infra.cz' (ED25519) to the list of known hosts.
X11 forwarding request failed on channel 0

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
user@vm-example-0:~$ 
```

At this point, you have running your VM for general purpose.

## Delete Running VM

If you VM is not needed any more, we kindly request to delete it. It can be deleted issuing:
```
kubectl delete -f vm-simple.yaml -n [namespace]
```
Where `vm-simple.yaml` is the file used for create and `[namespace]` is your *namespace* from Rancher.

## Installing Additional Software

There are two options, how to install additional packages to the VM. You can either rebuild the docker image or you can use existing one, install `conda` package manager for further package installation. Using docker, you can install all standard packages from the base system, i.e., Debian or Ubuntu, these packages will be part of the new image and will be always (even after container restart) available. 

**Note**: You cannot install any system package in the running container.

However, using `conda`, installation of `conda` packages is possible even in running container. See caveats below.

### Rebuilding Image

If you are not familiar with docker build. Check our [documentation](/docs/dockerfile.html). For docker image, docker registry is needed. You can use our [https://hub.cerit.io](https://hub.cerit.io) registry, that can store your docker image. Images can be referred as: `cerit.io/[project]/[image]:[tag]`. TBD: hub docs

To rebuild one of the images above, use the following `Dockerfile` example:
```
FROM cerit.io/pub/ssh-base:d10

RUN apt-get update && apt-get -t install vim less && apt-get clean && rm -rf /var/lib/apt/lists/
```

This `Dockerfile` creates new version of the docker image with installed `vim` and `less` packages. Store the example into the file `Dockerfile`, change the list of installed packages as desired. You can build the docker image using:
```
docker build -t cerit.io/[login]/[image]:[tag] - < Dockerfile
```
Replace `[login]` with our *project* name in `hub.cerit.io`, `[image]:[tag]` with image name and tag.

To store the image into registry, you need to login to the registry first using:
```
docker login cerit.io
```
with credentials you can get on [https://hub.cerit.io](https://hub.cerit.io).

After login, you can *push* your new image using:
```
docker push cerit.io/[login]/[image]:[tag]
```

Replace `image` in the manifest above with this new name `cerit.io/[login]/[image]:[tag]` and delete and run the manifest again.

### Conda Package Manager

Using [conda](https://docs.conda.io/en/latest/) or `mamba` tool, you can install new packages even in the running container. First, installing `conda/mamba`:
```
wget https://github.com/conda-forge/miniforge/releases/latest/download/Mambaforge-Linux-x86_64.sh
/bin/bash Mambaforge-Linux-x86_64.sh -f -b -p /home/user/conda
/home/user/conda/bin/conda init
echo '. ~/.bashrc' >> ~/.profile
```

Log out and log in again. You should see now prompt like this:
```
(base) user@vm-example-0:~$
```

You are now ready to install packages, e.g., `mc` package:
```
(base) user@vm-example-0:~$ mamba install mc
```

After a while, `mamba` finishes and you are able to use the installed package `mc`.

All packages are installed into the `/home/user/conda` directory.

### Persistent Home

As mentioned above, disks inside container are not persistent. It means that everything that is installed by `conda`/`mamba` is lost if the container is restarted or re-created. To deal with this, persistent home needs to be created. 
