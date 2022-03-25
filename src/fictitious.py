import util as ut
import numpy as np

nb_obj, nb_militants = 5, 7
# Matrice des probabilités
matProb = [[0 for x in range(nb_militants+1)] for y in range(nb_obj)]

# Mettre à jour la matrice de probabilités
def updateMatProba(strategy, jours_passes):
    for i in range(len(strategy)):
        j = strategy[i]
        p = matProb[i][j]*(jours_passes-1)
        matProb[i][j] = (p+1)/jours_passes

# Calcul des gains esperes pour une strategie donnée maStrategy
def gain_espere(maStrategy):
    gains = []
    for electeur in range(nb_obj):
        gain = 0
        monCoup = maStrategy[electeur]
        for j in range(0, monCoup+1): 
            gain += matProb[electeur][j]
        gains.append(round(gain, 2))
    return gains
    
# Implementation de l'algorithme par apprentissage fictitious play
def fictitious(mesCoups,adversCoups):
    possible_strategies, gains = [], []
    for nom_str in ut.STRATEGIES:
        strategy = ut.prochainCoup(mesCoups,adversCoups,nom_str)
        possible_strategies.append(strategy)
        gains.append(sum(gain_espere(strategy)))
    return ut.STRATEGIES[np.argmax(gains)], possible_strategies[np.argmax(gains)]