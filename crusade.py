import pygame
import os
import sys

pygame.init()
win = pygame.display.set_mode((1600, 700))
pygame.display.set_caption('Kubik Game')

clock = pygame.time.Clock()
x = 65
y = 571
w = 65
h = 65
speed = 5
isJump = False
jumpCount = 10
left = False
right = False
animCount = 0
LastMove = 'right'
FPS = 50
bullets = []
flag = False
flag2 = True
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
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
    'block_cross_normal': tiles[11]
}

tile_width = tile_height = 65
game_fon = load_image('green.png')
player_image = load_image('wh_normal.png')


def terminate():
    pygame.quit()
    sys.exit()


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip().split() for line in mapFile]
    return level_map[::-1]


class snaryad():
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.r = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self, window):
        pygame.draw.circle(window, self.color, (self.x, self.y),
                           self.r)


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, 635 - tile_height * pos_y)


def generate_level(level):
    new_player = None
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
            elif level[i][g] == '@':
                new_player = Player(g, i)
    return new_player, g, i


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.cur_frame = 0
        self.x = pos_x
        self.y = pos_y
        self.frames = player_sheet
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, 600 - tile_height * pos_y)

    def update(self):
        global left, right
        if left:
            self.rect = self.rect.move(0, 1)
            # self.rect = self.rect = self.rect.move(1, 0)

        if right:
            self.rect = self.rect.move(0, 1)
            # self.rect = self.rect.move(1, 0)

        if not pygame.sprite.spritecollideany(self, tiles_group):
            self.rect = self.rect.move(0, 1)
            #self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            #self.image = self.frames[self.cur_frame]


def drawWindow():
    for bullet in bullets:
        bullet.draw(win)
    pygame.display.update()


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
            if keys[pygame.K_f]:
                if LastMove == 'right':
                    facing = 1
                else:
                    facing = -1
                if len(bullets) < 5:
                    bullets.append(snaryad(round(x + w // 2),
                                           round(y + h // 2),
                                           5,
                                           (255, 000, 000),
                                           facing))
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
            else:
                if jumpCount >= -10:
                    if jumpCount < 0:
                        y += (jumpCount ** 2) / 2
                    else:
                        y -= (jumpCount ** 2) / 2
                    jumpCount -= 1

                else:
                    isJump = False
                    jumpCount = 10

            drawWindow()
            if flag2:
                generate_level(load_level('tutorial.txt'))
                win.blit(game_fon, (0, 0))
                tiles_group.draw(win)
                flag2 = False
            win.blit(game_fon, (0, 0))
            all_sprites.draw(win)
            all_sprites.update()
            pygame.display.flip()
            clock.tick(FPS)


start_screen()
