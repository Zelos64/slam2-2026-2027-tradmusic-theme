# TradMusic

Thème HTML/CSS pour le projet **TradMusic**, support du cours Symfony (BTS SIO 2ᵉ année).

TradMusic met en relation les musiciens de musique traditionnelle irlandaise, les pubs où ils jouent et le public. Le vocabulaire métier est défini dans [CONTEXT.md](CONTEXT.md), les choix structurants dans [docs/adr/](docs/adr/).

## Utilisation

Ouvrez `index.html` dans un navigateur : aucune installation ni compilation n'est nécessaire. Commencez par [components.html](components.html), qui présente tous les composants et leurs variantes.

## Contenu

| Dossier / fichier | Destination dans le projet Symfony |
|---|---|
| `*.html` | À découper en templates Twig dans `templates/` |
| `assets/styles/` | `assets/styles/` (AssetMapper) |
| `assets/images/` | `assets/images/` (logo, image d'accueil, images par défaut) |
| `uploads/` | `public/uploads/` (photos et icônes « téléversées ») |
| `FIXTURES.md` | Données à recopier dans les fixtures Doctrine |

`assets/styles/styleguide.css` ne sert qu'à `components.html` : ne le copiez pas.

Les écrans et `FIXTURES.md` sont générés par `tools/generate.py` : pour les modifier, voir [tools/README.md](tools/README.md). Le dossier `tools/` ne sert qu'à maintenir le thème et ne concerne pas les étudiants.

## Écrans

| Espace | Écrans |
|---|---|
| Public | `index.html`, `musicians.html`, `musician.html`, `venues.html`, `venue.html`, `gigs.html`, `gig.html`, `about.html` |
| Compte | `login.html`, `register.html` |
| Musician | `my-profile.html`, `my-join-requests.html` |
| Venue Manager | `my-venues.html`, `venue-form.html`, `venue-manage.html`, `gig-form.html`, `session-form.html`, `join-requests.html` |
| Divers | `components.html`, `404.html` |

L'espace d'administration n'est pas maquetté : il est réalisé avec EasyAdmin ([ADR 0004](docs/adr/0004-administration-avec-easyadmin.md)).

## Dépendances externes

- Polices [Fraunces](https://fonts.google.com/specimen/Fraunces) et [Source Sans 3](https://fonts.google.com/specimen/Source+Sans+3) (Google Fonts)
- [Font Awesome Free 6](https://fontawesome.com/) (`php bin/console importmap:require @fortawesome/fontawesome-free/css/all.min.css` dans Symfony)

## Crédits

Photos issues d'[Unsplash](https://unsplash.com) ([licence Unsplash](https://unsplash.com/license)) ; le détail figure à la fin de [FIXTURES.md](FIXTURES.md). Image d'accueil `assets/images/hero.jpg` : Jonathan Borba, [unsplash.com/photos/8A4ZnQ9vxYg](https://unsplash.com/photos/8A4ZnQ9vxYg).
