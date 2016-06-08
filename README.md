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
paquet = {'name': str(nomDuDestinataire),
          'type': int(numéroTypeDonnée),
          'data': dict(données)}
```

#### Type de données

Type | Famille | Données du paquet | Description
---- | ------- | ----------------- | ---------------------------------------------------------------
0    | Test    |                   |
1    | Logger  | 'data_1': int/str | Affiche un nombre de données arbitraire dans la fenêtre de log
     |         | 'data_N': int/str |
2    | Logger  | 'level': int      | Affiche un message avec un niveau d'information
     |         | 'message': str    |

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
