import random
import numpy as np

def init_alea_parti(nb_obj, nb_militants):
    obj_militants = [0 for k in range(nb_militants)]
    strategy = [0 for k in range(nb_obj)]
    for i in range(nb_militants):
        # Allouer aléatoirement un electeur à chaque militant
        obj = np.random.randint(0, nb_obj)
        obj_militants.append(obj)
        strategy[obj]+=1
    return strategy

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

def prochainCoup(mesCoups,adversCoups,nom):
    """selon la liste de mes coups et des coups de l'autre
    je choisis un coup """
    nb_obj, nb_militants = 5, 7
    #
    # strategies de base
    #
    if nom=='random':
        return init_alea_parti(nb_obj, nb_militants)
    
    if nom=='tetu':
        if len(mesCoups)==0:
            return init_alea_parti(nb_obj, nb_militants)
        else:
            return mesCoups[-1]
    
    if nom=='tetu_uniform':
        if len(mesCoups)==0:
            return init_uniforme(nb_obj, nb_militants)
        else:
            return mesCoups[-1]
    
    if nom=='titfortat':
        if adversCoups == []:
            return init_alea_parti(nb_obj, nb_militants)
        else:
            return adversCoups[-1]
    
    if nom=='best_response':
        if adversCoups == []:
            return init_alea_parti(nb_obj, nb_militants)
        else:
            adv_str = adversCoups[-1]
            idx_list = np.argsort(adv_str)[::-1]
            new_strategy = [0 for k in range(nb_obj)]
            for i in range(nb_obj):
                if i<nb_obj//2: new_strategy[idx_list[i]] = 0
                else: new_strategy[idx_list[i]] = adv_str[idx_list[i]]+1
            new_strategy[idx_list[i]] += (nb_militants - sum(new_strategy))
            return new_strategy
        
    if nom=='random':
        return random.choice(['t','c'])
    if nom=='alterne':
        if mesCoups == []:
            return 'c'
        elif mesCoups[-1]=='t':
            return 'c'
        else:
            return 't'