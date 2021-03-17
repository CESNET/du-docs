## Prepare tools
You will need `kubectl` installed on your machine, see [official documentation](https://kubernetes.io/docs/tasks/tools/#kubectl) and `config` file (see [main page](index.md)) for `hdha-cluster`. If you already have something in your `config`, you can only add new sections to existing file. See [adding multiple clusters to one config file](multiple.md)

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
                                                                                
4. Copy the id_rsa.pub to your `.ssh/authorized_keys` on storage-XXX.metacentrum.cz (according to where you have your data stored). E.g.
                                                                                
```                                                                             
cat sshfs-keys/id_rsa.pub | ssh {meta-username}@storage-brno3-cerit.metacentrum.cz -T "cat >> .ssh/authorized_keys"
```                                                                             
                                                                                

*Secondly*,  PersistentVolume + PersistentVolumeClaim have to be availbale to have your home mounted in hub. 

# TODO
how.
                                                                                

Now you can access notebook on `hub.cerit-sc.cz` where you can choose which notebook type you want to use. Sign in with your meta username (do not use @META, only username). In jupyterhub, your home is located in `/home/meta/{meta-username}`. 

## Feature requests
Any tips for features or new notebook types are welcomed in RT.

