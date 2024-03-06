
bit_length = 4

def gen_tree(a,b,tree,idx_tree):
    a_idx, b_idx = bit_length - 1, bit_length - 1 #change for 32
    for i in range(1,1 + bit_length):
        idxs = []
        for k in range(i):
            #pp.append(int(a[a_idx]) * int(b[b_idx]))
            idxs.append(f"pp[{a_idx}][{b_idx}]") # 'pp[{}][{}].
            if k != i - 1:
                a_idx = a_idx + 1
                b_idx = b_idx - 1
            else:
                b_idx = bit_length - 1
                a_idx = a_idx - i
        idx_tree.append(idxs)
        #tree.append(pp)
    a_idx , b_idx = 0, bit_length - 2
    for i in range(bit_length - 1,0,-1):
        idxs = []
        for k in range(i):
            #pp.append(int(a[a_idx]) * int(b[b_idx]))
            idxs.append(f"pp[{a_idx}][{b_idx}]")
            if k != i - 1:
                a_idx = a_idx + 1
                b_idx = b_idx - 1
            else:
                a_idx = 0
                b_idx = k - 1
        idx_tree.append(idxs)
    
    #idx_tree = idx_tree[::-1]
    #print(idx_tree)
    # print(tree)

def reduction(tree):
    stages = 2 #change for 32
    fa_tot, ha_tot = 0,0
    for i in range(stages):
        print(f'//stage {i} reduction')
        bit_idx = 0
        if i == 0: #change for 32
            target_height = 3
        else:
            target_height = 2
        # elif i == 1:
        #     target_height = 19
        # elif i == 2:
        #     target_height = 13
        # elif i == 3:
        #     target_height = 9
        # elif i == 4:
        #     target_height = 6
        # elif i == 5:
        #     target_height = 4
        # elif i == 6:
        #     target_height = 3
        # elif i == 7:
        #     target_height = 2
        for k in range(len(tree)):
            if len(tree[k]) <= target_height:
                continue
            elif len(tree[k]) - target_height == 1: # HA CASE
                first = tree[k].pop(0)
                second = tree[k].pop(0)
                print(f'HA ha{ha_tot}( .a({first}), .b({second}), .sum(s{i}[{bit_idx}]), .cout(c{i}[{bit_idx}]) );')
                tree[k].insert(0,f's{i}[{bit_idx}]')
                if k != len(tree) - 1:
                    tree[k+1].append(f'c{i}[{bit_idx}]')
                ha_tot += 1
                bit_idx += 1
            elif len(tree[k]) - target_height > 1: # FA CASE
                curr_height = len(tree[k]) - target_height
                ptr = 0
                while curr_height != 0:
                    if curr_height == 1:
                        first = tree[k].pop(ptr)
                        second = tree[k].pop(ptr)
                        print(f'HA ha{ha_tot}( .a({first}), .b({second}), .sum(s{i}[{bit_idx}]), .cout(c{i}[{bit_idx}]) );')
                        tree[k].insert(0,f's{i}[{bit_idx}]')
                        if k != len(tree) - 1:
                            tree[k+1].append(f'c{i}[{bit_idx}]')
                        ptr += 1
                        ha_tot += 1
                        bit_idx += 1
                        curr_height -= 1
                    else:
                        first = tree[k].pop(ptr)
                        second = tree[k].pop(ptr)
                        third = tree[k].pop(ptr)
                        print(f'FA fa{fa_tot}( .a({first}), .b({second}), .cin({third}), .sum(s{i}[{bit_idx}]), .cout(c{i}[{bit_idx}]) );')
                        tree[k].insert(0,f's{i}[{bit_idx}]')
                        if k != len(tree) - 1:
                            tree[k+1].append(f'c{i}[{bit_idx}]')
                        ptr += 1
                        fa_tot += 1
                        bit_idx += 1
                        curr_height -= 2
    print(fa_tot)
    print(ha_tot)
    print('//addition stage')
    C_idx = 1
    i = stages
    bit_idx = 0
    for k in range(len(tree)):
        if len(tree[k]) == 1:
            continue
        elif len(tree[k]) == 2:
            first = tree[k].pop(0)
            second = tree[k].pop(0)
            print(f'HA ha{ha_tot}( .a({first}), .b({second}), .sum(C[{C_idx}]), .cout(c{i}[{bit_idx}]) );')
            tree[k].insert(0,f's{i}[{bit_idx}]')
            if k != len(tree) - 1:
                tree[k+1].append(f'c{i}[{bit_idx}]')
            ha_tot += 1
            bit_idx += 1
            C_idx += 1
        elif len(tree[k]) == 3:
            first = tree[k].pop(0)
            second = tree[k].pop(0)
            third = tree[k].pop(0)
            print(f'FA fa{fa_tot}( .a({first}), .b({second}), .cin({third}), .sum(C[{C_idx}]), .cout(c{i}[{bit_idx}]) );')
            tree[k].insert(0,f's{i}[{bit_idx}]')
            if k != len(tree) - 1:
                tree[k+1].append(f'c{i}[{bit_idx}]')
            fa_tot += 1
            bit_idx += 1
            C_idx += 1



                        


a = '1001'
b = '0111'

#0 a[3] * b[3]
#1 a[2] * b[3], a[3] * b[2]
#2 a[1] * b[3], a[2] * b[2], a[3] * b[1]
#3 a[0] * b[3], a[1] * b[2], a[2] * b[1], a[3] * b[0]

#0 a[0] * b[2], a[1] * b[1], a[2] * b[0]
#1 a[0] * b[1], a[1] * b[0]
#3 a[0] * b[0]

#print(gen_pp(a,b))
tree, idx_tree = [], []
gen_tree(a,b,tree,idx_tree)
idx_tree = idx_tree[::-1]
print(idx_tree)
reduction(idx_tree)
#print(tree)

