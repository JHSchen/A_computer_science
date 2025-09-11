# 导入pygame模块
import pygame
import math
# 初始化pygame
pygame.init()
# 创建一个窗口，大小为800x600
screen = pygame.display.set_mode((800, 600))
# 设置窗口标题
pygame.display.set_caption("星球大战")
# 设置窗口图标
icon = pygame.image.load("planet.png")
pygame.display.set_icon(icon)
# 设置背景颜色
bg_color = (0, 0, 0)
# 创建一个大星球对象，位置为(400, 300)，半径为50，颜色为红色，质量为1000，速度为(0, 0)
big_planet = pygame.sprite.Sprite()
big_planet.image = pygame.Surface((100, 100))
big_planet.image.fill(bg_color)
big_planet.image.set_colorkey(bg_color)
pygame.draw.circle(big_planet.image, (255, 0, 0), (50, 50), 50)
big_planet.rect = big_planet.image.get_rect()
big_planet.rect.center = (400, 300)
big_planet.mass = 1000
big_planet.velocity = [0, 0]
# 创建一个小星球对象，位置为(200, 100)，半径为20，颜色为绿色，质量为100，速度为(2, 1)
small_planet = pygame.sprite.Sprite()
small_planet.image = pygame.Surface((40, 40))
small_planet.image.fill(bg_color)
small_planet.image.set_colorkey(bg_color)
pygame.draw.circle(small_planet.image, (0, 255, 0), (20, 20), 20)
small_planet.rect = small_planet.image.get_rect()
small_planet.rect.center = (200, 100)
small_planet.mass = 100
small_planet.velocity = [2, 1]
# 创建一个喷射方向对象，位置为(400, 300)，长度为100，颜色为白色，角度为0
jet_direction = pygame.sprite.Sprite()
jet_direction.image = pygame.Surface((100, 2))
jet_direction.image.fill((255, 255, 255))
jet_direction.rect = jet_direction.image.get_rect()
jet_direction.rect.center = (400, 300)
jet_direction.angle = 0
# 创建一个预测轨迹对象，位置为(400, 300)，长度为800，颜色为黄色，角度为0
predict_path = pygame.sprite.Sprite()
predict_path.image = pygame.Surface((800, 2))
predict_path.image.fill((255, 255, 0))
predict_path.rect = predict_path.image.get_rect()
predict_path.rect.center = (400, 300)
predict_path.angle = 0
# 创建一个分数对象，位置为(10, 10)，颜色为白色，字体为32
score = pygame.sprite.Sprite()
score.font = pygame.font.Font("freesansbold.ttf", 32)
score.text = "Score: 0"
score.image = score.font.render(score.text, True, (255, 255, 255))
score.rect = score.image.get_rect()
score.rect.topleft = (10, 10)
# 创建一个精灵组，包含所有的对象
sprites = pygame.sprite.Group()
sprites.add(big_planet, small_planet, jet_direction, predict_path, score)
# 定义一个常量，表示重力常数
G = 0.01
# 定义一个常量，表示喷射力
F = 10
# 定义一个变量，表示游戏是否结束
game_over = False
# 定义一个变量，表示游戏是否暂停
game_pause = False
# 定义一个变量，表示游戏的分数
game_score = 0
# 定义一个函数，计算两个星球之间的距离
def distance(p1, p2):
    dx = p1.rect.centerx - p2.rect.centerx
    dy = p1.rect.centery - p2.rect.centery
    return (dx**2 + dy**2)**0.5
# 定义一个函数，计算两个星球之间的引力
def gravity(p1, p2):
    d = distance(p1, p2)
    if d == 0:
        return [0, 0]
    else:
        f = G * p1.mass * p2.mass / d**2
        fx = f * (p2.rect.centerx - p1.rect.centerx) / d
        fy = f * (p2.rect.centery - p1.rect.centery) / d
        return [fx, fy]
# 定义一个函数，计算大星球的喷射力
def jet_force(p, a):
    fx = -F * p.mass * math.cos(math.radians(a))
    fy = -F * p.mass * math.sin(math.radians(a))
    return [fx, fy]
# 定义一个函数，更新大星球的位置和速度
def update_big_planet(p, dt):
    # 计算大星球受到的引力和喷射力
    gx, gy = gravity(p, small_planet)
    jx, jy = jet_force(p, jet_direction.angle)
    # 计算大星球的加速度
    ax = (gx + jx) / p.mass
    ay = (gy + jy) / p.mass
    # 计算大星球的速度
    p.velocity[0] += ax * dt
    p.velocity[1] += ay * dt
    # 计算大星球的位置
    p.rect.centerx += p.velocity[0] * dt
    p.rect.centery += p.velocity[1] * dt
    # 限制大星球的位置在窗口内
    if p.rect.left < 0:
        p.rect.left = 0
        p.velocity[0] = -p.velocity[0]
    if p.rect.right > 800:
        p.rect.right = 800
        p.velocity[0] = -p.velocity[0]
    if p.rect.top < 0:
        p.rect.top = 0
        p.velocity[1] = -p.velocity[1]
    if p.rect.bottom > 600:
        p.rect.bottom = 600
        p.velocity[1] = -p.velocity[1]
# 定义一个函数，更新小星球的位置和速度
def update_small_planet(p, dt):
    # 计算小星球受到的引力
    gx, gy = gravity(p, big_planet)
    # 计算小星球的加速度
    ax = gx / p.mass
    ay = gy / p.mass
    # 计算小星球的速度
    p.velocity[0] += ax * dt
    p.velocity[1] += ay * dt
    # 计算小星球的位置
    p.rect.centerx += p.velocity[0] * dt
    p.rect.centery += p.velocity[1] * dt
    # 限制小星球的位置在窗口内
    if p.rect.left < 0:
        p.rect.left = 0
        p.velocity[0] = -p.velocity[0]
    if p.rect.right > 800:
        p.rect.right = 800
        p.velocity[0] = -p.velocity[0]
    if p.rect.top < 0:
        p.rect.top = 0
        p.velocity[1] = -p.velocity[1]
    if p.rect.bottom > 600:
        p.rect.bottom = 600
        p.velocity[1] = -p.velocity[1]

# 定义一个函数，更新喷射方向的位置和角度
def update_jet_direction(p, a):
    # 设置喷射方向的位置为大星球的中心
    p.rect.center = big_planet.rect.center
    # 设置喷射方向的角度
    p.angle = a
    # 旋转喷射方向的图像
    p.image = pygame.transform.rotate(jet_direction.image, -p.angle)
    # 重新设置喷射方向的矩形
    p.rect = p.image.get_rect()
    p.rect.center = big_planet.rect.center
# 定义一个函数，更新预测轨迹的位置和角度
def update_predict_path(p, a):
    # 设置预测轨迹的位置为大星球的中心
    p.rect.center = big_planet.rect.center
    # 设置预测轨迹的角度
    p.angle = a
    # 旋转预测轨迹的图像
    p.image = pygame.transform.rotate(predict_path.image, -p.angle)
    # 重新设置预测轨迹的矩形
    p.rect = p.image.get_rect()
    p.rect.center = big_planet.rect.center
# 定义一个函数，更新分数的文本和图像
def update_score(p, s):
    # 设置分数的文本
    p.text = "Score: " + str(s)
    # 重新渲染分数的图像
    p.image = p.font.render(p.text, True, (255, 255, 255))
    # 重新设置分数的矩形
    p.rect = p.image.get_rect()
    p.rect.topleft = (10, 10)
# 定义一个函数，检查两个星球是否碰撞
def check_collision(p1, p2):
    # 如果两个星球的距离小于它们的半径之和，返回True，否则返回False
    return distance(p1, p2) < (p1.rect.width + p2.rect.width) / 4
# 定义一个函数，处理两个星球的碰撞
def handle_collision(p1, p2):
    # 计算两个星球的总质量
    total_mass = p1.mass + p2.mass
    # 计算两个星球的总动量
    total_momentum = [p1.mass * p1.velocity[0] + p2.mass * p2.velocity[0], p1.mass * p1.velocity[1] + p2.mass * p2.velocity[1]]
    # 计算两个星球的合并后的半径
    new_radius = ((p1.rect.width / 2)**3 + (p2.rect.width / 2)**3)**(1/3)
    # 计算两个星球的合并后的颜色
    new_color = [(p1.mass * p1.image.get_at((50, 50))[0] + p2.mass * p2.image.get_at((20, 20))[0]) / total_mass, (p1.mass * p1.image.get_at((50, 50))[1] + p2.mass * p2.image.get_at((20, 20))[1]) / total_mass, (p1.mass * p1.image.get_at((50, 50))[2] + p2.mass * p2.image.get_at((20, 20))[2]) / total_mass]
    # 创建一个新的星球对象，位置为两个星球的质心，半径为合并后的半径，颜色为合并后的颜色，质量为总质量，速度为总动量除以总质量
    new_planet = pygame.sprite.Sprite()
    new_planet.image = pygame.Surface((int(new_radius * 2), int(new_radius * 2)))
    new_planet.image.fill(bg_color)
    new_planet.image.set_colorkey(bg_color)
    pygame.draw.circle(new_planet.image, new_color, (int(new_radius), int(new_radius)), int(new_radius))
    new_planet.rect = new_planet.image.get_rect()
    new_planet.rect.center = ((p1.mass * p1.rect.centerx + p2.mass * p2.rect.centerx) / total_mass, (p1.mass * p1.rect.centery + p2.mass * p2.rect.centery) / total_mass)
    new_planet.mass = total_mass
    new_planet.velocity = [total_momentum[0] / total_mass, total_momentum[1] / total_mass]
    # 返回新的星球对象
    return new_planet
# 定义一个函数，绘制所有的精灵
def draw_sprites():
    # 填充背景颜色
    screen.fill(bg_color)
    # 绘制所有的精灵
    sprites.draw(screen)
    # 更新窗口显示
    pygame.display.flip()
# 定义一个函数，处理用户的输入
def handle_input():
    # 定义一个全局变量，表示喷射方向的角度
    global jet_direction
    # 定义一个全局变量，表示游戏是否结束
    global game_over
    # 定义一个全局变量，表示游戏是否暂停
    global game_pause

    # 遍历所有的事件
    for event in pygame.event.get():
        # 如果事件是退出，设置游戏结束为True
        if event.type == pygame.QUIT:
            game_over = True
        # 如果事件是按键按下
        if event.type == pygame.KEYDOWN:
            # 如果按键是空格，切换游戏暂停状态
            if event.key == pygame.K_SPACE:
                game_pause = not game_pause
            # 如果按键是左箭头，逆时针旋转喷射方向10度
            if event.key == pygame.K_LEFT:
                jet_direction.angle += 10
            # 如果按键是右箭头，顺时针旋转喷射方向10度
            if event.key == pygame.K_RIGHT:
                jet_direction.angle -= 10
# 定义一个主函数，运行游戏的主循环
def main():
    # 定义一个全局变量，表示游戏是否结束
    global game_over
    # 定义一个全局变量，表示游戏的分数
    global game_score
    # 创建一个时钟对象，控制游戏的帧率
    clock = pygame.time.Clock()
    # 游戏的主循环
    while not game_over:
        # 处理用户的输入
        handle_input()
        # 如果游戏没有暂停
        if not game_pause:
            # 获取上一帧的时间间隔，单位为秒
            dt = clock.tick(60) / 1000
            # 更新大星球的位置和速度
            update_big_planet(big_planet, dt)
            # 更新小星球的位置和速度
            update_small_planet(small_planet, dt)
            # 更新喷射方向的位置和角度
            update_jet_direction(jet_direction, jet_direction.angle)
            # 更新预测轨迹的位置和角度
            update_predict_path(predict_path, jet_direction.angle)
            # 检查两个星球是否碰撞
            if check_collision(big_planet, small_planet):
                # 处理两个星球的碰撞
                new_planet = handle_collision(big_planet, small_planet)
                # 从精灵组中移除两个星球
                sprites.remove(big_planet, small_planet)
                # 将新的星球添加到精灵组中
                sprites.add(new_planet)
                # 将大星球和小星球的引用指向新的星球
                big_planet = new_planet
                small_planet = new_planet
                # 增加游戏的分数
                game_score += 1
                # 更新分数的文本和图像
                update_score(score, game_score)
        # 绘制所有的精灵
        draw_sprites()
# 调用主函数
main()