import pygame
import os
import sys


pygame.init()
win = pygame.display.set_mode((1600, 700))
pygame.display.set_caption('I WANNA BE CRUSADER!')

clock = pygame.time.Clock()
x = 65
y = 571
w = 65
h = 65
j_c = False
speed = 5
on_ground = False
isJump = False
jumpCount = 9
health_point = 1
left = False
right = False
animCount = 0
LastMove = 'right'
FPS = 25
bullets = []
flag = False
flag2 = True
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
damage_group = pygame.sprite.Group()
player = None


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image


def cut_sheet(sheet, columns, rows):
    frames = []
    rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                       sheet.get_height() // rows)
    for j in range(rows):
        for i in range(columns):
            frame_location = (rect.w * i, rect.h * j)
            frames.append(sheet.subsurface(pygame.Rect(
                          frame_location, rect.size)))
    return frames


player_sheet = load_image('player_sheet.png')
columns = 5
rows = 1
player_sheet = cut_sheet(player_sheet, columns, rows)

tile_sheet = load_image('blocks3.png')
tiles = cut_sheet(tile_sheet, 9, 2)
tile_images = {
    'block_cult_normal': tiles[0],
    'block_cult_bloody': tiles[1],
    'block_cult_banner': tiles[2],
    'block_cult_altar': tiles[3],
    'block_cult_abandoned': tiles[4],
    'block_dirt': tiles[5],
    'block_dirt_roots': tiles[6],
    'block_dirt_puddle': tiles[7],
    'block_dirt_path': tiles[8],
    'block_brick_normal': tiles[9],
    'block_cross_bloody': tiles[10],
    'block_cross_normal': tiles[11],
    'block_box': tiles[12]
}

tile_width = tile_height = 65
game_fon = load_image('green.png')

ANIMATION_RIGHT = [load_image('kn_r1.png'),
                   load_image('kn_r2.png'),
                   load_image('kn_r3.png'),
                   load_image('kn_r4.png'),
                   load_image('kn_r5.png')]

ANIMATION_LEFT = [load_image('kn_l1.png'),
                  load_image('kn_l2.png'),
                  load_image('kn_l3.png'),
                  load_image('kn_l4.png'),
                  load_image('kn_l5.png')]

ANIMATION_JUMP_LEFT = load_image('kn_l4.png')
ANIMATION_JUMP_RIGHT = load_image('kn_r4.png')
ANIMATION_JUMP = load_image('teutonic_knight.png')
ANIMATION_STAY = load_image('teutonic_knight.png')

spike_images = [load_image('spike.png'),
                load_image('spike2.png'),
                load_image('spike3.png'),
                load_image('spike4.png')]

HERETIC_RIGHT = [load_image('heretic_r1.png'),
                 load_image('heretic_r2.png'),
                 load_image('heretic_r3.png'),
                 load_image('heretic_r4.png'),
                 load_image('heretic_r5.png')]

HERETIC_LEFT = [load_image('heretic_l1.png'),
                load_image('heretic_l2.png'),
                load_image('heretic_l3.png'),
                load_image('heretic_l4.png'),
                load_image('heretic_l5.png')]

HERETIC_STAY = load_image('heretic_knight.png')


def terminate():
    pygame.quit()
    sys.exit()


def death(pos_x, pos_y):
    return Player(pos_x, pos_y)


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip().split() for line in mapFile]
    return level_map[::-1]


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.type = tile_type
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, 635 - tile_height * pos_y)


def generate_level(level):
    new_player = None
    for i in range(len(level)):
        for g in range(len(level[i])):
            if level[i][g] == '@':
                new_player = Player(g, i)
                f_1 = g
                f_2 = i
    for i in range(len(level)):
        for g in range(len(level[i])):
            if level[i][g] == '-':
                continue
            elif level[i][g] == '0':
                continue
            elif level[i][g] == '1':
                Tile('block_cult_normal', g, i)
            elif level[i][g] == '2':
                Tile('block_cult_bloody', g, i)
            elif level[i][g] == '3':
                Tile('block_cult_banner', g, i)
            elif level[i][g] == '4':
                Tile('block_cult_altar', g, i)
            elif level[i][g] == '5':
                Tile('block_cult_abandoned', g, i)
            elif level[i][g] == '6':
                Tile('block_dirt', g, i)
            elif level[i][g] == '7':
                Tile('block_dirt_roots', g, i)
            elif level[i][g] == '8':
                Tile('block_dirt_puddle', g, i)
            elif level[i][g] == '9':
                Tile('block_dirt_path', g, i)
            elif level[i][g] == '10':
                Tile('block_brick_normal', g, i)
            elif level[i][g] == '11':
                Tile('block_cross_bloody', g, i)
            elif level[i][g] == '12':
                Tile('block_cross_normal', g, i)
            elif level[i][g] == '13':
                Tile('block_box', g, i)
            elif level[i][g] == 's_1':
                Spike(0, g, i)
            elif level[i][g] == 's_2':
                Spike(1, g, i)
            elif level[i][g] == 's_3':
                Spike(2, g, i)
            elif level[i][g] == 's_4':
                Spike(3, g, i)
    return new_player, f_1, f_2


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.cur_frame = 0
        self.x = pos_x
        self.y = pos_y
        self.left_frame = 0
        self.right_frame = 0
        self.image = ANIMATION_STAY
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, 600 - tile_height * pos_y)

    def update(self):
        global left, right, ANIMATION_RIGHT, ANIMATION_LEFT,\
               isJump, jumpCount, on_ground, LastMove, j_c, player
        flag3 = False
        for spike in damage_group:
            if pygame.sprite.collide_rect(self, spike):
                self.kill()
        for block in tiles_group:
            if pygame.sprite.collide_rect(self, block):  # столкновения
                if block.rect.top <= self.rect.bottom <= block.rect.top + 10 + (jumpCount ** 2) / 2 - 10:
                    self.rect.bottom = block.rect.top
                    on_ground = True
                    isJump = False
                    jumpCount = 9
                    j_c = False
                elif self.rect.top <= block.rect.bottom and isJump and \
                        self.rect.right > (block.rect.right - 55) and \
                        self.rect.left < (block.rect.left + 55):
                    self.rect.top = block.rect.bottom
                    isJump = False
                    jumpCount = 9
                    on_ground = False
                    j_c = False
                elif right and block.rect.left <= self.rect.right <= block.rect.left + 55:
                    self.rect.right = block.rect.left
                elif left and block.rect.right - 55 <= self.rect.left <= block.rect.right:
                    self.rect.left = block.rect.right

                elif not right and not left:
                    if LastMove == 'right':
                        self.rect.right = block.rect.left - 5
                    else:
                        self.rect.left = block.rect.right + 5
        for block in tiles_group:
            if block.rect.top == self.rect.bottom and(
               block.rect.left <= self.rect.left <= block.rect.right or
               block.rect.left <= self.rect.right <= block.rect.right):
                flag3 = True
            else:
                block.image = tile_images[block.type]

        if isJump and on_ground and not j_c:
            j_c = True
        if j_c:
            if jumpCount >= -9:
                if jumpCount < 0:
                    self.rect = self.rect.move(0, (jumpCount ** 2) / 2 - 10)
                else:
                    self.rect = self.rect.move(0, -(jumpCount ** 2) / 2 - 10)
                jumpCount -= 1

            else:
                isJump = False
                j_c = False
                jumpCount = 9
            if left:
                self.image = ANIMATION_JUMP_LEFT
                self.rect = self.rect.move(-10, 0)
            elif right:
                self.image = ANIMATION_JUMP_RIGHT
                self.rect = self.rect.move(10, 0)
            else:
                self.image = ANIMATION_JUMP

        elif left:
            self.right_frame = 0
            self.rect = self.rect.move(-10, 0)
            self.image = ANIMATION_LEFT[self.left_frame]
            self.left_frame += 1
            self.left_frame %= len(ANIMATION_LEFT)

        elif right:
            self.left_frame = 0
            self.image = ANIMATION_RIGHT[self.right_frame]
            self.rect = self.rect.move(10, 0)
            self.right_frame += 1
            self.right_frame %= len(ANIMATION_RIGHT)

        if not right and not left:
            self.left_frame = 0
            self.right_frame = 0
            self.image = ANIMATION_STAY

        if not on_ground:
            self.rect = self.rect.move(0, 10)
        if not flag3:
            on_ground = False


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - 1600 // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - 700 // 2)


class Spike(pygame.sprite.Sprite):
    def __init__(self, type, pos_x, pos_y):
        super().__init__(damage_group, all_sprites)
        self.image = spike_images[type]
        if type == 0:
            self.rect = self.image.get_rect().move(
                tile_width * pos_x, 660 - tile_height * pos_y)
        elif type == 1:
            self.rect = self.image.get_rect().move(
                tile_width * pos_x, 635 - tile_height * pos_y)
        elif type == 2:
            self.rect = self.image.get_rect().move(
                tile_width * pos_x + 25, 635 - tile_height * pos_y)
        elif type == 3:
            self.rect = self.image.get_rect().move(
                tile_width * pos_x, 635 - tile_height * pos_y)


camera = Camera()


def start_screen():
    global x, y, w, h,\
           speed, isJump, jumpCount, left,\
           right, animCount, LastMove, FPS,\
           flag, flag2

    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно",
                  'Нажмите ENTER для начала игры']

    fon = pygame.transform.scale(load_image('fon.jpg'), (1600, 700))
    win.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        win.blit(string_rendered, intro_rect)
        pygame.display.flip()

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        for bullet in bullets:
            if 0 < bullet.x < 500:
                bullet.x += bullet.vel
            else:
                bullets.pop(bullets.index(bullet))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            flag = True
        if flag:
            if keys[pygame.K_LEFT]:
                x -= speed
                left = True
                right = False
                LastMove = 'left'
            elif keys[pygame.K_RIGHT]:
                left = False
                right = True
                LastMove = 'right'
            else:
                left = False
                right = False
            if not isJump:
                if keys[pygame.K_SPACE]:
                    isJump = True
            if flag2:
                player, n, b = generate_level(load_level('tutorial.txt'))
                win.blit(game_fon, (0, 0))
                tiles_group.draw(win)
                flag2 = False
            if player not in all_sprites:
                player = death(n, b)
            win.blit(game_fon, (0, 0))
            all_sprites.draw(win)
            all_sprites.update()
            camera.update(player)
            for sprite in all_sprites:
                camera.apply(sprite)
            pygame.display.flip()
            clock.tick(FPS)


start_screen()
