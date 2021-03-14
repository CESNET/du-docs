# Welcome to CERIT-SC documetation for Kubernetes and Rancher usage

CERIT-SC's Kubernetes clusters are available for use to all people eligible to login via ELIXIR, EGI or MetaCentrum. 
Everybody gets default project in one of the clusters but group projects can be set up as well. To setup group project, a PERUN group must exist (in Meta VO) with all intended members.

One can maipulate with cluster through command line or graphical user tool _Rancher_. Nevertheless, it is mandatory to log into _Rancher_ to obtain token for command line tool. 

## Rancher

_Rancher_ instance is available on [rancher.cerit-sc.cz](rancher.cerit-sc.cz). Please login via CESNET or ELIXIR (EGI is not approved yet).
After logging in, you shall see default dashboard. Right now, you do not have any default project but after 5 minutes, one will be assigned to you. Please refresh the page after such time. 

You can find assigned project in the upper left corner of the page under tab `Global` &rarr; `hdhu-cluster` &rarr; `Default project (your name)`

[image]

It is possible to work to certain extent only with Rancher or use command line tool `kubectl` (or both). We do not recommend `kubectl` for users inexperienced with working in terminal.

More about Rancher [here](rancher.md).

Added new section [this section](jupyterhub.md)

## Kubectl

`Kubectl` is a powerful tool for interacting with Kubernetes clusters. For installation, see [official documentation](https://kubernetes.io/docs/tasks/tools/#kubectl). A `kube config` file is required for `kubectl` to function. The file is located under tab `Global` &rarr; `hdhu-cluster` (click on the cluster name) in upper right corner.

[image]



Markdown is a lightweight and easy-to-use syntax for styling your writing. It includes conventions for

```markdown
Syntax highlighted code block

# Header 1
## Header 2
### Header 3

- Bulleted
- List

1. Numbered
2. List

**Bold** and _Italic_ and `Code` text

[Link](url) and ![Image](src)
```

For more details see [GitHub Flavored Markdown](https://guides.github.com/features/mastering-markdown/).

### Jekyll Themes

Your Pages site will use the layout and styles from the Jekyll theme you have selected in your [repository settings](https://github.com/CERIT-SC/kube-docs/settings). The name of this theme is saved in the Jekyll `_config.yml` configuration file.

### Support or Contact

Having trouble with Pages? Check out our [documentation](https://docs.github.com/categories/github-pages-basics/) or [contact support](https://support.github.com/contact) and we’ll help you sort it out.
