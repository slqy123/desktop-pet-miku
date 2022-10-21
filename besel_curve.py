import numpy as np


def generate(width=2, height=2, dense=100, min_angle=np.pi/18, coord=np.array([1, 1]),
             speed=np.array([1, 0])):
    cos_min_angle = np.cos(min_angle)
    x = []
    y = []
    break_count = 15; count = 0  # 实在找不到合适的c3就算了
    
    def cos_vec(vec1, vec2):
        return np.dot(vec1, vec2) / np.linalg.norm(vec1) / np.linalg.norm(vec2)

    def in_rect(coord):
        if (0 < coord[0] < width and
                0 < coord[1] < height):
            return True
        else:
            return False

    # 生成贝塞尔曲线的参考点
    c1 = coord * 1
    c2 = coord + speed

    # 根据c2是否在屏幕里分两种情况
    if in_rect(c2):
        pass
    c3 = np.random.random(2) * (width, height)
    while cos_vec(c1-c2, c3-c2) > cos_min_angle or not in_rect(2*c3-c2):
        c3 = np.random.random(2) * (width, height)
        count += 1
        if count > break_count:
            break

    # 绘制曲线
    for i in range(dense):
        t = i / dense
        dot = (1-t)**2*c1 + 2*t*(1-t)*c2 + t**2*c3
        x.append(dot[0])
        y.append(dot[1])

    # 更新点的属性
    coord = c3
    speed = c3 - c2
    print(count)
    return x, y, speed*(0.7+0.3*(1-(count-1)/break_count)), c3
