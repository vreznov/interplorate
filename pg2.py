#coding=utf-8

# 通过给定的位置和时间，自动计算速度
'''
1.可以按固定间隔给出或者按照指定间隔给出时间轴
'''

import numpy as np
import matplotlib.pyplot as plt

# 给定数据
targets = []  #mm
endVels = []  #mm/ms
time_squence = []  #ms
time_interval = 10  #ms 0-使用time_squence给定的时间间隔 other：使用时间间隔等于time_interval
autoVel = True  # 是否自动计算速度

curTarget = 0  # 初始值，用于作为计算的第一个目标值
curVel = 0
curTime = 0
vnext = 0 # 下一段运动的均速
target = 0
endVel = 0

diffPos = 0
diffVel = 0
diffT = 0

a = np.zeros(5) # 系数，最高5阶

# 用于显示的数据
show_t = []
show_target = []
show_vel = []
show_acc = []

if __name__ == '__main__':
	# 初始化数据
    targets = np.random.randint(0, 1000, size=(1,10))[0]
    time_squence = np.random.randint(8, 100, size=(1,10))[0]
    
    # 以下两行测试使用
    targets = [100, 2000, 3000, 5000, 3000, 1000, 0]
    time_squence = [1000, 1000, 1000, 1000, 1000, 1000, 1000]
    
    endVels = np.zeros((1,10))[0]
    #show_t.append(0)
    print(targets)
    print(time_squence)
	
    # 附加末尾空数据
    targets = np.append(targets, 0)
    time_squence = np.append(time_squence,0)
	# 开始计算
    i = 0
    # for target, t in zip(targets,time_squence) :
    for i in np.arange(len(targets)-1):
        target = targets[i]
        
        # 自动计算速度
        if autoVel:
            diffT = time_interval
            endVel = (target - curTarget) / time_interval
            vnext = (targets[i+1] - target) / time_interval
            # 判断符号，如果本段速度与下段速度方向不同，则将本段速度末速度设置为0。如果最后一个点设置速度为0
            if endVel*vnext < 0 or i==len(targets)-1:
                endVel = 0
        else:
            endVel = endVels[i]
            diffT = time_squence[i]
                

        diffPos = target - curTarget
        diffVel = endVel
        
        a[0] = curTarget
        a[1] = curVel
        a[2] = (3 / pow(diffT, 2) * diffPos) - (2 / diffT * curVel) - (1 / diffT * endVel)
        a[3] = (-2 / pow(diffT, 3) * diffPos) + 1 / pow(diffT, 2) * (curVel + endVel)
        
        # 显示路径系数
        #print('========================================================================')
        # 生成显示的路径, 100细分
        if i == len(targets)-2: # 额外加了尾数据，所以是-2
            endTrue = True
        else:
            endTrue = False
        # tspan = np.linspace(0, diffT, 11, endpoint= endTrue)  # 定点插值
        tspan = np.linspace(0, diffT, 100, endpoint= endTrue)
        pnt = a[0] + a[1] * tspan + a[2] * pow(tspan, 2) + a[3] * pow(tspan, 3)
        vel = a[1] + 2 * a[2] * tspan + 3 * a[3] * pow(tspan, 2)
        acc = 2 * a[2] + 6 * a[3] * tspan
        if autoVel:
            xval = diffT*i
        else:
            xval = curTime
        for pvt in zip(tspan + curTime, pnt, vel, acc):
            show_t.append(pvt[0] )
            show_target.append(pvt[1])
            show_vel.append(pvt[2])
            show_acc.append(pvt[3])
            plt.plot(xval, curTarget, 'ro')
            
        
        # 更新数据
        curTarget = target
        curVel = endVel
        if autoVel:
            curTime = curTime + time_interval
        else:
            curTime = curTime + time_squence[i]
        i = i + 1
    
    if autoVel:
            xval = diffT*i
    else:
        xval = curTime + time_squence[i]
        
    try:
        fh = open('path.txt', mode = 'w')
        for pos in show_target:
            fh.write( '1,%f\n' % (pos))
        fh.close()
    except Exception as ex:
        print('写文件错误', ex)
        
    plt.plot(xval, curTarget, 'ro')
    plt.plot(show_t, show_target, 'b-', label='pos')
    plt.plot(show_t, show_vel, label='vel')
    plt.plot(show_t, show_acc, label='acc')
    plt.legend()
    plt.grid(True)
    plt.show()