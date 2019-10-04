from collections import namedtuple
from gurobipy import *
# import numpy as np

def main(input_data):

    lines = input_data.split('\n')

    firstLine = lines[0].split()
    actor_count, scene_count, Capacity = int(firstLine[0]), int(firstLine[1]), int(firstLine[2])
    # cost everyday
    C = 1500
    as_list = [[0]*scene_count for i in [0]*actor_count]
    salary_list = [0]*actor_count
    scenehour_list = [0]*scene_count
    salary_line = lines[1].split()
    scenehour_line = lines[2].split()
    # for i in range(3, len(lines)):
    for i in range(3, 3+actor_count):
        for j in range(0, scene_count):
            as_list[i-3][j] = int(lines[i].split()[j])
    for i in range(actor_count):
        salary_list[i] = float(salary_line[i])
    for i in range(scene_count):
        scenehour_list[i] = float(scenehour_line[i])
    print(as_list)



    # region Gurobi

    # Create a new model
    m = Model("mip")

    # Create variables
    x = {}
    for j in range(scene_count):
        for k in range(scene_count):
            n = "x_" + str(j) + "_" + str(k)
            x[j, k] = m.addVar(vtype=GRB.BINARY, name=n)

    y = {}
    for i in range(actor_count):
        for k in range(scene_count):
            n = "y_" + str(i) + "_" + str(k)
            y[i, k] = m.addVar(vtype=GRB.BINARY, name=n)

    z = {}
    for i in range(scene_count):
        n = "z_" + str(i)
        z[i] = m.addVar(vtype=GRB.BINARY, name=n)

    v = {}
    for i in range(actor_count):
        n = "v" + str(i)
        v[i] = m.addVar(vtype=GRB.INTEGER, name=n)


    # Set objective
    obj = LinExpr()
    for i in range(actor_count):
        obj.addTerms(salary_list[i], v[i])
    for k in range(scene_count):
        obj.addTerms(C, z[k])
    m.setObjective(obj, GRB.MINIMIZE)

    # Add constraint: x + 2 y + 3 z <= 4
    # m.addConstr(x + 2 * y + 3 * z <= 4)

    M = 9999

    '''Constraint 1'''
    for j in range(scene_count):
        constr1 = LinExpr()
        for k in range(scene_count):
            constr1.addTerms(1, x[j, k])
        m.addConstr(constr1 == 1, "c1")

    '''Constraint 2'''
    for k in range(scene_count):
        constr2 = LinExpr()
        for j in range(scene_count):
            constr2.addTerms(scenehour_list[j], x[j, k])
        m.addConstr(constr2 <= Capacity*z[k], "c2")

    '''Constraint 3'''
    for i in range(actor_count):
        for j in range(scene_count):
            for k in range(scene_count):
                m.addConstr(as_list[i][j]*x[j, k]-y[i, k] <= 0, "c3")


    '''Constraint 4'''

    for i in range(actor_count):
        for k1 in range(scene_count):
            for k2 in range(scene_count):
                if k2 < k1:
                    continue
                else:
                    m.addConstr((k2-k1+1)+M*(y[i, k1]-1)+M*(y[i, k2]-1) <= v[i], "c4")
    for i in range(actor_count):
        m.addConstr(v[i] >= 0, "c5")



    m.optimize()

    print('Obj: %g' % m.objVal)
    for v in m.getVars():
        print('%s %g' % (v.varName, v.x))
    return m.objVal
    # endregion


if __name__=="__main__":
    file_location="small_scale_data - new/a5s15c8.txt"
    with open(file_location, 'r') as input_data_file:
        input_data = ''.join(input_data_file.readlines())

    result = main(input_data)

    print(result)
    s = "result.txt"
    f = open("result/" + s, 'w')
    f.write(str(result) + "\n")