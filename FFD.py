from collections import defaultdict

def FFDget_init(f_h, f_capacity):
    total_time = sum(f_h)
    min_bin_num = int(total_time//f_capacity)
    ind = [0]*len(f_h)
    for i in range(len(f_h)):
        ind[i] = i
    ind.sort(key=lambda ind: f_h[ind], reverse=True)

    print(min_bin_num)
    dic = {}
    bin = [f_capacity]*min_bin_num

    # for i in range(len(bin)):

    s = 0
    total_days = 0
    # count = f_capacity
    while(s < len(f_h)):
        flag = False
        for i in range(len(bin)):
            if f_h[ind[s]] <= bin[i]:
                dic.setdefault(i, []).append(ind[s])
                bin[i] = bin[i] - f_h[ind[s]]
                s += 1
                flag = True
                break
            else:
                continue
        if flag == False:
            bin.append(f_capacity)

    # return total_days and a dictionary
    return len(dic), dic


FFD = FFDget_init([2.2, 1.5, 2.2, 3.2, 1.6, 2.0, 1.5], 5)
print(FFD)