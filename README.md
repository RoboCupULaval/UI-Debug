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

### Protocole de communication v1.0

L'API est disponible pour le langage Python. Tous les paquets de données transférés sont des dictionnaires python qui sont sérialisés avec la librairie pickle.
Chaque paquet de données se structure de la manière suivante :

```python
packet = {'name': str,      # Indique le nom de l'émetteur.
          'version': str,   # Indique la version de l'API utilisée.
          'type': int,      # Indique le type de données.
          'link': int,      # Indique la numéro du robot dont les données sont associées (None étant aucun).
          'data': dict(...) # Données du paquet dans un dictionnaire (cf. les données par type).
          }

""" Exemple de paquet : Afficher une ligne rouge pendant 5 secondes """
packet = {'name': 'JulienB',
          'version': '1.0',
          'type': 3001,
          'link': None,
          'data': {'start': (100, 100),
                   'end':   (200, 200),
                   'color': (255, 0, 0),
                   'width': 2,
                   'style': 'SolidLine',
                   'timeout': 5
                   }
          }
```

#### Définition des types de données

Les données sont divisées en 4 familles qui ont chacunes leurs spécificités :

  Valeur type | Nom de Famille | Description
------------- | -------------- | ---------------------------------------------------------------------------------------
0 <= 999      | Logger         | Affiche de l'information sous forme de texte dans la fenêtre assignée dans l'UI.
1000 <= 2999  | Setter/Getter  | Permet de paramétrer des données de l'IA dans l'UI ou de récupérer des données de l'UI de maniére ponctuelle.
3000 <= 4999  | Drawer         | Dessine des éléments dans la fenêtre du terrain.
5000 <= 6999  | Sender         | Commande envoyée de l'UI vers le client

### Description des données par type

L'information du paquet['data'] sont les données que l'on souhaite traiter. Il y a un type différent par données.

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

# Type 1000 - Envoie à l'UI d'un HandShake pour savoir si l'UI est connecté
data = {}                   # Dictionnaire vide

# Type 1001 - Envoie à l'UI la liste des stratégies, tactiques et actions disponibles.
data = {'strategy': list(str),      # Liste de toutes les stratégies
        'tactic': list(str),        # Liste de toutes les tactiques
        'action': list(str)}        # Liste de toutes les actions

# Type 1002 - Envoie à l'UI le statut d'un robot
data = {str:   {                                    # Identification de l'équipe ('yellow' | 'blue')
                 int:   {                           # Identification du robot (0-5)
                         'tactic': str,             # Correspond à la tactique active sur le robot
                         'action': str,             # Correspond à l'action active sur le robot
                         'target': tuple(int, int), # Correspond à la cible active du robot
                        }
                }
        }
==> exemple: {'yellow': {1: {'action': 'Kick', 'target': (0, 0)}, 5: {'tactic': 'GoToGoal'}},
              'blue': {0: {'tactic': 'GoalKeeper', 'action': 'Stop'}}}

# Type 1003 - Envoie à l'UI le statut du jeu
data = {'blue': str,               # Correspond à la Stratégie courrante de l'équipe bleue
        'yellow': str,             # Correspond à la Stratégie courrante de l'équipe jaune
        }

# Type 2000 - Envoie à l'UI d'un fragment binaire identifié pour le reconstruire par la suite.
data = {'id': str,                  # Identification du binaire à reconstruire
        'piece_number': int,        # Numéro de morceau courant
        'total_pieces': int,        # Nombre de morceaux total
        'binary': bin}              # Morceau binaire

""" ... """

# Type 3001 - Dessine une Ligne simple dans la fenêtre graphique du terrain.
data = {'start': tuple(int, int),       # Coordonnées du premier point
        'end': tuple(int, int),         # Coordonnées du point final
        # === Options supplémentaires ===
        'color': tuple(int, int, int),  # Couleur RGB
        'width': int,                   # Épaisseur du trait
        'style': str,                   # SolidLine | DashLine | DotLine | DashDotLine
        'timeout': int}                 # Temps d'affichage en seconde (0 étant un temps infini)

# Type 3002 - Dessine une Série de Lignes dans la fenêtre graphique du terrain.
data = {'points': list(tuple(int, int)), # Liste de coordonnées du premier point
        # === Options supplémentaires ===
        'color': tuple(int, int, int),  # Couleur RGB
        'width': int,                   # Épaisseur du trait
        'style': str,                   # SolidLine | DashLine | DotLine | DashDotLine
        'timeout': int}                 # Temps d'affichage en seconde (0 étant un temps infini)

# Type 3003 - Dessine un Cercle dans la fenêtre graphique du terrain.
data = {'center': tuple(int, int),      # Coordonnées du centre du cercle
        'radius': int,                  # Rayon du cercle
        # === Options supplémentaires ===
        'color': tuple(int, int int),   # Couleur RGB
        'style': str,                   # SolidLine | DashLine | DotLine | DashDotLine
        'is_fill': bool,                # Si le cercle est rempli ou non
        'timeout': int}                 # Temps d'affichage en seconde (0 étant un temps infini)

# Type 3004 - Dessine un Point dans la fenêtre graphique du terrain.
data = {'point': tuple(int, int),       # Coordonnées du centre du cercle
        # === Options supplémentaires ===
        'width': int,                   # Taille en pixel du point
        'color': tuple(int, int int),   # Couleur RGB
        'timeout': int}                 # Temps d'affichage en seconde (0 étant un temps infini)

# Type 3005 - Dessine une Série de Point dans la fenêtre graphique du terrain.
data = {'points': list(tuple(int, int)),# Coordonnées du centre du cercle
        # === Options supplémentaires ===
        'width': int,                   # Taille en pixel du point
        'color': tuple(int, int int),   # Couleur RGB
        'timeout': int}                 # Temps d'affichage en seconde (0 étant un temps infini)

# Type 3006 - Dessine un Rectangle dans la fenêtre graphique du terrain.
data = {'top_left': tuple(int, int),    # Coordonnées du premier point
        'bottom_right': tuple(int, int),# Coordonnées du point final
        # === Options supplémentaires ===
        'color': tuple(int, int, int),  # Couleur RGB
        'width': int,                   # Épaisseur du trait
        'style': str,                   # SolidLine | DashLine | DotLine | DashDotLine
        'is_fill': bool,                # Si le forme est rempli ou non
        'timeout': int}                 # Temps d'affichage en seconde (0 étant un temps infini)

# Type 3007 - Dessine les informations d'une Influence Map sur le terrain.
data = {'field_data': list(int, int, ...),      # Données de l'Influence Map
        # === Options supplémentaires ===
        'size': tuple(int, int),                # Taille de la grille
        'focus': tuple(int, int, int, int)      # Affiche uniquement les données dans un rectangle prédéfini
        'hottest_numb': int,                     # Nombre le plus élevé
        'hottest_color': tuple(int, int ,int ),  # Couleur RGB du nombre le plus élevé
        'coldest_numb': int,                    # Nombre le moins élevé
        'coldest_color': tuple(int, int, int),  # Couleur RGB du nombre le moins élevé
        'has_grid': bool,                       # Affichage de la grille ?
        'grid_color': tuple(int, int, int),     # Couleur RGB des traits de la grille
        'grid_width': int,                      # Taille des traits de la grille
        'grid_style': str,                      # SolidLine | DashLine | DotLine | DashDotLine
        'opacity': int}                         # Indice d'opacité de la grille de 0 à 10 (0 étant transparente)
        'timeout': int                          # Temps d'affichage en seconde (0 étant un temps infini)
        }

# Type 3008 - Dessine un Texte de couleur
data = {'position': tuple(int, int)     # Position de l'affichage du texte
        'text': str,                    # Texte à afficher
        # === Options supplémentaires ===
        'size': int,                    # Taille du texte en pixel
        'font': str,                    # Arial | Courier New | Verdana
        'align': str,                   # Right | Left | Center
        'color': tuple(int, int, int),  # Couleur RGB
        'has_bold': bool,               # Si le texte est en gras
        'has_italic': bool,             # Si le texte est en italic
        'timeout': int}                 # Temps d'affichage en seconde (0 étant un temps infini)
        }

# Type 3009 - Dessine un Arbre
data = {'tree': list(tuple(tuple(int, int), tuple(int, int)), ...)
                                        # Liste de toutes les arêtes
        # === Options supplémentaires ===
        'width': int                    # Épaisseur du trait
        'color': tuple(int, int, int),  # Couleur RGB
        'timeout': int}                 # Temps d'affichage en seconde (0 étant un temps infini)
        }
        
""" ... """

# Type 5000 - Envoie la réponse du HandShake au client
data = {}                           # Dictionnaire vide

# Type 5001 - Basculer l'IA en mode contrôle humain/machine (toggle-human-control)
data = {'is_human_control': bool    # Donne le contrôle de l'IA à la humain ou à la machine
       }

# Type 5002 - Envoie la Stratégie à adopter pour l'IA (set-strategy)
data = {'strategy': str             # Nom de la stratégie
       }

# Type 5003 - Envoie la tactique à adopter pour un robot (set-robot-tactic)
data = {'tactic': str,              # Nom de la tactique
        'id': int                   # ID du robot
        # === Options supplémentaires ===
        'target': tuple(int, int)   # Position de la cible du robot
        'goal': tuple(int, int)     # Position du but du robot
       }

# Type 5004 - Envoie la cible d'un robot (set-robot-target)
data = {'id': int,                  # ID du robot
        'target': tuple(int, int)   # Position de la cible du robot
       }

# Type 5005 - Envoie les dimensions du terrain
data = {'width': int,               # Longueur du terrain
        'height': int,              # Largeur du terrain
        'center_radius': int,       # Rayon du cercle central
        'defense_radius': int,      # Rayon des cercles en défense
        'defense_stretch': int,     # Longueur de la ligne de séparation en défense
        'goal_width': int,          # Longueur de la cage du but
        'goal_height': int,         # Largeur de la cage du but
        }

""" ... """
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
