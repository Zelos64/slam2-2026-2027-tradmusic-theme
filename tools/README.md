# Outils de maintenance du thème

Ces scripts servent **uniquement à maintenir le thème**. Ils ne font pas partie du support donné aux étudiants et ne doivent pas être copiés dans le projet Symfony.

## Générer les écrans et les fixtures

```bash
python3 tools/generate.py
```

Le script régénère les 19 écrans HTML (tous sauf `components.html`) et `FIXTURES.md` à partir d'une source unique :

- `data.py` : toutes les données fictives (Instruments, Towns, Users, Musicians, Venues, Gigs, Sessions, Join Requests), la date « aujourd'hui » de la maquette et les crédits photos ;
- `generate.py` : les gabarits des écrans et de `FIXTURES.md`.

Grâce à cette source unique, la maquette et `FIXTURES.md` restent strictement identiques (voir [ADR 0003](../docs/adr/0003-donnees-fictives-dans-fixtures-md.md)). Avant d'écrire les fichiers, le script vérifie aussi les règles métier dans les données : une Join Request *Accepted* correspond à un Musician du Lineup, une Join Request *Pending* ne concerne qu'un Upcoming Gig, etc.

## Règles

- **Modifiez `data.py` ou `generate.py`, jamais les fichiers générés** : toute modification manuelle d'un écran ou de `FIXTURES.md` serait écrasée à la prochaine génération.
- `components.html` n'est **pas** généré : mettez-le à jour à la main si les données qu'il reprend changent.
- Une nouvelle photo doit être ajoutée dans `uploads/` et créditée dans `PHOTO_CREDITS` (`data.py`).
- Prérequis : Python 3.12 ou plus récent, sans dépendance externe.
