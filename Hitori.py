from upemtk import *
from fonctions_utiles import *
###Constantes###

dico_jeu = dict()
dico_jeu["HAUTEUR"] = 500
dico_jeu["LARGEUR"] = 500
dico_jeu["LARGEUR_BORD"] = 300

###Définition des fonctions###

def init_jeu (nom_fichier):
    """
    Initialise les données du jeu
    :param str: nom du fichier contenant la grille à charger
    """
    dico_jeu["grille"] = lire_grille(nom_fichier)
    dico_jeu["noircies"] = set()
    dico_jeu["historique_cases"] = []

def pixel_vers_case(grille, pixel):
    """
    Prends les coordonnées x, y en pixel d'un événement, et retourne l'abscisse et l'ordonné de la case cliquée
    param: couple (x , y) coordoonées du pixel
    return: coordonnées de la case
    >>> TAILLE_CASES = 100
    >>> pixel_vers_case((48, 56))
    (0, 0)
    >>> pixel_vers_case((425, 415))
    (4, 4)
    >>> pixel_vers_case((143, 55))
    (1, 0)
    """
    x, y = pixel
    return int((x - dico_jeu["LARGEUR_BORD"]) // (dico_jeu["HAUTEUR"] / len(grille))), int(y // (dico_jeu["HAUTEUR"] / len(grille)))
    
##Tâche 1

def lire_grille(nom_fichier):
    """
    Permet de lire une grille sauvegarder dans un fichier
    :param str: nom_fichier = nom du fichier contenant la sauvegarde
    :return lst: Grille du jeu
    """
    fichier = open(nom_fichier,"r")
    lignes = fichier.readlines()
    fichier.close()
    
    #rajoute le contenu de fichier dans la liste grille
    grille = []
    for ligne_fichier in lignes:
        ligne = []
        for case in ligne_fichier.split():
            #verifie si la case contient une bonne valeur
            try:
                int(case)
            except:
                return None
            ligne.append(case)
        grille.append(ligne)
    return grille

def afficher_grille(grille):
    """
    Permet d'afficher une grille de jeu dans le terminal
    :param lst: Grille du jeu
    """
    for ligne in grille:
        print(ligne)
    print("\n")
    

def ecrire_grille(grille, nom_fichier):
    """
    Permet de sauvegarder une grille dans un fichier .txt
    :param lst: Grille du jeu
    :param str: Nom du fichier dans lequel on souhaite sauvegarder la grille 
    """
    fichier = open(nom_fichier,"w")
    #parcours 0 au nombre de lignes
    for i in range(len(grille)):
        for j in range(len(grille[i])):
            #condition ternaire pour sauter de ligne à la fin de chaque ligne
            fichier.write(grille[i][j] + " " if (j < len(grille[i]) - 1) else grille[i][j] + "\n") 
    fichier.close()

##Tâche 2
    
def sans_voisines_noircies(grille, noircies):
    """
    Permet de vérifier si les cases noircies sont voisines ou non
    :param lst: Grille du jeu
    :param set: Ensemble des cases noircies
    :return bool: True si il n'y a qu'un seul même chiffre dans chaque case d'une ligne et d'une colonne sinon False
    >>>sans_voisines_noircies([[2, 2, 2],[3, 3, 3],[4, 4, 4]],{(0,0), (0,1),(2,2)})
    False
    >>>sans_voisines_noircies([[2, 2, 2],[3, 3, 3],[4, 4, 4]],{(0,0), (2,2)})
    True
    """
    # parcourt les cases noircies
    for cases_noircies in noircies:
        #cree la liste des cases voisines de la case noircie
        cases_noircies_voisines = voisines(grille, cases_noircies)
        
        #parcout des cases voisines de la case noircie
        for cases in cases_noircies_voisines:
            #verifie si la case noircie possèdes des voisines noircies
            if cases in noircies:
                return False
    return True
    
def sans_conflit_aux(grille, noircies, type):
    """
    Permet de vérifier si il y a la même valeur dans 2 cases de la même ligne ou colonne
    :param lst: grille du jeu
    :param set: Ensemble des cases noircies
    :return bool: True si la règle est respectée False sinon
    """
    for cases_noircies in noircies:
        if type == "ligne":
            x, y = cases_noircies
        else:
            y, x = cases_noircies
        grille[y][x] = "N"
    #parcourt ligne
    for ligne in grille:
        #parcourt valeur case
        for case in ligne:
            if ligne.count(case) >= 2 and case != "N":
                return False
    return True
    
def sans_conflit(grille, noircies):
    return sans_conflit_aux(copie_grille(grille), noircies, "ligne") and sans_conflit_aux(transposee(grille), noircies, "colonne")
    
def detecter_zone(grille, colonne, ligne, zone):
    """
    Remplit l'ensemble zone, initialement vide, de toute les cases non noire et adjacentes
    :param lst: Grille du jeu
    :param int: colonne de la case
    :param int: ligne de la case
    :param set: zone
    
    """
    #ne fait rien si la case est déjà dans zone
    if (colonne, ligne) in zone:
        pass
    else:
        #ajoute la case et vérifie les voisines si la case n'est pas noire
        if grille[ligne][colonne] != "N":
            zone.add((colonne, ligne))
            if 0 < colonne:
                detecter_zone(grille, colonne - 1, ligne, zone)
            if colonne < len(grille[ligne]) - 1:
                detecter_zone(grille, colonne + 1, ligne, zone)
            if 0 < ligne:
                detecter_zone(grille, colonne, ligne - 1, zone)
            if ligne < len(grille) - 1:
                detecter_zone(grille, colonne, ligne + 1, zone)
            
def connexe(grille, noircies):
    """
    Permet de vérifier si la grille ne forme qu'une seule zone
    :param lst: grille du jeu
    :param set: Ensemble de cases noircies
    :return bool: True si la grille ne forme qu'une seule zone, False sinon
    """
    zone = set()
    grille_bis = copie_grille(grille)
    
    #remplace les cases de la grille par un "N" si la case est noircies
    for cases_noircies in noircies:
        x, y = cases_noircies
        grille_bis[y][x] = "N"
        
    colonne, ligne = trouve_nombre(grille_bis) #pour eviter le cas ou (colonne, ligne) = "N"
    detecter_zone(grille_bis, colonne, ligne, zone) #detection d'une zone commencant par la case (colonne, ligne)
    if len(zone) != len(grille) * len(grille[0]) - len(noircies):
        return False
    return True
    
def gagne (grille, noircies):
    return sans_voisines_noircies(grille, noircies) and sans_conflit(grille, noircies) and connexe(grille, noircies)

##Tâche 3

def affiche_grille_graphique(grille, noircies):
    """
    Permet d'afficher une grille de jeu
    :param lst: Grille du jeu
    """
    rectangle(dico_jeu["LARGEUR_BORD"] - 5, 0, dico_jeu["LARGEUR_BORD"] + dico_jeu["LARGEUR"], dico_jeu["HAUTEUR"], couleur = 'black', remplissage = '#626567')
    #parcours 0 au nombre de lignes
    for i in range(len(grille)):
        #parcours 0 au nombre de colonnes
        for j in range(len(grille[i])):
            rectangle(dico_jeu["LARGEUR_BORD"] + (dico_jeu["LARGEUR"] / len(grille[i])) * j, (dico_jeu["HAUTEUR"] / len(grille)) * i + 5, dico_jeu["LARGEUR_BORD"] + (dico_jeu["LARGEUR"] / len(grille[i])) * (j + 1) - 5, (dico_jeu["HAUTEUR"] / len(grille)) * (i + 1) - 5,
            couleur = 'black', remplissage = '#AEB6BF')
            
            texte(dico_jeu["LARGEUR_BORD"] + ((dico_jeu["LARGEUR"] / len(grille[i])) * j) + dico_jeu["LARGEUR"] / (2*len(grille)) - 2, (dico_jeu["HAUTEUR"] / len(grille)) * i + dico_jeu["HAUTEUR"] / (2*len(grille[i])) - 2, grille[i][j],
            ancrage = "center", taille = '18', couleur = "black", police ="calibri")

def affiche_cases_noires(grille, noircies):
    """
    Affiche les cases noircies
    """
    for case_noire in noircies:
        x, y = case_noire
        rectangle(dico_jeu["LARGEUR_BORD"] + x * (dico_jeu["LARGEUR"] / len(grille)), y * (dico_jeu["HAUTEUR"] / len(grille)) + 5, dico_jeu["LARGEUR_BORD"] + (x + 1) * (dico_jeu["LARGEUR"]/len(grille)) - 5, (y + 1) * (dico_jeu["LARGEUR"] / len(grille)) - 5, couleur = '#373838', remplissage = '#373838')

def affiche_ext_gauche():
    """
    Permet d'afficher la partie à gauche du tableau
    """
    rectangle(0, 0, dico_jeu["LARGEUR_BORD"] - 5, dico_jeu["HAUTEUR"], couleur = 'black', remplissage = '#566573')
    
def affiche_bouton(point1, point2 ,texte_bouton, couleur_texte, taille_texte, couleur_remplissage):
    """
    Affiche un bouton contenant du texte
    :param tuple: premier point
    :param tuple: second point
    :param str: texte dans le bouton
    :param str: couleur du texte
    :param str: Taille du texte
    :param str: fond du bouton
    """
    x1, y1 = point1
    x2, y2 = point2
    rectangle(x1, y1, x2, y2, couleur = "black", remplissage = couleur_remplissage)
    texte((x1 + x2) / 2, (y1 + y2) / 2, texte_bouton, ancrage = "center", couleur = couleur_texte, police = "calibri", taille = taille_texte)

def affiche_texte(point, texte_aff, couleur_texte, taille_texte):
    """
    Permet d'afficher du texte
    :param tuple: coordonnées du points d'ancrage
    :param str: texte à afficher
    :param str: couleur du texte
    """
    x, y = point
    texte(x, y, texte_aff, couleur = couleur_texte, ancrage = "center", police = "calibri", taille = taille_texte)

def dessine_menu():
    """
    Dessine le menu du jeu
    """
    rectangle(0, 0,  dico_jeu["LARGEUR_BORD"] + dico_jeu["LARGEUR"], dico_jeu["HAUTEUR"], couleur = "#566573", remplissage = "#566573")
    affiche_texte((((dico_jeu["LARGEUR"] + dico_jeu["LARGEUR_BORD"]) / 2) + 4, dico_jeu["HAUTEUR"] / 4 - 46), "HITORI", "black", 70)
    affiche_texte(((dico_jeu["LARGEUR"] + dico_jeu["LARGEUR_BORD"]) / 2, dico_jeu["HAUTEUR"] / 4 - 50), "HITORI", "white", 70)
    affiche_bouton((280, 180), (520, 220), "Continuer", "black", 14, "ivory")
    affiche_bouton((280, 250), (520, 290), "Charger", "black", 14, "ivory")
    affiche_bouton((280, 320), (520, 360), "Quitter", "black", 14, "ivory")
    
def dessine_jeu(grille, noircies):
    """
    Dessine l'interface graphique du jeu
    :param lst: grille du jeu
    :param set: ensemble des cases noircies
    """
    affiche_ext_gauche()
    affiche_grille_graphique(grille, noircies)
    affiche_cases_noires(grille, noircies)
    affiche_bouton((20, 450), (130, 480), "Résoudre", "blue", 10, "ivory")
    affiche_bouton((170, 450), (280, 480), "Annuler", "blue", 10, "ivory")
    affiche_bouton((20, 400), (130, 430), "Menu", "blue", 10, "ivory")
    affiche_bouton((170, 400), (280, 430), "Recommencer", "blue", 10, "ivory")
    affiche_texte((85, 80), "Sans voisines :", "white", 14)
    affiche_texte((75, 160), "Sans conflit :", "white", 14)
    affiche_texte((60, 240), "Connexe :", "white", 14)

def dessine_fin_de_jeu():
    """
    Permet d'afficher l'écran de fin de partie
    """
    rectangle(0, 0,  dico_jeu["LARGEUR_BORD"] + dico_jeu["LARGEUR"], dico_jeu["HAUTEUR"], couleur = "#566573", remplissage = "#566573")
    texte((dico_jeu["LARGEUR"] + dico_jeu["LARGEUR_BORD"]) / 2, dico_jeu["HAUTEUR"] / 4 - 50, "Vous avez gagné !", couleur = 'red', ancrage = "center", police = "calibri", taille = 24)
    affiche_bouton((dico_jeu["LARGEUR_BORD"] - 70, dico_jeu["HAUTEUR"] / 4 - 75), (dico_jeu["LARGEUR_BORD"] + 280, dico_jeu["HAUTEUR"] / 4), "Vous avez gagné !", "white", 24, "#626567")
    affiche_bouton((240, 250), (390, 285), "Menu", "#F0F3F4", 14, "#AEB6BF" )
    affiche_bouton((420, 250), (570, 285), "Quitter", "#F0F3F4", 14, "#AEB6BF")
    

###Programme principal###



if __name__ == "__main__":
    
    niveau = "niveausujet.txt" #niveau de base
    init_jeu(niveau) #charge la grille de base
    
    cree_fenetre(dico_jeu["LARGEUR"] + dico_jeu["LARGEUR_BORD"], dico_jeu["HAUTEUR"])
    
    menu = True #entre dans la boucle menu
    jouer = False
    fin_de_jeu = False
        
    ##menu##
        
    while menu:
            
        #efface et dessine le menu
        efface_tout()
        dessine_menu()
            
        #recuperation des ev
        ev = donne_ev()
        ty = type_ev(ev)
            
        #gestion des ev
        if ty == 'ClicGauche':
                
            #bouton continuer
            if (280 <= abscisse(ev) <= 520) and (180 <= ordonnee(ev) <= 220):
                afficher_grille(dico_jeu["grille"])
                jouer = True
                menu = False
                
            #bouton charger
            if (280 <= abscisse(ev) <= 520) and (250 <= ordonnee(ev) <= 290):
                #chargement niveau
                niveau = input("Quel niveau voulez-vous chargez ?\n")
                
                # verification nom de niveau valide
                try :
                    init_jeu(niveau)
                    nom_valide = True
                except:
                    nom_valide = False
                    niveau = "niveausujet.txt"
                    print("Nom de niveau pas valide, entrez un nom valide s'il vous plait\n")
                    
                #verification niveau valide
                if nom_valide:
                    if dico_jeu["grille"] is not None:
                        afficher_grille(dico_jeu["grille"])
                        jouer = True
                        menu = False
                    else:
                        print("Grille non valide, entrez une grille valide s'il vous plait\n")
                        init_jeu("niveausujet.txt")
                        
            #bouton quitter
            if(280 <= abscisse(ev) <= 520) and (320 <= ordonnee(ev) <= 360):
                menu = False
                    
        #Quitte avec la croix
        if ty == 'Quitte':
            menu = False
            
        ##jeu##
            
        while jouer:
                
            #efface et dessine le jeu
            efface_tout()
            dessine_jeu(dico_jeu["grille"], dico_jeu["noircies"])
                
            #recuperation des ev
            ev = donne_ev()
            ty = type_ev(ev)
                
            #gestion des ev
            if ty == 'ClicGauche':
                    
                #Si le curseur est dans la zone de jeu lors du clique
                if (dico_jeu["LARGEUR_BORD"] < abscisse(ev) < dico_jeu["LARGEUR_BORD"] + dico_jeu["LARGEUR"]) and (0 < ordonnee(ev) < dico_jeu["HAUTEUR"]):
                    case = pixel_vers_case(dico_jeu["grille"], (abscisse(ev), ordonnee(ev)))
                        
                    #ajoute ou enlève la case cliquée dans l'ensemble noircies
                    if (case not in dico_jeu["noircies"]):
                        dico_jeu["noircies"].add(case)
                        dico_jeu["historique_cases"].append(case)
                            
                    else:
                        dico_jeu["noircies"].discard(case)
                        dico_jeu["historique_cases"].remove(case)

                #bouton resoudre
                if (20 <= abscisse(ev) <= 130) and (450 <= ordonnee(ev) <= 480):
                    print("resoudre à faire (tâche 4)")
                
                #bouton annuler
                if (170 <= abscisse(ev) <= 270) and (450 <= ordonnee(ev) <= 480):
                    try:
                        dico_jeu["noircies"].discard(dico_jeu["historique_cases"][-1])
                        del dico_jeu["historique_cases"][-1]
                    except:
                        print("Pas de cases noircies")

                #bouton menu
                if (20 <= abscisse(ev) <= 130) and (400 <= ordonnee(ev) <= 430):
                    menu = True
                    jouer = False
                
                #bouton recommencer
                if (170 <= abscisse(ev) <= 270) and (400 <= ordonnee(ev) <= 430):
                    dico_jeu["noircies"] = set()
                    dico_jeu["historique_touches"] = []

            #Quitter avec la croix
            if ty == 'Quitte':
                jouer = False
                    
            #Règle respectées ?
            affiche_texte((220, 80), "Pas d'erreurs", 'lightgreen', 14) if (sans_voisines_noircies(dico_jeu["grille"], dico_jeu["noircies"])) else affiche_texte((200, 80), "Erreur(s)", '#E74C3C', 14)
            affiche_texte((220, 160), "Pas d'erreurs", 'lightgreen', 14) if (sans_conflit(dico_jeu["grille"], dico_jeu["noircies"])) else affiche_texte((200, 160), "Erreur(s)", '#E74C3C', 14)
            affiche_texte((190, 240), "Pas d'erreurs", 'lightgreen', 14) if (connexe(dico_jeu["grille"], dico_jeu["noircies"])) else affiche_texte((200, 240), "Erreur(s)", '#E74C3C', 14)
                
            #Partie finie
            if gagne(dico_jeu["grille"], dico_jeu["noircies"]):
                affiche_bouton((170, 350), (280, 380), "Continuer", "blue", 10, "ivory")
                if ty == 'ClicGauche':
                    if (170 <= abscisse(ev) <= 280) and (350 <= ordonnee(ev) <= 380):
                        fin_de_jeu = True #entre dans la boucle fin de jeu
                        jouer = False #quitte la boucle du jeu
                    
                ##fin de jeu##
                    
                while fin_de_jeu:
                        
                    #efface et dessine l'ecran de fin de jeu
                    efface_tout()
                    dessine_fin_de_jeu()
                        
                    #recuperation des ev
                    ev = donne_ev()
                    ty = type_ev(ev)
                        
                    #gestion des ev
                    if ty == 'ClicGauche':
                            
                        #bouton menu
                        if (240 <= abscisse(ev) <= 390) and (250 <= ordonnee(ev) <= 285):
                            init_jeu("niveausujet.txt")
                            fin_de_jeu = False
                            menu = True
                            
                        #bouton quitter
                        if (420 <= abscisse(ev) <= 570) and (250 <= ordonnee(ev) <= 285):
                            fin_de_jeu = False
                                
                    #Quitte avec la croix
                    if ty =='Quitte':
                        fin_de_jeu = False
                                
                    mise_a_jour()
                    
            mise_a_jour()
                
        mise_a_jour()
            
    ferme_fenetre()
    
    
    
    
    
    
    
    
    
    