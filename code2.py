import itertools

'''
1~19不重复填充后，横竖斜和都是38：
     (16, 19, 3)
    (12, 2, 7, 17)
  (10, 4, 5, 1, 18)
   (13, 8, 6, 11)
    (15, 14, 9)
遍历解决之。

先找出所有可行的边框。然后填充内部。如果满足要求，则输出

'''

t = sum([i for i in range(1, 19+1)])
avg = t / 5.
assert avg == 38
SUM = int(avg)

def find(arr, last_i, arr_len, total):
    # Find all the subarrays with a length equal to arr_len and a sum equal to total
    if arr_len <= 0:
        return None
    total_arr = []
    for i in range(len(arr)):
        a = arr[i]
        #print (a, arr_len, total)
        if a <= last_i: continue

        if a == total and arr_len == 1:
            total_arr.append([a])
        else:
            out = find(arr, a, arr_len-1, total-a)
            if out:
                for o in out:
                    total_arr.append([a] + o)
                    #print (out, arr_len, 'v', total_arr)
    if not total_arr:
        return None
    return total_arr

arr = [i for i in range(1, 19+1)]
out3 = find(arr, last_i=0, arr_len=3, total=SUM)

out3 = [set(o) for o in out3] # 含3个元素且和为SUM的所有数组

for o in out3: assert sum(o) == SUM
print (len(out3))

def find_ring(arr, already_idx, already_arr, cnt, last_end, end):
    def get2(arr, st):
        aa, bb = [a for a in arr if a != st]
        return [st, aa, bb], [st, bb, aa]
    
    if cnt >= 5: return []
    out = []
    for i in range(len(arr)):
        if i in already_idx: continue

        cur = arr[i]
        if last_end not in cur: continue

        arr1, arr2 = get2(cur, last_end)
        if cnt == 4 and  arr1[-1] == end:
            out.append([arr1])
        elif cnt == 4 and  arr2[-1] == end:
            out.append([arr2])
        else:
            r1 = find_ring(arr, already_idx + [i], already_arr + [arr1], cnt+1, arr1[-1], end)
            r2 = find_ring(arr, already_idx + [i], already_arr + [arr2], cnt+1, arr2[-1], end)
            if r1: 
                for r in r1:
                    out.append([arr1] + r)
            if r2: 
                for r in r2:
                    out.append([arr2] + r)
    #if len(out) > 0: print ('aaaaa', out)
    return out

def find_answer(arr):
    ''' a0, a1, a2, a3, a4, a5 顺时针首尾相接组成六边形(每个边3个数据点):
                 (a0[0], a0[1], a0[2]))
              (a5[1],   x0,   x1,   a1[1]))
           (a5[0],   x5,   x6,   x2,   a2[0]))
              (a4[1],   x4,   x3,  a2[1]))
                (a2[-1], a3[1], a3[0]))
    '''
    set_all = set([i for i in range(1, 20, 1)])
    set_used = set() # 六条边已经用了哪些1~19中数字
    for a1 in arr:
        for a2 in a1:
            set_used.add(a2)
    set_not_used = set_all - set_used # 还有哪7个数字没用

    a0, a1, a2, a3, a4, a5 = arr
    for v in set_not_used: # 余下的7个数字，只要给出一个，就可以算出余下六个。也就是说只需要遍历7遍即可
        x0 = v
        x1 = SUM - a5[1] - a1[1] - x0
        if not (1<= x1 <= 19 and x1 not in set_used): continue

        x2 = SUM - a0[1] - a2[1] - x1
        if not (1<= x2 <= 19 and x2 not in set_used): continue

        x3 = SUM - a1[1] - a3[1] - x2
        if not (1<= x3 <= 19 and x3 not in set_used): continue

        x4 = SUM - a2[1] - a4[1] - x3
        if not (1<= x4 <= 19 and x4 not in set_used): continue

        x5 = SUM - a3[1] - a5[1] - x4
        if not (1<= x5 <= 19 and x5 not in set_used): continue

        x6 = SUM - a0[-1] -a3[-1] - x1 - x4
        if not (1<= x6 <= 19 and x5 not in set_used): continue

        if len(set([x0, x1, x2, x3, x4, x5, x6])) == len(set_not_used):
            print ("     %02d %02d %02d" % (a0[0], a0[1], a0[2]))
            print ("   %02d %02d %02d %02d" % (a5[1], x0, x1, a1[1]))
            print (" %02d %02d %02d %02d %02d" % (a5[0], x5, x6, x2, a2[0]))
            print ("   %02d %02d %02d %02d" % (a4[1], x4, x3, a2[1]))
            print ("     %02d %02d %02d" % (a2[-1], a3[1], a3[0]))
            print ("---")
            return True
    return False


def find_result(arr):
    c = 0
    c1 = 0
    for  i in range(len(arr)):
        for arr1 in itertools.permutations(arr[i]):
            already_idx = [i]
            already_arr = [arr1]
            r1 = find_ring(arr, already_idx, already_arr, 0, arr1[-1], arr1[0])
            if r1:
                for r in r1:
                    arr2 = [list(arr1)] + r
                    res = find_answer(arr2)
                    #print (i, "vvv", out, "xxxx")
                    c += 1
                    if res:
                        print ('Find', c, c1, arr2)
                        c1 += 1

find_result(out3) 

