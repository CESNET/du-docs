## Prepare tools
You will need `kubectl` installed on your machine, see [official documentation](https://kubernetes.io/docs/tasks/tools/#kubectl) and `config` file (see [main page](index.md)) for `hdha-cluster`. If you already have something in your `config`, you can add new sections to it. See [adding multiple clusters to one config file](multiple.md)

## Create Kuberentes resources 

*Firstly*, create a Secret. The secret contains private ssh key to your MetaCentrum home which needs to be generated and copied into your home.
There's a couple of steps you need to take:                                                                                                               
                                                                                
1. Generate ssh key using keygen on Linux, leave passphrase empty (press enter 2 times)
                                                                                
```                                                                             
mkdir -p sshfs-keys; ssh-keygen -t rsa -b 4096 -f sshfs-keys/id_rsa             
                                                                                
```                                                                             
                                                                                
2. Rename the id_rsa (needed for setup to work)                                 
```                                                                             
mv sshfs-keys/id_rsa sshfs-keys/ssh-privatekey                                  
```                                                                             
                                                                                
3. Create Kubernetes secret using kubectl, *change {meta-username} to yours!*     
                                                                                
```                                                                             
kubectl create secret generic {meta-username}-secret  --type=kubernetes.io/ssh-auth --from-file sshfs-keys/ssh-privatekey  -n jupyterhub-prod-ns
```                                                                             
                                                                                
4. Copy the `id_rsa.pub` to your `.ssh/authorized_keys` on storage-XXX.metacentrum.cz (according to where you have your data stored). 
Possible locations are:

brno10-ceitec-hsm | brno11-elixir | brno12-cerit | brno14-ceitec | vestec1-elixir
--- | --- | --- | --- |--- 
brno1-cerit | brno2 | brno3-cerit | brno6  | praha1
brno8 | brno9-ceitec | budejovice1 | du-cesnet | praha2-natur
liberec3-tul | ostrava1 | ostrava2-archive | pruhonice1-ibot | praha5-elixir
plzen1 | plzen4-ntis 

The command to run:

```                                                                             
cat sshfs-keys/id_rsa.pub | ssh {meta-username}@storage-brno3-cerit.metacentrum.cz -T "mkdir -p .ssh; cat >> .ssh/authorized_keys"
```                  
 
 
## Access notebook
You can access notebook on `hub.cerit-sc.cz`. Sign in with your meta username (do not use @META, only username). 

Any Jupyter image can be run, options already provided:
- jupyter/minimal-notebook
- jupyter/datascience-notebook
- jupyter/scipy-notebook
- jupyter/tensorflow-notebook

If you choose custom, you have to provide image name together with its repo and optional tag - input text in format _repo/imagename:tag_.
`minimal-notebook` is chosen as default image.

You can choose to mount any of your homes. It is possible to mount only one home to notebook at time. `brno3-cerit` is chosen as default storage.  In hub, your home is located in `/home/meta/{meta-username}`.

If you want to mount other home and you already have one notebook existing, you have to wait until it deletes. Culling is set to 5h so you have to wait.

## Error handling
Wrong form input results in _HTTP 500:Internal Server Error_ . The most common reasons:
- secret
  - doesn't exist at all/in wrong namespace 
  - is spelled badly (misspelled username) 
- custom image name
  - has incorrect format - slash or colon at the beginning or end
  - has more than one slash (exactly one has to exist to differentiate between repo and image name _repo/imagename_)
  - has more than one colon (zero on one are possible - to separate imagename and tag if provided)
  - generally has to be in form either *repo/imagename* or *repo/imagename:tag*

If you exeprience error while spawning, clicking on small arrow `Event log` provides more information. The most common:
- `TimeoutError("Server at http://10.42.3.77:8888/user/{username}/ didn't respond in 30 seconds")> after timeout` - specified image is too large and didn't get pulled in 10 minuts - contact us
- `output: "read: Connection reset by peer` - secret exists but you haven't copied `id_rsa.pub` to remote location. See point 4 in _Create Kuberentes resources_.
  - if you've certainly done this *before* spawning notebook, contact us
  - if you've done this only when error appeared, wait for a minute. If you experience red progress bar and , wait a minute and refresh the page. You will be presented with new form.
- `output: "{username}@storage-{storage}.metacentrum.cz:/home/{username}: Not a directory` - contact us



## Feature requests
Any tips for features or new notebook types are welcomed in RT.


