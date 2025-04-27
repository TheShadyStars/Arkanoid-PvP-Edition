import pygame
from time import time as timer

pygame.init()
window = pygame.display.set_mode((500, 500))

clock = pygame.time.Clock()
red = (255, 0, 0)
yellow = (255, 255, 0)
game_over = False
move_left_down = False
move_right_down = False
move_left_up = False
move_right_up = False
ball_speed_x = 3
ball_speed_y = 3
platform_speed = 4
FPS = 40
total_score = 0
missed_down = 0
missed_up = 0

class Area():
    def __init__(self, x=0, y=0, width=10, height=10, color=(255, 255, 255)):
        self.rect = pygame.Rect(x, y, width, height)
        self.fill_color = yellow

    def draw(self):
        pygame.draw.rect(window, self.fill_color, self.rect)
        window.blit(self.image, (self.rect.x + shift_x, self.rect.y + shift_y))

    def colliderect(self, rect):
        return self.rect.colliderect(rect)

class Picture(Area):
    def __init__(self, filename, x=0, y=0, width=10, height=10):
        super().__init__(x=x, y=y, width=width, height=height, color=None)
        self.image = pygame.image.load(filename)

    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

platform_down = Picture('platform.png', 200, 450, 100, 1)
platform_down.draw()
platform_up = Picture('platform.png', 200, 50, 100, 24)
platform_up.draw()

ball = Picture('ball.png', 125, 300, 50, 50)
ball.draw()

font = pygame.font.Font(None, 72)
score_font = pygame.font.Font(None, 360)
missed_font = pygame.font.Font(None, 48)
bg_font = pygame.font.SysFont("Arial.ttf", 450)
win_down = font.render('ИГРОК 1 ВЫИГРАЛ', True, ((64, 64, 255)))
win_up = font.render('ИГРОК 2 ВЫИГРАЛ', True, ((64, 255, 64)))
score = score_font.render(str(total_score), True, ((184, 0, 0)))
missed_down_text = missed_font.render(str(missed_down), True, ((127, 0, 0)))
missed_up_text = missed_font.render(str(missed_up), True, ((127, 0, 0)))

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                move_left_down = True
            elif event.key == pygame.K_RIGHT:
                move_right_down = True
            elif event.key == pygame.K_a:
                move_left_up = True
            elif event.key == pygame.K_d:
                move_right_up = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                move_left_down = False
            elif event.key == pygame.K_RIGHT:
                move_right_down = False
            elif event.key == pygame.K_a:
                move_left_up = False
            elif event.key == pygame.K_d:
                move_right_up = False
    window.fill(red)
    score = score_font.render(str(total_score), True, ((184, 0, 0)))
    if total_score < 10:
        window.blit(score, (196, 150))
    if total_score >= 10 and total_score < 100:
        window.blit(score, (120, 150))
    if total_score >= 100:
        window.blit(score, (36, 150))
    missed_down_text = missed_font.render(str(missed_down), True, ((127, 0, 0)))
    missed_up_text = missed_font.render(str(missed_up), True, ((127, 0, 0)))
    window.blit(missed_down_text, (platform_down.rect.x + 40, 420))
    window.blit(missed_up_text, (platform_up.rect.x + 40, 74))
    platform_down.draw()
    platform_up.draw()
    ball.draw()
    ball.rect.x += ball_speed_x
    ball.rect.y += ball_speed_y
    if ball.colliderect(platform_down.rect):
        FPS += 2
        ball_speed_y *= -1
        total_score += 1
    if ball.colliderect(platform_up.rect):
        FPS += 2
        ball_speed_y *= -1
        total_score += 1
    if ball.rect.x > 450 or ball.rect.x < 0:
        ball_speed_x *= -1
    if ball.rect.y < 0:
        missed_up += 1
        ball_speed_y *= -1
    if ball.rect.y > 505:
        missed_down += 1
        ball_speed_y *= -1

    if move_left_down == True and platform_down.rect.x > 0:
        platform_down.rect.x -= platform_speed
    if move_right_down == True and platform_down.rect.x < 400:
        platform_down.rect.x += platform_speed
    
    if move_left_up == True and platform_up.rect.x > 0:
        platform_up.rect.x -= platform_speed
    if move_right_up == True and platform_up.rect.x < 400:
        platform_up.rect.x += platform_speed

    if missed_down > 3 or missed_up > 3:
        platform_down.rect.x = 200
        platform_up.rect.x = 200
        total_score = 0
        missed_down = 0
        missed_up = 0
        last_time = timer()
        FPS = 40
        now_time = timer()

        while now_time - last_time < 3:
            platform_down.rect.x = 200
            platform_up.rect.x = 200
            ball.rect.x = 125
            ball.rect.y = 300
            ball_speed_x = 0
            ball_speed_y = 0
            platform_speed = 0
            now_time = timer()
            if now_time - last_time >= 3:
                break

        ball_speed_x = 3
        ball_speed_y = 3
        platform_speed = 4

    pygame.display.flip()
    clock.tick(FPS)