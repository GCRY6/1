import pygame
import math
import random

# 初始化 pygame
pygame.init()

# 设置窗口的尺寸
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Moving Ball")

# 定义颜色
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

# 球的初始位置和半径
ball_x = width // 2
ball_y = height // 2
ball_radius = 20

# 正方形的初始位置和边长
square_x = 50
square_y = 50
square_size = 30

# 生成静态障碍物
num_obstacles = 5
obstacles = []
for _ in range(num_obstacles):
    obs_x = random.randint(100, width - 100)
    obs_y = random.randint(100, height - 100)
    obs_size = random.randint(30, 60)
    obstacles.append((obs_x, obs_y, obs_size))

# 生成动态障碍物
num_dynamic_obstacles = 3
dynamic_obstacles = []
for _ in range(num_dynamic_obstacles):
    dyn_obs_x = random.randint(100, width - 100)
    dyn_obs_y = random.randint(100, height - 100)
    dyn_obs_size = random.randint(20, 40)
    dyn_obs_speed_x = random.choice([-2, 2])
    dyn_obs_speed_y = random.choice([-2, 2])
    dynamic_obstacles.append([dyn_obs_x, dyn_obs_y, dyn_obs_size, dyn_obs_speed_x, dyn_obs_speed_y])


# 障碍物属性
obstacles = []
for _ in range(5):
    obs_x = random.randint(100, width - 100)
    obs_y = random.randint(100, height - 100)
    obs_size = random.randint(30, 60)
    obstacles.append((obs_x, obs_y, obs_size))

# 动态障碍物属性
dynamic_obstacles = []
for _ in range(3):
    dyn_obs_x = random.randint(100, width - 100)
    dyn_obs_y = random.randint(100, height - 100)
    dyn_obs_size = random.randint(20, 40)
    dyn_obs_speed_x = random.choice([-2, 2])
    dyn_obs_speed_y = random.choice([-2, 2])
    dynamic_obstacles.append([dyn_obs_x, dyn_obs_y, dyn_obs_size, dyn_obs_speed_x, dyn_obs_speed_y])

# 车道属性
lane_width = 100
num_lanes = width // lane_width
ball_lane = num_lanes // 2
lane_change_cooldown = 0
lane_change_duration = 30  # 变道持续帧数

# 球的初始速度
ball_speed = 3
ball_speed_x = random.choice([-ball_speed, ball_speed])
ball_speed_y = random.choice([-ball_speed, ball_speed])

# 正方形的移动速度
square_speed = 5
square_speed_x = 0
square_speed_y = 0

# 用于控制速度和大小变化的计数器
speed_change_counter = 0
size_change_counter = 0
direction_change_counter = 0

# 时间限制（秒）
time_limit = 60
start_time = pygame.time.get_ticks()

# 游戏主循环
running = True
clock = pygame.time.Clock()

while running:
    elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
    if elapsed_time >= time_limit:
        print("Time's up! You lose.")
        running = False

    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                square_speed_y = -square_speed
            elif event.key == pygame.K_DOWN:
                square_speed_y = square_speed
            elif event.key == pygame.K_LEFT:
                square_speed_x = -square_speed
            elif event.key == pygame.K_RIGHT:
                square_speed_x = square_speed
            elif event.key == pygame.K_SPACE and lane_change_cooldown == 0:
                # 尝试变道
                new_lane = ball_lane + random.choice([-1, 1])
                if 0 <= new_lane < num_lanes:
                    ball_lane = new_lane
                    lane_change_cooldown = lane_change_duration
        elif event.type == pygame.KEYUP:
            if event.key in [pygame.K_UP, pygame.K_DOWN]:
                square_speed_y = 0
            elif event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                square_speed_x = 0

    # 变道冷却时间递减
    if lane_change_cooldown > 0:
        lane_change_cooldown -= 1

    # 每隔一段时间改变球的速度
    speed_change_counter += 1
    if speed_change_counter % 60 == 0:  # 每60帧（1秒）改变一次速度
        # 随机改变球的速度，变化范围在原速度的0.5倍到1.5倍之间
        ball_speed = random.uniform(ball_speed * 0.5, ball_speed * 1.5)
        speed_change_counter = 0

    # 每隔一段时间改变正方形的大小
    size_change_counter += 1
    if size_change_counter % 90 == 0:  # 每90帧（1.5秒）改变一次大小
        # 随机改变正方形的大小，变化范围在原大小的0.8倍到1.2倍之间
        square_size = random.uniform(square_size * 0.8, square_size * 1.2)
        # 限制正方形大小的范围，避免过大或过小
        square_size = max(20, min(50, square_size))
        size_change_counter = 0

    # 每隔一段时间随机改变球的移动方向
    direction_change_counter += 1
    if direction_change_counter % 30 == 0:  # 每30帧（0.5秒）尝试改变方向
        if random.random() < 0.3:  # 有30%的概率改变方向
            angle = random.uniform(0, 2 * math.pi)
            ball_speed_x = ball_speed * math.cos(angle)
            ball_speed_y = ball_speed * math.sin(angle)
        direction_change_counter = 0

    # 为球的速度添加小的随机偏移
    ball_speed_x += random.uniform(-0.1, 0.1)
    ball_speed_y += random.uniform(-0.1, 0.1)

    # 更新球的目标车道位置
    target_ball_x = ball_lane * lane_width + lane_width // 2
    if lane_change_cooldown > 0:
        # 变道过程中逐渐靠近目标车道
        dx = target_ball_x - ball_x
        if abs(dx) > 2:
            ball_speed_x = dx / abs(dx) * ball_speed
        else:
            ball_x = target_ball_x
            ball_speed_x = 0

    # 更新球的位置
    new_ball_x = ball_x + ball_speed_x
    new_ball_y = ball_y + ball_speed_y

    # 检查球是否会撞到障碍物
    collision = False
    for obs_x, obs_y, obs_size in obstacles:
        if (new_ball_x + ball_radius > obs_x and
                new_ball_x - ball_radius < obs_x + obs_size and
                new_ball_y + ball_radius > obs_y and
                new_ball_y - ball_radius < obs_y + obs_size):
            ball_speed_x = -ball_speed_x
            ball_speed_y = -ball_speed_y
            collision = True
            break
    if not collision:
        ball_x = new_ball_x
        ball_y = new_ball_y

    # 边界检测 - 球
    if ball_x - ball_radius < 0 or ball_x + ball_radius > width:
        ball_speed_x = -ball_speed_x
    if ball_y - ball_radius < 0 or ball_y + ball_radius > height:
        ball_speed_y = -ball_speed_y

    # 更新动态障碍物位置
    for dyn_obs in dynamic_obstacles:
        dyn_obs[0] += dyn_obs[3]
        dyn_obs[1] += dyn_obs[4]
        # 边界检测
        if dyn_obs[0] < 0 or dyn_obs[0] + dyn_obs[2] > width:
            dyn_obs[3] = -dyn_obs[3]
        if dyn_obs[1] < 0 or dyn_obs[1] + dyn_obs[2] > height:
            dyn_obs[4] = -dyn_obs[4]

        # 检查球是否会撞到动态障碍物
        if (ball_x + ball_radius > dyn_obs[0] and
                ball_x - ball_radius < dyn_obs[0] + dyn_obs[2] and
                ball_y + ball_radius > dyn_obs[1] and
                ball_y - ball_radius < dyn_obs[1] + dyn_obs[2]):
            ball_speed_x = -ball_speed_x
            ball_speed_y = -ball_speed_y

    # 更新正方形的位置
    new_square_x = square_x + square_speed_x
    new_square_y = square_y + square_speed_y

    # 检查正方形是否会撞到障碍物
    collision = False
    for obs_x, obs_y, obs_size in obstacles:
        if (new_square_x + square_size > obs_x and
                new_square_x < obs_x + obs_size and
                new_square_y + square_size > obs_y and
                new_square_y < obs_y + obs_size):
            square_speed_x = 0
            square_speed_y = 0
            collision = True
            break
    if not collision:
        square_x = new_square_x
        square_y = new_square_y

    # 边界检测 - 正方形
    if square_x < 0:
        square_x = 0
    elif square_x + square_size > width:
        square_x = width - square_size
    if square_y < 0:
        square_y = 0
    elif square_y + square_size > height:
        square_y = height - square_size

    # 检测碰撞
    if (square_x < ball_x + ball_radius and
            square_x + square_size > ball_x and
            square_y < ball_y + ball_radius and
            square_y + square_size > ball_y):
        print("You caught the ball! You win.")
        running = False

    # 填充背景色
    screen.fill(WHITE)

    # 绘制车道线
    for i in range(1, num_lanes):
        pygame.draw.line(screen, BLACK, (i * lane_width, 0), (i * lane_width, height), 2)

    # 绘制障碍物
    for obs_x, obs_y, obs_size in obstacles:
        pygame.draw.rect(screen, BLACK, (obs_x, obs_y, obs_size, obs_size))

    # 绘制动态障碍物
    for dyn_obs in dynamic_obstacles:
        pygame.draw.rect(screen, YELLOW, (dyn_obs[0], dyn_obs[1], dyn_obs[2], dyn_obs[2]))

    # 绘制球
    pygame.draw.circle(screen, BLUE, (ball_x, ball_y), ball_radius)

    # 绘制正方形
    pygame.draw.rect(screen, RED, (square_x, square_y, square_size, square_size))

    # 显示剩余时间
    font = pygame.font.Font(None, 36)
    text = font.render(f"Time left: {time_limit - elapsed_time}", True, BLACK)
    screen.blit(text, (10, 10))

    # 更新显示
    pygame.display.flip()

    # 控制帧率
    clock.tick(90)

# 退出 pygame
pygame.quit()