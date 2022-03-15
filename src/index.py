# -*- coding: utf-8 -*-

# Nicolas, 2021-03-05
from __future__ import absolute_import, print_function, unicode_literals

import random
from stat import IO_REPARSE_TAG_MOUNT_POINT
from matplotlib.pyplot import hist
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

import util as ut
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
    score = {1: 0, 2: 0}
    strategy1 = [0 for k in range(nb_obj)] # liste pour sauvegarder la strategie précédente du parti 1
    strategy2 = [0 for k in range(nb_obj)] # liste pour sauvegarder la strategie précédente du parti 2
    historique = {1:[], 2:[]}

    NBJOURS = 3
    # -------------------------------
    # Carte demo
    # Tous les joueurs exécutent A*
    # -------------------------------

    # par defaut la matrice comprend des True
    g = np.ones((nbLignes, nbCols), dtype=bool)
    for w in wallStates:            # putting False for walls
        g[w] = False

    posPlayers = initStates
    # Boucle principale des elections
    for jour in range(NBJOURS):
        # Initialisation aléatoire des strateegies d'affectation
        #obj_milit1,strategy1 = ut.init_alea_parti(nb_obj, nb_militants//2)
        #obj_milit2,strategy2 = ut.init_alea_parti(nb_obj, nb_militants//2)
        #obj_milit,strategy1, strategy2 = ut.init_alea(nb_obj, nb_militants)

        strategy1 = ut.prochainCoup(historique[1],historique[2],'titfortat')
        strategy2 = ut.prochainCoup(historique[2],historique[1],'aleatoire')
        obj_milit = ut.str_to_obj(strategy1, nb_militants//2) +  ut.str_to_obj(strategy2, nb_militants//2)
        historique[1].append(strategy1)
        historique[2].append(strategy2)
        
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
        score_parti1, score_parti2 = ut.calcul_score_jour(strategy1, strategy2)
        # Sauvegarder le score journalier de chaque parti
        score[1] += score_parti1
        score[2] += score_parti2

        # Affichage de score et de strategies
        print("-------------------------------------------------------------------------")
        print("Strategie parti 1 : {}".format(strategy1))
        print("Strategie parti 2 : {}".format(strategy2))
        print("-------------------------------------------------------------------------")
        print("le score du parti 1 : {}".format(score_parti1))
        print("le score du parti 2 : {}".format(score_parti2))
        print("Le partie qui a emporté la journée : {}".format('1' if score_parti1 > score_parti2 else '2'))
    
    # Affichage du score après la fin des elections
    print("-------------------------------------------------------------------------")
    print("le score du parti 1 à la fin des elections: {}".format(score[1]))
    print("le score du parti 2 à la fin des elections: {}".format(score[2]))
    print("Le parti qui a emporté l'election : {}".format('1' if score[1] > score[2] else '2'))
    # Affichage de l'historique des stratégies
    for str1, str2 in zip(historique[1], historique[2]):
        print("---")
        print("str1:", str1)
        print("str2:", str2)

    # -------------------------------

if __name__ == '__main__':
    main()