import pygame
import sys
import random
import math

# 初始化
pygame.init()

# 游戏参数
WIDTH, HEIGHT = 800, 600
FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
G = 0.1  # 重力常数
THRUST = 0.5  # 喷射推力
MASS_GAIN = 0.5  # 吞噬小星球获得的质量增量
PREDICTION_FRAMES = 60  # 预测轨迹的帧数

# 创建窗口
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("星球吞噬游戏")
clock = pygame.time.Clock()

# 定义星球类
class Planet:
    def __init__(self, x, y, mass, color):
        self.x = x
        self.y = y
        self.mass = mass
        self.color = color
        self.radius = int(math.sqrt(self.mass))

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

# 创建大星球（玩家控制）
player_planet = Planet(WIDTH // 2, HEIGHT // 2, 100, WHITE)
player_velocity = [0, 0]

# 创建黑洞
black_hole = Planet(WIDTH // 4, HEIGHT // 4, 500, BLACK)

# 创建小星球列表
small_planets = [Planet(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50), random.randint(5, 30), GRAY)
                 for _ in range(5)]

# 游戏循环
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    # 更新大星球状态
    player_planet.x += player_velocity[0]
    player_planet.y += player_velocity[1]

    # 计算重力作用
    for small_planet in small_planets:
        dx = small_planet.x - player_planet.x
        dy = small_planet.y - player_planet.y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        force = G * (player_planet.mass * small_planet.mass) / distance ** 2
        angle = math.atan2(dy, dx)
        force_x = force * math.cos(angle)
        force_y = force * math.sin(angle)

        # 更新速度
        player_velocity[0] += force_x / player_planet.mass
        player_velocity[1] += force_y / player_planet.mass

    # 更新小星球状态
    for small_planet in small_planets:
        small_planet.draw()

    # 更新黑洞状态
    black_hole.draw()

    # 画出预测轨迹虚线
    prediction_positions = []
    prediction_planet = player_planet
    for _ in range(PREDICTION_FRAMES):
        prediction_planet.x += player_velocity[0]
        prediction_planet.y += player_velocity[1]
        prediction_positions.append((int(prediction_planet.x), int(prediction_planet.y)))

    pygame.draw.lines(screen, WHITE, False, prediction_positions, 1)

    # 更新大星球状态
    player_planet.draw()

    # 更新屏幕
    pygame.display.flip()

    # 控制帧率
    clock.tick(FPS)

    # 清空屏幕
    screen.fill(BLACK)
