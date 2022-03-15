import numpy as np


# Initialisation aléatoire 
def init_alea(nb_obj, nb_militants):
    strategie_p = []
    strategie_p1 = [0 for k in range(nb_obj)]
    strategie_p2 = [0 for k in range(nb_obj)]
    elec_dic = {k: [] for k in range(nb_obj)}
    for i in range(nb_militants):
        # Allouer aléatoirement un electeur à chaque militant
        obj = np.random.randint(0, nb_obj)
        strategie_p.append(obj)
        if i<nb_militants//2:
            strategie_p1[obj]+=1
        else:
            strategie_p2[obj]+=1
        elec_dic[obj].append(i)
    return strategie_p, strategie_p1, strategie_p2, elec_dic

def init_alea_bis(nb_obj, nb_militants):
    # random.shuffle(objectifs)
    strategie_p1 = [0 for k in range(nb_obj)]
    strategie_p2 = [0 for k in range(nb_obj)]
    elec_dic = {k: [] for k in range(nb_obj)}
    for i in range(nb_militants):
        # Allouer aléatoirement un electeur à chaque militant
        obj = np.random.randint(0, nb_obj)
        if i<nb_militants//2:
            strategie_p1[obj]+=1
        else:
            strategie_p2[obj]+=1
        elec_dic[obj].append(i)
    return strategie_p1, strategie_p2, elec_dic

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

nb_obj = 5
nb_militants = 14

print(init_uniforme(nb_obj, nb_militants))


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

obj_milit, str1, str2, elec_dic = init_alea(nb_obj, nb_militants)
print("obj militants :", obj_milit)
print("strategy 1:", str1)
print("strategy 2:", str2)

