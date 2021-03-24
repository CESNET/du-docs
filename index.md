# Welcome to CERIT-SC documetation for Kubernetes and Rancher usage

CERIT-SC's Kubernetes clusters are available for use to all people eligible to login via ELIXIR, EGI or MetaCentrum. 
Everybody has default project in one of the clusters but group projects for team collaboration can be set up as well. To create group project, a _PERUN_ group must exist (in Meta VO) with all intended members.

One can manipulate with cluster through command line tool `kubectl` or graphical user tool _Rancher_. Nevertheless, it is mandatory to log into _Rancher_ to obtain token for command line tool. 

## Rancher

_Rancher_ instance is available on [rancher.cerit-sc.cz](rancher.cerit-sc.cz). Please login via CESNET or ELIXIR (EGI is not approved yet).
After logging in, you shall see default dashboard. Right now, you do not have any default project but after 5 minutes, one will be assigned to you. Please refresh the page after such time. 

You can find assigned project in the upper left corner of the page under tab `Global` &rarr; `hdhu-cluster` &rarr; `Default project (your name)`

![default project](https://github.com/CERIT-SC/kube-docs/blob/gh-pages/default.png?raw=true)

It is possible to work to certain extent only with Rancher. However, command line tool `kubectl` allows more actions. You can utilize both ways but we do not recommend `kubectl` for users inexperienced with working in terminal.

More about working with Rancher [here](rancher.md).


## Kubectl

`Kubectl` is a powerful tool for interacting with Kubernetes clusters. For installation, see [official documentation](https://kubernetes.io/docs/tasks/tools/#kubectl). After installation, a `kube config` file is required to function. The file is located under tab `Global` &rarr; `hdhu-cluster` (click on the cluster name) in upper right corner.

![kube config](https://github.com/CERIT-SC/kube-docs/blob/gh-pages/config.png?raw=true)

Copy contents of this file into `$HOME/.kube/config` and change permissions to 700 (`chmod 700 $HOME/.kube/config`). 

It is possible to have multiple cluster configurations in one config file. More about working with `kubectl` with access to multiple clusters [here](multiple.md).

## Applications available for users

There are applications currently available for users that run solely in Kubernetes clusters. They are maintained either by CERIT-SC or individuals under Institute of Computer Science. 

Applications for users:

- [JupyterHub](jupyterhub.md)
- [Galaxy](galaxy.md)
- [MagicForceField](mff.md)
- [Tes/WES](teswes.md)

## Operational applications running in Kuberentes 

There are some applications that are not directly used by users but function in containers and are managed in Kubernetes. Numerous applications can be turned into containers and microservices. You can be inspired by some of ours, but presently we run:

- whole proxy (the one used for logging into Rancher) 

## Examples and hands-ons

We provide a short tutorial on how to deploy a sample hello-world web to acknowledge yourself with working in clusters.

[Hello-world tutorial](helloworld-cmd.md)

[How to expose applications](expose.md)

## Further information

If you need support or advice on whether (and how) you can use Kubernetes and containers for your use case, contact us in RT. 

