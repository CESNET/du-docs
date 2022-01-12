---
layout: article
title: GitLab Kubernetes Agent
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
  Infrastructure -> Kubernetes clusters -> Install a new agent -> Select an agent -> Register
  
- Make an opaque secret in your namespace named `gitlab-kubernetes-agent-token` with `key named token`, `value=<Your Agent Token>`
  
  Or by kubectl: `kubectl create secret generic -n <Your Namespace> gitlab-kubernetes-agent-token --from-literal=token=<Your Token>`

- Download deployment file [resources.yaml](deployments/resources.yaml).
  
  In the file, in this section:
  
  ```
  apiVersion: rbac.authorization.k8s.io/v1
  kind: Role
  metadata:
    name: gitlab-kubernetes-agent-role
  rules:
  - resources: ["configmaps", "secrets", "pods"]
    apiGroups: 
    - ""
    verbs: ["get", "list", "watch", "create", "update", "delete", "patch"]
  ```
  
  You need to specify the resources to your choosing. 
  You can list all resources you have permission to by this command `kubectl api-resources --verbs=list -n <Your Namespace>`

- Apply the deployment with the following command:
`kubectl apply -n <Your Namespace> -f resources.yaml`

- Check if the agent is running. Either in rancher or using kubectl `kubectl get pods -n <Your Namespace>`

## Manage deployments

- In your repository make manifest file: `/manifest/manifest.yaml`
 
 
For the purpose of testing the agent, we will make simple manifest file that will create ConfigMap in `<Your Namespace>`.

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: test-map
  namespace: <Your Namespace>  # Can be any namespace managed by you that the agent has access to.
data:
  key: value
```

If everything went smoothly, you should have a ConfigMap named test-map.

***
