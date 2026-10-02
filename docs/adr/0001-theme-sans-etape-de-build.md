# Thème sans étape de build, compatible AssetMapper

Le thème sert de support à un cours Symfony en BTS SIO 2ᵉ année : les étudiants doivent pouvoir déposer ses fichiers dans `assets/` d'un projet Symfony utilisant AssetMapper (le défaut de Symfony), sans installer Node ni configurer un outil de build. Le thème est donc écrit en CSS natif (variables, nesting) et en JavaScript en modules ES, et livré sous forme de pages HTML complètes, une par écran, avec l'en-tête et le pied de page dupliqués pour que les étudiants pratiquent eux-mêmes le découpage en `base.html.twig`, `{% raw %}{% block %}{% endraw %}` et `{% raw %}{% include %}{% endraw %}`.

## Considered Options

- **Sources Sass** (ancien thème, webpack) : écartées, car elles imposent une compilation (sass-bundle ou Webpack Encore) et font perdre du temps de cours sur l'outillage front.
- **Partiels déjà découpés** : écartés, car le découpage en templates Twig est justement un objectif pédagogique.
