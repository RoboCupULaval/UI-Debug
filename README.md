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
data = {str:   {                                    # Couleur de l'équipe ('yellow' | 'blue')
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

# Type 2001 - Demande à l'UI pour récupérer les données géométriques du terrain
data = {}                   # Dictionnaire vide

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
data = {'strategy': str,            # Nom de la stratégie
        'team': str                 # Couleur de l'équipe: 'yellow' | 'blue'
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

# Type 5006 - Envoie la configuration du réseau de la vision
data = {'is_serial': bool,          # La communication avec StrategyIA est en mode serial(True) ou UDP(False)
        'ip': str,                  # L'adresse ip de la vision 
        'port': int                 # Le port de la vision
}

# Type 5007 - Envoie la configuration des ports de communication
data = {'recv_port': int            # Le port de réception
        'send_port': int            # Le port d'envoie
}

# Type 5008 - Envoie la configuration du réseau UDP de StrategyIA
data = {'ip': str                   # L'adresse IP
        'port': int                 # Le numéro de port
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

# HOW TO:
## Paquet de Communication
Créer un nouveau paquet de communication se fait en suivant les étapes suivantes :

* Définition du paquet
* Création du paquet
* Traitement du paquet

### Définition du paquet :
La définition du paquet se fait dans le fichier **REAMDE.md** dans la section Protocole de communication.
Il faut déterminer les paramètres suivants :

* Déterminer dans quelle famille se situe le paquet _(Logger | Accesseur | Dessin | Répondeur)_
* Déterminer le numéro de type en fonction de la famille en sachant qu'un numéro est unique _(exemple : Pour la famille Logger je dois trouver un chiffre entre 0 et 999 qui ne soit pas pris)_
* Définir et décrire les paramètres des données transmises sous le forme : _data = { ... }_

Soyez bien explicite dans la description de votre paquet pour éviter de générer des erreurs lorsque vous recevrez un paquet.

Dans la pratique, votre paquet est un dictionnaire à plusieurs niveaux avec une première couche qui va décrire le type de paquet et sa provenance, puis un second niveau qui contient les données. Votre paquet va prendre le chemin suivant :

[ Serveur UDP ] => [ DataInModel -> DataInModel._datain_factory -> DataInModel._distrib_specific_packet ]

* _datain_factory _[DataFactory]_ : On doit créer un objet qui va vérifier les données de la seconde couche de données du paquet
* _distrib_specific_packet _[dict]_ : On va créer une méthode qui va s'occuper d'effectuer une action spécifique en fonction du paquet

### Création du paquet

Pour qu'un paquet soit accepté, il faut créer un nouvel objet en prenant le chemin suivant :

* **_Model.DataObject.famille_de_votre_paquet.nom_du_paquet_**

Plusieurs paquets sont déjà créés donc prenez le temps de bien comprendre son fonctionnement.
Chaque objet DataIn hérite d'un objet de famille _(BaseDataLog | BaseDataAccessor | BaseDataDraw | BaseDataSending)_

Dans ces objects, il y a 4 méthodes importantes :

* **check_obligatory_data()** :
On doit tester par des **assert** toutes les données qui sont **OBLIGATOIRES** sans lesquelles le paquet ne sera pas conforme et sera rejeté.

* **check_optional_data()** :
On doit tester par des **assert** toutes les données **OPTIONNELLES** et combler par des valeurs défauts les paramètres qui ne sont pas remplis.

* **get_default_data_dict()** :
Doit retourner un paquet de données par défaut. Cette méthode est utilisée par le _DataOutModel_ lorsque l'on va vouloir envoyer un paquet.

* **get_type()** :
Doit retourner le numéro de type _(int)_ du paquet. Cette méthode est utilisée par la _DataFactory_ afin d'indexer l'objet avec le paquet correspondant.

/ ! \   Explicitez le message d'erreur provoqué par chaque **assert** afin que l'utilisateur ait le plus d'informations possibles   / ! \

### Traitement du paquet

Une fois que le paquet est vérifié, la _DataFactory_ va retourner un _DataIn_ au _DataInModel_ qui va s'occuper d'excuter une méthode en fonction du paquet.
Cette méthode est stocké dans un dictionnaire et est indexé par le nom du _DataIn_

Pour traiter le _DataIn_, vous devez faire les étapes suivantes :

* **Définir la méthode de traitement du paquet** :
Vous devez créer une méthode de la forme qui suit en sachant que l'argument _data_ de la méthode correspond à l'objet _DataIn_
```python
def _distrib_NOM_DE_DATAIN(self, data):
        """ Traite le paquet spécifique NOM_DE_DATAIN """
        ...
```

* **Indexer le _DataIn_ avec la méthode adéquate** :
Pour indexer, allez dans la méthode _DataInModel._init_distributor. C'est à cet endroit que vous allez ajouter la ligne qui suit.
```python
self._distrib_specific_packet[NOM_DE_DATAIN.__name__] = self._distrib_NOM_DE_DATAIN
```

**BRAVO ! Vous venez de créer un tout nouveau paquet ! CONGRATZ..**

## Créer un nouveau dessin
Voici les étapes à suivre pour créer un nouveau dessin :

* Déterminer les caractéristiques du dessin
* Créer un nouveau paquet de communication _(voir rubrique précédente)_
* Créer l'objet dessin correspondant

### Déterminer les caractéristiques du dessin
Les dessins utilisent les méthodes de l'objet _QPainter_ qui sont disponibles par ce [lien](http://pyqt.sourceforge.net/Docs/PyQt4/qpainter.html).
Le parcours de toutes ces méthodes va vous permettre de déterminer les paramètres dont vous avez besoin.

```
Exemple :
Pour une ligne droite, il s'agit de la méthode QPainter.drawLine(). En observant la documentation, je peux déterminer qu'il me faut :
  - Un point de départ
  - Un point d'arrivée
  - Une couleur de trait
  - Un type de trait
  - Une épaisseur de trait
```

Bien évidemment, vous pouvez augmenter ou réduire la compléxité de votre dessin à votre guise !

### Créer un nouveau paquet de communication
Rappelez vous qu'il existe une _famille Dessin_ dans les paquets de communication. Je vous invite donc à suivre les étapes de la [rubrique correspondante](#paquet-de-communication)

### Créer l'objet dessin correspondant
Il existe deux types de dessins. Ceux qui sont fixes _(exemple DrawLine)_ et ceux qui sont mobiles _(exemple robot)_ qui se trouve dans ```Controller > DrawingObject/MobileObject```.

Pour le cas du dessin, créer un nouveau fichier dans le chemin suivant : ```Controller > DrawingObject > NOM_DU_DESSINDrawing.py```

Prenons l'exemple du ```LineDrawing``` :
```python
class LineDrawing(BaseDrawingObject):
    def __init__(self, data_in):
        BaseDrawingObject.__init__(self, data_in)

    def draw(self, painter):
        if self.isVisible():
            # == SET PEN == 
            painter.setPen(QtToolBox.create_pen(color=self.data['color'],
                                                style=self.data['style'],
                                                width=self.data['width']))
                                                
            # == SET BRUSH == 
            painter.setBrush(QtToolBox.create_brush(is_visible=False))
            
            # == SET DRAW == 
            x1, y1, _ = QtToolBox.field_ctrl.convert_real_to_scene_pst(*self.data['start'])
            x2, y2, _ = QtToolBox.field_ctrl.convert_real_to_scene_pst(*self.data['end'])
            painter.drawLine(x1, y1, x2, y2)

    @staticmethod
    def get_datain_associated():
        return DrawLineDataIn.__name__
```

Voici les étapes importantes lors de la création de l'objet :

* ```LineDrawing``` hérite de ```BaseDrawingObject```

* La méthode ```def draw(self, painter):``` est celle qui sera appelée par un signal à chaque rafraîchissement de la fenêtre. _(Pour des raisons d'optimisation, nous utilisons cette manière et non celle Orienté Objet que propose PyQt)_

    * Dans cette méthode, il faut mettre la condition ```if self.isVisible():``` obligatoirement, sans laquelle nous ne pourrons pas contrôler la visibilité du dessin (filtre, timeout, etc.)

    * Il faut toujours assigner le PEN et le BRUSH avant de dessiner. Dans le cas contraitre vous vous retrouverez avec le PEN et BRUSH du dessin précédent.
    
    * Lorsque vous utilisez des coordonnées pour dessiner, gardez toujours à l'esprit que les coordonnées sur le terrain ne sont pas les mêmes que sur l'écran. Utilisez l'objet QtToolBox.field_ctrl pour convertir ces derniers.

* La méthode ```def get_datain_associated():``` retourne le nom du _DataIn_ associé à ce dessin.

```
REMARQUE:
Vous pouvez vous aider de l'objet Controller.QtToolBox pour créer vos dessins.
```

## Créer un nouveau widget Model / View
### Architecture MVC

Nous appliquons le modèle MVC (modèle-vue-contrôleur) à l'UI-debug.

<p><a href="https://commons.wikimedia.org/wiki/File:ModeleMVC.png#/media/File:ModeleMVC.png"><img src="https://upload.wikimedia.org/wikipedia/commons/6/63/ModeleMVC.png" alt="ModeleMVC.png" height="480" width="578"></a><br>Par <a href="//commons.wikimedia.org/w/index.php?title=User:Deltacen&amp;action=edit&amp;redlink=1" class="new" title="User:Deltacen (page does not exist)">Deltacen</a> — <span class="int-own-work" lang="fr">Travail personnel</span>, <a href="http://creativecommons.org/licenses/by-sa/3.0" title="Creative Commons Attribution-Share Alike 3.0">CC BY-SA 3.0</a>, <a href="https://commons.wikimedia.org/w/index.php?curid=23724069">https://commons.wikimedia.org/w/index.php?curid=23724069</a></p>

* **M pour Modèle (Model) :**
    Le modèle représente le cœur (algorithmique) de l'application : traitements des données, interactions avec la base de données, etc. Il décrit les données manipulées par l'application. Il regroupe la gestion de ces données et est responsable de leur intégrité. La base de données sera l'un de ses composants. Le modèle comporte des méthodes standards pour mettre à jour ces données (insertion, suppression, changement de valeur). Il offre aussi des méthodes pour récupérer ces données. Les résultats renvoyés par le modèle ne s'occupent pas de la présentation. Le modèle ne contient aucun lien direct vers le contrôleur ou la vue. Sa communication avec la vue s'effectue au travers du patron Observateur.
    
    Le modèle peut autoriser plusieurs vues partielles des données. Si par exemple le programme manipule une base de données pour les emplois du temps, le modèle peut avoir des méthodes pour avoir tous les cours d'une salle, tous les cours d'une personne ou tous les cours d'un groupe de TD.

* **V pour Vue (View) :**
    Ce avec quoi l'utilisateur interagit se nomme précisément la vue. Sa première tâche est de présenter les résultats renvoyés par le modèle. Sa seconde tâche est de recevoir toute action de l'utilisateur (hover, clic de souris, sélection d'un bouton radio, cochage d'une case, entrée de texte, de mouvements, de voix, etc.). Ces différents événements sont envoyés au contrôleur. La vue n'effectue pas de traitement, elle se contente d'afficher les résultats des traitements effectués par le modèle et d'interagir avec l'utilisateur.
    
    Plusieurs vues peuvent afficher des informations partielles ou non d'un même modèle. Par exemple si une application de conversion de base a un entier comme unique donnée, ce même entier peut être affiché de multiples façons (en texte dans différentes bases, bit par bit avec des boutons à cocher, avec des curseurs). La vue peut aussi offrir à l'utilisateur la possibilité de changer de vue. Ceci permet une certaine récursivité du modèle.

* **C pour Contrôleur (Controller) :**
    Le contrôleur prend en charge la gestion des événements de synchronisation pour mettre à jour la vue ou le modèle et les synchroniser. Il reçoit tous les événements de la vue et enclenche les actions à effectuer. Si une action nécessite un changement des données, le contrôleur demande la modification des données au modèle afin que les données affichées se mettent à jour. D'après le patron de conception observateur/observable, la vue est un « observateur » du modèle qui est lui « observable ». Certains événements de l'utilisateur ne concernent pas les données mais la vue. Dans ce cas, le contrôleur demande à la vue de se modifier. Le contrôleur n'effectue aucun traitement, ne modifie aucune donnée. Il analyse la requête du client et se contente d'appeler le modèle adéquat et de renvoyer la vue correspondant à la demande.
    
    Par exemple, dans le cas d'une base de données gérant les emplois du temps des professeurs d'une école, une action de l'utilisateur peut être l'entrée (saisie) d'un nouveau cours. Le contrôleur ajoute ce cours au modèle et demande sa prise en compte par la vue. Une action de l'utilisateur peut aussi être de sélectionner une nouvelle personne pour visualiser tous ses cours. Ceci ne modifie pas la base des cours mais nécessite simplement que la vue s'adapte et offre à l'utilisateur une vision des cours de cette personne.
    
    Quand un même objet contrôleur reçoit les événements de tous les composants, il lui faut déterminer l'origine de chaque événement. Ce tri des événements peut s'avérer fastidieux et peut conduire à un code peu élégant (un énorme switch). C'est pourquoi le contrôleur est souvent scindé en plusieurs parties dont chacune reçoit les événements d'une partie des composants.

``` source: https://fr.wikipedia.org/wiki/Modèle-vue-contrôleur```

### Ajouter un widget
Dans notre architecture, nous allons considéré comme **widget** un modèle ou une vue, puisqu'il n'y a qu'un seul contrôleur.

* **Widget: Modèle**
    Actuellement, chaque Modèle tourne sur son propre **_thread_** pour pouvoir mettre à jour régulière ses données.
    
    Donc il faut simplement créer une classe qui hérite de ```threading.Thread```. Pour des raisons de performance, nous n'utilisons pas la classe **_QThread_** qui est fourni avec PyQt4 puisqu'elle fonctionne très mal à haute fréquence d'utilisation.
    
    ________
    **_Exemple:_**
    ModelFrame récupère les données provenants du système de vision ou simulateur (grSim) via un serveur UDP. Il met à jour les données à chaque fois qu'il récupère un nouveau paquet de frame.

* **Widget: Vue**
    Les Vues est un ```QtGui.QWidget``` que vous pouvez représenter comme bon vous semble.
    Voici une classe standard de Vue:
    
    ```python
    from PyQt4 import QtGui
    
    class View(QtGui.QWidget):
        def __init__(self, controller=None):
            super().__init__()
            self.controller = controller
            self.main_layout = QtGui.QVBoxLayout(self)
            self.label_welcome = QtGui.QLable('HelloWorld!')
            ...
            
            # === INIT ===
            self.init_ui()
            ...
        
        def init_ui(self):
            self.setLayout(self.main_layout)
            self.main_layout.addWidget(self.label_welcome)
            ...
    ```
    Les Widgets fonctionnent avec un système de calques _(Layout)_ que vous devez utiliser pour rendre votre interface agréable pour l'utilisateur (cf: [QLayout](http://web.univ-pau.fr/~puiseux/enseignement/python/tutoQt-zero/tuto-PyQt-zero.7.html)).
    ```python
    # Exemple Utilisation Calque:
    self.main_layout = QtGui.QVBoxLayout(self)
    ...
    self.setLayout(self.main_layout)
    ...
    ```
    Dans ces calques vous pourrez intégrer des fenêtres / boutons / afficheurs / champs / conteneurs / etc. en fonction de vos besoins (cf: [Base QtGui](http://web.univ-pau.fr/~puiseux/enseignement/python/tutoQt-zero/tuto-PyQt-zero.8.html)).
    ```python
    # Exemple Utilisation Label:
    self.label_welcome = QtGui.QLable('HelloWorld!')
    ...
    self.main_layout.addWidget(self.label_welcome)
    ...
    ```

### Intéragir entre widget

La règle est très simple: Toutes les intéractions entre widgets doivent passer par le Contrôleur.
Une _Vue_ qui veut obtenir certaines informations dans un _Modèle_ doit faire comme suit :
```
class Controller:
    def __init__(self):
        self.model = Model(controller=self)
        self.view = View(controller=self)
    ...
    def model_get_ball_position(self):
        return self.model.get_ball_position()
    ...
    
class View:
    def __init__(self, controller=None):
        self.controller = controller
    ...
     def view_get_ball_position(self):
        return self.controler.model_get_ball_position()
    ...

class Model:
    def __init__(self, controller=None):
        self.controller = controller
    ...
    def get_ball_position(self):
        return ball_pst
    ...
    
```

C'est le contrôleur qui est responsable des widgets (Création / Destruction / Interaction).
Ce qui signifie que pour chaque nouveau widget, vous devez l'instancier dans le contrôleur.
