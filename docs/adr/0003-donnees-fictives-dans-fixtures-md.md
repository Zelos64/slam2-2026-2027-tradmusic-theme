# Données fictives fournies dans FIXTURES.md, identiques à la maquette

Les données fictives sont fournies aux étudiants dans un fichier `FIXTURES.md` (un tableau par entité, dans l'ordre de dépendance), qu'ils recopient dans leurs propres fixtures Doctrine : écrire les fixtures fait partie de l'apprentissage. Chaque élément affiché dans la maquette HTML correspond exactement à une ligne de `FIXTURES.md`, pour qu'un étudiant puisse vérifier son travail en comparant son rendu à la maquette.

## Considered Options

- **JSON, dump SQL ou classes de fixtures prêtes à l'emploi** : écartés, car ils retirent l'exercice d'écriture des fixtures ou supposent un schéma de base imposé.
- **Recopier les données depuis le HTML** : envisagé puis abandonné, car il obligeait à afficher chaque champ de chaque entité dans la maquette.

## Consequences

- Les relations sont exprimées par **slug** (et non par identifiant numérique, qui dépend de l'auto-incrément), ce qui prépare l'usage des références de fixtures.
- Les dates des Gigs sont écrites comme des **modificateurs relatifs PHP** (`+5 days 21:00`, `-3 days 20:30`) et mêlent Upcoming Gigs et Past Gigs : des dates absolues rendraient la maquette obsolète d'une année sur l'autre et videraient la liste des Upcoming Gigs. La maquette affiche ces dates pour un « aujourd'hui » d'exemple.
- Les comptes (e-mail, rôles, mot de passe en clair commun, à hacher) figurent aussi dans `FIXTURES.md`, puisqu'ils n'apparaissent sur aucune page publique.
