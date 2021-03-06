#coding=utf-8

# 连续给定路径点测试
import numpy as np
import matplotlib.pyplot as plt

class KTarget:
    '''
    '''
    pos = 0  # 目标位置
    finalVel = 0  # 尾速
    t = 0  # 经过时间(ms)
    def __init__(self, fpos, ffinalVel, ft):
        self.pos = fpos
        self.finalVel = ffinalVel
        self.t = ft

if __name__ == '__main__':
    targets = [KTarget(100, 0.1, 1000)
               , KTarget(2000, 1, 2000)
               , KTarget(5000, 0, 3000)
               , KTarget(3000, -4, 4000)
               , KTarget(1000, 0, 5000)
               , KTarget(0, 0, 6000)]
    show_t = []
    show_target = []
    show_vel = []
    show_acc = []
    curTarget = KTarget(0, 0, 0)
    timeInterval = 1  # 控制器时间处理间隔 10ms
    # a = np.zeros((5, len(targets)))
    a = np.zeros(5)
    i = 0
    for target in targets:
        diffPos = target.pos - curTarget.pos
        diffVel = target.finalVel - curTarget.finalVel
        diffT = target.t - curTarget.t
        a[0] = curTarget.pos
        a[1] = curTarget.finalVel
        a[2] = (3 / pow(diffT, 2) * diffPos) - (2 / diffT * curTarget.finalVel) - (1 / diffT * target.finalVel)
        a[3] = (-2 / pow(diffT, 3) * diffPos) + 1 / pow(diffT, 2) * (curTarget.finalVel + target.finalVel)
        
        # 显示路径系数
        print('======================================================================================================================')
        print(a)
        # 生成显示的路径, 100细分
        if i == len(targets)-1:
            endTrue = True
        else:
            endTrue = False
        # tspan = np.linspace(0, diffT, 11, endpoint= endTrue)  # 定点插值
        tspan = np.linspace(0, diffT, 100, endpoint= endTrue)
        path = a[0] + a[1] * tspan + a[2] * pow(tspan, 2) + a[3] * pow(tspan, 3)
        vel = a[1] + 2 * a[2] * tspan + 3 * a[3] * pow(tspan, 2)
        acc = 2 * a[2] + 6 * a[3] * tspan
        for pvt in zip(tspan + curTarget.t, path, vel, acc):
            show_t.append(pvt[0] )
            show_target.append(pvt[1])
            show_vel.append(pvt[2])
            show_acc.append(pvt[3])
        plt.plot(target.t, target.pos, 'ro')
        curTarget = target
        
        i = i + 1
    try:
        fh = open('path.txt', mode = 'w')
        for pos in show_target:
            fh.write( '1,%f\n' % (pos))
        fh.close()
    except Exception as ex:
        print('写文件错误', ex)

    plt.plot(show_t, show_target, 'b-', label='pos')
    plt.plot(show_t, show_vel, label='vel')
    plt.plot(show_t, show_acc, label='acc')
    plt.legend()
    plt.grid(True)
    plt.show()
