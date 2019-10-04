from FFD import FFDget_init
from callf import *
from tabu_embedded_SA import *

if __name__ == '__main__':
    file_location = "small_scale_data - new/a15s20c8.txt"
    #region preprocess
    with open(file_location, 'r') as input_data_file:
        input_data = ''.join(input_data_file.readlines())

    lines = input_data.split('\n')

    firstLine = lines[0].split()
    actor_num, scene_num, capacity = int(firstLine[0]), int(firstLine[1]), int(firstLine[2])

    # list of each actor's salary
    salary = [0] * actor_num
    for i in range(actor_num):
        salary[i] = float(lines[1].split(" ")[i])

    # list of each scene's length
    h = [0]*scene_num
    for i in range(scene_num):
        h[i] = float(lines[2].split(" ")[i])

    # p is 2d actor_scene array
    ac_list = [[0]*scene_num for i in [0]*actor_num]

    for i in range(actor_num):
        for j in range(scene_num):
            ac_list[i][j] = int(lines[i+3].split(" ")[j])
    #endregion

    # number of days & dictionary for init dictionary by FFD
    days, FFD_dic = FFDget_init(f_h=h, f_capacity=capacity)
    init_seq = [0]*days
    for i in range(days):
        init_seq[i] = i

    initial_fitness = fitness(ac_list, init_seq, FFD_dic, salary)
    print("initial:",initial_fitness)

    print(tabu_embedded_SA(ac_list,init_seq,FFD_dic,salary))






