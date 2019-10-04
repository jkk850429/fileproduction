def fitness(aslist, sequence, dictionary, salary):
    '''
    :param aslist: actor_scene list
    :param sequence: ex:[3,1,4,2,5,0]
    :param dictionary: constructed by FFD
    :return: total cost
    '''
    n_actors = len(aslist)
    n_days = len(dictionary)
    ad_list = [[0]*n_days for i in [0]*n_actors]
    actor_salary = [0]*n_actors


    for i in range(n_actors):
        for j in range(n_days):
            subseq = sequence[j]
            #print(subseq)
            for day, scene in dictionary.items():
                if day == subseq:
                    for k in range(len(scene)):
                        s = scene[k]
                        if aslist[i][s] == 1:
                            ad_list[i][j] = 1
                            break
                        else:
                            ad_list[i][j] = 0
    # print(ad_list)


    sum = 0
    for i in range(n_actors):
        left = 0
        right = n_days-1
        for l in range(0, n_days):
            if ad_list[i][l] == 1:
                left = l
                break
        for r in range(0, n_days):
            if ad_list[i][n_days-1-r] == 1:
                right = n_days-1-r
                break
        actor_salary[i] = salary[i]*(right-left+1)
        sum += actor_salary[i]
    # print(actor_salary, sum)

    sum += 1500*n_days
    return sum

