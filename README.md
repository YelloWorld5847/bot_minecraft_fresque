
# Animation Minecraft Command Generator

Ce projet permet de créer une animation à l'aide de commandes Minecraft basées sur une image d'entrée. Les commandes sont générées pour Minecraft et réparties dans des fichiers `.mcfunction` en fonction de leur taille. Le script est conçu pour inverser l'ordre de création de la fresque (de bas en haut).
vidéo de démonstration : https://youtu.be/QHdG7ZzVEB8

---

## Fonctionnalités

- **Création d'animations à partir d'images** : Transforme une image en commandes Minecraft.
- **Gestion des fichiers `.mcfunction`** : Divise les commandes en plusieurs fichiers si nécessaire.
- **Inversion de l'ordre de création** : Les commandes sont générées de bas en haut.
- **Personnalisation des couleurs** : Associe les couleurs des blocs Minecraft aux pixels de l'image.

---

## Prérequis

1. Bibliothèques Python requises :
   - `numpy`
   - `Pillow`
   - `matplotlib`
2. Accès au dossier `development_behavior_packs` de Minecraft Bedrock Edition.

---

## Installation

Clonez ce dépôt, puis installez les dépendances avec la commande suivante :

```bash
pip install numpy pillow matplotlib
