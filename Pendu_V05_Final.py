# JEU DU PENDU (avec interface Tkinter, dégradé rouge, gestion difficulté croissante)

# --- IMPORTATIONS ---
import random                          # Pour tirer un mot aléatoire dans la liste
import sys                             # Pour accéder à certaines informations système (ex: dossier du script)
import tkinter as tk                   # Pour créer l'interface graphique
from tkinter import messagebox         # Pour afficher des boîtes de dialogue (alertes, informations)
from pathlib import Path               # Pour manipuler les chemins de fichiers de manière portable
import unicodedata                     # Pour retirer les accents des lettres facilement (utile pour comparer les mots sans erreur)

# --- LOCALISATION DU FICHIER DE MOTS ---
if hasattr(sys, "_MEIPASS"):           # Si on est dans un exécutable PyInstaller (mode compilation en .exe)
    current_dir = Path(sys._MEIPASS)  # On récupère le dossier temporaire où les fichiers sont extraits par PyInstaller
elif "__file__" in globals():         # Si on exécute un script Python classique
    current_dir = Path(__file__).resolve().parent  # On prend le dossier où se trouve le script
else:                                  # Sinon (cas rare : exécution en REPL, notebook, ou environnement inconnu)
    current_dir = Path.cwd()           # On prend le répertoire courant de travail

file_path = current_dir / "liste_francais.txt"  # Chemin complet vers le fichier de mots à utiliser

# --- CHARGEMENT DES MOTS ---
mots = []                              # Liste vide qui contiendra tous les mots du fichier
if file_path.exists():                  # Vérifie si le fichier de mots existe
    try:
        with open(file_path, "r", encoding="cp1252") as file:  # On essaye de lire le fichier avec encodage Windows
            mots = [ligne.strip() for ligne in file if ligne.strip()]  # On garde les lignes non vides et on retire les espaces
    except UnicodeDecodeError:         # Si le fichier n'est pas encodé en cp1252
        with open(file_path, "r", encoding="utf-8") as file:   # On tente avec UTF-8 (plus courant sur Linux/Mac)
            mots = [ligne.strip() for ligne in file if ligne.strip()]  # Même opération de nettoyage
else:
    messagebox.showerror("Erreur", f"Fichier introuvable : {file_path}")  # Alerte à l’utilisateur si le fichier est absent
    sys.exit(1)                        # Quitte le programme proprement

# --- OUTILS ---
def enlever_accents(texte):
    # Supprime les accents d'un texte pour faciliter la comparaison des lettres (ex: é -> e).
    texte_normalise = unicodedata.normalize('NFD', texte)  # Décompose les caractères accentués en base + accent séparé
    return ''.join(c for c in texte_normalise if unicodedata.category(c) != 'Mn')  # On supprime les marques d’accents

def definir_valeur_entiere(mot):
    # Calcule la "difficulté" du mot en fonction du nombre de lettres uniques (plus il y a de lettres différentes, plus c’est dur)
    lettres_uniques = {lettre for lettre in mot if lettre.isalpha()}  # Ensemble des lettres uniques
    return len(lettres_uniques)  # Retourne le nombre de lettres distinctes comme indicateur de difficulté

# --- INITIALISATION DE BASE ---
code_debug = "DEBUG"                 # Code spécial que l’utilisateur peut entrer pour afficher le mot secret (mode dev)
mot = random.choice(mots).upper()    # Choisit un mot aléatoire dans la liste et le met en majuscules
mot = enlever_accents(mot)           # On retire les accents pour standardiser les comparaisons
mot_affiche = "_" * len(mot)         # Mot caché affiché sous forme de underscores (_)
tentatives = definir_valeur_entiere(mot) * 2  # Donne deux essais par lettre unique
lettres_donnees = []                 # Liste qui garde les lettres déjà proposées par le joueur
nb_parties = 0                        # Compteur du nombre total de parties jouées
difficultee = 0                       # Niveau de difficulté progressif qui augmente au fil des parties
nb_victoires = 0                      # Nombre de victoires totales du joueur

# --- STYLES ET COULEURS ---
BG_COLOR = "#1E1E1E"                 # Couleur de fond initiale (gris foncé)
TEXT_COLOR = "#D4D4D4"               # Couleur principale du texte
ACCENT_COLOR = "#569CD6"             # Couleur d'accentuation (non utilisée ici, mais prête pour des évolutions)
current_rgb = (30, 30, 30)           # Couleur de fond en format RGB utilisée pour générer le dégradé vers le rouge

# --- FENÊTRE PRINCIPALE ---
fenetre = tk.Tk()                     # Création de la fenêtre principale Tkinter
fenetre.title("Jeu du Pendu")         # Définit le titre affiché sur la barre de la fenêtre
fenetre.geometry("400x400")           # Définit la taille fixe de la fenêtre (400x400 pixels)
fenetre.resizable(False, False)       # Empêche l’utilisateur de redimensionner la fenêtre
fenetre.configure(bg=BG_COLOR)        # Définit la couleur de fond de base

# --- ÉLÉMENTS INTERFACE ---
label_mot = tk.Label(fenetre, text=mot_affiche, font=("Courier", 22), bg=BG_COLOR, fg=TEXT_COLOR)  # Label qui montre le mot caché
label_mot.pack(pady=20)              # Placement du label du mot avec un espacement vertical

label_info = tk.Label(fenetre, text=f"Nombre de tentatives : {tentatives}", font=("Arial", 12), bg=BG_COLOR, fg=TEXT_COLOR)
label_info.pack()                     # Label informant du nombre d’essais restants

label_lettres = tk.Label(fenetre, text="Lettres données : ", font=("Arial", 12), bg=BG_COLOR, fg=TEXT_COLOR)
label_lettres.pack(pady=10)          # Label affichant les lettres déjà proposées

entree = tk.Entry(fenetre, font=("Arial", 14), width=5, justify="center", bg="#252526", fg=TEXT_COLOR, insertbackground=TEXT_COLOR)
entree.pack()                         # Zone de saisie où l’utilisateur entre une lettre ou un mot complet

# --- COULEUR DYNAMIQUE : DÉGRADÉ VERS LE ROUGE ---
def rgb_to_hex(rgb):
    # Convertit une couleur RGB (tuple) en code hexadécimal compréhensible par Tkinter.
    return '#{:02X}{:02X}{:02X}'.format(*rgb)

def tendre_vers_rouge(rgb, r_incr=5, g_decr=5, b_decr=5):
    # Fait progressivement évoluer la couleur du fond vers le rouge à chaque erreur du joueur.
    r, g, b = rgb
    r = min(255, r + r_incr)  # Augmente la composante rouge
    g = max(0, g - g_decr)    # Diminue la composante verte
    b = max(0, b - b_decr)    # Diminue la composante bleue
    return (r, g, b)          # Retourne la nouvelle couleur RGB

def mettre_a_jour_couleur_fond():
    # Met à jour dynamiquement la couleur de fond pour créer un effet visuel de "stress" quand on perd des tentatives.
    global current_rgb
    current_rgb = tendre_vers_rouge(current_rgb)
    nouvelle_couleur = rgb_to_hex(current_rgb)
    fenetre.configure(bg=nouvelle_couleur)
    label_mot.configure(bg=nouvelle_couleur)
    label_info.configure(bg=nouvelle_couleur)
    label_lettres.configure(bg=nouvelle_couleur)

# --- GESTION DE LA PROPOSITION ---
def proposer_lettre():
    global mot_affiche, tentatives, mot, lettres_donnees, nb_victoires
    proposition = entree.get().strip().upper()  # Récupère le texte entré (lettre ou mot) et le met en majuscules
    entree.delete(0, tk.END)  # Vide le champ après lecture

    if proposition == code_debug:  # Si le joueur entre "DEBUG", on affiche le mot caché
        fenetre_debugage()
        return  

    if not proposition.isalpha():  # Vérifie que la saisie contient uniquement des lettres
        messagebox.showinfo("Erreur", "Merci d’entrer une lettre ou un mot valide.")
        return

    if proposition == mot:  # Si le joueur devine directement le mot entier
        mot_affiche = mot
        label_mot.config(text=mot_affiche)
        messagebox.showinfo("Victoire", f"Bravo ! Vous avez trouvé le mot : {mot}")
        nb_victoires += 1
        return

    if len(proposition) > 1:  # Si la saisie contient plus d’une lettre mais n’est pas le bon mot
        messagebox.showinfo("Erreur", "Proposez soit une lettre, soit le mot entier.")
        return

    lettre = proposition
    if lettre in lettres_donnees:  # Empêche de reproposer une lettre déjà utilisée
        messagebox.showinfo("Information", f"La lettre '{lettre}' a déjà été donnée.")
        return

    lettres_donnees.append(lettre)  # Ajoute la lettre à la liste des propositions
    label_lettres.config(text="Lettres données : " + " ".join(lettres_donnees))

    if lettre not in mot:  # Si la lettre n’est pas dans le mot
        tentatives -= 1  # On perd une tentative
        label_info.config(text=f"Tentatives restantes : {tentatives}")
        mettre_a_jour_couleur_fond()  # Fait évoluer le fond vers le rouge
        if tentatives == 0:  # Si plus de tentatives, le joueur perd
            messagebox.showinfo("Perdu", f"Vous avez perdu.\nLe mot était : {mot}")
            bouton_proposer.config(state="disabled")  # Désactive le bouton pour éviter de continuer
        return

    # Mise à jour du mot affiché quand la lettre est correcte
    nouveau_affiche = ""
    for i in range(len(mot)):
        if mot[i] == lettre:
            nouveau_affiche += lettre
        else:
            nouveau_affiche += mot_affiche[i]
    mot_affiche = nouveau_affiche
    label_mot.config(text=mot_affiche)

    if mot_affiche == mot:  # Si toutes les lettres ont été trouvées
        messagebox.showinfo("Victoire", f"Bravo ! Vous avez trouvé le mot : {mot}")
        nb_victoires += 1
        nouvelle_partie()  # Lance une nouvelle partie automatiquement

# --- BOUTON POUR VALIDER UNE LETTRE ---
bouton_proposer = tk.Button(fenetre, text="Proposer", command=proposer_lettre, font=("Arial", 12),
                            bg=BG_COLOR, fg="white", activebackground="#1177BB", activeforeground="white")
bouton_proposer.pack(pady=10)  # Bouton principal qui déclenche la vérification de la saisie

# --- NOUVELLE PARTIE ---
def nouvelle_partie():
    # Réinitialise le jeu avec un nouveau mot, ajuste la difficulté et réinitialise les compteurs.
    global mot, mot_affiche, tentatives, lettres_donnees, nb_parties, difficultee, nb_victoires
    if nb_victoires >= 1:  # Si le joueur a gagné au moins une fois
        bouton_Nouvelle.config(state="disabled")  # On désactive le bouton de nouvelle partie
        fenetre_victoire()  # On affiche la fenêtre d’animation de victoire
    if nb_parties <= 10:                    # On limite à 10 parties avant de stabiliser la difficulté
        if nb_parties % 2 == 0:            # Augmente la difficulté toutes les deux parties
            difficultee += 1
        mot = random.choice(mots).upper()  # Tire un nouveau mot au hasard
        mot = enlever_accents(mot)
        mot_affiche = "_" * len(mot)
        tentatives = definir_valeur_entiere(mot) * 2 - difficultee  # Moins de tentatives avec la difficulté
        while tentatives <= 1:             # On garantit au moins une tentative possible
            tentatives += 1
        lettres_donnees = []               # Réinitialise la liste des lettres
        label_mot.config(text=mot_affiche)
        label_info.config(text=f"Tentatives restantes : {tentatives}")
        label_lettres.config(text="Lettres données : ")
        bouton_proposer.config(state="normal")  # Réactive le bouton si besoin
        nb_parties += 1                     # Incrémente le compteur de parties jouées
        
        mettre_a_jour_couleur_fond()      # Continue le dégradé de fond rouge au fil du jeu

# --- FENÊTRE DE DÉBUGGAGE ---
def fenetre_debugage():
    # Ouvre une petite fenêtre secondaire affichant le mot actuel (utile pour le test ou le développement).
    global mot
    fenetre_debug = tk.Tk()
    fenetre_debug.title("Débug jeu du pendu - Programmeur mode")
    fenetre_debug.geometry("400x50")
    fenetre_debug.resizable(True, True)
    fenetre_debug.configure(bg=BG_COLOR)
    label_info_01 = tk.Label(fenetre_debug, text=f"Le mot actuel est {mot}", font=("Arial", 12),
                             bg=BG_COLOR, fg=TEXT_COLOR)
    label_info_01.pack()

# --- UTILITÉ : CHARGER UN GIF ANIMÉ (sans Pillow) ---
def load_gif_frames(gif_path: Path):
    # Charge toutes les frames d’un GIF animé manuellement sans dépendances externes.
    if not gif_path.exists():
        raise FileNotFoundError(f"GIF non trouvé : {gif_path}")  # Lève une erreur si le GIF est absent
    frames = []
    i = 0
    while True:
        try:
            frame = tk.PhotoImage(file=str(gif_path), format=f"gif -index {i}")  # Charge chaque frame du GIF
            frames.append(frame)
            i += 1
        except tk.TclError:  # Arrête la boucle quand il n’y a plus de frame
            break
    if not frames:  # Si aucune frame détectée, charge une image fixe
        frames.append(tk.PhotoImage(file=str(gif_path)))
    return frames

# --- FENÊTRE DE VICTOIRE (avec GIF animé sans Pillow) ---
def fenetre_victoire():
    # Crée une nouvelle fenêtre pour célébrer la victoire du joueur avec animation GIF.
    gif_path = current_dir / "victoire.gif"  # Chemin vers le fichier du GIF de victoire

    fenetre_victory = tk.Toplevel(fenetre)  # Crée une fenêtre secondaire (non bloquante)
    fenetre_victory.title("VICTOIRE !! 🎉")
    fenetre_victory.geometry("500x500")
    fenetre_victory.configure(bg="#000000")  # Fond noir pour mieux voir le GIF

    txt = tk.Label(fenetre_victory, text="Bravo ! Vous avez gagné !", font=("Helvetica", 16, "bold"),
                   bg="#000000", fg=TEXT_COLOR)
    txt.pack(pady=10)  # Affiche un texte de félicitations

    gif_container = tk.Label(fenetre_victory, bg="#000000")
    gif_container.pack(expand=True)  # Zone qui contiendra l’animation

    try:
        frames = load_gif_frames(gif_path)  # Charge les frames du GIF
    except FileNotFoundError:
        info = tk.Label(fenetre_victory,
                        text=f"(Aucun GIF 'victory.gif' trouvé dans :\n{current_dir}\nPlacez votre GIF ici pour l'animer.)",
                        font=("Arial", 10), bg=BG_COLOR, fg=TEXT_COLOR, justify="center")
        info.pack(pady=10)
        return

    fenetre_victory.victory_frames = frames  # Sauvegarde les frames dans l’objet pour éviter leur suppression
    fenetre_victory._after_id = None         # Identifiant pour stopper proprement l’animation

    def animate(idx=0):
        # Boucle d’animation affichant les frames du GIF une par une avec un délai fixe.
        frame = fenetre_victory.victory_frames[idx]
        gif_container.config(image=frame)
        gif_container.image = frame
        next_idx = (idx + 1) % len(fenetre_victory.victory_frames)
        fenetre_victory._after_id = fenetre_victory.after(100, animate, next_idx)  # 100 ms par frame (10 FPS)

    def on_close():
        # Ferme proprement la fenêtre et annule l’animation si elle est en cours
        if getattr(fenetre_victory, "_after_id", None):
            try:
                fenetre_victory.after_cancel(fenetre_victory._after_id)
            except Exception:
                pass
        fenetre_victory.destroy()

    fenetre_victory.protocol("WM_DELETE_WINDOW", on_close)  # Gère la fermeture correcte de la fenêtre
    animate(0)  # Démarre l’animation dès l’ouverture

# --- BOUTON NOUVELLE PARTIE ---
bouton_Nouvelle = tk.Button(fenetre, text="Nouvelle partie", command=nouvelle_partie,
                            font=("Arial", 11), bg=BG_COLOR, fg="white",
                            activebackground="#1177BB", activeforeground="white")
bouton_Nouvelle.pack(pady=10)  # Bouton pour relancer une partie après victoire ou défaite

# --- LANCEMENT DU PROGRAMME ---
fenetre.mainloop()  # Démarre la boucle principale Tkinter (interface interactive)