"""CONTROLS
Anywhere -> ESC: exit
Main menu -> 1: go to previous level. 2: go to next level. SPACE: start game.
Game -> SPACE/UP: jump, and activate orb
    orb: jump in midair when activated
If you die or beat the level, press SPACE to restart or go to the next level

"""

import csv
import os
import sys
import random

import pygame

# dễ dàng sử dụng các hàm ở pygame hơn
from pygame.math import Vector2
from pygame.draw import rect
from Obstacle import Trick, Spike, Orb, Platform, End

# khởi tạo pygame
pygame.init()

# tạo ra màn hình kích thước 800 x 600
screen = pygame.display.set_mode([800, 600])

# kiểm tra xem game đã kết thúc hay chưa
done = False

# kiểm tra xem có bắt đầu game từ main menu hay không
start = False

# thiết lập khung hình
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

color = lambda: tuple([random.randint(0, 255) for i in range(3)])  # hàm lambda cho màu ngẫu nhiên
GRAVITY = Vector2(0, 0.86)  # trọng lực
# background màn hình start, game over, win
bg_start = pygame.image.load(os.path.join("images", "bg_start.png"))
bg_game_over = pygame.image.load(os.path.join("images", "bg_game_over.png"))
bg_won = pygame.image.load(os.path.join("images", "bg_won.png"))

"""
PlayerClass
"""


class Player(pygame.sprite.Sprite):
    win: bool #kiểm tra xem đã thắng chưa
    died: bool #kiểm tra xem đã thua chưa

    def __init__(self, image, platforms, pos, *groups):
        """
        image: ảnh của nhân vật
        platforms: các vật cản có thể tương tác với player
        pos: vị trí bắt đầu
        groups: biến sprite groups
        """
        super().__init__(*groups)
        self.onGround = False  # kiểm tra player có ở trên mặt đất không
        self.platforms = platforms  # một biến trong lớp gán bằng loại vật cản truyền vào
        self.died = False
        self.win = False

        self.image = pygame.transform.smoothscale(image, (32, 32))
        self.rect = self.image.get_rect(center=pos)
        self.jump_amount = 10  # độ cao khi nhảy
        self.particles = []  # trail di chuyển
        self.isjump = False  # kiểm tra player có đang nhảy không
        self.vel = Vector2(0, 0)  # vận tốc bắt đầu

    def draw_particle_trail(self, x, y, color=(255, 255, 255)):
        # vẽ trail

        self.particles.append(
                [[x - 5, y - 8], [random.randint(0, 25) / 10 - 1, random.choice([0, 0])],
                 random.randint(5, 8)])

        for particle in self.particles:
            particle[0][0] += particle[1][0]
            particle[0][1] += particle[1][1]
            particle[2] -= 0.5
            particle[1][0] -= 0.4
            rect(alpha_surf, color,
                 ([int(particle[0][0]), int(particle[0][1])], [int(particle[2]) for i in range(2)]))
            if particle[2] <= 0:
                self.particles.remove(particle)

    def collide(self, yvel, platforms):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                """kiểm tra va chạm"""""
                if isinstance(p, Orb) and (keys[pygame.K_UP] or keys[pygame.K_SPACE]):
                    pygame.draw.circle(alpha_surf, (255, 255, 0), p.rect.center, 18)
                    #screen.blit(pygame.image.load("images/editor-0.9s-47px.gif"), p.rect.center)
                    self.jump_amount = 12 # boost 1 tí khi va chạm với Orb
                    self.jump()
                    self.jump_amount = 10  # đưa độ nhảy về chỉ số ban đầu

                if isinstance(p, End):
                    self.win = True

                if isinstance(p, Spike):
                    self.died = True  # thua vì spike

                if isinstance(p, Trick):
                    p.enter(trick_enter)

                if isinstance(p, Platform):  # vật cản ô khối

                    if yvel > 0:
                        """nếu player đang rơi xuống (v.y dương)"""
                        self.rect.bottom = p.rect.top  # không cho player đi xuyên tường
                        self.vel.y = 0  # v.y = 0 vì player ở trên nền

                        self.onGround = True

                        self.isjump = False
                    elif yvel < 0:
                        """nếu v.y đang âm, player va chạm khi đang nhảy"""
                        self.rect.top = p.rect.bottom  # set player ở dưới đáy của khối va chạm
                    else:
                        """trong các trường hợp va chạm với khối còn lại thì bị tính là thua"""
                        self.vel.x = 0
                        self.rect.right = p.rect.left  # không để player đi xuyên tường
                        self.died = True

    def jump(self):
        self.vel.y = -self.jump_amount

    def update(self):

        if self.isjump:
            if self.onGround:
                """chỉ nhảy khi player đang ở trên mặt đất"""
                self.jump()

        if not self.onGround:  # nếu player không ở trên mặt đất thì phải bị kéo xuống bởi trọng lực
            self.vel += GRAVITY  # trọng lực

            # vận tốc rơi tối đa
            if self.vel.y > 100: self.vel.y = 100

        # va chạm theo trục x
        self.collide(0, self.platforms)

        self.rect.top += self.vel.y

        self.onGround = False

        # va chạm theo trục y
        self.collide(self.vel.y, self.platforms)

        # kiểm tra xem người chơi thắng hay thua
        eval_outcome(self.win, self.died)




"""
Hàm
"""


def init_level(map):
    """Xây dựng một map trong không gian 2D"""
    x = 0
    y = 0

    for row in map:
        for col in row:

            if col == "0":
                Platform(block, (x, y), elements)


            if col == "Spike":
                Spike(spike, (x, y), elements)
            if col == "Orb":
                orbs.append([x, y])

                Orb(orb, (x, y), elements)

            if col == "T":
                Trick(trick, (x, y), elements)

            if col == "End":
                End(avatar, (x, y), elements)
            x += 32
        y += 32
        x = 0


def won_screen():
    """màn hình chiến thắng"""
    global attempts, level, fill
    attempts = 0
    player_sprite.clear(player.image, screen)

    screen.blit(bg_won, (0, 0))
    level += 1

    wait_for_key()
    reset()


def death_screen():
    """màn hình thua cuộc"""
    global attempts, fill
    fill = 0
    player_sprite.clear(player.image, screen)
    attempts += 1
    screen.blit(bg_game_over, (0, 0))
    wait_for_key()
    reset()


def eval_outcome(won: bool, died: bool):
    """kiểm tra xem người chơi thắng hay thua"""
    if won:
        won_screen()
    if died:
        death_screen()


def block_map(level_num):
    """mở file csv lưu map của game"""
    lvl = []
    with open(level_num, newline='') as csvfile:
        trash = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in trash:
            lvl.append(row)
    return lvl


def start_screen():
    """màn hình start"""
    global level
    if not start:
        if pygame.key.get_pressed()[pygame.K_1]:
            level = 0
        if pygame.key.get_pressed()[pygame.K_2]:
            level = 1
        screen.blit(bg_start, (0, 0))

def reset():
    """reset khi người chơi thua hoặc đến màn mới"""
    global player, elements, player_sprite, level

    player_sprite = pygame.sprite.Group()
    elements = pygame.sprite.Group()
    player = Player(avatar, elements, (150, 150), player_sprite)
    init_level(
            block_map(
                    level_num=levels[level]))


def move_map():
    """di chuyển vật cản"""
    for sprite in elements:
        sprite.rect.x -= CameraX


def draw_stats(surf, money=0):
    """thanh trạng thái"""
    global fill
    progress_colors = [pygame.Color("red"), pygame.Color("orange"), pygame.Color("yellow"), pygame.Color("lightgreen"),
                       pygame.Color("green")]

    tries = font.render(f" Attempt {str(attempts)}", True, WHITE)
    BAR_LENGTH = 600
    BAR_HEIGHT = 10
    fill += 0.5
    outline_rect = pygame.Rect(0, 0, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(0, 0, fill, BAR_HEIGHT)
    col = progress_colors[int(fill / 100)]
    rect(surf, col, fill_rect, 0, 4)
    rect(surf, WHITE, outline_rect, 3, 4)
    screen.blit(tries, (BAR_LENGTH, 0))


def wait_for_key():
    """thể hiện giao diện trong khi chờ người chơi bấm nút"""
    global level, start
    waiting = True
    while waiting:
        clock.tick(60)
        pygame.display.flip()

        if not start:
            start_screen()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    start = True
                    waiting = False
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()


def resize(img, size=(32, 32)):
    """resize ảnh"""
    resized = pygame.transform.smoothscale(img, size)
    return resized


"""
Các biến toàn cục
"""
font = pygame.font.Font("FFFFORWA.ttf", 12)

avatar = pygame.image.load(os.path.join("images", "avatar.png"))  # ảnh nhân vật player
pygame.display.set_icon(avatar)
#  Màu sắc của surface
alpha_surf = pygame.Surface(screen.get_size(), pygame.SRCALPHA)

# sprite groups
player_sprite = pygame.sprite.Group()
elements = pygame.sprite.Group()

# images
spike = pygame.image.load(os.path.join("images", "obj-spike.png"))
spike = resize(spike)
block = pygame.image.load(os.path.join("images", "block_1.png"))
block = pygame.transform.smoothscale(block, (32, 32))
orb = pygame.image.load((os.path.join("images", "orb-yellow.png")))
orb = pygame.transform.smoothscale(orb, (32, 32))
trick = pygame.image.load((os.path.join("images", "block_2.png")))
trick = pygame.transform.smoothscale(trick, (32, 32))
trick_enter = pygame.image.load((os.path.join("images", "block_3.png")))
trick_enter = pygame.transform.smoothscale(trick_enter, (32, 32))

#  ints
fill = 0
num = 0
CameraX = 0
attempts = 0
angle = 0
level = 0

# list
particles = []
orbs = []
win_cubes = []

# initialize level with
levels = ["level_1.csv", "level_2.csv"]
level_list = block_map(levels[level])
level_width = (len(level_list[0]) * 32)
level_height = len(level_list) * 32
init_level(level_list)

# set window title suitable for game
pygame.display.set_caption('Block')

# initialize the font variable to draw text later
text = font.render('image', False, (255, 255, 0))

# music
#music = pygame.mixer_music.load(os.path.join("music", "bossfight-Vextron.mp3"))
#pygame.mixer_music.play()

# bg image
bg = pygame.image.load(os.path.join("images", "bg.jpg"))

# create object of player class
player = Player(avatar, elements, (150, 150), player_sprite)

while not done:
    keys = pygame.key.get_pressed()

    if not start:
        wait_for_key()
        reset()

        start = True

    player.vel.x = 6

    eval_outcome(player.win, player.died)
    if keys[pygame.K_UP] or keys[pygame.K_SPACE]:
        player.isjump = True

    # Reduce the alpha of all pixels on this surface each frame.
    # Control the fade2 speed with the alpha value.

    alpha_surf.fill((255, 255, 255, 1), special_flags=pygame.BLEND_RGBA_MULT)

    player_sprite.update()
    CameraX = player.vel.x  # for moving obstacles
    move_map()  # apply CameraX to all elements

    screen.blit(bg, (0, 0))  # Clear the screen(with the bg)

    player.draw_particle_trail(player.rect.left - 1, player.rect.bottom + 2,
                               WHITE)
    screen.blit(alpha_surf, (0, 0))  # Blit the alpha_surf onto the screen.

    player_sprite.draw(screen)
    elements.draw(screen)  # draw all other obstacles

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True

    pygame.display.flip()
    clock.tick(60)
pygame.quit()
