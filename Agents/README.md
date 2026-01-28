# Défi de Sauvetage par Robot 🤖🔥

## Aperçu

Un robot doit naviguer dans un bâtiment en feu pour secourir une personne piégée. Votre tâche est d'implémenter un algorithme de sauvetage efficace qui trouve un chemin sûr vers la personne, la récupère et la ramène à la sortie.

## Description du Problème

Vous contrôlez un robot de sauvetage opérant sur une grille 2D. Le robot doit :

1. **Naviguer vers la personne** piégée dans le bâtiment (position connue)
2. **Éviter les cases en feu** qui détruiront le robot
3. **Retourner à la sortie** avec la personne

### Règles

- Le robot **commence à la sortie**
- Il y a **exactement une personne** à secourir
- La **position de la personne est connue** dès le départ
- Quand le robot atteint la case avec une personne, il **la porte automatiquement**
- Quand le robot (portant une personne) atteint la sortie, la **mission se termine avec succès**
- Si le robot marche sur une **case en feu**, il est **détruit** et la mission échoue immédiatement
- Vous ne pouvez pas utiliser de librairie qui résout le problème en entier, mais vous avez le droit d'utiliser des librairies qui simplifient la solution (ex: Numpy). (Aucune librairie n'est nécessaire.)
- Svp inclure un fichier requirements.txt si vous utilisez une librairie.

### Coûts en Temps

| Action | Coût en Temps |
|--------|---------------|
| Déplacement (toute direction) | 1 seconde |
| Scanner les positions des feux | 10 secondes |
| Détecter les feux à proximité | Gratuit |

## API du Robot

### Déplacement

```python
robot.move(Direction.FORWARD)   # Aller vers le haut (y décroissant)
robot.move(Direction.BACKWARD)  # Aller vers le bas (y croissant)
robot.move(Direction.LEFT)      # Aller à gauche (x décroissant)
robot.move(Direction.RIGHT)     # Aller à droite (x croissant)
```

Retourne `True` si le déplacement a réussi, `False` si bloqué (hors limites).

**Note :** Se déplacer sur une case en feu détruit le robot immédiatement. Se déplacer vers la sortie en portant une personne termine la mission avec succès.

### Capteurs

```python
# Compter les feux dans les cases adjacentes (4 directions cardinales) - GRATUIT
nombre_feux = robot.sense_fires_around()

# Obtenir les positions exactes des feux dans les cases environnantes - COÛTE 10 SECONDES
positions_feux = robot.scan_fires()  # Retourne Set[Position]
```

### État

```python
robot.position              # Position actuelle Position(x, y)
robot.is_carrying_person    # True si porte quelqu'un
robot.time_elapsed          # Total des secondes écoulées
```

### Informations sur la Grille

```python
largeur, hauteur = robot.get_grid_dimensions()
pos_sortie = robot.get_exit_position()
pos_personne = robot.get_person_position()  # Position connue de la personne
```

## Structure des Fichiers

```
Agents/
├── grid.py              # Moteur de simulation principal (NE PAS MODIFIER)
├── robot.py             # API du robot (NE PAS MODIFIER)
├── maps.py              # Cartes de test (NE PAS MODIFIER)
├── solution.py          # VOTRE SOLUTION VA ICI
└── README.md            # Ce fichier
```

## Pour Commencer

1. Implémentez votre solution dans `solution.py`

2. Exécutez les tests pour valider :
   ```bash
   python main.py
   ```

## Format de la Grille

La grille utilise les symboles suivants :

| Symbole | Signification |
|---------|---------------|
| `.` | Case vide |
| `F` | Feu (mortel !) |
| `P` | Personne à secourir |
| `E` | Sortie (départ du robot) |

Exemple de grille :
```
. . . . .
. F . . .
. . P . .
. . . F .
E . . . .
```

## Système de Coordonnées

- L'origine `(0, 0)` est dans le **coin supérieur gauche**
- `x` augmente vers la **droite**
- `y` augmente vers le **bas**
- `Direction.FORWARD` se déplace vers des valeurs `y` plus basses (haut de la grille)
- `Direction.BACKWARD` se déplace vers des valeurs `y` plus hautes (bas de la grille)

## Notation

Votre solution sera évaluée sur :

1. **Exactitude** : La personne doit être sauvée (succès de la mission)
2. **Efficacité** : Un temps total plus bas est meilleur
3. **Robustesse** : Doit fonctionner sur diverses configurations de cartes

## Conseils

- Utilisez `sense_fires_around()` fréquemment - c'est gratuit !
- N'utilisez `()` que si absolument nécessaire (coûte 10 secondes)
- Essayez de déduire où se trouvent les feux
- La position de la personne est connue via `get_person_position()`, planifiez votre route en conséquence
- Planifiez des routes efficaces pour minimiser les retours en arrière

## Exemple de Structure de Solution

```python
def solve(robot: Robot) -> None:
    # Obtenir les infos initiales
    largeur, hauteur = robot.get_grid_dimensions()
    pos_sortie = robot.get_exit_position()
    pos_personne = robot.get_person_position()
    
    # Naviguer vers la personne (éviter les feux !)
    # ...
    
    # Retourner à la sortie avec la personne - la mission se termine automatiquement !
    # ...
```

Bonne chance, et sauvez la personne ! 🚀
