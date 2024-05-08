import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


latences_changees = False

# Instance de Braess
aretes_suivantes = [[1,4], [], [3], [], [3]]
paires_od = [{"demande":1,"origine":[0,2],"destination":[1,3]},
            {"demande":2,"origine":[1,4],"destination":[1,3]}]

# Instance de Pigou
# aretes_suivantes = [[],[]]
# paires_od = [{"demande":1,"origine":[0,1],"destination":[0,1]}]

def latence(a,x):
    """Renvoie la valeur associée à la fonction de latence de l'arête a pour une demande x,
    -1 si l'arête n'existe pas"""
    if a==0 or a==3:
        return x
    elif a==1 or a==2:
        return 1
    elif a==4:
        return 0
    else:
        return -1


# Instance de Awerbuch-Azar-Epstein
# POA de 25/2 contre 5/2, trop grosses approximations dans Wardrop()
# aretes_suivantes = [[1,5], [2,4], [0,3], [2,4], [1,5], [0,3]]
# paires_od = [{"demande":1,"origine":[2,4],"destination":[2,5]},
#       {"demande":2,"origine":[1,5],"destination":[2,5]},
#       {"demande":3,"origine":[1,5],"destination":[1,3]},
#       {"demande":4,"origine":[2,4],"destination":[0,4]}]

# def latence(a,x):
#     """Renvoie la valeur associée à la fonction de latence de l'arête a pour une demande x,
#       -1 si l'arête n'existe pas"""
#     if a==0 or a==1 or a==3 or a==4:
#         return x
#     elif a==2 or a==5:
#         return 0
#     else:
#         return -1


# # Instance de Roughgarden sans situation d'équilibre
# # Wardrop() boucle indéfiniment
# aretes_suivantes = [[], [2,3], [], [5], [5], []]
# paires_od = [{"demande":1,"origine":[0,1,4],"destination":[0,2,5]},
#       {"demande":2,"origine":[0,1,4],"destination":[0,2,5]}]

# def latence(a,x):
#     """Renvoie la valeur associée à la fonction de latence de l'arête a pour une demande x,
#       -1 si l'arête n'existe pas"""
#     if a==0:
#         return 47*x
#     elif a==1:
#         return 3*x*x
#     elif a==2:
#         return x*x+44
#     elif a==3:
#         return 6*x*x 
#     elif a==4:
#         return x+33
#     elif a==5:
#         return 13*x
#     else:
        # return -1


# Ne fonctionne pas pour l'instance AAE car nous autorisons seulement 2 stratégies
# 1 arête directe ou 2 arêtes, mais pas de cycle
def chemins_faisables(k):
    """Renvoie tous les chemins faisables pour chaque paire, ceux-ci étant
    listés par leur indice, à prendre dans cet ordre"""
    origine,destination = paires_od[k]["origine"],paires_od[k]["destination"]                                                      
    candidats = [[i] for i in origine]                                                              
    # tous les chemins de la longueur considérée, démarant dans "origine"
    chemins_trouves = [[i] for i in origine if i in destination]   
    # tous les chemins faisables, commençant dans "origine" et finissant dans "destination" 
    while candidats != []:
        candidats = [chemin+[j] for chemin in candidats for j in aretes_suivantes[chemin[-1]] if not j in chemin]    
        # tous les chemins candidats pour la taille de aretes_suivantes
        chemins_trouves = chemins_trouves + [chemin for chemin in candidats if chemin[-1] in destination]              
        # ajout des "chemins_trouves" terminant dans "destination"
    return chemins_trouves

chemins = [chemins_faisables(i) for i in range(len(paires_od))]   
# Pour AAE :
# chemins = [[[2], [4,5]], [[5], [1,2]], [[1], [5,3]], [[4], [2,0]]]   


def calcul_charge_aretes(charges_chemins):
    """ Calcule la charge des liens en se basant sur la charge des chemins,
    ceux-ci étant listés dans la liste chemins"""
    charge_aretes = [0]*len(aretes_suivantes)
    for k in range(len(paires_od)):
        for index_chemin in range(len(chemins[k])):
            for a in chemins[k][index_chemin]:
                charge_aretes[a] += charges_chemins[k][index_chemin]
    return charge_aretes


def cout_chemin(chemin, charge_aretes, taxes_aretes):
    """Calcule le cout d'un chemin, en prenant en compte les taxes pigouviennes ou non"""
    if latences_changees:
       epsilon = 0.000001
       return sum([latence(a,charge_aretes[a]) + charge_aretes[a] *
       (latence(a,charge_aretes[a]+epsilon)-latence(a,charge_aretes[a])) / epsilon
       for a in chemin])
    else:
        return sum([latence(a,charge_aretes[a])+taxes_aretes[a] for a in chemin])


def Wardrop(taxes_aretes):
    """Approximation de l'équilibre de Wardrop,
    renvoie charges_chemins, charge_aretes, et couts_chemins"""
    pas,delta_arret = 0.1, 0.000001
    # pas à chaque itération et précision pour l'arret
    charges_chemins = []
    # Initialisation des flux de chemins
    for k in range(len(paires_od)):
        taille_chemin = len(chemins[k])                                                        
        # nombre de chemins pour la paire de paires_od actuellement séléctionnée
        charges_chemins = charges_chemins+[[paires_od[k]["demande"]/taille_chemin]*taille_chemin]
        # répartition égale de la demande parmi ces chemins
    delta_cout = [1]*len(paires_od)                                                             
    # Ecart entre les chemins utilisés les plus couteux et les moins couteux pour chaque paire

    # Phase de convergence
    while max(delta_cout) > delta_arret:                                                   
        # Tant que l'on est trop loin de l'équilibre
        for k in range(len(paires_od)):                                
            # Chaque paire peut contenir des usagers qui doivent changer de chemins
            charge_aretes = calcul_charge_aretes(charges_chemins)
            pcosts = [cout_chemin(chemin,charge_aretes,taxes_aretes) for chemin in chemins[k]]    
            # Cout actuel du chemin subi pour cette paire - celui le moins couteux
            index_chemin_moins_couteux =  pcosts.index(min(pcosts))       
            for i in range(len(pcosts)):
                debit_a_transferer = min(pas*(pcosts[i]-min(pcosts)), charges_chemins[k][i])
                charges_chemins[k][i] -= debit_a_transferer
                charges_chemins[k][index_chemin_moins_couteux] += debit_a_transferer    

  # Mise à jour des variables, en particulier de delta_cout
        charge_aretes = calcul_charge_aretes(charges_chemins)
        couts_chemins = []
        for k in range(len(paires_od)):
            couts_chemins.append([cout_chemin(chemin,charge_aretes,taxes_aretes) for chemin in chemins[k]])
            couts_chemins_utilises_disponibles = [couts_chemins[k][i]*(charges_chemins[k][i]>0) for i in range(len(couts_chemins[k]))]              
            # Cout parmi les chemins utilisés, 0 sinon
            delta_cout[k] = max(couts_chemins_utilises_disponibles) - min(couts_chemins[k])

  # Affichage des résultats
    print("Charges des chemins = ",[[round(charges_chemins[k][a],3) for a in range(len(charges_chemins[k]))] for k in range(len(paires_od))])
    print("Coûts des chemins = ",[[round(couts_chemins[k][a],3) for a in range(len(charges_chemins[k]))] for k in range(len(paires_od))])
    charge_aretes = calcul_charge_aretes(charges_chemins)
    print("Charges des arêtes correspondantes = ", [round(x_A,3) for x_A in calcul_charge_aretes(charges_chemins)], '\n')
    return charges_chemins


def optimum_social():
    global latences_changees
    latences_changees = True
    charges_chemins = Wardrop([0]*len(aretes_suivantes))
    latences_changees = False
    return charges_chemins


def cout(charges_chemins):
    charge_aretes = calcul_charge_aretes(charges_chemins)
    return [charge_aretes[a]*latence(a,charge_aretes[a]) for a in range(len(charge_aretes))]


def cout_total(charges_chemins):
    return sum(cout(charges_chemins))


def POA(taxes_aretes):
    optimal = cout_total(optimum_social())
    equilibre = cout_total(Wardrop(taxes_aretes))
    return (equilibre, optimal, equilibre/optimal)


def variation_taxe():
    taxes = np.linspace(0,1,40)
    PoAs = []
    for tax in taxes:
        _,_,PoA = POA([0,0,0,0,tax])
        PoAs.append(PoA)
    plt.plot(taxes,PoAs)
    plt.xlabel("Niveau de taxe")
    plt.ylabel("Prix de l'anarchie")
    plt.show()


def taxes_optimales():
    epsilon = 0.000001
    # pour dériver
    x = calcul_charge_aretes(optimum_social())
    return [x[a] * (latence(a,x[a]+epsilon) - latence(a,x[a])) / epsilon
            for a in range(len(x))]   


print(f"Chemins = {chemins} \n")
taxes_aretes = [0]*len(aretes_suivantes)
Wardrop(taxes_aretes)
variation_taxe()


# Affichage graphique

G = nx.DiGraph()

# Dessine charge_aretes avec la distribution de optimum_social()
subax1 = plt.subplot(121)
charges_chemins = optimum_social()
subax1.set_title(f"Distribution optimale de la charge sur les arêtes \nCoût total = {round(cout_total(charges_chemins),1)}")

charges_chemins_brutes = calcul_charge_aretes(charges_chemins)
charge_aretes = [round(elt, 1) for elt in charges_chemins_brutes]

G.add_weighted_edges_from([(0,1,charge_aretes[0]), (1,2,charge_aretes[1]), (0,3,charge_aretes[2]),
                          (3,2,charge_aretes[3]), (1,3,charge_aretes[4])])

pos = nx.spring_layout(G, seed=7) 
nx.draw_networkx_nodes(G, pos, node_size=500, node_color='r')
nx.draw_networkx_edges(G, pos, width=4)
nx.draw_networkx_labels(G, pos, font_size=20, font_family="sans-serif")
edge_labels = nx.get_edge_attributes(G, "weight")
nx.draw_networkx_edge_labels(G, pos, edge_labels)


# Dessine charge_aretes avec la distribution de Wardrop()
subax2 = plt.subplot(122)
charges_chemins = Wardrop([0]*len(aretes_suivantes))
subax2.set_title(f"Distribution de la charge sur les arêtes pour l'équilibre des utilisateurs \nCoût total = {round(cout_total(charges_chemins),1)}")

charges_chemins_brutes = calcul_charge_aretes(charges_chemins)
charge_aretes = [round(elt, 1) for elt in charges_chemins_brutes]
G.add_weighted_edges_from([(0,1,charge_aretes[0]), (1,2,charge_aretes[1]), (0,3,charge_aretes[2]),
                          (3,2,charge_aretes[3]), (1,3,charge_aretes[4])])

pos = nx.spring_layout(G, seed=7) 
nx.draw_networkx_nodes(G, pos, node_size=500, node_color='r')
nx.draw_networkx_edges(G, pos, width=4)
nx.draw_networkx_labels(G, pos, font_size=20, font_family="sans-serif")
edge_labels = nx.get_edge_attributes(G, "weight")
nx.draw_networkx_edge_labels(G, pos, edge_labels)


ax = plt.gca()
ax.margins(0.08)
plt.axis("off")
plt.tight_layout()
plt.show()