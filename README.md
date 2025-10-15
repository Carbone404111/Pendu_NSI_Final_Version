# Pendu_NSI_Final_Version
La version finale du jeu du pendu 
 Jeu du Pendu – Interface Tkinter avec gestion de difficulté et effets visuels

Ce projet implémente un **jeu du pendu complet en Python**, avec une interface graphique développée à l’aide de **Tkinter**.  
Le jeu inclut un **système de difficulté progressive**, un **effet visuel de dégradé vers le rouge** lors des erreurs, et une **animation de victoire** sans dépendance externe.

---

## Sommaire

1. [Présentation]
2. [Fonctionnalités]
3. [Structure du projet] 
4. [Installation et exécution]
5. [Fichiers requis]
6. [Utilisation]
7. [Mode développeur]
8. [Dépendances]
9. [Licence]

---

## Présentation

Ce projet a pour objectif de proposer une version modernisée du **jeu du pendu**, en mettant l’accent sur :

- une interface graphique simple et intuitive,
- une évolution progressive de la difficulté,
- des retours visuels dynamiques selon les performances du joueur.

L’ensemble du code est écrit en **Python pur**, sans dépendances externes, pour garantir une **compatibilité multiplateforme** (Windows, macOS, Linux).

---

## Fonctionnalités

- **Interface Tkinter complète** : zone de saisie, affichage dynamique du mot, compte des tentatives et des lettres proposées.  
- **Effet visuel de dégradé rouge** : la couleur d’arrière-plan s’intensifie à mesure que le joueur commet des erreurs.  
- **Difficulté progressive** : le nombre de tentatives autorisées diminue au fil des parties.  
- **Fichier de mots externe** : la liste des mots est stockée dans un fichier texte personnalisable.  
- **Mode débogage intégré** : affichage du mot courant via un mot-clé spécial (`DEBUG`).  
- **Animation de victoire** : affichage d’un GIF animé en cas de réussite (sans bibliothèque tierce).  

---

## Structure du projet

JeuDuPendu/
│
├── pendu_V05_Final.py # Script principal du jeu
├── liste_francais.txt # Liste de mots utilisés pour les parties
├── victoire.gif # Animation affichée lors d’une victoire
└── README.md # Documentation du projet

---

## Installation et exécution

### Prérequis

- Python **3.8 ou supérieur**
- Aucune bibliothèque externe requise

### Étapes d’installation

1. Cloner le dépôt :
   ```bash
   git clone https://github.com/Carbone404111/Pendu_NSI_Final_Version
