---
layout: article
title: Alphafold
permalink: /docs/alphafold.html
key: alphafold
aside:
  toc: true
sidebar:
  nav: docs
---

We provide [Alphafold](https://www.deepmind.com/research/highlighted-research/alphafold) on demand service running on Kubernetes. Alphafold is available on [https://alphafold.cloud.e-infra.cz](https://alphafold.cloud.e-infra.cz), sign with e-INFRA CZ AAI or LifeScience AAI. 

Application is based on Jupyer notebook, therefore notebook loader is shown after login. *It may take few minutes before Alphafold is ready to run.*

## Alphafold Parameters

After successful login, you will see screen as shown below. You need to fill parameters for alphafold computation, at least Proteins (arrow 2) is required, everything else can be left default. See [here](https://github.com/deepmind/alphafold#running-alphafold) for additional parameters. Protein name (arrow 1) can be changed but must be unique (you cannot run several computations with the same name) or you will see the message: **A job with this name already exists, please specify a different name**.

By default, all computation results are public, it means, that everyone who is able to login can see them, but name of user that initiated the computation is not shown. If this is not desired, publication can be disabled (arrow 9). 

If you fill email (arrow 10), you will receive notification when computation is complete. 

Run (arrow 11) will start computation.

![hub](/docs/alphafold/1.png)

## Alphafold Running

If job has been submitted, it can be seen under `Running Jobs` tab. It can be `Pending`, `Running`, or `Succeeded`.

![rj](/docs/alphafold/1a.png)

![rj1](/docs/alphafold/6.png)

## Viewing Results

This application allows to preview computed results in tab `View Results`. You find your Protein name in selector (arrow 2), you can choose basic display parameters -- whether to show atoms or not (arrow 3). `View Result` (4) button shows result in browser. Viewer is interactive allowing rotation and moving. 

![vr](/docs/alphafold/2.png)

We also provide more complex viewer -- [Mol*](https://molstar.org/) clicking on the link `OPEN`. 

![vr1](/docs/alphafold/3.png)

Results can be downloaded on the bottom of this page hitting Generate download button and following `download zipfile` link.

![vr2](/docs/alphafold/5.png)
