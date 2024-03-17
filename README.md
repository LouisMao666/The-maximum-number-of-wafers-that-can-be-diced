Solved by genetic algorithm, the maximum number of wafers that can be cut

## 遗传算法

1. **初始化种群**：
   - 初始化一组初始的切割方案作为种群。每个个体表示一种切割方案，包含多个晶片的位置和尺寸。

2. **计算适应度**：
   - 对于每个个体，计算晶片的数量作为适应度值。晶片数量越多，适应度越高。

3. **选择操作**：
   - 根据个体的适应度值，使用选择算子（例如轮盘赌选择）选择一部分个体用于产生下一代。

4. **交叉操作**：
   - 从选择的个体中随机选取一对个体进行交叉操作，产生新的个体。交叉点可以是晶片的边界位置。

5. **变异操作**：
   - 对交叉后的个体进行变异操作。变异可以是随机改变晶片位置或尺寸的操作。

6. **替换**：
   - 使用选择算子从父代和子代中选择出下一代的种群。

7. **终止条件**：
   - 如果满足终止条件（例如达到最大迭代次数或者找到满意的解决方案），则停止优化过程，否则返回步骤3。

8. **输出结果**：
   - 输出最优的切割方案，即具有最多晶片数量的方案。

### 初次尝试

```python
import random
import math

# 定义晶圆直径和切割晶片的长宽尺寸
DIAMETER = 30
CHIP_LENGTH = 3
CHIP_WIDTH = 2

# 定义遗传算法参数
POP_SIZE = 20
MAX_GENERATIONS = 100
MUTATION_RATE = 0.1

# 计算晶片的对角线长度
CHIP_DIAGONAL = math.sqrt(CHIP_LENGTH ** 2 + CHIP_WIDTH ** 2)


# 计算一个晶片的坐标
def random_chip():
    x = random.uniform(0, DIAMETER - CHIP_LENGTH)
    y = random.uniform(0, DIAMETER - CHIP_WIDTH)
    return (x, y)


# 计算一个切割方案的晶片数量
def count_chips(solution):
    chip_count = 0
    for x, y in solution:
        chip_count += 1
        # 检查该晶片是否与其他晶片重叠
        for x2, y2 in solution:
            if x != x2 and y != y2 and abs(x - x2) < CHIP_LENGTH and abs(y - y2) < CHIP_WIDTH:
                chip_count -= 1
                break
    return chip_count


# 计算适应度
def fitness(solution):
    return count_chips(solution)


# 选择操作
def selection(population):
    return random.choices(population, weights=[fitness(solution) for solution in population], k=2)


# 交叉操作
def crossover(parent1, parent2):
    # 选择较短的父代作为子代长度
    child_length = min(len(parent1), len(parent2))
    # 随机选择交叉点
    crossover_point = random.randint(0, child_length)
    # 生成子代
    child = parent1[:crossover_point] + parent2[crossover_point:]
    return child



# 变异操作
def mutation(child):
    for i in range(len(child)):
        if random.random() < MUTATION_RATE:
            child[i] = random_chip()
    return child


# 遗传算法主函数
def genetic_algorithm():
    # 初始化种群
    population = [[random_chip() for _ in range(random.randint(1, math.ceil(DIAMETER / CHIP_DIAGONAL)))] for _ in
                  range(POP_SIZE)]

    # 迭代优化
    for generation in range(MAX_GENERATIONS):
        # 选择操作
        parent1, parent2 = selection(population)
        # 交叉操作
        child = crossover(parent1, parent2)
        # 变异操作
        child = mutation(child)
        # 替换操作
        population[random.randint(0, POP_SIZE - 1)] = child

        best_solution = max(population, key=fitness)
        print(f"Generation {generation + 1}, Best Chip Count: {fitness(best_solution)}")

    best_solution = max(population, key=fitness)
    print(f"Best Solution: {best_solution}, Chip Count: {fitness(best_solution)}")


if __name__ == "__main__":
    genetic_algorithm()
```

结果：

坐标为晶片位置

![2024-03-17](https://github.com/LouisMao666/The-maximum-number-of-wafers-that-can-be-diced/assets/149593046/957b1d1f-d703-4c61-80f5-b6feaef1bafa)


这种方法没有考虑晶片摆放的方向，得到的结果并不理想，直径30的晶圆只能切割出8个尺寸为2*3的晶片，找到问题继续优化，加上了晶片的方向。

### 优化后的算法

```python
import random
import math

# 定义晶圆直径和切割晶片的长宽尺寸
DIAMETER = 30
CHIP_LENGTH = 3
CHIP_WIDTH = 2

# 定义遗传算法参数
POP_SIZE = 20
MAX_GENERATIONS = 100
MUTATION_RATE = 0.1


# 生成随机晶片的坐标
def random_chip():
    x = random.uniform(0, DIAMETER - CHIP_LENGTH)
    y = random.uniform(0, DIAMETER - CHIP_WIDTH)
    return (x, y)


# 计算晶片在晶圆内的最大数量
def max_chips():
    # 计算晶片在行和列上的最大数量
    max_rows = math.floor(DIAMETER / CHIP_LENGTH)
    max_cols = math.floor(DIAMETER / CHIP_WIDTH)
    # 返回晶片在晶圆内的最大数量
    return max_rows * max_cols


# 生成初始种群
def initialize_population():
    population = []
    for _ in range(POP_SIZE):
        solution = []
        for row in range(math.ceil(DIAMETER / CHIP_LENGTH)):
            for col in range(math.ceil(DIAMETER / CHIP_WIDTH)):
                solution.append(random_chip())
        population.append(solution)
    return population


# 计算适应度
def fitness(solution):
    return len(set(solution))


# 选择操作
def selection(population):
    return random.choices(population, weights=[fitness(solution) for solution in population], k=2)


# 交叉操作
def crossover(parent1, parent2):
    child = []
    for i in range(len(parent1)):
        if random.random() < 0.5:
            child.append(parent1[i])
        else:
            child.append(parent2[i])
    return child


# 变异操作
def mutation(child):
    for i in range(len(child)):
        if random.random() < MUTATION_RATE:
            child[i] = random_chip()
    return child


# 遗传算法主函数
def genetic_algorithm():
    population = initialize_population()
    for generation in range(MAX_GENERATIONS):
        parent1, parent2 = selection(population)
        child = crossover(parent1, parent2)
        child = mutation(child)
        population[random.randint(0, POP_SIZE - 1)] = child

        best_solution = max(population, key=fitness)
        print(f"Generation {generation + 1}, Best Chip Count: {fitness(best_solution)}")

    best_solution = max(population, key=fitness)
    print(f"Best Solution: {best_solution}, Chip Count: {fitness(best_solution)}")


if __name__ == "__main__":
    genetic_algorithm()
```

结果:
![image](https://github.com/LouisMao666/The-maximum-number-of-wafers-that-can-be-diced/assets/149593046/a5f4b056-02bf-4783-a7af-fec534677687)

结果显然是有误的，晶片的总面积远超了晶圆总面积，违背常理。

![image](https://github.com/LouisMao666/The-maximum-number-of-wafers-that-can-be-diced/assets/149593046/6cfd2114-fe74-4b9e-8ac1-fbe33bbd73a6)

经过思考发现错在初始晶片位置的时候，没有考虑到重叠的情况，因此估算结果偏大很多。

### 优化算法

加上了重叠的情况

```python
# 检查晶片位置是否重叠
def is_overlapping(new_chip, existing_chip):
    x1, y1 = new_chip
    x2, y2 = existing_chip
    return not (x1 + CHIP_LENGTH <= x2 or x2 + CHIP_LENGTH <= x1 or y1 + CHIP_WIDTH <= y2 or y2 + CHIP_WIDTH <= y1)
```

理论上这样是可以的，但是这样修改在插入新的晶片时，需要遍历以前所有已插入的晶片，所以运行效率很低。

在我的电脑上运行不出结果。

## 更快速的算法

在网上搜索die per wafer找到很多网站，这些网站的解法给我很大的启发。

### web：http://www.silicon-edge.co.uk/j/index.php/resources/die-per-wafer

简介：Mike Davison
Mike Davison has over 30 years experience working for telecommunications, consumer electronics and fabless semiconductor companies.

From 2011 to 2014 Mike served as COO at NXT plc which subsequently became HiWave Technologies plc, and then Redux Laboratories following privatisation. This role was based in Hong Kong where Mike also managed the Hong Kong office, dealing with manufacturers and customer CEMs in China, Taiwan and Japan. He managed several new product introductions including BMR loudspeakers, haptics transducers and bluetooth audio amplifier modules.

Mike previously established and managed the Operations departments at VC-funded fabless semiconductor start-ups picoChip and Audium Semiconductor where he was reponsible for taking multiple devices and board-level products from design to volume manufacture, working extensively with suppliers and customers in the Far East, Europe and the USA.

Mike's experience goes far beyond Operations - he has directly contributed to the architecture and design of many semiconductor devices and electronic systems. He established and led hardware and software design teams developing high-speed digital & RF boards and embedded operating systems for board-level products.

Prior to picoChip, Mike helped establish a UK chip design centre for Oak Technology Inc. which developed receiver chips for the set-top box and digital TV market. This was subsequently acquired by Conexant where he was appointed as Managing Director. He also held engineering management roles at Pioneer (Japan) and Brooktree (US).

Mike started his career with GEC Telecommunications Ltd. (later GPT). He holds an honours degree in Electronics and an MSc in Telecommunications Technology.

![image](https://github.com/LouisMao666/The-maximum-number-of-wafers-that-can-be-diced/assets/149593046/28e02f8f-0e0c-42dc-9ec5-4d5a53869482)

### 基本思路

这个算法的基本思路很好理解，可以将在晶圆中切取尽可能多晶片的问题，抽象为让一个圆尽可能的包括更多的长方形（晶片为长方形）。

那么我们可以让晶片的位置不动，改变圆心的位置，来求出最多的晶片数量。

原先的算法：尽可能多的在一个圆里插入长方形

![？](https://github.com/LouisMao666/The-maximum-number-of-wafers-that-can-be-diced/assets/149593046/358ceadc-6e64-4c8d-9b9f-777dff9abb6a)   

改进的算法： 尽可能多的让长方形包含在圆中

![image](https://github.com/LouisMao666/The-maximum-number-of-wafers-that-can-be-diced/assets/149593046/d68ea94f-8990-4c70-b631-0dcb09d65c14)

#### 代码解释

标准库和常量定义

```python
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

# 参数
grid_width = 50 # 格子的宽度，单位为格子数量
grid_height = 50  # 格子的高度，单位为格子数量
cell_width = 0.7  # 格子的宽度，单位为mm
cell_height = 1.4  # 格子的高度，单位为mm
circle_diameter = 30  # 圆的直径，单位为mm
```

由于圆的对称性，所以无论我们如何选择、平移这个圆，其结果都可以看做这个圆在一个格子内平移的等价情况。

因此直接选择整个网格的中心作为圆心，为了解决问题，直接简单粗暴地随机在格子中取1000个点作为圆心，以包含格子最多的情况作为圆心的最佳位置。

（这里没有用更加高深的算法实在是因为觉得杀鸡何须用牛刀，晶片面积是远小于晶圆面积的，在晶片中随机取1000个点，精度完全够用）

```python
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
```

定义一个判断格子是否在圆内的函数，判断标准为格子的四个顶点都在圆内。

```pyhton
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
```

计算包含在圆内格子的数量，这个不用多解释

```python
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
```

使用matplotlib可视化结果

```python
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
```

### 结果展示

#### 第一组是题目1中的数据：

cell_width = 0.7  # 格子的宽度，单位为mm
cell_height = 0.7  # 格子的高度，单位为mm
circle_diameter = 30  # 圆的直径，单位为mm

![image](https://github.com/LouisMao666/The-maximum-number-of-wafers-that-can-be-diced/assets/149593046/fa00c182-53c4-4648-8f4d-dc7e34eec5af)
![image](https://github.com/LouisMao666/The-maximum-number-of-wafers-that-can-be-diced/assets/149593046/514067eb-c55d-4075-98b9-a4a1d79a8dd4)

#### 第二组测试一下长方形的情况：

cell_width = 0.7  # 格子的宽度，单位为mm
cell_height = 1.4  # 格子的高度，单位为mm
circle_diameter = 30  # 圆的直径，单位为mm

![image](https://github.com/LouisMao666/The-maximum-number-of-wafers-that-can-be-diced/assets/149593046/b2e62ce3-8eeb-467b-bfd6-6d9bbf41ad2a)
![image](https://github.com/LouisMao666/The-maximum-number-of-wafers-that-can-be-diced/assets/149593046/66a74f16-df9e-48f6-aed9-0ddcb6f85674)

### 对比传统算法

![a8ffec2ad96a17bdd7db41dc783b3ee](https://github.com/LouisMao666/The-maximum-number-of-wafers-that-can-be-diced/assets/149593046/df3505e5-7e72-4f9a-acdd-19ef2d1c5878)

在晶片长宽比较大的情况下，传统算法对晶圆边缘处晶片的估算误差较大。

新型算法在精确度上有明显优势，同时这种算法可以轻松的实现结果可视化。













