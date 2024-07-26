---
layout: article
title: Nbgrader authorize student
permalink: /docs/nbgrader-auth-student.html
key: nbgrader-auth-student
aside:
  toc: true
sidebar:
  nav: docs
---

# Pridavanie studenta do nbgrader
Student sa musi registrovat na hlavnej stranke avi-sem hubu cez "Sign up", co sa nachadza rovno pod tym formularom na prihlasenie. Vyplna sa meno, heslo a email. 
Email nemusi byt funkcny ani realny, to sa nekontroluje a ani to nema ziadnu funkciu (mohol by mat, ale nema a s pripravovanymi zmenami v auth ani nebude mat)

Na to, aby sa student vedel prihlasit do hubu ho:
- musi admin autorizovat.

Na to, aby student videl nejaky kurz a vedel s nim pracovat:
- musi byt pridany do skupiny "nbgrader-(nazov kurzu)"

## Autorizovanie studenta

Autorizovat vedia iba admini. Zoznam adminov sa da zistit cez horny panel po prihlaseni a tento panel vidia iba admini. Ak ho nevidite, nieste admin ale viete poziadat hociktoreho admina, aby vas pridal ako admina.

![admini](nbgrader/admins.png)

Samotna autorizacia sa deje cez panel "Authorize" v ktorom cakaju registrovani uzivatelia. Akykolvek admin vie autorizovat studenta.

![authorize](nbgrader/authorize.png)

Po autorizacii sa vie uz student prihlasit do hubu ale stale nevidi ziadne kurzy. 


## Pridavanie studenta do kurzu (skupiny spojenej s kurzom)

Studenta mozte pridat do kurzu = skupiny ktora je spojena s kurzom,  cez `nbgrader db add [prihlasovacie meno studenta]` (co je moznost ktoru si chcete skusit) alebo aj cez GUI (ak by ste to chceli rychlejsie pre test)

Najdite si "Admin" v hornom paneli a vyberte manage groups

![manage](nbgrader/managegroups.png)

`formgrade-[predmet]` skupina je pre instruktorov a `nbgrader-[predmet]` su pre studentov. Pridavajte studentov do `nbgrader...` daneho predmetu.

![groups](nbgrader/groups.png)

Pridavajte cez meno studneta (tak jak sa prihasil, jeho prihlasovacie meno), nasledne pridat a Apply, to je dolezite!!

![adduser](nbgrader/adduser.png)
