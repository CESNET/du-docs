---
layout: article
title: Nbgrader New Tutorial
permalink: /docs/nbgrader-new-interaction.html
key: nbgrader-auth-student
aside:
  toc: true
sidebar:
  nav: docs
---

# URL Adresy

Produkcia: jupytul.cloud.e-infra.cz

Váš pôvodný testovací: avi-sem.cloud.e=infra.cz 

> [!IMPORTANT]
> Pôvodný testovací sa BUDE RUŠIŤ 20.9.2024 !!!


# Prihlasovanie

Prihlasovanie je zabezpečené cez jednotné prihlásenie. Inštruktori aj študenti musia patriť do správnych skupín.

Zatiaľ nie je potrebná registrácia do Meta, toto sa ale bude riešiť a bude potrebné. Pravdepodobne sa bude jednať o presun nejakých resourcov v Perune - neviem zatiaľ, ako veľmi vás to ovplyvní, ale budete to musieť mať všetci (inštruktori, študenti). 

## Študent

Študent si po prihlásení vyberie kurz s ktorým chce pracovať, či chce premazať home a klikne na start. Po spustení notebooku uvidí túto stránku. Väčšinou neni vidieť kurzy hneď, treba kliknúť na refresh button a v zozname sa objavia. 

![coursesrefresh](nbgrader/courses_refresh.png)

## Inštruktor

Inštruktor po prihlásení uvidí (jednoduchý) klikací list s kurzami, kde je inštruktor. Po kliknutí na meno kurzu bude presmerovaný do známeho prostredia nbgradru. 

![instructorlist](nbgrader/instructor_list.png)

![formgradert](nbgrader/formgrader.png)


# Kurzy - pridávanie a správa

Nutné pre pridanie/odobranie kurzu komunikovať s nami. 

## Pridanie študentov do kurzu

Človek je študentom, ak je členom Perun subgroup `{kurz}-students` pod group `NBGrader Tulhub`.  Na pridanie študenta do skupiny potrebujem jeho mail, ideálne vo formáte `mail, meno studenta`. Študentovi príde pozvánka, je na ňom aby to odklikol. Kým to neurobí, nevidí kurz.

Zatiaľ vám Perun budem suportiť ja.


> [!IMPORTANT]
> K dnešnému dňu viem iba kedy rozposlať pozvánky študentom ZAP !!!!!!!

## Pridanie inštruktorov do kurzu

Človek je študentom, ak je členom Perun subgroup `{kurz}-instructors` pod group `NBGrader Tulhub`.  Na pridanie inštruktora do skupiny potrebujem jeho mail, ideálne vo formáte `mail, meno instruktora`. Inštruktorovi príde pozvánka, je na ňom aby to odklikol. Kým to neurobí, nevidí kurz.

Zatiaľ vám Perun budem suportiť ja.

> [!NOTE]
> Ak bol inštruktor pridaný ako inštruktor dodatočne (už sa niekedy prihlásil na avisem hub a ostal prihlásený) tak sa musí odhĺásiť a prihlásiť.

> [!CAUTION]
> Nemalo by sa stať, že inštruktor nejakého kurzu je zároveň aj študent iného. To zatiaľ vedie k mixu práv a nbgrader tak nefunguje dobre. Ak by to bolo v budúcnosti nutné, pozrieme sa na to no zatiaľ neodporúčame tento stav.


## Pridávanie assignments

ASSIGNMENTS NESMÚ BYŤ V HOME!!! Assigments patria JEDINE A IBA do `/mnt/exchange/{kurz}/source`. Ak sa vyrobí `gradebook.db` inde než v  `/mnt/exchange/{kurz}/` tak je niečo zle.

ODPORÚČAME vytvárať assignemnts cez UI (pretože si ten nbgrader možno vytvára ešte nejaké iné relácie než len dir) a do vytvoreného diru potom nakopírovať to, čo už máte natvorené. 

![image](nbgrader/image.png)

![image1](nbgrader/image1.png)

![image2](nbgrader/image2.png)

![image3](nbgrader/image3.png)


## Custom konfigurácia nbgrader_config.py

Ak sa releasne assignemnt s nejakým configom, výsledok už nejde zmeniť. Ak zmeníte config, ďalší release už sa udeje s tým zmeneným configom.


# Konfigurácia notebookového prostredia

Notebooky študentov sú spúšťatné ako samostatné kontajnere. Inštruktori pracujú rovno v hub pode (tak to má nbgrader, dá sa to preprogramovať ak by bolo nutné) no tieto rozdiely spôsobujú iné možnosti ďalšej konfigurácie prostredia.

## Notebooky študentov

Študenti majú k dispozícii perzistentný home v `/home/jovyan` ktorý sa dá premazať, ak je potrebné (voľba pri spúšťaní notebooku). Podľa dohody majú študenti CPU request=1 a CPU limit=2. Memory request=memory limit=4GB.

Študenti si môžu spustiť až 3 notebooky (jeden na predmet) súčasne. Pužíva sa 1 image keďže užívate rovnaké knižnice. Cez `fakeroot apt-get install ...` sa dajú nainštalovať systémové knižnice rovno do notebooku. Mal by fungovať pip i conda. 

Ak bol študent pridaný do kurzu dodatočne, stačí si spustiť nový notebook a vybrať s ktorým predmetom chce pracovať, prípadne reload na home stránku. 

## Prostredie inštruktora

Keďže inštuktori pracujú priamo v hub pode, nemajú možnosť si po prihlásení nakonfigurovať prostredie pretože hub už existuje a sú v ňom. Ak by bolo potrebné.

Na prianie som doinštalovala balíčky, nastavila `HOME=/mnt/exchange/{kurz}/home`. Home je perzistentný.

> [!CAUTION]
> HOME NEPOUŽÍVAJTE NA NIČ INÉ NEŽ NA UKLADANIE NEJAKÝCH EXTRA SÚBOROV NESÚVSIACICH S ASSIGNMENTS A NBGRADROM. NEBUDE TO FUNGOVAŤ!!!! 
> 


# Vytvorenie named servers

Zo straný študenta, prvý notebook je možné vyrobiť rovno po prihlásení, keď klikne na štart. Tento notebook ale nebude pomenovaný a tak sa dá prejsť do časti `Home`.

![homenamed](nbgrader/homenamed.png)

V tejto časti sa dajú naklikať názvy notebookov a tak vytvoriť. Do panelu home sa dá prejšt vždy, čiže študent si môže vyrobiť jeden notebook, spustiť a keď bude chcieť ďalší, môže prejsť buď do home alebo z notebooku cez `Hub Control Panel` do toho istého menu (obr v ďalšej sekcii).

![add](nbgrader/add.png)

# Mazanie notebookov po skončení práce

Ak prvý notebook nebol vyrobený cez zoznam ale rovno po prihlásení, nemá meno a maže sa veľkým červeným tlačítkom `Stop My Server` v Home časti (prípadne sa sem dá prejsť z `Hub Control Panel`).

![stopmyserver](nbgrader/stopmyserver.png)

Spustené pomenované notebooky sa dajú vymazať cez `Hub Control Panel - Stop`. 

![controlpanel](nbgrader/controlpanel.png)

![stop](nbgrader/stop.png)

To vedie k zmazaniu reálneho kontajnera v Kubernetoch. Nie je nutné kliknúť na Delete, no doporučujeme pretože študenti majú potom prehľad. 

![startdelete](nbgrader/startdelete.png)



# Výpočetné zdroje

Dohodnuté na vymazanie notebookov o polnoci.
