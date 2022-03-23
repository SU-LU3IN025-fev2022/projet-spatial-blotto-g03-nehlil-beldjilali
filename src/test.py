import util as ut
import numpy as np
import random

nb_obj, nb_militants = 5, 7

def possible_moves(myPosition, myBudget):
    
    return








'''
pos_secteurs = {0:[(1,3),(1,4)],1:[(1,3),(8,11)],2:[(1,3),(15,18)],
                3:[(5,9),(1,4)],4:[(5,9),(15,18)],5:[(11,14),(1,4)],
                6:[(11,14),(15,18)],7:[(16,18),(1,6)],8:[(16,18),(8,11)],
                9:[(16,18),(15,18)]}

l = random.sample(range(10), 5)
for el in l:
    pos = pos_secteurs[el]
    x, y = random.randint(pos[0][0],pos[0][1]), random.randint(pos[1][0],pos[1][1])

str1, str2 = ut.init_alea_parti(nb_obj, nb_militant_p), ut.init_alea_parti(nb_obj, nb_militant_p)
print("strategy 1:", str1)
print("strategy 2:", str2)

idx_list = np.argsort(str1)[::-1]
new_strategy = [0 for k in range(nb_obj)]
for i in range(nb_obj):
    if i<nb_obj//2: new_strategy[idx_list[i]] = 0
    else: new_strategy[idx_list[i]] = str1[idx_list[i]]+1
new_strategy[idx_list[i]] += (nb_militant_p - sum(new_strategy))
'''

"""
        affec_alea = random.sample(pos_secteurs, 5)
        s = 0
        for o in game.layers['ramassable']:
            row, col = affec_alea[s]
            s+=1
            o.set_rowcol(row, col)
        objectifs = [o.get_rowcol() for o in game.layers['ramassable']]
        """