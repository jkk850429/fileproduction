import random
import math
import statistics
from queue import *
from callf import *



def tabu_embedded_SA(aclist,init_seq,FFD_dic,salary):
    #initial

    gbest = init_seq.copy()
    gNoimpro = 0
    k = 5


    while(gNoimpro<k):
        n = random.randint(5,7)
        tabu = Queue(maxsize=n)
        S = gbest.copy()

        #localSearch(S)
        Sb = S.copy()
        #random.shuffle(Sb)
        Sb = Local_Search(Sb,aclist,FFD_dic,salary,10)

        MSNI = 3
        NoImprove = 0
        T = find_temp(init_seq,aclist,FFD_dic,salary)

        while(NoImprove<MSNI):
            T,S1 = SA(T,S,aclist,FFD_dic,salary,tabu,gbest)
            S1 = Local_Search(S1,aclist,FFD_dic,salary,10)

            if(fitness(aclist,Sb,FFD_dic,salary)>fitness(aclist,S1,FFD_dic,salary)):
                #print("improve")
                S = S1.copy()
                Sb = S1.copy()
                NoImprove = 0
            else:
                #print("NoImprove")
                NoImprove = NoImprove+1
                S = S1.copy()

        if(fitness(aclist,Sb,FFD_dic,salary)<fitness(aclist,gbest,FFD_dic,salary)):
            #print("gbestImprove")
            gbest = Sb.copy()
            gNoimpro = 0
        else:
            gNoimpro = gNoimpro+1
            #print("gbestNoImprove")

    print("gbest:",fitness(aclist,gbest,FFD_dic,salary))
    two_swap(gbest)
    return gbest

def two_opt(seq):
    #2opt
    i = random.randint(0,len(seq)-1)
    j = random.randint(0,len(seq)-1)

    while(i==j):
        j = random.randint(0, len(seq) - 1)

    if(i>j):
        temp = j
        j = i
        i = temp

    new_list_1 = seq[0:i]
    new_list_2 = seq[i:j]
    new_list_3 = seq[j:len(seq)]

    new_list = new_list_1.copy()
    new_list.extend(new_list_2[::-1])
    new_list.extend(new_list_3)
    #print(new_list)

    return new_list

def two_swap(seq):
    i = random.randint(0, len(seq) - 1)
    j = random.randint(0, len(seq) - 1)

    while (i == j):
        j = random.randint(0, len(seq) - 1)

    new_list = seq.copy()
    temp = new_list[i]
    new_list[i] = new_list[j]
    new_list[j] = temp

    #print(new_list)

    return new_list

def two_swap_tabu(seq):
    i = random.randint(0, len(seq) - 1)
    j = random.randint(0, len(seq) - 1)

    while (i == j):
        j = random.randint(0, len(seq) - 1)

    new_list = seq.copy()
    temp = new_list[i]
    new_list[i] = new_list[j]
    new_list[j] = temp
    res = [new_list,new_list[i],new_list[j]]
    #print(new_list)

    return res

def Local_Search(seq,aclist,FFD_dic,salary,k):
    L_opt_seq = seq
    L_opt_fit = fitness(aclist, seq, FFD_dic, salary)
    L_seq = seq
    L_fit = L_opt_fit

    while(True):
        for i in range(0,k):
            if(i<(k/2)):
                temp_seq = two_swap(L_opt_seq)
            else:
                temp_seq = two_opt(L_opt_seq)
            if(fitness(aclist,temp_seq,FFD_dic,salary) < L_fit):
                L_seq = temp_seq
                L_fit = fitness(aclist,temp_seq,FFD_dic,salary)
        if(L_fit>=L_opt_fit):
            break
        else:
            L_opt_fit = L_fit
            L_opt_seq = L_seq

    return L_opt_seq

def SA(Tep, SS,ac_list,FFD_dic,salary,tabu,gbest):
    find = False
    while (not find):
        print(list(tabu.queue))
        temp = two_swap_tabu(SS)
        temp_list = temp[0]
        tabu_list = list(tabu.queue)

        if([temp[1],temp[2]] in tabu_list or [temp[2],temp[1]] in tabu_list):
            if(fitness(ac_list,temp_list,FFD_dic,salary)<fitness(ac_list,gbest,FFD_dic,salary)):
                Tep = 0.95*Tep
                find = True
                return Tep, temp_list
            else:
                continue
        else:
            change = fitness(ac_list, temp_list, FFD_dic, salary) - fitness(ac_list, SS, FFD_dic, salary)
            if (change < 0):
                pro = 1
            else:
                pro = math.exp(-change / Tep)
                #print('pro', pro)
            if (pro > random.random()):
                if(tabu.full()):
                    tabu.get()
                    tabu.put([temp[1],temp[2]])
                else:
                    tabu.put([temp[1], temp[2]])

                Tep = 0.95 * Tep
                find = True
                return Tep, temp_list

def SA_2(Tep, SS,ac_list,FFD_dic,salary,tabu,gbest):
    find = False
    while (not find):
        print(list(tabu.queue))
        temp = two_swap_tabu(SS)
        temp_list = temp[0]
        tabu_list = list(tabu.queue)

        if(fitness(ac_list,temp_list,FFD_dic,salary) in tabu_list):
            if(fitness(ac_list,temp_list,FFD_dic,salary)<fitness(ac_list,gbest,FFD_dic,salary)):
                Tep = 0.95*Tep
                find = True
                return Tep,temp_list
            else:
                continue

        else:
            change = fitness(ac_list, temp_list, FFD_dic, salary) - fitness(ac_list, SS, FFD_dic, salary)
            if (change < 0):
                pro = 1
            else:
                pro = math.exp(-change / Tep)
                #print('pro', pro)
            if (pro > random.random()):
                if(tabu.full()):
                    tabu.get()
                    tabu.put(fitness(ac_list,temp_list,FFD_dic,salary))
                else:
                    tabu.put(fitness(ac_list,temp_list,FFD_dic,salary))

                Tep = 0.95 * Tep
                find = True
                return Tep, temp_list


def find_temp(seq,ac_list,FFD_dic,salary):
    sample = []
    value = []
    for i in range(0, 101):
        random.shuffle(seq)
        seq1 = seq
        sample.append(fitness(ac_list, seq1, FFD_dic, salary))
    for i in range(0, 100):
        diff = sample[i + 1] - sample[i]
        value.append(diff)
    mean = statistics.mean(value)
    dev = statistics.stdev(value)
    Tep = -(mean + dev) / (math.log(0.9) / math.log(math.e))
    return Tep

def tabu_with_gbest(element, tabu):
    tabu_list = tabu
    if element in tabu_list:
        x = tabu_list.index(element)
        l = len(tabu_list) - 1
        C_list = tabu_list.copy()
        while((x-1)!=l):
            if(l == (len(tabu_list)-1)):
                C_list[l] = element
                l = l-1
            else:
                C_list[l] = tabu_list[l+1]
                l = l-1
    # Q = Queue(maxsize=len(tabu_list))
    # for e in C_list:
    #     Q.put(e)

    return tabu_list


