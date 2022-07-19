---
layout: article
title: BinderHub
permalink: /docs/binderhub.html
key: binderhub
aside:
  toc: true
sidebar:
  nav: docs
---
# BinderHub

BinderHub is a Binder instance working on Kubernetes located on [binderhub.cloud.e-infra.cz](https://binderhub.cloud.e-infra.cz/). Binder turns a Git repo into collection of interactive notebooks. It is enough to fill the git repository name (optionally specific notebook or branch) and binderhub will turn it into a web notebook. 

## Authentication
To use CERIT-SC BinderHub instance, you have to authenticate. Authentication is performed via unified login. 

## Persistence
After the notebook is spawned, a persistent volume is mounted to path `/home/{username}-nfs-pvc`. The same persistent volume is mounted to mentioned path in each notebook you spawned. Therefore, if you want to use data generated in BinderHub instance *A* in instance of BinderHub *B*, you can write the data to path `/home/{username}-nfs-pvc` and they will be available for use. 

Note: Pay attention to paths used in notebooks. Imagine you have two BinderHub running. In both, you write outputs to location `/home/{username}-nfs-pvc/test`. If both notebooks create file named `result.txt`, you would be overwriting the file. It is a good practice to create new directory in path `/home/{username}-nfs-pvc` for each BinderHub instance. 

## Resources
Each user on your JupyterHub can use certain amount of memory and CPU. You are guaranteed **1G of RAM** and **1 CPU** and you can utilize up to **16G of RAM** and **8 CPU**. Resource limits represent a hard limit on the resources available. 

### Custom resources
If you need to specify other resource amounts or attach GPU, you can create a *.resources* file in the root of git repository. The file can look like:
```
# This file is for resource requests in CERIT-SC
# Do not change
gpu=1
cpur=2
cpul=4
memr=1
meml=4  
```

Lines starting with `#` are ignored (useful for commens); other stand for:
- `gpu=[number_of_gpu_request]`
- `cpur=[number_of_cpu_request]`
- `cpul=[number_of_cpu_limit]`
- `memr=[GB_of_RAM_request]`
- `meml=[GB_of_RAM_limit]`

RAM is assigned in *GB*, do not specify any units. By default, no GPU is assigned. If the *.resources* file does not contain any of the lines, defaults are used. Similarly, if the file specifies only some lines, the defaults for the missing lines are used.

The setting currently works for repositories hosted on `github.com`. If you use another git service (gitlab, zenodo, ...), please contact us at <a href="mailto:k8s@ics.muni.cz">IT Service desk</a>.


## SSH key inside the instance
To ensure more flexibility, we generate SSH keypair for everyohe who spawns at least one Jupyter notebook via BinderHub. This SSH keypair is mounted to notebook instance (`/home/jovyan/.ssh/ssh.priv` and `/home/jovyan/.ssh/ssh.pub`) and can be used e.g. to import public key to GitHub account. That way you can update and work with your Git repositories directly from notebook.

Same SSH keypair is mounted to all your BinderHub notebooks.

## Where to find running notebooks
Your running notebooks can be found at `https://bhub.cloud.e-infra.cz/`. Clicking on address redirects you to the notebook instance. Because redirection links include random strings it is advised to work in one browser where cookies can be stored and you don;t have to remember long notebook addresses. Also, avoid incognito windows because the session cookie won't save and when you close the tab, you will not find the instance in control panel. 

## Limits
Currently, every user is limited to spawn 5 projects. If you reach quota but you want to deploy new instance, an error will appear under loading bar of BinderHub index page.

![projects_limit](binderhub-images/limit.png)

To spawn new instance, you have to delete one of your running instances.  This can be done in JupyterHub control panel (JupyterHub is used underneath BinderHub). Navigate to `https://bhub.cloud.e-infra.cz/` and stop any instance you don't need. When red button `delete` appears, click on that one as well. After that, it should be possible to spawn new instance at [binderhub.cloud.e-infra.cz](https://binderhub.cloud.e-infra.cz/).

![projects_panel](binderhub-images/hubpanel.png)

![projects_stop](binderhub-images/stop.png)

![projects_delete](binderhub-images/delete.png)

❗️<ins>Notebooks are deleted automatically after one week of inactivity (inactivity = idle kernel or no connection to notebook).</ins>❗️

## Customizations
### Custom Dockerfile
The hub spawns notebook instances with default image not conatining any special libraries. However, you can create custom `Dockerfile` with all dependencies and it will be used as base image. The `Dockerfile` must be located in the repository you are going to launch in Binder. 

When creating the `Dockerfile` bear in mind it has to be runnable under *user*. Furthermore, it is important to `chown` all used directories to user, e.g. :
```
RUN chown -R 1000:1000 /work /home/jovyan
```

### Install Various Libraries and Software
Creating custom Dockerfile might be an overkill for your needs so there are several other ways of installing e.g. `conda` environment, `Python` packages or some `Debian` packages (e.g. vim). 

See [all possible file types](https://repo2docker.readthedocs.io/en/latest/config_files.html) with complete description and intended usage that can be included in repository. These files are resolved at startup. You can include multiple files in repo so if you need to install `Python` packages as well as a couple of `Debian` packages, both `apt.txt` and `requirements.txt` can be present.

Brief list of files:
- `environment.yml` - conda env, [example](https://github.com/binder-examples/python-conda_pip/tree/3b7126f39253f92bb13ce7ea155fd8a121082afe)
- `Pipfile` - Python env, [example](https://github.com/binder-examples/pipfile)
- `setup.py` - Python packages, [example](https://github.com/binder-examples/setup.py)
- `requirements.txt` - Python packages, [example](https://github.com/binder-examples/requirements)
- `Project.toml` - Julia env, [example](https://github.com/binder-examples/demo-julia)
- `apt.txt` - Debian packages, [example](https://github.com/binder-examples/apt_install)
- `install.R` - R packages, [example](https://github.com/binder-examples/r)

See [binder examples repository](https://github.com/orgs/binder-examples/repositories?page=1&type=all) for plenty types of repositories, file combinations and interesting usages.

## Unknown Error While Spawning
If you experience any unknown error while spawning notebook (or your notebook is not spawned at all), please email <a href="mailto:k8s@ics.muni.cz">IT Service desk</a>.





