import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import math

def calculate_max_coverage(grid_width, grid_height, cell_width, cell_height, circle_diameter):
    max_coverage = 0
    best_center = (0, 0)

    for k in range(1000):
        # 随机选取圆心位置
        center_x = grid_width * cell_width / 2 + np.random.uniform(0, cell_width)
        center_y = grid_height * cell_height / 2 + np.random.uniform(0, cell_height)

        # 计算圆心位置的覆盖格子数量
        coverage = calculate_coverage(grid_width, grid_height,center_x, center_y, cell_width, cell_height, circle_diameter)
        print("No.", k , ":")
        print("最大覆盖格子数:", max_coverage)
        print("最佳圆心位置:", best_center)
        if coverage > max_coverage:
            max_coverage = coverage
            best_center = (center_x, center_y)

    return max_coverage, best_center

def is_in_coverage(grid_width, grid_height, center_x, center_y, cell_width, cell_height, circle_diameter,i,j):
    radius = circle_diameter / 2
    top_left_x = i * cell_width
    top_left_y = j * cell_height
    bottom_right_x = (i + 1) * cell_width
    bottom_right_y = (j + 1) * cell_height

    # 检查格子的四个顶点是否都在圆形范围内
    if (top_left_x - center_x) ** 2 + (top_left_y - center_y) ** 2 <= radius ** 2 and \
            (bottom_right_x - center_x) ** 2 + (top_left_y - center_y) ** 2 <= radius ** 2 and \
            (top_left_x - center_x) ** 2 + (bottom_right_y - center_y) ** 2 <= radius ** 2 and \
            (bottom_right_x - center_x) ** 2 + (bottom_right_y - center_y) ** 2 <= radius ** 2:
        return 1
    else: return 0



def calculate_coverage(grid_width, grid_height, center_x, center_y, cell_width, cell_height, circle_diameter):
    # 计算圆的半径
    radius = circle_diameter / 2
    # 计算圆形覆盖的格子数量
    coverage = 0
    # 遍历圆形边界内的每个格子
    for i in np.arange(0, grid_width , 1):
        for j in np.arange(0, grid_height , 1):
            if is_in_coverage(grid_width, grid_height, center_x, center_y, cell_width, cell_height, circle_diameter,i,j):
                coverage += 1
    return coverage




def visualize(grid_width, grid_height, cell_width, cell_height, circle_diameter, best_center):
    fig = plt.figure(figsize=(8, 8))
    gs = gridspec.GridSpec(2, 2, width_ratios=[10, 1], height_ratios=[1, 10])

    ax_main = plt.subplot(gs[1, 0])
    ax_top = plt.subplot(gs[0, 0], sharex=ax_main)
    ax_right = plt.subplot(gs[1, 1], sharey=ax_main)

    # 绘制主图
    for i in np.arange(0, grid_width, 1):
        for j in np.arange(0, grid_height, 1):
            x = i * cell_width
            y = j * cell_height
            rect = plt.Rectangle((x, y), cell_width, cell_height, color='lightgray', fill=True)
            # 检查格子的四个顶点是否都在圆内
            if is_in_coverage(grid_width, grid_height, best_center[0], best_center[1], cell_width, cell_height, circle_diameter,i,j):
                rect.set_color('blue')
            ax_main.add_patch(rect)

    # 绘制圆心位置及其覆盖的格子
    circle = plt.Circle(best_center, radius=circle_diameter / 2, color='black', fill=False)
    ax_main.add_artist(circle)

    # 设置坐标轴范围，确保完整显示网格
    ax_main.set_xlim([0, grid_width * cell_width])
    ax_main.set_ylim([0, grid_height * cell_height])

    ax_main.set_aspect('equal', adjustable='box')

    ax_top.set_aspect('equal', adjustable='box')
    ax_right.set_aspect('equal', adjustable='box')

    # 隐藏顶部和右侧的刻度标签
    ax_top.xaxis.set_visible(False)
    ax_right.yaxis.set_visible(False)

    # 绘制网格线
    for i in range(grid_width + 1):
        ax_top.axvline(x=i * cell_width, color='black', linewidth=0.5)
        ax_main.axvline(x=i * cell_width, color='black', linewidth=0.5)

    for j in range(grid_height + 1):
        ax_right.axhline(y=j * cell_height, color='black', linewidth=0.5)
        ax_main.axhline(y=j * cell_height, color='black', linewidth=0.5)

    plt.xlabel('Width (mm)', fontsize=12)
    plt.ylabel('Height (mm)', fontsize=12)
    plt.title('Circle Packing in Grid', fontsize=14)

    plt.show()

def former_formula(cell_width,cell_height,circle_diameter):
    area = cell_width * cell_height
    part1 = (math.pi * (circle_diameter / 2) ** 2) / area
    part2 = (math.pi * circle_diameter) / (math.sqrt(2 * area))
    former_coverage = part1 - part2
    return former_coverage

def latter_formula(cell_width,cell_height,circle_diameter):
    area = cell_height * cell_width
    part1 = (math.pi * (circle_diameter / 2) ** 2) / area
    part2 = (math.pi * circle_diameter) / math.sqrt(cell_height ** 2 + cell_width ** 2)
    latter_coverage = part1 - part2
    return latter_coverage

# 参数
grid_width = 50 # 格子的宽度，单位为格子数量
grid_height = 50  # 格子的高度，单位为格子数量
cell_width = 2  # 格子的宽度，单位为mm
cell_height = 6  # 格子的高度，单位为mm
circle_diameter = 30  # 圆的直径，单位为mm

# 计算最佳圆心位置
max_coverage, best_center = calculate_max_coverage(grid_width, grid_height, cell_width, cell_height, circle_diameter)
former_coverage = former_formula(cell_width,cell_height,circle_diameter)
latter_coverage = latter_formula(cell_width,cell_height,circle_diameter)
print("最大覆盖格子数:", max_coverage)
print("原始公式结果:", former_coverage)
print("新型公式结果:",latter_coverage)
print("最佳圆心位置:", best_center)



# 可视化结果
visualize(grid_width, grid_height, cell_width, cell_height, circle_diameter, best_center)
