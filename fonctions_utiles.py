def voisines(grille, case):
    """
    Renvoi la liste une liste contenant les cases voisines d'une case
    :param tuple: coordoonnées de la case
    :return lst: Liste des cases voisines
    >>>voisines([[0, 0, 0], [0, 0, 0], [0 ,0 , 0]], (0, 0))
    [(1, 0), (0, 1)]
    >>>voisinesvoisines([[0, 0, 0], [0, 0, 0], [0, 0, 0]], (1, 1))
    [(0, 1), (1, 0), (2, 1), (1, 2)]
    """
    i, j = case
    cases_voisines = [(i - 1, j), (i, j - 1), (i + 1, j), (i, j + 1)]
    k = 0
    while k < len(cases_voisines):
        x = cases_voisines[k][0]
        y = cases_voisines[k][1]
        if x < 0 or x > len(grille[0]):
            cases_voisines.pop(k)
            k -= 1
        if y < 0 or y > len(grille):
            cases_voisines.pop(k)
            k -= 1
        k += 1
    return cases_voisines

def copie_grille(grille):
    """
    Copie la grille en paramètre
    :param lst: Grille de jeu
    :return lst: copie de la grille du jeu
    >>>copie_grille([[1, 2, 3], [1, 5, 4]])
    [[1, 2, 3], [1, 5, 4]]
    >>>copie_grille([[2, 2, 2], [3, 3, 3], [4, 4, 4]])
    [[2, 2, 2], [3, 3, 3], [4, 4, 4]]
    """
    grille_bis = []
    for ligne in grille:
        ligne_bis = []
        for element in ligne:
            ligne_bis.append(element)
        grille_bis.append(ligne_bis)
    return grille_bis

def transposee(grille):
    """
    Renvoie la transposée de la grille
    :param lst: Grille du jeu
    :return lst: Transposée de la grille du jeu
    >>>grille_transposee([[1, 2, 3], [4, 5, 8]])
    [[1, 4],[2, 5],[3, 8]]
    """
    grille_transposee = []
    for j in range(len(grille)):
        ligne_transposee = []
        for i in range(len(grille[j])):
            ligne_transposee.append(grille[i][j])
        grille_transposee.append(ligne_transposee)
    return grille_transposee

def trouve_nombre(grille):
    """
    Cherche la première case contenant un chiffre (Pour choisir où commencer la detection de pièce)
    :param lst: Grille du jeu
    :return tuple: coordonnées de la première case contenant un chiffre
    >>>trouve_nombre([["N", 2, 3], [2, 5, "N"], [4, 5, 6]])
    (1, 0)
    >>>trouve_nombre([["N", "N", "N"], [2, 5, "N"], [4, 5, 6]])
    (0, 1)
    """
    for j in range(len(grille)):
        for i in range(len(grille[j])):
            try:
                if int(grille[j][i]):
                    return (i,j)
            except:
                pass