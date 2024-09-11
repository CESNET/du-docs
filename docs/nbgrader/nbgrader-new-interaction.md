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

# Prihlasovanie do hubu

Prihlasovanie je zabezpečené cez jednotné prihlásenie s extra kontrolou, či je človek z TULu. Keďže čistá kontrola iba TUL domény nezabezpečuje, že sa prihlasuje človek, ktorý je študentom/inštruktorom, vykonáva sa na pozadí kontrola emailu z vyššie spomínaných súborov a podľa (ne)existenciu mailu v niektorom z týchto súborov sa buď zobrazí prístup do kurzov pre inštruktora, spawn form pre študenta alebo nič.

Zatiaľ nie je potrebná registrácia do Meta, toto sa vyrieši počas října. Pravdepodobne sa bude jednať o presun nejakých resourcov v Perune - nič, čo by ovplyvnilo chod hubu a spôsobilo zmenu pre študentov. 

Testovací hub: https://avi-semt.dyn.cloud.e-infra.cz

Produkcia: https://jupytul.cloud.e-infra.cz

------
Nie je nutná iná registrácia okrem MetaCentra a eINFRA. Ak študent/inštruktor nie je členom meta, musí sa zaregistrovať tu: https://metavo.metacentrum.cz/en/application/index.html. 

# Kurzy - pridávanie a správa

Prerobili sme systém pridávania kurzov, ich študentov a inštruktorov. Pôvodne bolo nutné nám poslať názov kurzu, my sme založili potrebné zložky a až potom ste si mohli (a museli) popridávať študentov ručne. 
## Pridanie kurzu:

Do konkrétneho súboru, ktorý slúži ako konfigurák sa pridá pre každý kurz sekcia pod `courses`, ktorá obsahuje meno kurzu a cesty, kde sú mountnuté súbory so študentmi a inštruktormi. Zatiaľ je nutné pre pridanie/odobranie kurzu komunikovať s nami, ale mohle by ste si to ľahko robiť aj vy sami, ak by ste chceli nad tým správu. 

```
courses:
  - name: course1
    studentFile: /mnt/course_users/course1_students.txt
    instructorFile: /mnt/course_users/course1_instructors.txt

```

## Pridanie študentov do kurzu

Vyrobí sa súbor s názvom `[meno_kurzu]_students.txt` v stanovenej lokácii. Súbor obsahuje *IBA* emaile študentov ktorí sú zapísaní do daného predmetu (oficiálne TUL emaile, ktoré sa dajú vytiahnuť z vášho ISu). V súbore je jeden mail na jednom riadku. Nič viac nie je potrebné, študent automaticky uvidí kurz, do ktorého má prístup. 

> [!IMPORTANT]
> Ak študent nevidí kurz a jeho email je určite v súbore, je možné, že má v Perune nastavený iný preferred email - ak už používal metacentrum a nastavil si iný preferred email než je oficiálny TUL email. Obráťte sa na nás s menom študenta a vyriešime. 



## Pridanie inštruktorov do kurzu

Vyrobí sa súbor s názvom `[meno_kurzu]_instructors.txt` v stanovenej lokácii. Súbor obsahuje *IBA* emaile inštruktorov ktorí sú vedení jak lektori daného predmetu (oficiálne TUL emaile, ktoré sa dajú vytiahnuť z vášho ISu). V súbore je jeden mail na jednom riadku. Nič viac nie je potrebné, inštruktor automaticky uvidí kurz, do ktorého má prístup. 

> [!IMPORTANT]
> Ak inštruktor nevidí kurz a jeho email je určite v súbore, je možné, že má v Perune nastavený iný preferred email - ak už používal metacentrum a nastavil si iný preferred email než je oficiálny TUL email. Obráťte sa na nás s menom inštruktora a vyriešime. 

> [!NOTE]
> Ak bol inštruktor pridaný ako inštruktor dodatočne (už sa niekedy prihlásil na avisem hub a ostal prihlásený) tak sa musí odhĺásiť a prihlásiť.

> [!CAUTION]
> Nemalo by sa stať, že inštruktor nejakého kurzu je zároveň aj študent iného. To zatiaľ vedie k mixu práv a nbgrader tak nefunguje dobre. Ak by to bolo v budúcnosti nutné, pozrieme sa na to no zatiaľ neodporúčame tento stav.


# Konfigurácia notebookového prostredia

Notebooky študentov sú spúšťatné ako samostatné kontajnere. Inštruktori pracujú rovno v hub pode (tak to má nbgrader, dá sa to preprogramovať ak by bolo nutné) no tieto rozdiely spôsobujú iné možnosti ďalšej konfigurácie prostredia.

## Notebooky študentov

Študenti majú k dispozícii perzistentný home v `/home/jovyan` ktorý sa dá premazať, ak je potrebné (voľba pri spúšťaní notebooku). Podľa dohody majú študenti CPU request=1 a CPU limit=2. Memory request=memory limit=4GB.

Študenti si môžu spustiť až 3 notebooky (jeden na predmet) súčasne. Pužíva sa 1 image keďže užívate rovnaké knižnice. Cez `fakeroot apt-get install ...` sa dajú nainštalovať systémové knižnice rovno do notebooku. Mal by fungovať pip i conda. 

Ak bol študent pridaný do kurzu dodatočne, stačí si spustiť nový notebook a vybrať s ktorým predmetom chce pracovať, prípadne reload na home stránku. 

## Prostredie inštruktora

Keďže inštuktori pracujú priamo v hub pode, nemajú možnosť si po prihlásení nakonfigurovať prostredie pretože hub už existuje a sú v ňom. Ak by bolo potrebné, dali by sa natvoriť samostatné perzistentné úložiská pre inštruktorov, ktoré by boli pripojené do hubu a tak by mal každý svoj priestor (na nejaké extra súbory ap.). Všetky zložky by ale boli mountnuté naraz čže každý inštruktor by si musel dať pozor, kde zapisuje pri práci.

# Po prihlásení

## Študent

Študent si po prihlásení vyberie kurz s ktorým chce pracovať, či chce premazať home a klikne na start. Po spustení notebooku uvidí túto stránku. Väčšinou neni vidieť kurzy hneď, treba kliknúť na refresh button a v zozname sa objavia. 

![coursesrefresh](nbgrader/courses_refresh.png)

## Inštruktor

Inštruktor po prihlásení uvidí (jednoduchý) klikací list s kurzami, kde je inštruktor. Po kliknutí na meno kurzu bude presmerovaný do známeho prostredia nbgradru. 

![instructorlist](nbgrader/instructor_list.png)

![formgradert](nbgrader/formgrader.png)

# Vytvorenie named servers

Zo straný študenta, prvý notebook je možné vyrobiť rovno po prihlásení, keď klikne na štart. Tento notebook ale nebude pomenovaný a tak sa dá prejsť do časti `Home`.

![homenamed](nbgrader/homenamed.png)

V tejto časti sa dajú naklikať názvy notebookov a tak vytvoriť. Do panelu home sa dá prejšt vždy, čiže študent si môže vyrobiť jeden notebook, spustiť a keď bude chcieť ďalší, môže prejsť buď do home alebo z notebooku cez `Hub Control Panel` do toho istého menu (obr v ďalšej sekcii).

![add](nbgrader/add.png)

# Mazanie notebookv po skončení práce

Ak prvý notebook nebol vyrobený cez zoznam ale rovno po prihlásení, nemá meno a maže sa veľkým červeným tlačítkom `Stop My Server` v Home časti (prípadne sa sem dá prejsť z `Hub Control Panel`).

![stopmyserver](nbgrader/stopmyserver.png)

Spustené pomenované notebooky sa dajú vymazať cez `Hub Control Panel - Stop`. 

![controlpanel](nbgrader/controlpanel.png)

![stop](nbgrader/stop.png)

To vedie k zmazaniu reálneho kontajnera v Kubernetoch. Nie je nutné kliknúť na Delete, no doporučujeme pretože študenti majú potom prehľad. 

![startdelete](nbgrader/startdelete.png)



# Výpočetné zdroje

Zdroje sú samostatná kategória pretože predstavujú najdôležitejšiu časť. Z viacerých rokov menežovania iných hubov pre výuku (a všeobecného hubu) vieme, že zdrojmi sa hrozne plytvá. Ľudia si vyrobia notebook s mnoho CPU, GPU a pamäťou a buď ho využívajú veľmi málo (overestimated resources) alebo ho absolútne nepoužívajú, iba blokujú zdroje tým, že si raz dačo skúsili. Najdrahší zdroj sú GPU a preto pre notebooky využívajúce GPU platí najtvrdšia politika. 

Z tohto dôvodu máme pre každý takýto hub nejakú politiku "resource reclamation":
1. Pre všeobecný hub sledujeme metriky každého podu a ak využitie nepresiahne nami stanovenú priemernú hranicu za 2 alebo 3 dni existencie notebooku, zmažeme ho. Užívateľ je informovaný každý deň mailom, že mu bude notebook zmazaný ak nenavýši svoje spotrebu a teda má dosť času si zálohovať data.

2. Pre výukový hub na FI MUNI máme politiku, že každý notebook ktorý alokouje GPU je natvrdo po 48h zmazaný, či niečo robí alebo nie. CPU, pamäť a storage zatiaľ obmedzené nie sú. 

Podobná politika bude musieť byť nastavená i vo vašom prípade, len bude potrebné si rozmyslieť aká. 
