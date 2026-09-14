# Données fictives (fixtures)

Ce fichier contient toutes les données à charger dans l'application Symfony. Recopiez-les dans vos classes de fixtures (DoctrineFixturesBundle) : une fois chargées, votre application doit afficher exactement les écrans de la maquette.

## Consignes

- **Ordre de chargement** : les tableaux sont présentés dans l'ordre de dépendance. Une entité ne référence que des entités des tableaux précédents.
- **Relations** : les relations sont indiquées par le **slug** de l'entité liée (ou l'**e-mail** pour un User). N'utilisez jamais d'identifiant numérique : il dépend de l'auto-incrément. Utilisez plutôt les références de fixtures (`addReference()` / `getReference()`).
- **Gigs** : un Gig n'a pas de slug. La colonne *Reference* sert uniquement à le désigner dans les fixtures ; ce n'est pas un champ de l'entité.
- **Dates relatives** : les dates des Gigs et des Join Requests sont des modificateurs à passer tels quels à PHP, par exemple `new \DateTimeImmutable('+4 days 21:00')`. Ainsi, il y a toujours des Upcoming Gigs et des Past Gigs, quelle que soit la date du jour. La maquette affiche ces dates en prenant pour « aujourd'hui » le **lundi 12 octobre 2026** (en anglais dans les écrans).
- **Mots de passe** : tous les comptes utilisent le mot de passe `password`. Il doit être haché avec `UserPasswordHasherInterface` avant d'être enregistré.
- **Images** : copiez le dossier `uploads/` du thème dans `public/uploads/` de votre projet. Les colonnes *Photo* et *Icon* donnent le nom du fichier.
- **Traduction** : les données restent en anglais, comme le contenu du site.


## 1. Instruments

| Slug | Name | Icon |
|---|---|---|
| `banjo` | Banjo | `banjo.svg` |
| `bodhran` | Bodhrán | `bodhran.svg` |
| `bouzouki` | Bouzouki | `bouzouki.svg` |
| `button-accordion` | Button accordion | `button-accordion.svg` |
| `concertina` | Concertina | `concertina.svg` |
| `fiddle` | Fiddle | `fiddle.svg` |
| `flute` | Flute | `flute.svg` |
| `guitar` | Guitar | `guitar.svg` |
| `harp` | Harp | `harp.svg` |
| `low-whistle` | Low whistle | `low-whistle.svg` |
| `tin-whistle` | Tin whistle | `tin-whistle.svg` |
| `uilleann-pipes` | Uilleann pipes | `uilleann-pipes.svg` |

## 2. Towns

| Slug | Name |
|---|---|
| `doolin` | Doolin |
| `dublin` | Dublin |
| `ennis` | Ennis |
| `galway` | Galway |

## 3. Users

Mot de passe de tous les comptes : `password`.

| Email | First name | Last name | Roles |
|---|---|---|---|
| `admin@tradmusic.test` | Fiona | Hayes | `ROLE_ADMIN` |
| `aoife.brennan@tradmusic.test` | Aoife | Brennan | `ROLE_MUSICIAN` |
| `cillian.walsh@tradmusic.test` | Cillian | Walsh | `ROLE_MUSICIAN` |
| `niamh.doherty@tradmusic.test` | Niamh | Doherty | `ROLE_MUSICIAN` |
| `ronan.keane@tradmusic.test` | Ronan | Keane | `ROLE_MUSICIAN` |
| `owen.doyle@tradmusic.test` | Owen | Doyle | `ROLE_MUSICIAN`, `ROLE_VENUE_MANAGER` |
| `siobhan.murphy@tradmusic.test` | Siobhán | Murphy | `ROLE_MUSICIAN` |
| `declan.farrell@tradmusic.test` | Declan | Farrell | `ROLE_MUSICIAN` |
| `maire.quinlan@tradmusic.test` | Máire | Quinlan | `ROLE_MUSICIAN` |
| `padraig.lynch@tradmusic.test` | Pádraig | Lynch | `ROLE_MUSICIAN` |
| `clodagh.nolan@tradmusic.test` | Clodagh | Nolan | `ROLE_MUSICIAN` |
| `grainne.kelly@tradmusic.test` | Gráinne | Kelly | `ROLE_VENUE_MANAGER` |
| `liam.byrne@tradmusic.test` | Liam | Byrne | `ROLE_VENUE_MANAGER` |

## 4. Musicians

| Slug | User | Town | Instruments | Available | Photo | Bio |
|---|---|---|---|---|---|---|
| `aoife-brennan` | `aoife.brennan@tradmusic.test` | `galway` | `fiddle`, `tin-whistle` | yes | `aoife-brennan.jpg` | Aoife grew up in Connemara, learning tunes by ear from her grandfather. She now plays fiddle in the pubs of Galway most weekends and teaches at the Crooked Bow's slow session. |
| `cillian-walsh` | `cillian.walsh@tradmusic.test` | `ennis` | `uilleann-pipes` | no | `cillian-walsh.jpg` | Piper from County Clare, Cillian has been playing the uilleann pipes for twenty years. He is busy recording an album this autumn. |
| `niamh-doherty` | `niamh.doherty@tradmusic.test` | `galway` | `flute`, `tin-whistle` | yes | `niamh-doherty.jpg` | Niamh plays a wooden flute in the Sligo style. You will often find her at the Friday gigs of Quay Street. |
| `ronan-keane` | `ronan.keane@tradmusic.test` | `doolin` | `bodhran` | yes | `ronan-keane.jpg` | Ronan keeps the rhythm for half the sessions of Doolin. He plays a goatskin bodhrán made by his uncle. |
| `owen-doyle` | `owen.doyle@tradmusic.test` | `doolin` | `fiddle` | no | `owen-doyle.jpg` | Owen runs Doyle's of Doolin and The Old Forge, and never misses a chance to take out his fiddle behind the bar. |
| `siobhan-murphy` | `siobhan.murphy@tradmusic.test` | `dublin` | `concertina` | yes | `siobhan-murphy.jpg` | Siobhán plays an Anglo concertina and loves polkas and slides from Sliabh Luachra. |
| `declan-farrell` | `declan.farrell@tradmusic.test` | `dublin` | `banjo`, `guitar` | yes | `declan-farrell.jpg` | Tenor banjo player and guitar accompanist, Declan has toured with several Dublin bands. |
| `maire-quinlan` | `maire.quinlan@tradmusic.test` | `ennis` | `harp` | no | `maire-quinlan.jpg` | Máire plays the Irish harp, from O'Carolan airs to modern compositions. |
| `padraig-lynch` | `padraig.lynch@tradmusic.test` | `dublin` | `button-accordion` | yes | `padraig-lynch.jpg` | Pádraig plays a B/C button accordion and leads the Monday night session at the Tipper & Reel. |
| `clodagh-nolan` | `clodagh.nolan@tradmusic.test` | `galway` | `bouzouki`, `guitar`, `low-whistle` | yes | `clodagh-nolan.jpg` | Clodagh backs tunes on the bouzouki and guitar, and brings out her low whistle for slow airs. |

## 5. Venues

| Slug | Name | Town | Address | Manager | Photo | Description |
|---|---|---|---|---|---|---|
| `the-crooked-bow` | The Crooked Bow | `galway` | 14 Quay Street, Galway | `grainne.kelly@tradmusic.test` | `the-crooked-bow.jpg` | A narrow, wood-panelled pub on Quay Street with live music seven nights a week. Musicians gather by the fireplace at the back. |
| `the-salmon-weir` | The Salmon Weir | `galway` | 3 Newtownsmith, Galway | `grainne.kelly@tradmusic.test` | `the-salmon-weir.jpg` | A lively bar near the river, known for its big Friday gigs and its snug full of old photographs. |
| `doyles-of-doolin` | Doyle's of Doolin | `doolin` | Fisher Street, Doolin | `owen.doyle@tradmusic.test` | `doyles-of-doolin.jpg` | A family pub on the road to the pier, where tunes start at lunchtime in summer. |
| `the-tipper-and-reel` | The Tipper & Reel | `dublin` | 27 Capel Street, Dublin 1 | `liam.byrne@tradmusic.test` | `the-tipper-and-reel.jpg` | A Dublin bar with a long counter and a small stage, home of the Monday night session. |
| `the-half-door` | The Half Door | `dublin` | 8 Francis Street, Dublin 8 | `liam.byrne@tradmusic.test` | `the-half-door.jpg` | A tiny pub in the Liberties with red benches and late-night tunes on Fridays. |
| `the-old-forge` | The Old Forge | `ennis` | 11 Abbey Street, Ennis | `owen.doyle@tradmusic.test` | `the-old-forge.jpg` | A former forge turned pub, with a courtyard where concerts are held on summer evenings. |

## 6. Gigs

La description est facultative (vide = `null`).

| Reference | Venue | Starts at | Lineup | Description |
|---|---|---|---|---|
| `gig-01` | `the-crooked-bow` | `+4 days 21:00` | `aoife-brennan`, `ronan-keane` | Aoife and Ronan open the weekend with a set of Connemara reels and slides. |
| `gig-02` | `the-crooked-bow` | `+5 days 21:30` | `clodagh-nolan`, `cillian-walsh` |  |
| `gig-03` | `the-salmon-weir` | `+11 days 20:30` | `niamh-doherty`, `clodagh-nolan` | Flute, whistles and bouzouki: an evening of slow airs and jigs. |
| `gig-04` | `doyles-of-doolin` | `+2 days 21:00` | `owen-doyle`, `ronan-keane` |  |
| `gig-05` | `doyles-of-doolin` | `-4 days 20:30` | `cillian-walsh` | A solo evening of piping, with stories from County Clare. |
| `gig-06` | `the-tipper-and-reel` | `+3 days 21:00` | `siobhan-murphy`, `declan-farrell`, `padraig-lynch` | Polkas, slides and a few songs with three Dublin regulars. |
| `gig-07` | `the-tipper-and-reel` | `-9 days 21:00` | `declan-farrell` |  |
| `gig-08` | `the-half-door` | `+6 days 17:00` | `padraig-lynch`, `siobhan-murphy` | A relaxed Sunday afternoon of box and concertina duets. |
| `gig-09` | `the-old-forge` | `+9 days 20:00` | `maire-quinlan`, `cillian-walsh` | Harp and pipes in the old forge: O'Carolan tunes and airs. |
| `gig-10` | `the-salmon-weir` | `-2 days 21:00` | `aoife-brennan`, `clodagh-nolan` |  |

## 7. Sessions

| Venue | Name | Day of week | Time |
|---|---|---|---|
| `the-crooked-bow` | Slow Session for Learners | Tuesday | `19:30` |
| `the-crooked-bow` | Sunday Evening Session | Sunday | `18:00` |
| `doyles-of-doolin` | Big Thursday Session | Thursday | `21:30` |
| `the-tipper-and-reel` | Monday Night Session | Monday | `21:00` |
| `the-half-door` | Tunes at the Half Door | Friday | `22:00` |

## 8. Join Requests

Le message est facultatif (vide = `null`). Une Join Request *Accepted* correspond à un Musician déjà présent dans le Lineup du Gig.

| Musician | Gig | Status | Created at | Message |
|---|---|---|---|---|
| `niamh-doherty` | `gig-01` | `pending` | `-1 day 09:40` | I play flute and whistle, I know most of the Friday regulars. |
| `clodagh-nolan` | `gig-01` | `pending` | `-2 days 18:15` |  |
| `cillian-walsh` | `gig-02` | `accepted` | `-6 days 11:00` |  |
| `declan-farrell` | `gig-08` | `declined` | `-3 days 14:20` | Happy to bring the banjo along. |
| `siobhan-murphy` | `gig-09` | `pending` | `-1 day 20:05` | I'll be in Clare that week, I'd love to join Máire and Cillian. |
| `aoife-brennan` | `gig-04` | `pending` | `-2 days 10:30` | Ronan told me you were looking for a fiddle on Wednesday. |
| `aoife-brennan` | `gig-10` | `accepted` | `-8 days 16:45` |  |
| `aoife-brennan` | `gig-08` | `declined` | `-4 days 12:00` | I'm in Dublin that weekend, I can play some Galway tunes. |

## Crédits photos

Toutes les photos proviennent d'[Unsplash](https://unsplash.com) et sont utilisées selon la [licence Unsplash](https://unsplash.com/license).

| File | Photographer | Source |
|---|---|---|
| `uploads/musicians/aoife-brennan.jpg` | Nancy Hughes | [unsplash.com/photos/ysyRG_lkmiM](https://unsplash.com/photos/ysyRG_lkmiM) |
| `uploads/musicians/cillian-walsh.jpg` | Mary Borysova | [unsplash.com/photos/iLCM22Qe_C0](https://unsplash.com/photos/iLCM22Qe_C0) |
| `uploads/musicians/niamh-doherty.jpg` | Aswin Raj | [unsplash.com/photos/wfVREQs7KXQ](https://unsplash.com/photos/wfVREQs7KXQ) |
| `uploads/musicians/ronan-keane.jpg` | Caleb Toranzo | [unsplash.com/photos/xD8DPNDYG6E](https://unsplash.com/photos/xD8DPNDYG6E) |
| `uploads/musicians/owen-doyle.jpg` | Lucia Macedo | [unsplash.com/photos/d9_2kPJBG0U](https://unsplash.com/photos/d9_2kPJBG0U) |
| `uploads/musicians/siobhan-murphy.jpg` | The Metropolitan Museum of Art | [unsplash.com/photos/BgTZHWcXvqY](https://unsplash.com/photos/BgTZHWcXvqY) |
| `uploads/musicians/declan-farrell.jpg` | Duncan McNab | [unsplash.com/photos/inj45s7t9WY](https://unsplash.com/photos/inj45s7t9WY) |
| `uploads/musicians/maire-quinlan.jpg` | Patti Black | [unsplash.com/photos/AGYEwWQ6Nww](https://unsplash.com/photos/AGYEwWQ6Nww) |
| `uploads/musicians/padraig-lynch.jpg` | David Vilches | [unsplash.com/photos/Yy5YeqtXjSc](https://unsplash.com/photos/Yy5YeqtXjSc) |
| `uploads/musicians/clodagh-nolan.jpg` | Joel Swick | [unsplash.com/photos/WnIZ57zUK-E](https://unsplash.com/photos/WnIZ57zUK-E) |
| `uploads/venues/the-crooked-bow.jpg` | K. Mitch Hodge | [unsplash.com/photos/3fDv4xwdFZs](https://unsplash.com/photos/3fDv4xwdFZs) |
| `uploads/venues/the-salmon-weir.jpg` | Jonathan Borba | [unsplash.com/photos/4kLy0asVZhA](https://unsplash.com/photos/4kLy0asVZhA) |
| `uploads/venues/doyles-of-doolin.jpg` | Help Stay | [unsplash.com/photos/xzLogOO5cmo](https://unsplash.com/photos/xzLogOO5cmo) |
| `uploads/venues/the-tipper-and-reel.jpg` | Jon Tyson | [unsplash.com/photos/nHBZT4Qi44Y](https://unsplash.com/photos/nHBZT4Qi44Y) |
| `uploads/venues/the-half-door.jpg` | Theme Photos | [unsplash.com/photos/kPHYuzqoaz0](https://unsplash.com/photos/kPHYuzqoaz0) |
| `uploads/venues/the-old-forge.jpg` | K. Mitch Hodge | [unsplash.com/photos/dE8kZkt25bs](https://unsplash.com/photos/dE8kZkt25bs) |
| `assets/images/hero.jpg` | Jonathan Borba | [unsplash.com/photos/8A4ZnQ9vxYg](https://unsplash.com/photos/8A4ZnQ9vxYg) |
