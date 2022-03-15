# -*- coding: utf-8 -*-

# Nicolas, 2021-03-05
from __future__ import absolute_import, print_function, unicode_literals

import random
from stat import IO_REPARSE_TAG_MOUNT_POINT
import numpy as np
import sys
from itertools import chain


import pygame

from pySpriteWorld.gameclass import Game, check_init_game_done
from pySpriteWorld.spritebuilder import SpriteBuilder
from pySpriteWorld.players import Player
from pySpriteWorld.sprite import MovingSprite
from pySpriteWorld.ontology import Ontology
import pySpriteWorld.glo

from search.grid2D import ProblemeGrid2D
from search import probleme

# ---- ---- ---- ---- ---- ----
# ---- Misc                ----
# ---- ---- ---- ---- ---- ----


# ---- ---- ---- ---- ---- ----
# ---- Main                ----
# ---- ---- ---- ---- ---- ----

game = Game()


def init(_boardname=None):
    global player, game
    name = _boardname if _boardname is not None else 'blottoMap'
    game = Game('./Cartes/' + name + '.json', SpriteBuilder)
    game.O = Ontology(True, 'SpriteSheet-32x32/tiny_spritesheet_ontology.csv')
    game.populate_sprite_names(game.O)
    game.fps = 5  # frames per second
    game.mainiteration()
    player = game.player

# Initialisation aléatoire
def init_alea(nb_obj, nb_militants):
    # random.shuffle(objectifs)
    strategie_p = []
    elec_dic = {k: [] for k in range(nb_obj)}
    for i in range(nb_militants):
        # Allouer aléatoirement un electeur à chaque militant
        obj = np.random.randint(0, nb_obj)
        strategie_p.append(obj)
        elec_dic[obj].append(i)
    return strategie_p, elec_dic

def init_uniforme(nb_obj, nb_militants):
    affec_list = []
    q, r = nb_militants//nb_obj, nb_militants%nb_obj
    for i in range(nb_obj):
        affec_list[i] = q
    for i in range(r):
        affec_list[i] += 1
    return affec_list

def main():

    # for arg in sys.argv:
    iterations = 100  # default
    if len(sys.argv) == 2:
        iterations = int(sys.argv[1])
    print("Iterations: ")
    print(iterations)

    init()

    # -------------------------------
    # Initialisation
    # -------------------------------

    nbLignes = game.spriteBuilder.rowsize
    nbCols = game.spriteBuilder.colsize

    print("lignes", nbLignes)
    print("colonnes", nbCols)

    players = [o for o in game.layers['joueur']]
    nbPlayers = len(players)
    print("Trouvé ", nbPlayers, " militants")

    # on localise tous les états initiaux (loc du joueur)
    # positions initiales des joueurs
    # Retourne des couples (x,y) : positions des joueurs
    initStates = [o.get_rowcol() for o in players]
    print("Init states:", initStates)
    print("Number of players:", len(initStates))

    # on localise tous les secteurs d'interet (les votants)
    # sur le layer ramassable
    # Retourne des couples (x,y) : positions des votants
    goalStates = [o.get_rowcol() for o in game.layers['ramassable']]
    print("Goal states:", goalStates)
    print("Number of goals:", len(goalStates))

    # on localise tous les murs
    # sur le layer obstacle
    wallStates = [w.get_rowcol() for w in game.layers['obstacle']]
    print("Wall states:", wallStates)

    def legal_position(row, col):
        # une position legale est dans la carte et pas sur un mur
        return ((row, col) not in wallStates) and row >= 0 and row < nbLignes and col >= 0 and col < nbCols

    # -------------------------------
    # Attributaion aleatoire des fioles
    # -------------------------------

    objectifs = goalStates
    nb_militants = len(initStates)
    nb_obj = len(objectifs)

    obj_milit, elec_dic = init_alea(nb_obj, nb_militants)

    # -------------------------------
    # Carte demo
    # Tous les joueurs exécutent A*
    # -------------------------------

    # par defaut la matrice comprend des True
    g = np.ones((nbLignes, nbCols), dtype=bool)
    for w in wallStates:            # putting False for walls
        g[w] = False

    NBJOURS = 3
    score = {1: 0, 2: 0}
    objectifs = goalStates

    posPlayers = initStates
    log_strategy1 = [0 for k in range(nb_obj)] # liste pour sauvegarder la strategie précédente du parti 1
    log_strategy2 = [0 for k in range(nb_obj)] # liste pour sauvegarder la strategie précédente du parti 2

    index_list = np.argmax(posPlayers)
    # Boucle principale des elections
    for jour in range(NBJOURS):
        # obj_milit, elec_dic = init_alea(nb_obj, nb_militants)
        index_list = np.argsort(log_strategy1)
        k = (nb_obj//2 -1) if nb_obj%2==0 else (nb_obj//2)
        for a in range(nb_obj):
            if a<k:
                pass


        for militant in range(nb_militants):
            obj = obj_milit[militant]
            p = ProblemeGrid2D(posPlayers[militant], objectifs[obj], g, 'manhattan')
            path = probleme.astar(p)
            print("Chemin trouvé:", path)

            # -------------------------------
            # Boucle principale de déplacements
            # -------------------------------

            for i in range(iterations):

                # on fait bouger chaque joueur séquentiellement

                # Joueur militant: suit son chemin trouve avec A*

                row, col = path[i]
                posPlayers[militant] = (row, col)
                players[militant].set_rowcol(row, col)
                print("pos :", row, col)
                if (row, col) == objectifs[obj]:
                    # Si nouvelle position alors la sauvegarder
                    posPlayers[militant] = (row, col)
                    print("le joueur {} a atteint son but!".format(militant))
                    break

                # on passe a l'iteration suivante du jeu
                # game.mainiteration()

        # pygame.quit()

        # Calculer le score de chaque parti en ce jour
        score_parti1, score_parti2 = 0, 0
        for (elec, militants) in elec_dic.items():
            a, b = 0, 0
            str1, str2 = 0,0
            for militant in militants:
                if militant < (nb_militants//2):
                    a += 1
                    str1+=1
                else:
                    b += 1
                    str2+=1
            # Sauvegarder les strategies de chaque parti
            log_strategy1[elec] = str1
            log_strategy2[elec] = str2
            if a > b:
                score_parti1 += 1
            elif a < b:
                score_parti2 += 1
        # Sauvegarder le score journalier de chaque parti
        score[1] += score_parti1
        score[2] += score_parti2

        # Affichage de score et de strategies
        print("-------------------------------------------------------------------------")
        print("le score du parti 1 : {}".format(score_parti1))
        print("le score du parti 2 : {}".format(score_parti2))
        print("Le partie qui a emporté la journée : {}".format('1' if score_parti1 > score_parti2 else '2'))
        print("-------------------------------------------------------------------------")
        print("Strategie parti 1 : {}".format(log_strategy1))
        print("Strategie parti 2 : {}".format(log_strategy2))
    print("-------------------------------------------------------------------------")
    print("le score du parti 1 à la fin des elections: {}".format(score[1]))
    print("le score du parti 2 à la fin des elections: {}".format(score[2]))
    print("Le parti qui a emporté l'election : {}".format('1' if score[1] > score[2] else '2'))
    # -------------------------------

if __name__ == '__main__':
    main()
