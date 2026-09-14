# TradMusic

Plateforme qui met en relation les musiciens de musique traditionnelle irlandaise, les lieux où ils jouent et le public qui vient les écouter.

Les termes restent en anglais (ils sont utilisés tels quels dans le site et le code) ; leurs définitions sont en français.

## Language

### People

**User** :
Personne disposant d'un compte sur la plateforme. Un User peut être Musician, Venue Manager, les deux à la fois, ou Admin.
_Avoid_ : Account, member

**Musician** :
User qui joue de la musique traditionnelle irlandaise et possède un profil public, rattaché à une Town.
_Avoid_ : Artist, player, performer

**Available** :
État d'un Musician qui a déclaré être ouvert aux propositions d'engagement. C'est un simple interrupteur, sans lien avec des dates.
_Avoid_ : Free, bookable

**Instrument** :
Entrée de la liste de référence des instruments de la plateforme (ex. Fiddle, Tin whistle, Uilleann pipes, Bodhrán), dont joue un Musician.
_Avoid_ : Violin (dire Fiddle)

**Venue Manager** :
User qui gère une ou plusieurs Venues et y publie des Gigs et des Sessions. Chaque Venue a exactement un Venue Manager.
_Avoid_ : Owner, publican, organizer

**Admin** :
User qui administre la plateforme elle-même, notamment les listes de référence des Instruments et des Towns.
_Avoid_ : Moderator, superuser

### Places and events

**Town** :
Entrée de la liste de référence des villes d'Irlande où se trouvent les Venues et où résident les Musicians (ex. Dublin, Galway, Doolin).
_Avoid_ : City, location, county

**Venue** :
Pub situé dans une Town, où ont lieu des Gigs et des Sessions. Chaque Venue a sa propre page présentant sa programmation.
_Avoid_ : Pub, bar, location

**Gig** :
Concert ponctuel dans une Venue, à une date et une heure précises, avec un Lineup. Un Gig n'a pas de titre : il est désigné par sa Venue et sa date.
_Avoid_ : Concert, show, event

**Lineup** :
Ensemble des Musicians qui jouent lors d'un Gig. Seul le Venue Manager du Gig en décide la composition.
_Avoid_ : Cast, performers, band

**Join Request** :
Demande d'un Musician, accompagnée d'un message facultatif, pour intégrer le Lineup d'un Upcoming Gig. Elle est **Pending** jusqu'à ce que le Venue Manager la passe à **Accepted** (le Musician rejoint le Lineup) ou **Declined**. Un Musician ne peut faire qu'une seule Join Request par Gig ; elle garde la trace d'une décision passée et n'est pas modifiée par les changements ultérieurs du Lineup.
_Avoid_ : Application, booking, invitation

**Upcoming Gig** / **Past Gig** :
Gig dont la date est, respectivement, postérieure ou antérieure au moment présent.

**Session** :
Rencontre informelle et hebdomadaire dans une Venue, désignée par un nom (ex. « Slow Session for Learners »), un jour de la semaine et à une heure donnés, où des musiciens jouent ensemble des airs traditionnels. Tout musicien peut s'y joindre ; il n'y a pas d'animateur et aucun Musician n'y est rattaché.
_Avoid_ : Jam, seisiún
