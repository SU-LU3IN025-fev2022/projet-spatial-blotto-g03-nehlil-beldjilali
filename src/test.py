import util as ut

nb_obj = 5
nb_militants = 14
nb_militants_p = nb_militants//2
print(ut.init_uniform(nb_obj,nb_militants_p))

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