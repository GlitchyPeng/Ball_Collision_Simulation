import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random
import math

# 初始化Pygame
pygame.init()
display = (800, 600)
screen = pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
pygame.display.set_caption("三维小球碰撞模拟")

# 设置视角
gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
glTranslatef(0.0, 0.0, -20)

# 定义小球类
class Ball:
    def __init__(self, x, y, z, radius, color, speed):
        self.x = x
        self.y = y
        self.z = z
        self.radius = radius
        self.color = color
        self.speed = speed
        self.angle_xy = random.uniform(0, 2 * math.pi)
        self.angle_z = random.uniform(-math.pi / 4, math.pi / 4)
    
    def move(self):
        self.x += math.cos(self.angle_xy) * self.speed
        self.y += math.sin(self.angle_xy) * self.speed
        self.z += math.sin(self.angle_z) * self.speed

        # 碰撞检测 - 盒子边界
        if self.x - self.radius <= -5 or self.x + self.radius >= 5:
            self.angle_xy = math.pi - self.angle_xy
        if self.y - self.radius <= -5 or self.y + self.radius >= 5:
            self.angle_xy = -self.angle_xy
        if self.z - self.radius <= -5 or self.z + self.radius >= 5:
            self.angle_z = -self.angle_z
    
    def draw(self):
        glColor3fv(self.color)
        glPushMatrix()
        glTranslatef(self.x, self.y, self.z)
        glutSolidSphere(self.radius, 20, 20)
        glPopMatrix()

# 创建小球实例
balls = [
    Ball(random.uniform(-4, 4), random.uniform(-4, 4), random.uniform(-4, 4), 0.5, (1, 0, 0), 0.05),
    Ball(random.uniform(-4, 4), random.uniform(-4, 4), random.uniform(-4, 4), 0.5, (0, 0, 1), 0.05)
]

# 盒子摆动的参数
swing_angle = 0
swing_speed = 0.01
swing_radius = 10

# 主循环
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    # 计算盒子的摆动
    swing_angle += swing_speed
    box_offset_y = swing_radius * math.sin(swing_angle)
    
    # 绘制盒子（使用线框）
    glColor3fv((1, 1, 1))
    glPushMatrix()
    glTranslatef(0, box_offset_y, 0)
    glBegin(GL_LINES)
    for edge in [(0,1),(1,2),(2,3),(3,0),(4,5),(5,6),(6,7),(7,4),(0,4),(1,5),(2,6),(3,7)]:
        for vertex in edge:
            glVertex3fv([
                (vertex & 1) * 10 - 5,
                ((vertex >> 1) & 1) * 10 - 5,
                ((vertex >> 2) & 1) * 10 - 5])
    glEnd()
    
    # 更新和绘制小球
    for ball in balls:
        ball.move()
        ball.draw()
    
    glPopMatrix()
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
