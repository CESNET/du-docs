---
layout: article
title: Running Nextflow Pipelines in Kubernetes
permalink: /docs/agentk.html
key: agentk
aside:
  toc: true
sidebar:
  nav: docs
---

## Prerequisites
- Namespace on your cluster
- Gitlab repository
- kubectl


## Define a configuration repository

In your desired repository, add the agent configuration file: `.gitlab/agents/<agent-name>/config.yaml`

Make sure that `<agent-name>` conforms to the [Agent’s naming format](https://gitlab.com/gitlab-org/cluster-integration/gitlab-agent/-/blob/master/doc/identity_and_auth.md#agent-identity-and-name).

```yaml
gitops:
    manifest_projects:
        - id: <Your Project ID>
          default_namespace: <Your Namespace>
          paths:
              - glob: '/manifest/*.{yaml,yml,json}'
```
**Note**: `<Your Project ID>` can be replaced by your project path.


## Connect to cluster

- Register agent and get his token.
  In your project go to: 
  Infrastructure -> Kubernetes clusters -> Actions -> Select an agent 
- Make a secret in your namespace named `gitlab-kubernetes-agent-token` with `key named token` and `value=<Your Agent Token>`
  
  Or by using kubectl: `kubectl create secret generic -n <Your Namespace> gitlab-kubernetes-agent-token --from-literal=token=<Your Token>`

- Create deployment file `resources.yaml`:
```yaml
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: gitlab-kubernetes-agent
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: gitlab-kubernetes-agent
spec:
  replicas: 1
  selector:
    matchLabels:
      app: gitlab-kubernetes-agent
  template:
    metadata:
      labels:
        app: gitlab-kubernetes-agent  
    spec:
      serviceAccountName: gitlab-kubernetes-agent
      containers:
      - name: agent
        image: "registry.gitlab.com/gitlab-org/cluster-integration/gitlab-agent/agentk:stable"
        args:
        - -n gitlab-kubernetes-agent
        - --token-file=/config/token
        - --kas-address
        - wss://gitlab.ics.muni.cz/-/kubernetes-agent/
        volumeMounts:
        - name: token-volume
          mountPath: /config
      volumes:
      - name: token-volume
        secret:
          secretName: gitlab-kubernetes-agent-token
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 0
      maxUnavailable: 1
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: gitlab-kubernetes-agent-role
rules:
- resources: ["configmaps", "secrets"]  #need of specification
  apiGroups: 
  - ""
  verbs: ["get", "list", "watch", "create", "update", "delete", "patch"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: gitlab-kubernetes-agent-role-binding
roleRef:
  name: gitlab-kubernetes-agent-role
  kind: Role
  apiGroup: rbac.authorization.k8s.io
subjects:
- name: gitlab-kubernetes-agent
  kind: ServiceAccount
---
```
- Apply the deployment with the following command:
`kubectl apply -n <Your Namespace> -f resoures.yaml`

- Check if the agent is running. Either in rancher or using kubectl `kubectl get pods -n <Your Namespace>`

## Manage deployments

- In your repository make manifest file: `/manifest/manifest.yaml`
 
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: test-map
  namespace: <Your Namespace>  # Can be any namespace managed by you that the agent has access to.
data:
  key: value
```
For the purpose of testing the agent we will make simple manifest file that will create ConfigMap in `<Your Namespace>`.
If everything went smoothly, you should have a ConfigMap named test-map.

***
