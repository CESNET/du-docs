---
layout: article
title: Dockerfile
permalink: /docs/dockerfile.html
key: desktop
aside:
  toc: true
sidebar:
  nav: docs
---
## Docker Image

Docker image is essential component of container infrastructure. It is an image that contains an application and all its required parts (libraries and other files). 

Docker image is created usually using a `Dockerfile`. The `Dockerfile` contains commands that builds the image, environment variables, command to run when starting the container, entrypoint and many other items.

Docker images are named using the following schema: `registry/name:tag`. If `registry` is omitted, docker hub registry is used. Example of docker image name is: `cerit.io/xserver:v1.0`. 

Before building own docker image, it is strongly recommended to search public registry for an existing image that contains desired application, but also check what is the time stamp of last image, i.e., if someone makes new releases and bug fixes. We can recommend, e.g., `bitnami` images. There some limitation of using external docker images on our infrastructure, see [limitations](/docs/limitations.html).

## Create Own Docker Image

If you find it necessary to create own image, you find below a brief guide. For full guide see [official docker documentation](https://docs.docker.com/develop/).

Here you find most common Dockerfile commands:

1. `FROM image` -- defines image name you start your docker image from, e.g. `ubuntu`.
2. `RUN cmd` -- run command that modifies the starting image, more than one `RUN` command can be used.
3. `COPY localfile containerfile` -- copy local files into docker image, you can use optional `--chown=user:group` to change ownership during copy. Copy and changing ownership later using `RUN chown` is discouraged as resulting image is twice as big.
4. `USER uid` -- switch user to `uid` (or name), from this line, all other commands will run under identity of specified user, if this command was not used, everything is done as `root` user. The last `USER uid` directive also specifies as which user the container will run by default.
5. `CMD command` -- run `command` as default command when starting the container.

```dockerfile
FROM debian:buster
RUN apt update -y && apt upgrade -y && apt install build-essential libssh-dev git -y
RUN git clone https://gitlab.con/zvon/iobench && cd iobench && make && make install
USER 1000
CMD /bin/bash -c "tail -f /dev/null"
```

## Dockerfile Tips
