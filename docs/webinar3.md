---
layout: article
title: Sitola - Úvod do Kubernetes - 2
permalink: /docs/webinar3.html
key: webinar
aside:
  toc: true
---
## Rancher

### Přihlášení

Přihlášení do webového rozhraní rancher je na adrese [https://rancher.cloud.e-infra.cz](https://rancher.cloud.e-infra.cz). 

## Aplikace

Následuje ukázka spuštění předpřipravených aplikací jako je RStudio server.

Na úvod upozornění, pro aplikace se zadávají požadavky na zdroje. Jak bylo zmíněno v prezentaci, je limit 20 CPU a 40GB Memory, zadání vyšších požadavků způsobí nespuštění aplikace.

### Rstudio

V předchozí sekci bylo ukázáno jak se dostat na hlavní plochu `kuba-cluster`. Pro úspěšný začátek spuštění je nutné začít na táto ploše.

#### Výběr Aplikace

Následně se pokračuje v navigaci přes `Apps & Marketplace` a pak `Charts`. Je třeba vybrat pouze `cerit-sc`, jinak se nepřehledně ukazují i ostatní nerelevantní aplikace. A nakonec se vybere samotná aplikace `rstudio-server`.

#### Instalace Aplikace

Pod `Chart Versions` lze vybrat verzi instalační šablony. Vybereme verzi 1.3. Tato verze nijak nesouvisí s verzí RStudio serveru. Následně pokračujeme `Install`.

Nyní začínáme parametrizovat instalaci a spuštění aplikace. Ve většině případů necháme vybraný *Namespace* ve tvaru `příjmení-ns`. Rovněž jméno aplikace lze nechat výchozí. Pokračujeme Next.

Nyní se dostáváme k samotné parametrizaci aplikace. V první odrážce vybereme verzi R, pro vyzkoušení vybereme `R 4.0.5/Ubuntu 20.04` bez `Full` přípony. 

V další záložce s názvem `Security` vyplníme heslo. Je vhodné se vyvarovat jednoduchých hesel a zároveň z technických důvodů je nutné nepoužívat znaky `{` a `}`. Zároveň je doporučeno zvolit heslo, které není běžně použité jinde. `Network policy` zůstane nezatrhnutá.

V třetí záložce necháme pouze zatrženou volbu `Enable persistent home`. 

Poslední záložku se zdroji necháme pro demo s předvyplněnými hodnotami. A pokračujeme volbou Install. 

Zobrazí se překryv, kde je nutné počkat na oznámení `SUCCESS`. Tímto se aplikace nainstalovala a je připravena k použití. Předchozí výpis s instalací zavřeme křížkem.

#### Přihlášení do běžící instance

Projdeme přes menu vlevo `Service Discovery` do `Ingresses`. Pokud uvidíme řádek s názvem `cm-acme-http-solver...`, je třeba chvíli vyčkat dokud nezmizí (v tomto momentě se získává SSL certifikát). Následně se pokračuje kliknutím na modrý odkaz. Každý uživatel má vlastní podobu odkazu. Obsahuje zvolené jméno (typicky `rstudio`) a zvolený *Namespace*.

### S3/Web úložiště

Opět přes `Apps & Marketplace` a pak `Charts` vybereme aplikaci `minio`.

#### Instalace Apliace

Tato aplikace má jedinou verzi, takže pokačujeme na `Install`. Necháme vybraný *Namespace* ve tvaru `příjmení-ns`. Rovněž jméno aplikace lze nechat výchozí. Pokračujeme Next.

V další záložce s názvem `Authentication` můžeme nechat vyplněné `user`, ale rozhodně zvolíme `password`. Pozor, heslo musí mít alespoň 8 znaků.

V třetí záložce vybereme `PVC`, mělo by být k dispozici právě jedno a to `home-rstudio-0`. A pokračujeme volbou Install.

Zobrazí se překryv, kde je nutné počkat na oznámení `SUCCESS`. Tímto se aplikace nainstalovala a je připravena k použití. Předchozí výpis s instalací zavřeme křížkem.

#### Přihlášení do běžící instance

Projdeme přes menu vlevo `Service Discovery` do `Ingresses`. Pokud uvidíme řádek s názvem `cm-acme-http-solver...`, je třeba chvíli vyčkat dokud nezmizí (v tomto momentě se získává SSL certifikát). Následně se pokračuje kliknutím na modrý odkaz v němž je `minio` (a nikoli `s3`). 

### Práce s daty

Stáhneme vzorový příklad [sla.csv](http://botanika.prf.jcu.cz/fibich/bash/sla.csv). V `minio` webu klikneme na `Buckets` a následně `Root`. Vpravo nahoře je ikona upload, pomocí ní nahrajeme stažený `sla.csv`. 

Přepneme se do R studio. V něm vložíme postupně následující kód:

```
sla<-read.csv("sla.csv")
slaspe<-table(sla$species))
boxplot(LEAFAREA_mm2~species,data=sla[sla$species %in% names(slaspe[slaspe>6]), ])
write.table(slaspe, file = "sla1.tab")
```

Hláška o chybějící knihovně je neškodná.

Přepneme se znova do `minia`, po chvilce a kliknutím na `refresh` vpravo nahoře by měl být vidět soubor `sla1.tab`. Kliknutí na něj a následně ikonu `Download` lze soubor stáhnout.

### Windows úložiště

Opět přes `Apps & Marketplace` a pak `Charts` vybereme aplikaci `samba`.

#### Instalace Apliace

Tato aplikace má jedinou verzi, takže pokačujeme na `Install`. Necháme vybraný *Namespace* ve tvaru `příjmení-ns`. Rovněž jméno aplikace lze nechat výchozí. Pokračujeme Next.

V další záložce s názvem `Server Settings` zvolíme `password` a dále vybereme PVC, mělo by být k dispozici právě jedno a to `home-rstudio-0`. A pokračujeme volbou Install.

Zobrazí se překryv, kde je nutné počkat na oznámení `SUCCESS`. Tímto se aplikace nainstalovala a je připravena k použití. Předchozí výpis s instalací zavřeme křížkem.

#### Práce s daty

Připojíme windows síťový disk `\\[namespace]-samba.dyn.cloud.e-infra.cz\data`. Přihlašovací jméno je `user`. Heslo je zvolené heslo. 


#### Smazání aplikace

Pokud aplikace již není potřeba, je vhodné ji smazat. Ze základní plochy Rancheru se pokračuje do `App & Marketplace` přes `Installed Apps`, vybereme aplikaci a následně přes `Delete`  smažeme. 


## Docker

Je potřeba aplikace smazat, jinak nebude možné pustit tuto další. 

Pro docker build je možné použít stroj `zefron5.cerit-sc.cz` s přihlašovacím jménem `sitola`.

Do souboru s názvem `Dockerfile` dáme následující obsah nebo si jej [stáhneme](webinar3/Dockerfile)
```
FROM nvcr.io/nvidia/tensorflow:22.02-tf2-py3

ENV DEBIAN_FRONTEND=noninteractive 
ENV TZ=Europe/Prague

RUN apt update && apt install -y python3-notebook python3-pip wget 

RUN pip3 install jupyterhub

WORKDIR /home/jovyan
ENV HOME /home/jovyan

RUN wget https://raw.githubusercontent.com/ljocha/binder-demo2/main/img-classifier.ipynb -O /home/jovyan/img-classifier.ipynb

RUN useradd -m -u 1000 jovyan
RUN chown -R 1000:1000 /home/jovyan

CMD jupyter notebook --NotebookApp.token='' --NotebookApp.password=''
```

pomocí dockeru jej sestavíme a to buď na `zefron5.cerit-sc.cz` nebo na vlastním stroji s dockerem.

V případě vlastního stroje je nutné začít příkazem:
```docker login cerit.io```

jméno je `sitola`

následně již

```docker build -t cerit.io/sitola-prijmeni - < Dockerfile```

Po úspěšném buildu:

```docker push cerit.io/sitola-prijmeni:latest```

Tímto končí dockerová část.

## Aplikace

Zde je potřeba mít stažený a funkční program `kubectl` a jeho konfiguraci `kube-config`. 

Následně [stáhneme](webinar3/pod.yaml) manifest na běžící aplikaci.

V ní vyměníme všechny výskyty `[prijmeni]` za své vlastní příjmení (bez diakritiky malými písmeny, celkem 4x)

Uložíme a pomocí 

```kubectl create -f pod.yaml -n prijmeni-ns``` spustíme aplikaci.

Vrátíme se do `rancheru`. Pod `Workload` -> `Pods` bychom měli vidět aplikaci `sitola`, která běží.

`Service Discovery` -> `Ingresses` bude k dispozici odkas `https://sitola`. 

Klikneme na něj a následně na `img-classifier.ipynb`. Tím jsme v jupyter aplikaci. 

```kubectl delete -f pod.yaml -n prijmeni-ns``` smaže aplikaci.
