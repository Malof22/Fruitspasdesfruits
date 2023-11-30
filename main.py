import math
import random
import pygame
import time

window = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Les fruits qui ne sont pas des fruits")
pygame.font.init()

class Ball:
    COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255), (255, 0, 255), (0, 0, 0)]

    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.color = self.COLORS[radius - 1]
        self.radius = 15*radius
        self.mass = radius**2
        self.velocity = [0, 0]

    def draw(self):
        pygame.draw.circle(window, self.color, (int(self.x), int(self.y)), int(self.radius))

    def fall(self, ball_list):
        if not self.is_colliding(ball_list):
            # Ajustez la gravité en fonction de la masse
            self.velocity[1] += 0.1 * self.mass

    def move(self, ball_list):
        self.fall(ball_list)
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        self.collide(ball_list)

    def collide(self, ball_list):
        for other in ball_list:
            if other != self:
                dx = other.x - self.x
                dy = other.y - self.y
                distance = math.sqrt(dx ** 2 + dy ** 2)
                overlap = (self.radius + other.radius) - distance

                if overlap > 0:
                    angle = math.atan2(dy, dx)
                    move_x = overlap * math.cos(angle) / 2
                    move_y = overlap * math.sin(angle) / 2

                    self.x -= move_x
                    self.y -= move_y
                    other.x += move_x
                    other.y += move_y

                    self.merge(other, ball_list)

        # Gestion de la collision avec les bords de l'écran
        if self.x + self.radius > 500:
            self.x = 500 - self.radius
            self.velocity[0] = -self.velocity[0]
        if self.x - self.radius < 0:
            self.x = self.radius
            self.velocity[0] = -self.velocity[0]
        if self.y + self.radius > 500:
            self.y = 500 - self.radius
            self.velocity[1] = -self.velocity[1] * 0.1  # Rebond partiel pour simuler l'élasticité
        if self.y - self.radius < 0:
            self.y = self.radius
            self.velocity[1] = -self.velocity[1]

    def is_colliding(self, ball_list):
        for other in ball_list:
            if other != self:
                dx = other.x - self.x
                dy = other.y - self.y
                distance = math.sqrt(dx**2 + dy**2)

                if distance < self.radius + other.radius:
                    return True  # Le cercle est en collision avec un autre
        return False

    def adjust_position(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        distance = math.sqrt(dx**2 + dy**2)
        overlap = (self.radius + other.radius) - distance
        angle = math.atan2(dy, dx)

        self.x -= overlap * math.cos(angle)
        self.y -= overlap * math.sin(angle)

    def merge(self, other, ball_list):
        global running
        if self.radius == other.radius:
            if self.radius/15 == 7:
                print("Game Over")
                running = False
            if running:
                ball_list.append(Ball(self.x, self.y, int(self.radius/15) + 1))
                ball_list.remove(self)
                ball_list.remove(other)


ball_list = [Ball(250, 250, random.randint(1, 4))]
last_time = 0

running = True
while running:
    print("Running", running)
    window.fill((255, 255, 255))
    pygame.time.delay(10)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if pygame.mouse.get_pressed()[0]:
        t = time.time()
        if t - last_time > 0.5:
            last_time = t
            x = pygame.mouse.get_pos()[0]
            ball = Ball(x, 0, random.randint(1, 4))
            ball_list.append(ball)

    for ball in sorted(ball_list, key=lambda b: b.radius, reverse=True):
        ball.draw()
        ball.move(ball_list)

    pygame.display.update()


window.fill((255, 255, 255))
font = pygame.font.SysFont("Arial", 30)
text = font.render("Game Over", True, (0, 0, 0))
window.blit(text, (200, 200))
pygame.display.update()
time.sleep(10)
