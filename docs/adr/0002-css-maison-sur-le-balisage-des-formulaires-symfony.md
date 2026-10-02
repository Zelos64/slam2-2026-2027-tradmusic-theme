# CSS maison ciblant le balisage par défaut des formulaires Symfony

Les formulaires du thème reproduisent exactement le HTML produit par le form theme par défaut de Symfony (`form_div_layout.html.twig`), y compris les états d'erreur, et le CSS maison les stylise tel quel : un simple `{% raw %}{{ form(form) }}{% endraw %}` donne le rendu de la maquette, sans form theme personnalisé. On garde ainsi une identité visuelle propre au site tout en évitant aux étudiants l'écriture d'un form theme.

## Considered Options

- **Bootstrap 5** avec `bootstrap_5_layout.html.twig` : rendu immédiat mais générique, et les étudiants n'écrivent quasiment pas de CSS.
- **CSS maison avec ses propres classes** : oblige à écrire un form theme, notion trop avancée pour ce cours.

## Consequences

Toute modification du balisage des formulaires dans la maquette doit rester fidèle à ce que génère Symfony ; un « nettoyage » du HTML des formulaires casserait le rendu dans les projets des étudiants.
