import numpy as np
import random
import math

def output_txt(a_num, s_num, c_num):
    s = "a"+str(a_num)+"s"+str(s_num)+"c"+str(c_num)+".txt"
    f = open("small_scale_data/"+s, 'w')
    f.write(str(a_num)+" "+str(s_num)+" "+str(c_num)+"\n")
    for i in range(a_num):
        f.write(str(round(np.random.normal(loc=250, scale=50, size=None), 0)) + " ")
    f.write("\n")
    for j in range(s_num):
        f.write(str(round(np.random.normal(loc=c_num/2 , scale=0.85, size=None), 1)) + " ")
    f.write("\n")
    for a in range(a_num):
        for s in range(s_num):
            f.write(str(random.randint(0, 1)) + " ")
        f.write("\n")
    f.close()



actor_num = [5, 10, 15]
scene_num = [10, 15, 20]
capacity_num = [6, 7, 8]

for i in range(len(actor_num)):
    for j in range(len(scene_num)):
        for k in range(len(capacity_num)):
            output_txt(actor_num[i], scene_num[j], capacity_num[k])












