# UI-Debug
Ce dépôt contient une interface de débogage pour faciliter les travaux de développement pour StrategyIA et le reste du projet RoboCupULaval.

L'interface permet de visualiser diverses informations:

* Les robots identifiés par la vue
* Leur direction vectorielle
* Les positions du pathfinder
* Informations arbitraires en provenance d'un client (_e.g_: StrategyIA)

## Communication et API

L'application agit comme un serveur et une interface graphique selon le cadre **MVC**.
Un serveur UDP sur une adresse multicast est créé et les clients s'y connectent pour envoyer les informations de débogage.
Pour le client de l'IA, une communication bidirectionnelle est activée afin de permettre à l'interface d'envoyer des commandes.

L'**UI-Debug** assumme aussi la présence du serveur de vision: _vision-SSL_ ou _grSim_.
Il va obtenir directement de ce serveur les frames de visions et les clients se synchronisent tous en utilisant le numéro de frame.

La **version 0.0** garantie les API suivante:

### API Schema v1

L'API est disponible pour le langage Python. Tous les paquets de données transférés sont des dictionnaires python.
Chaque paquet de données se structure de la manière suivante :

```python
packet = {'name': str,      # Indique le nom du destinataire.
          'version': str,   # Indique la version de l'API utilisée
          'type': int,      # Indique le type de données.
          'link': int,      # Indique la numéro du robot dont les données sont associées (None étant aucun).
          'data': dict()}   # Données du paquet dans un dictionnaire (cf. les données par type).
```

#### Type de données

Les données sont divisées en 4 familles qui ont chacunes leurs spécificités:

Valeur type | Nom de Famille | Description
----------- | -------------- | ---------------------------------------------------------------------------------------
0 <= 9      | Logger         | Affiche de l'information sous forme de texte dans la fenêtre assignée dans l'UI.
10 <= 29    | Setter/Getter  | Permet de paramétrer des données de l'IA dans l'UI ou de récupérer des données de l'UI de maniére ponctuelle.
30 <= 49    | Drawer         | Dessine des éléments dans la fenêtre du terrain.
50 <= 59    | Initializer    | Permet d'initialiser l'UI avec des données de l'IA à la connexion.

```python
# Type 1 - Affiche n'importe quelles données dans la fenêtre du logger.
data = {'data_header_1': int/str,
        'data_header_2': int/str,
        ...
        'data_header_n': int/str}

# Type 2 - Affiche un message texte avec un niveau d'importance.
data = {'level': int,       # 0:NOSET | 1:DEBUG | 2:INFO | 3:WARN | 4:ERR | 5:CRIT
        'message': str}     # Message à envoyer

""" ... """

# Type 11 - Envoie à l'UI la liste des stratégies, tactiques et actions disponibles.
data = {'strategy': list(str),      # Liste de toutes les stratégies
        'tactic': list(str),        # Liste de toutes les tactiques
        'action': list(str)}        # Liste de toutes les actions

""" ... """

# Type 31 - Dessine une ligne simple dans la fenêtre graphique du terrain.
data = {'start': tuple(int, int),       # Coordonnées du premier point
        'end': tuple(int, int),         # Coordonnées du point final
        'color': tuple(int, int, int),  # Couleur RGB
        'width': int,                   # Épaisseur du trait
        'style': str,                   # SolidLine | DashLine | DotLine | DashDotLine
        'timeout': int}                 # Temps d'affichage en seconde (0 étant un temps infini)

# Type 32 - Dessine une série de lignes dans la fenêtre graphique du terrain.
data = {'points': list(tuple(int, int)), # Liste de coordonnées du premier point
        'color': tuple(int, int, int),  # Couleur RGB
        'width': int,                   # Épaisseur du trait
        'style': str,                   # SolidLine | DashLine | DotLine | DashDotLine
        'timeout': int}                 # Temps d'affichage en seconde (0 étant un temps infini)

# Type 33 - Dessine un cercle dans la fenêtre graphique du terrain.
data = {'center': tuple(int, int),      # Coordonnées du centre du cercle
        'radius': int,                  # Rayon du cercle
        'color': tuple(int, int int),   # Couleur RGB
        'style': str,                   # SolidLine | DashLine | DotLine | DashDotLine
        'is_fill': bool,                # Si le cercle est rempli ou non
        'timeout': int}                 # Temps d'affichage en seconde (0 étant un temps infini)

# Type 34 - Dessine un point dans la fenêtre graphique du terrain.
data = {'point': tuple(int, int),       # Coordonnées du centre du cercle
        'width': int,                   # Taille en pixel du point
        'color': tuple(int, int int),   # Couleur RGB
        'timeout': int}                 # Temps d'affichage en seconde (0 étant un temps infini)

# Type 35 - Dessine une série de point dans la fenêtre graphique du terrain.
data = {'points': list(tuple(int, int)),# Coordonnées du centre du cercle
        'width': int,                   # Taille en pixel du point
        'color': tuple(int, int int),   # Couleur RGB
        'timeout': int}                 # Temps d'affichage en seconde (0 étant un temps infini)

# Type 36 - Dessine un rectangle dans la fenêtre graphique du terrain.
data = {'top_left': tuple(int, int),    # Coordonnées du premier point
        'bottom_right': tuple(int, int),# Coordonnées du point final
        'color': tuple(int, int, int),  # Couleur RGB
        'width': int,                   # Épaisseur du trait
        'style': str,                   # SolidLine | DashLine | DotLine | DashDotLine
        'is_fill': bool,                # Si le forme est rempli ou non
        'timeout': int}                 # Temps d'affichage en seconde (0 étant un temps infini)
```

### API serveur->ia

* _toggle-human-control_
* _set-robot-tactic_
* _set-robot-target_
* _set-strategy_

### API client->serveur

* _draw-line_
* _draw-circle_
* _display-text_
* _create-filter_


## Évolution

**UI-Debug** est une appplication indépendante avec comme seule dépendance le serveur de vision.
L'application a donc la responsabilité de déterminer comment afficher et dessiner les différents éléments.
Les différents clients sont libres de choisir comment ils gèrent leur envoi d'information, la frontière d'E/S étant codifiée par les API décris ci-haut.

Les versions majeures peuvent potentiellement modifier ces API.

## Standard de code

Le projet respecte les mêmes standards de code décrit dans le dépôt RoboCupULavalHautNiveau/Admin.

* PEP-8
* Docstring PEP-257
* Unit Test: nosetests

## Responsable

_(30 mai 2016)_ Julien B. jusqu'au _31 août 2016_
