import pandas as pd
import itertools
import ast

# Calculating strategies for the agents
def calc_all_statergies(rounds,starting_purse):
    statergies = [x for x in list(itertools.product(list(range(0,starting_purse+1)),repeat=rounds)) if sum(x) <=3]
    statergies_p1, statergies_p2 = statergies,statergies
    return statergies_p1,statergies_p2

# To create a dictionary with keys as strategy pair of agents and values as utilities pair.
def bid(statergies_p1,statergies_p2,first_bid):
    dict_all = {}
    for i in statergies_p1:
        sub_list = []
        for j in statergies_p2:
            purse = [3,3]
            won = [0,0]
            round_count = 0
            total_spend = 0
            for round_spend in zip(i,j):
                round_spend = list(round_spend)
                if(round_spend[0] > round_spend[1]):
                    purse[0] = purse[0] - round_spend[0]
                    won[0] = won[0]+3
                    total_spend += round_spend[0]
                elif(round_spend[1] > round_spend[0]):
                    purse[1] = purse[1] - round_spend[1]
                    won[1] = won[1]+3
                    total_spend += round_spend[1]
                else:
                    purse[first_bid[round_count]] = purse[first_bid[round_count]] - round_spend[first_bid[round_count]]
                    won[first_bid[round_count]] = won[first_bid[round_count]]+3
                    total_spend += round_spend[first_bid[round_count]]
                round_count+=1
                dict_all[(i,j)] = [purse[0]+won[0],purse[1]+won[1]]
            sub_list.append([purse[0]+won[0],purse[1]+won[1]])
    return dict_all


def create_tree(order,s1,s2,dic): 
    bidding_order = {} # Contains actual order of bidding appended to utility pair as keys with startegy pair as values.
    reverse_bidding_order = {} # reverse bidding order to calculate subgame equilibrium.
    for i in s1:
        for j in s2:
            t_order = []
            for z in zip(i,j,order):
                t_order.append(z[z[2][0]]);
                t_order.append(z[z[2][1]]);
                keyy = [dic[(i,j)]+t_order] # appending bidding order to utility pair.
            reverse_bidding_order[str(t_order[::-1])] = keyy
            bidding_order[str(keyy)] = [i,j]
    return reverse_bidding_order,bidding_order


def traverse_back(reverse_bidding_order,order_single_list):
    current_dict = reverse_bidding_order
    for i in order_single_list[::-1]:
        build_new_dict = {}
        for j in current_dict:
            parent_path = ast.literal_eval(j)[1:]
            if(str(parent_path) in build_new_dict):
                temp_list = []
                for k in build_new_dict[str(parent_path)]:
                    for l in current_dict[j]:
                        if(k[i] > l[i]):
                            temp_list.append(k)
                if(len(temp_list) == 0):
                    build_new_dict[str(parent_path)] = current_dict[j]
                else:
                    build_new_dict[str(parent_path)] = temp_list
            else:
                build_new_dict[str(parent_path)] = current_dict[j]
        current_dict = build_new_dict
    return current_dict['[]'][0]


def calc_eqi(n,m):
    s1,s2 = calc_all_statergies(n,m) # to calculate strategies of agents
    first_bid = ([0,1]*int(n/2+1))[:n] # to calculate which agent bids first in each round. agent1=0 and agent2=1
    dic = bid(s1,s2,first_bid) 
    order = [[0,1] if i%2==0 else [1,0] for i in range(0,n)] #creating order in which agents bid for each round (0 to n-1).
    order_single_list = [ordd for sublist in order for ordd in sublist]
    tree,reverse_strat = create_tree(order,s1,s2,dic)
    out = traverse_back(tree,order_single_list)
    return(out[0:2],reverse_strat[str([out])])


print(calc_eqi(3,3))

