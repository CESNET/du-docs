---
layout: article
title: Webinář - Úvod do Kubernetes
permalink: /docs/webinar1.html
key: webinar
aside:
  toc: true
sidebar:
  nav: docs
---
# Praktické ukázky

## Jupyterhub

TBD

## Binderhub

TBD

## Rancher

### Přihlášení

Přihlášení do webového rozhraní rancher je na adrese [https://rancher.cloud.e-infra.cz](https://rancher.cloud.e-infra.cz). Na úvodní obrazovce pokračujte kliknutím na `Log in with Shibboleth`.

![login1](webinar1/login1.png)

Následně zvolte `e-INFRA CZ AAI`

![login2](webinar1/login2.png)

Dále pak `e-INFRA CZ password`. Abyste nemuseli v dlouhém seznamu hledat, doporučujeme do políčka `Log in with` napsat `infra`. A následně vybrat `e-INFRA CZ password`.

![login3](webinar1/login3.png)

Zobrazí se výzva pro zadání jména a hesla do Metacentra. V případě, že nemáte účet v Metacentru, lze zvolit vaši domovskou instituci.

![login4](webinar1/login4.png)

Pro pokračování je třeba odsouhlasit předání údajů jako je např. vaše e-mailová adresa.

![login5](webinar1/login5.png)

### Dashboard

Po úspěšném přihlášení se zobrazí úvodní plocha. 

![dashboard](cluster.png)

Může se stát, že po přihlášení není viditelný žádný cluster, zejména `kuba-cluster`. V tomto případě počkejte cca 1 minutu a dejte obnovit stránku prohlížeče (Reload). Přebytečná okna jako `Getting Started` nebo `What do you want to see when you log in?` křížkem zavřít. 

Dále je třeba pokračovat kliknutím na `kuba-cluster`.

![dashboard1](cluster2.jpg)

Tím se dostáváte k ploše konkrétního clusteru, kde lze zobrazit přehledy, pouštět předpřipravené aplikace, atd.

![dashboard2](kuba-cluster.png)

---

## Aplikace

Následují ukázky spuštění předpřipravených aplikací jako jsou RStudio server a Matlab. Pro Matlab je nutné mít fungujícího `vnc` klienta, na Linuxu např. `vncviewer`, na Mac OS stačí *Safari* prohlížeč.

Na úvod upozornění, pro aplikace se zadávají požadavky na zdroje. Jak bylo zmíněno v prezentaci, je limit 20 CPU a 40GB Memory, zadání vyšších požadavků způsobí nespuštění aplikace.

### Rstudio

V předchozí sekci bylo ukázáno jak se dostat na hlavní plochu `kuba-cluster`. Pro úspěšný začátek spuštění je nutné začít na táto ploše.

![dashboard2](kuba-cluster.png)

#### Výběr Aplikace

Prvně je třeba se ujistit, že není zvolený žádný *Namespace* (viz šipka číslo 1). Jde o dočasnou chybu Rancheru, kdy při zvoleném *Namespace* neukazuje některé položky v Menu vlevo. Následně se pokračuje v navigaci přes `Apps & Marketplace` (šipka 2) a pak `Charts` (šipka 3). Dle šipky 4 je třeba vybrat pouze `cerit-sc`, jinak se nepřehledně ukazují i ostatní nerelevantní aplikace. A nakonec se vybere samotná aplikace `rstudio-server` (viz šipka 5, skutečná poloha ikony aplikace se liší, jak aplikace přibývají). 

![selectapp](rstudio/selectapp.png)

#### Instalace Aplikace

Pod `Chart Versions` lze vybrat verzi instalační šablony. Vybereme verzi 1.3. Tato verze nijak nesouvisí s verzí RStudio serveru. Následně pokračujeme `Install`.

![selectapp](rstudio/selectversion.png)

Nyní začínáme parametrizovat instalaci a spuštění aplikace. Ve většině případů necháme vybraný *Namespace* ve tvaru `příjmení-ns` (šipka 1). Rovněž jméno aplikace lze nechat výchozí (šipka 2).

![appinst](rstudio/appinst.png)


### Matlab

## Vlastní aplikace
