from math import exp

tc_decay = 20.0 # 20 ms
for dt in range(0,200):
    print(exp(-dt/tc_decay))
    

