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

TBD: ljocha

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

Nyní začínáme parametrizovat instalaci a spuštění aplikace. Ve většině případů necháme vybraný *Namespace* ve tvaru `příjmení-ns` (šipka 1). Rovněž jméno aplikace lze nechat výchozí (šipka 2). Pokračujeme Next (šipka 3).

![appinst](rstudio/appinst.png)

Nyní se dostáváme k samotné parametrizaci aplikace. V první odrážce vybereme verzi R, pro vyzkoušení vybereme `R 4.0.5/Ubuntu 20.04` bez `Full` přípony. 

![appinst](rstudio/appform1.png)

V další záložce s názvem `Security` vyplníme heslo. Je vhodné se vyvarovat jednoduchých hesel a zároveň z technických důvodů je nutné nepoužívat znaky `{` a `}`. Zároveň je doporučeno zvolit heslo, které není běžně použité jinde. `Network policy` zůstane nezatrhnutá.

![appform1](rstudio/appform2.png)

V třetí záložce necháme pouze zatrženou volbu `Enable persistent home`. 

![appinst](rstudio/appform3.png)

Poslední záložku se zdroji necháme pro demo s předvyplněnými hodnotami. A pokračujeme volbou Install. 

![appform2](rstudio/appform4.png)

Zobrazí se následující překryv, kde je nutné počkat na oznámení `SUCCESS`. Tímto se aplikace nainstalovala a je připravena k použití.

![apphelm](rstudio/apphelm.png)

#### Přihlášení do běžící instance

Předchozí výpis s instalací končící oznámením `SUCCESS` zavřeme křížkem a projdeme přes menu vlevo `Service Discovery` (šipka 1) do `Ingresses` (šipka 2). Pokud uvidíme řádek s názvem `cm-acme-http-solver...` (šipka 3), je třeba chvíli vyčkat dokud nezmizí (v tomto momentě se získává SSL certifikát). Následně se pokračuje kliknutím na odkaz u šipky 4. Každý uživatel má vlastní podobu odkazu. Obsahuje zvolené jméno (typicky `rstudio`) a zvolený *Namespace*. 

![appacme](rstudio/appacme.png)

Pokud vše šlo dobře, po kliknutí na zmíněný odkaz se zobrazí přihlašovací obrazovka. Zde se vyplní jméno **`rstudio`** (to je fixně přednastavené) a heslo, které bylo zadáno do formuláře při parametrizaci (to, co nemělo obsahovat znaky `{` a `}`).

![applogin](rstudio/applogin.png)

#### Použití aplikace

Po spuštění lze aplikaci začít používat např. jednoduchým `print` příkazem nebo `barplot` příkazem (červené upozornění nemá na demo vliv, při použití `Full` verze R by se nemělo zobrazit). 

![appuse](rstudio/rstudio-w2.png)

#### Smazání aplikace

Pokud aplikace již není potřeba, je vhodné ji smazat. Ze základní plochy Rancheru se pokračuje do `App & Marketplace` (šipka 1) přes `Installed Apps` (šipka 2), vybereme aplikaci (šipka 3) a následně přes `Delete` (šipka 4) smažeme. 

![appdel](rstudio/appdel.png)

---

### Matlab

Další ukázkovou aplikací je Matlab. Doporučujeme před zkoušením Matlabu smazat předchozí aplikaci - RStudio dle posledního bodu postupu. Stejně jako u RStudia začneme na úvodní ploše. Návrat na ni lze provést Kliknutím vlevo nahoře na symbol menu `≡` a následně na `kuba-cluster`.

![dashboard3](cluster1.jpg)

#### Výběr Aplikace

Následně vybereme aplikaci stejným postupem. Prvně je třeba se ujistit, že není zvolený žádný *Namespace* (viz šipka číslo 1). Jde o dočasnou chybu Rancheru, kdy při zvoleném *Namespace* neukazuje některé položky v Menu vlevo. Následně se pokračuje v navigaci přes `Apps & Marketplace` (šipka 2) a pak `Charts` (šipka 3). Dle šipky 4 je třeba vybrat pouze `cerit-sc`, jinak se nepřehledně ukazují i ostatní nerelevantní aplikace. A nakonec se vybere samotná aplikace `Matlab` (viz šipka 5, skutečná poloha ikony aplikace se liší, jak aplikace přibývají).

![selectapp](matlab/selectapp.png)

#### Instalace Aplikace

Pod `Chart Versions` lze vybrat verzi instalační šablony. Vybereme verzi 9.11. V tomto případě verze šablony přesně odpovídá i verzi aplikace. Následně pokračujeme `Install`.

![selectapp](matlab/selectversion.png)

Nyní začínáme parametrizovat instalaci a spuštění aplikace. Ve většině případů necháme vybraný *Namespace* ve tvaru `příjmení-ns` (šipka 1). Rovněž jméno aplikace lze nechat výchozí (šipka 2). Dále zatrhneme `Customize Helm options before install` (šipka 3). Pokračujeme Next (šipka 4).

![appinst](matlab/appinst.png)

Nyní se dostáváme k samotné parametrizaci aplikace. V první odrážce necháme vybranou VNC verzi. 

![appform1](matlab/appform1.png)

V další záložce s názvem `Password Settings` vyplníme heslo. Je vhodné se vyvarovat jednoduchých hesel a zároveň z technických důvodů je nutné nepoužívat znaky `{` a `}`. Zároveň je doporučeno zvolit heslo, které není běžně použité jinde.

![appform2](matlab/appform2.png)

V třetí záložce necháme pouze zatrženou volbu `Enable persistent home`. Tj. nebude zatrženo a vybráno PVC ani External storage.

![appform3](matlab/appform3.png)

Poslední záložku se zdroji necháme pro demo s předvyplněnými hodnotami. A pokračujeme volbou `Next`. 

![appform4](matlab/appform4.png)

Objeví se poslední část formuláře, kam je potřeba vyplnit `Timeout` na hodnotu 1200 (Matlab je velký kontejner a může trvat, než se stáhne). A následně již dáme `Install`.

![appform5](matlab/appform5.png)

Zobrazí se následující překryv, kde je nutné počkat na oznámení `SUCCESS`. Tímto se aplikace nainstalovala, ale na rozdíl od RStudia ještě není připravena k použití.

![apphelm](matlab/apphelm.png)

## Vlastní aplikace
