import numpy as np
import util as ut


# Initialisation aléatoire 
def init_uniforme(nb_obj, nb_militants):
    affec_list = []
    q, r = nb_militants//nb_obj, nb_militants%nb_obj
    for i in range(nb_obj):
        affec_list.append(q)
    for i in range(r):
        affec_list[i] += 1
    return affec_list

def calcul_score_jour(strategy1, strategy2):
    score1, score2 = 0, 0
    for el1, el2 in zip(strategy1, strategy2):
        if el1>el2:
            score1+=1
        elif el1<el2:
            score2+=1
    return score1, score2

def obj_to_strategy(obj_militant, nb_obj):
    strategy = [0 for k in range(nb_obj)]
    for obj in obj_militant:
        strategy[obj]+=1
    return strategy

def str_to_obj(strategy, nb_militants):
    obj_milit = [0 for k in range(nb_militants)]
    k=0
    for i in range(len(strategy)):
        for j in range(strategy[i]):
            #print(strategy.index(obj))
            obj_milit[k] = i
            k+=1
    return obj_milit


nb_obj = 5
nb_militants = 14
nb_militants_p = nb_militants//2
print(ut.init_uniforme(nb_obj,nb_militants_p))

'''
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