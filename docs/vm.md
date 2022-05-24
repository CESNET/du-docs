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
1. `cerit.io/pub/ssh-base:d10`
2. `cerit.io/pub/ssh-base:d11`
3. `cerit.io/pub/ssh-base:ubuntu20.04`
4. `cerit.io/pub/ssh-base:ubuntu22.04`

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
