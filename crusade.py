import pygame
import os
import sys
import random

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
health_point = 0
left = False
right = False
music_cur = -1
animCount = 0
save_time = 20
level_cur = 0
camera_velocity = 2
LastMove = 'right'
FPS = 25
score = 0
music_paying = False
restart_ans = False
flag2 = True
player = None
music_stat = True
songs_list = {
    0: 'legends.mp3',
    1: 'peep.mp3',
    2: 'march.mp3',
    3: 'army_of_the_night.mp3',
    4: 'combat.mp3',
    5: 'in_the_name_of_god.mp3',
    6: 'anihilate.mp3'
}
rank = ''
tile_width = tile_height = 65
playing = False
all_bt = []

levels = {1: True,
          2: False,
          3: False,
          4: False}

ranks = ['крестьянин'
         'простолюдин',
         'оруженосец',
         'рыцарь',
         'крестоносец']

difficulty = None
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
damage_group = pygame.sprite.Group()
nothing_group = pygame.sprite.Group()
special_group = pygame.sprite.Group()
kill_group = pygame.sprite.Group()
win_group = pygame.sprite.Group()


def prepare():
    global difficulty, levels, score, rank, music_stat
    filename = "data/" + 'save.txt'
    with open(filename, 'r') as mapFile:
        info = [line.strip().split() for line in mapFile]
    difficulty = info[0][0]
    score = int(info[2][0])
    rank = info[3][0]
    if info[4][0] == 'True':
        music_stat = True
    else:
        music_stat = False
    for i in range(4):
        line = info[1][i].split(':')
        if line[1] == 'True':
            levels[int(line[0])] = True


def del_saves():
    global difficulty, levels, score, rank, music_stat
    filename = "data/" + 'copy.txt'
    with open(filename, 'r') as mapFile:
        info = [line.strip().split() for line in mapFile]
    score = int(info[2][0])
    rank = info[3][0]
    for i in range(4):
        line = info[1][i].split(':')
        if line[1] == 'True':
            levels[int(line[0])] = True
        else:
            levels[int(line[0])] = False


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if color_key is not None:
        if color_key is -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
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

HERETIC_STRONG_RIGHT = [load_image('heretic_str_r1.png'),
                        load_image('heretic_str_r2.png'),
                        load_image('heretic_str_r3.png'),
                        load_image('heretic_str_r4.png'),
                        load_image('heretic_str_r5.png')]

HERETIC_STRONG_LEFT = [load_image('heretic_str_l1.png'),
                       load_image('heretic_str_l2.png'),
                       load_image('heretic_str_l3.png'),
                       load_image('heretic_str_l4.png'),
                       load_image('heretic_str_l5.png')]

HERETIC_STRONG_STAY = load_image('heretic_knight_strong.png')

transparent_im = load_image('transparent.png')
d_w_image = load_image('death_wall.png')
main_fon_image = load_image('main_bg.png')
portal_image = load_image('portal_2.png')


def terminate():
    global difficulty, levels, score, rank, music_stat
    result = open('data/save.txt', 'w')
    result.write(difficulty + '\n')
    line = ''
    for i in range(1, 5):
        line += str(i) + ':' + str(levels[i]) + ' '
    result.write(line + '\n')
    result.write(str(score) + '\n')
    result.write(rank + '\n')
    result.write(str(music_stat) + '\n')
    result.close()
    music_stop()
    pygame.quit()
    sys.exit()


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip().split() for line in mapFile]
    return level_map[::-1]


class Particle(pygame.sprite.Sprite):
    blood = [load_image("blood.png")]
    for scale in (5, 10, 20):
        blood.append(pygame.transform.scale(blood[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        super().__init__(special_group, all_sprites)
        self.image = random.choice(self.blood)
        self.rect = self.image.get_rect()
        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = pos
        self.gravity = 0.35

    def update(self):
        self.velocity[1] += self.gravity
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        if not self.rect.colliderect((0, 0, 6239, 846)):
            self.kill()


def create_particles(position):
    particle_count = 20
    numbers = range(-5, 6)
    for _ in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers))


def music_start(m_number):
    global music_paying
    music_paying = True
    pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)
    pygame.mixer.music.load(songs_list[m_number])
    pygame.mixer.music.play(-1)


def music_stop():
    global music_paying
    pygame.mixer.music.stop()
    music_paying = False


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.type = tile_type
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, 635 - tile_height * pos_y)


class Nothing(pygame.sprite.Sprite):
    def __init__(self):  # спрайт на котором будет фокусироваться камера
        super().__init__(nothing_group, all_sprites)
        self.image = transparent_im
        self.all_movement = 0
        self.rect = self.image.get_rect().move(
            783, 335)

    def update(self):
        global camera_velocity, player

        for pl in player_group:
            if level_cur == 4 and \
                    difficulty == 'сложный':
                camera_velocity = 8
            else:
                if pl.rect.right >= 1000:
                    camera_velocity = 7
                else:
                    camera_velocity = 2
        if not self.all_movement >= 4638:
            self.rect = self.rect.move(camera_velocity, 0)
            self.all_movement += camera_velocity

    def restart(self):
        self.rect = self.rect.move(-self.all_movement, 0)
        self.all_movement = 0


def generate_level(level):
    global start_pos_x, start_pos_y, health_point
    new_player = None
    for i in range(len(level)):
        for g in range(len(level[i])):
            if level[i][g] == '@':
                new_player = Player(g, i, health_point)
                start_pos_x = g
                start_pos_y = i

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
            elif level[i][g] == 'h':
                Heretic(g, i)
            elif level[i][g] == 'H':
                HereticStrong(g, i)
            elif level[i][g] == 'p':
                Portal(g, i)
    return new_player


def restart():
    global start_pos_x, start_pos_y, health_point
    pl = Player(start_pos_x + 1, start_pos_y, health_point)
    return pl


class MainMenu:  # класс, отвечающий за прорисовку меню, кнопок и.т.д
    def __init__(self):
        self.score = score
        self.rank = rank
        self.dif = difficulty
        self.font = pygame.font.SysFont('arial', 120)
        self.font_bt = pygame.font.SysFont('arial', 60)

    def menu(self):
        global all_bt, music_stat, music_paying, music_cur, score, rank

        if music_stat and not music_cur == 2:
            music_cur = 2
            music_start(music_cur)

        all_bt = []
        win.blit(main_fon_image, (0, 0))
        text = self.font_bt.render("Rank:" + rank, 1, (255, 160, 0))
        text_x = 110
        text_y = 120
        win.blit(text, (text_x, text_y))
        text = self.font_bt.render("Score:" + str(score), 1, (255, 160, 0))
        text_x = 110
        text_y = 240
        win.blit(text, (text_x, text_y))
        text = self.font.render("I Wanna be CRUSADER", 1, (255, 204, 0))
        text_x = 200
        text_y = -22
        win.blit(text, (text_x, text_y))
        bt_play = Button(self.font_bt, 150, 'Играть')
        all_bt.append(bt_play)
        bt_set = Button(self.font_bt, 250, 'Настройки')
        all_bt.append(bt_set)
        bt_note = Button(self.font_bt, 350, 'Примечание')
        all_bt.append(bt_note)
        bt_ex = Button(self.font_bt, 450, 'Выход')
        all_bt.append(bt_ex)

    def levels(self):
        global all_bt
        all_bt = []
        win.blit(main_fon_image, (0, 0))
        text = self.font.render("Levels", 1, (255, 204, 0))
        text_x = 650
        text_y = -22
        win.blit(text, (text_x, text_y))
        bt_play = Button(self.font_bt, 150, 'Начало')
        all_bt.append(bt_play)
        bt_set = Button(self.font_bt, 250, 'Подземелье')
        all_bt.append(bt_set)
        bt_note = Button(self.font_bt, 350, 'Конец')
        all_bt.append(bt_note)
        bt_ex = Button(self.font_bt, 450, 'Эпилог???')
        all_bt.append(bt_ex)
        bt_back = Button(self.font_bt, 552, 'Назад')
        all_bt.append(bt_back)

    def settings(self):
        global difficulty, music_stat, all_bt

        all_bt = []
        win.blit(main_fon_image, (0, 0))
        text = self.font.render("Настройки", 1, (255, 204, 0))
        text_x = 550
        text_y = -22
        win.blit(text, (text_x, text_y))
        if music_stat:
            bt_music = Button(self.font_bt, 150, 'Музыка:вкл')
            all_bt.append(bt_music)
        else:
            bt_music = Button(self.font_bt, 150, 'Музыка:выкл')
            all_bt.append(bt_music)
        bt_dif = Button(self.font_bt, 250, 'Уровень сложности:' + difficulty)
        all_bt.append(bt_dif)
        bt_back = Button(self.font_bt, 552, 'Назад')
        all_bt.append(bt_back)
        bt_del_prog = Button(self.font_bt, 350, 'Сброс прогресса')
        all_bt.append(bt_del_prog)

    def note(self):
        global all_bt, music_cur, music_stat

        if music_stat and not music_cur == 1:
            music_cur = 1
            music_start(music_cur)
        all_bt = []
        intro_text = ['Примечание', '',
                      'Автор данной игры никого не хотел оскорбить.',
                      'Все совпадения случайны и не несут никакого смысла.',
                      'Если вы нашли в игре что-то задевающее ваши чуства,',
                      'то я приношу свои искренние извинения.']

        win.blit(main_fon_image, (0, 0))
        text_coord = 50
        for line in intro_text:
            string_rendered = self.font_bt.render(line, 1,
                                                  pygame.Color('yellow'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            win.blit(string_rendered, intro_rect)

        bt_back = Button(self.font_bt, 552, 'Назад')
        all_bt.append(bt_back)

    def difficulty(self):
        win.blit(main_fon_image, (0, 0))
        text = self.font.render("Уровень сложности", 1, (255, 200, 0))
        text_x = 350
        text_y = -22
        win.blit(text, (text_x, text_y))
        bt_easy = Button(self.font_bt, 150, 'Легкий')
        all_bt.append(bt_easy)
        bt_ramp = Button(self.font_bt, 250, 'Сложный')
        all_bt.append(bt_ramp)

    def death_screen(self):
        global restart_ans, music_stat, music_cur, all_bt, score

        all_bt = []
        score += 1
        if music_stat and not music_cur == 0:
            music_cur = 0
            music_start(music_cur)
        restart_ans = False
        text = self.font_bt.render("Вы умерли!", 1, (255, 200, 0))
        text_x = 650
        text_y = 100
        pygame.draw.polygon(win, (109, 41, 1), ((600, 100),
                                                (1000, 100),
                                                (1000, 650),
                                                (600, 650)), 0)
        pygame.draw.rect(win, (46, 196, 24), (600, 100, 400, 550), 5)
        win.blit(text, (text_x, text_y))
        bt_back = Button(self.font_bt, 552, 'Назад')
        all_bt.append(bt_back)
        bt_set = Button(self.font_bt, 350, 'Настройки')
        all_bt.append(bt_set)
        bt_restart = Button(self.font_bt, 250, 'Заново')
        all_bt.append(bt_restart)

    def win_screen(self):
        global restart_ans, music_stat, music_cur,\
               all_bt, score, level_cur, levels, rank

        all_bt = []
        music_stop()
        restart_ans = False
        text = self.font_bt.render("Вы победили!", 1, (255, 200, 0))
        text_x = 650
        text_y = 100
        pygame.draw.polygon(win, (109, 41, 1), ((600, 100),
                                                (1000, 100),
                                                (1000, 650),
                                                (600, 650)), 0)
        pygame.draw.rect(win, (46, 196, 24), (600, 100, 400, 550), 5)
        win.blit(text, (text_x, text_y))
        bt_win = Button(self.font_bt, 552, 'Deus Vult!')
        all_bt.append(bt_win)
        if level_cur == 1:
            score += 50
            levels[2] = True
            rank = 'простолюдин'
        elif level_cur == 2:
            score += 150
            levels[3] = True
            rank = 'оруженосец'
        elif level_cur == 3:
            score += 370
            levels[4] = True
            rank = 'рыцарь'
        elif level_cur == 4:
            score += 890
            rank = 'крестоносец'

    def pause(self):
        global music_stat, music_cur, all_bt, score

        all_bt = []
        score += 1
        pygame.mixer.music.pause()
        text = self.font_bt.render("Пауза", 1, (255, 200, 0))
        text_x = 720
        text_y = 100
        pygame.draw.polygon(win, (109, 41, 1), ((600, 100),
                                                (1000, 100),
                                                (1000, 650),
                                                (600, 650)), 0)
        pygame.draw.rect(win, (46, 196, 24), (600, 100, 400, 550), 5)
        win.blit(text, (text_x, text_y))
        bt_back = Button(self.font_bt, 552, 'Назад')
        all_bt.append(bt_back)
        bt_set = Button(self.font_bt, 350, 'Настройки')
        all_bt.append(bt_set)
        bt_restart = Button(self.font_bt, 250, 'Продолжить')
        all_bt.append(bt_restart)


class Button:
    def __init__(self, font, pos_y, string):
        self.font = font
        self.y = pos_y
        self.string = string
        self.text = self.font.render(self.string, 1, (255, 123, 0))
        self.x = 1600 // 2 - self.text.get_width() // 2
        self.text_w = self.text.get_width()
        self.text_h = self.text.get_height()
        self.mouse_on = False

    def draw(self, pos_x, pos_y):
        text_x = self.x
        text_y = self.y
        if self.x < pos_x < self.x + self.text_w + 10 and\
                self.y < pos_y < self.text_h + self.y + 10:
            self.mouse_on = True
        else:
            self.mouse_on = False
        if self.mouse_on:
            pygame.draw.polygon(win, (255, 235, 0),
                                ((self.x - 10, self.y),
                                (self.x + 10 + self.text_w, self.y),
                                (self.x + self.text_w + 9,
                                 self.y + self.text_h + 10),
                                (self.x - 10, self.y + self.text_h + 10)), 0)
            win.blit(self.text, (text_x, text_y))
            pygame.draw.rect(win, (109, 41, 1), (text_x - 10, text_y,
                                                 self.text_w + 20,
                                                 self.text_h + 10), 5)
        else:
            pygame.draw.polygon(win, (120, 120, 120),
                                ((self.x - 10, self.y),
                                (self.x + 10 + self.text_w, self.y),
                                (self.x + self.text_w + 9,
                                 self.y + self.text_h + 10),
                                (self.x - 10, self.y + self.text_h + 10)), 0)
            win.blit(self.text, (text_x, text_y))
            pygame.draw.rect(win, (109, 41, 1), (text_x - 10, text_y,
                                                 self.text_w + 20,
                                                 self.text_h + 10), 5)

    def clicked(self, pos_x, pos_y):
        if self.x < pos_x < self.x + self.text_w and\
                self.y < pos_y < self.text_h + self.y:
            return True
        return False


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, health):
        super().__init__(player_group, all_sprites)
        self.cur_frame = 0
        self.x = pos_x
        self.y = pos_y
        self.left_frame = 0
        self.health = health
        self.right_frame = 0
        self.image = ANIMATION_STAY
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, 635 - tile_height * pos_y)

    def update(self):
        global left, right, ANIMATION_RIGHT, ANIMATION_LEFT,\
               isJump, jumpCount, on_ground, LastMove, j_c, player,\
               playing, save_time, health_point

        flag3 = False
        for end in win_group:
            if pygame.sprite.collide_rect(self, end):
                screen.win_screen()
                playing = False
                self.kill()
        for entity in kill_group:
            if pygame.sprite.collide_rect(self, entity):
                screen.death_screen()
                playing = False
                self.kill()
        for spike in damage_group:
            if pygame.sprite.collide_rect(self, spike) and save_time == 0:
                create_particles((self.rect.right - (self.rect.right -
                                                     self.rect.left) // 2,
                                  self.rect.top))

                self.health -= 1
                health_point -= 1
                save_time = 20
                if self.health <= 0:
                    playing = False
                    screen.death_screen()
                    self.kill()
        for block in tiles_group:
            if pygame.sprite.collide_rect(self, block):  # столкновения
                if block.rect.top <= self.rect.bottom <= block.rect.top + 10 +\
                        (jumpCount ** 2) / 2 - 10:
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
                elif right and \
                        block.rect.left <= self.rect.right <= \
                        block.rect.left + 55:
                    self.rect.right = block.rect.left
                elif left and \
                        block.rect.right - 55 <= self.rect.left <= \
                        block.rect.right:
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


class Portal(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(win_group, all_sprites)
        self.image = portal_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, 635 - tile_height * pos_y)


class Spike(pygame.sprite.Sprite):
    def __init__(self, side, pos_x, pos_y):
        super().__init__(damage_group, all_sprites)
        self.image = spike_images[side]
        if side == 0:
            self.rect = self.image.get_rect().move(
                tile_width * pos_x, 660 - tile_height * pos_y)
        elif side == 1:
            self.rect = self.image.get_rect().move(
                tile_width * pos_x, 635 - tile_height * pos_y)
        elif side == 2:
            self.rect = self.image.get_rect().move(
                tile_width * pos_x + 25, 635 - tile_height * pos_y)
        elif side == 3:
            self.rect = self.image.get_rect().move(
                tile_width * pos_x, 635 - tile_height * pos_y)


class Heretic(pygame.sprite.Sprite):  # класс простенького ai
    def __init__(self, pos_x, pos_y):
        super().__init__(damage_group, all_sprites)
        self.cur_frame = 0
        self.x = pos_x
        self.y = pos_y
        self.cur_move = 'left'  # первое движение всегда влево
        self.count = 0
        self.left_frame = 0
        self.right_frame = 0
        self.image = HERETIC_STAY
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, 634 - tile_height * pos_y)

    def update(self):
        self.count += 1
        if 70 <= self.count <= 100:
            self.image = HERETIC_STAY
        else:
            for block in tiles_group:
                if pygame.sprite.collide_rect(self, block):
                    if self.cur_move == 'left' and \
                            self.rect.left <= block.rect.right:
                        self.cur_move = 'right'
                        self.rect.left = block.rect.right
                    else:
                        self.cur_move = 'left'
                        self.rect.right = block.rect.left

            if self.cur_move == 'left':
                self.right_frame = 0
                self.rect = self.rect.move(-10, 0)
                self.image = HERETIC_LEFT[self.left_frame]
                self.left_frame += 1
                self.left_frame %= len(HERETIC_LEFT)

            else:
                self.left_frame = 0
                self.rect = self.rect.move(10, 0)
                self.image = HERETIC_RIGHT[self.right_frame]
                self.right_frame += 1
                self.right_frame %= len(HERETIC_RIGHT)
        self.count %= 100


class HereticStrong(pygame.sprite.Sprite):  # класс сильного ai
    def __init__(self, pos_x, pos_y):
        super().__init__(damage_group, all_sprites)
        self.cur_frame = 0
        self.x = pos_x
        self.y = pos_y
        self.cur_move = 'left'  # первое движение тоже всегда влево
        self.count = 0
        self.left_frame = 0
        self.right_frame = 0
        self.image = HERETIC_STRONG_STAY
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, 634 - tile_height * pos_y)

    def update(self):
        self.count += 1
        if 75 <= self.count <= 100:
            self.image = HERETIC_STRONG_STAY
        else:
            for block in tiles_group:
                if pygame.sprite.collide_rect(self, block):
                    if pygame.sprite.collide_rect(self, block):
                        if self.cur_move == 'left' and \
                                self.rect.left <= block.rect.right:
                            self.cur_move = 'right'
                            self.rect.left = block.rect.right
                        else:
                            self.cur_move = 'left'
                            self.rect.right = block.rect.left

            if self.cur_move == 'left':
                self.right_frame = 0
                self.rect = self.rect.move(-20, 0)
                self.image = HERETIC_STRONG_LEFT[self.left_frame]
                self.left_frame += 1
                self.left_frame %= len(HERETIC_STRONG_LEFT)

            else:
                self.left_frame = 0
                self.rect = self.rect.move(20, 0)
                self.image = HERETIC_STRONG_RIGHT[self.right_frame]
                self.right_frame += 1
                self.right_frame %= len(HERETIC_STRONG_RIGHT)
        self.count %= 100


class DeathWall(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(kill_group, all_sprites)
        self.image = d_w_image
        self.all_movement = 0
        self.rect = self.rect = self.image.get_rect().move(
                -105, -146)

    def update(self):
        self.rect = self.rect.move(3, 0)
        self.all_movement += 3

    def restart(self):
        self.rect = self.rect.move(-self.all_movement, 0)
        self.all_movement = 0


screen = MainMenu()
prepare()


def start_screen():
    global x, y, w, h,\
           speed, isJump, jumpCount, left,\
           right, animCount, LastMove, FPS,\
           playing, flag2, focus, death, all_bt,\
           player, difficulty, music_stat, music_cur,\
           restart_ans, level_cur, health_point, save_time, win_group

    if difficulty == 'None':
        screen.difficulty()
    else:
        screen.menu()
    pygame.display.flip()

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEMOTION:
                for bt in all_bt:
                    Button.draw(bt, event.pos[0], event.pos[1])
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0] == 1:
                    for bt in all_bt:
                        if Button.clicked(bt, event.pos[0], event.pos[1]) and \
                                bt.string == 'Играть':
                            screen.levels()
                        elif Button.clicked(bt, event.pos[0],
                                            event.pos[1]) and \
                                bt.string == 'Настройки':
                            screen.settings()
                        elif Button.clicked(bt, event.pos[0],
                                            event.pos[1]) and \
                                bt.string == 'Примечание':
                            screen.note()
                        elif Button.clicked(bt, event.pos[0],
                                            event.pos[1]) and \
                                bt.string == 'Выход':
                            terminate()
                        elif Button.clicked(bt, event.pos[0],
                                            event.pos[1]) and \
                                bt.string == 'Назад':
                            for s in all_sprites:
                                s.kill()
                            screen.menu()
                        elif Button.clicked(bt, event.pos[0],
                                            event.pos[1]) and \
                                bt.string == 'Легкий':
                            difficulty = 'легкий'
                            screen.menu()
                        elif Button.clicked(bt, event.pos[0],
                                            event.pos[1]) and \
                                bt.string == 'Сложный':
                            difficulty = 'сложный'
                            screen.menu()
                        elif Button.clicked(bt, event.pos[0],
                                            event.pos[1]) and \
                                bt.string.startswith('Уровень'):
                            if difficulty == 'сложный':
                                difficulty = 'легкий'
                            else:
                                difficulty = 'сложный'
                            screen.settings()
                        elif Button.clicked(bt, event.pos[0],
                                            event.pos[1]) and \
                                bt.string.startswith('Музыка'):
                            if music_stat:
                                music_stat = False
                                music_stop()
                            else:
                                music_start(2)
                                music_stat = True
                            screen.settings()
                        elif Button.clicked(bt, event.pos[0],
                                            event.pos[1]) and \
                                bt.string == 'Начало':
                            all_bt = []
                            level_cur = 1
                            if level_cur == 1:
                                music_cur = 4
                            if level_cur == 2:
                                music_cur = 5
                            if level_cur == 3:
                                music_cur = 3
                            if level_cur == 4:
                                music_cur = 6
                            music_cur = 4
                            win.blit(game_fon, (0, 0))
                            tiles_group.draw(win)
                            flag2 = False
                            playing = True
                            if music_stat:
                                music_start(4)
                            camera = Camera()
                            focus = Nothing()
                            death = DeathWall()
                            if difficulty == 'сложный':
                                health_point = 1
                            else:
                                health_point = 5
                            player = generate_level(load_level('level_1.txt'))
                        elif Button.clicked(bt, event.pos[0],
                                            event.pos[1]) and \
                                bt.string == 'Подземелье':
                            if levels[2]:
                                all_bt = []
                                win.blit(game_fon, (0, 0))
                                tiles_group.draw(win)
                                flag2 = False
                                playing = True
                                if music_stat:
                                    music_start(5)
                                music_cur = 5
                                camera = Camera()
                                focus = Nothing()
                                death = DeathWall()
                                level_cur = 2
                                if difficulty == 'сложный':
                                    health_point = 1
                                else:
                                    health_point = 5
                                player = generate_level(load_level(
                                    'level_2.txt'))
                        elif Button.clicked(bt, event.pos[0],
                                            event.pos[1]) and \
                                bt.string == 'Конец':
                            if levels[3]:
                                all_bt = []
                                win.blit(game_fon, (0, 0))
                                tiles_group.draw(win)
                                flag2 = False
                                playing = True
                                if music_stat:
                                    music_start(3)
                                camera = Camera()
                                focus = Nothing()
                                death = DeathWall()
                                level_cur = 3
                                music_cur = 3
                                if difficulty == 'сложный':
                                    health_point = 1
                                else:
                                    health_point = 5
                                player = generate_level(
                                    load_level('level_3.txt'))
                        elif Button.clicked(bt, event.pos[0],
                                            event.pos[1]) and \
                                bt.string == 'Эпилог???':
                            if levels[4]:
                                all_bt = []
                                win.blit(game_fon, (0, 0))
                                tiles_group.draw(win)
                                flag2 = False
                                playing = True
                                camera = Camera()
                                focus = Nothing()
                                death = DeathWall()
                                music_cur = 6
                                if music_stat:
                                    music_start(6)
                                level_cur = 4
                                if difficulty == 'сложный':
                                    health_point = 1
                                else:
                                    health_point = 5
                                player = generate_level(load_level(
                                    'level_4.txt'))
                        elif Button.clicked(bt, event.pos[0],
                                            event.pos[1]) and \
                                bt.string == 'Заново':
                            all_bt = []
                            restart_ans = True
                            playing = True
                            if difficulty == 'сложный':
                                health_point = 1
                            else:
                                health_point = 5
                            playing = True
                            if level_cur == 1:
                                music_cur = 4
                            if level_cur == 2:
                                music_cur = 5
                            if level_cur == 3:
                                music_cur = 3
                            if level_cur == 4:
                                music_cur = 6
                            if music_stat:
                                music_start(music_cur)
                        elif Button.clicked(bt, event.pos[0],
                                            event.pos[1]) and \
                                bt.string == 'Deus Vult!':
                            for s in all_sprites:
                                s.kill()
                            screen.menu()
                        elif Button.clicked(bt, event.pos[0],
                                            event.pos[1]) and \
                                bt.string == 'Продолжить':
                            all_bt = []
                            playing = True
                            if music_stat:
                                music_start(music_cur)
                        elif Button.clicked(bt, event.pos[0],
                                            event.pos[1]) and \
                                bt.string == 'Сброс прогресса':
                            del_saves()

        pygame.display.flip()
        keys = pygame.key.get_pressed()

        if playing:
            if keys[pygame.K_ESCAPE]:
                playing = False
                screen.pause()
                continue
            if save_time > 0:
                save_time -= 1
            pygame.mouse.set_visible(False)
            if keys[pygame.K_a]:
                x -= speed
                left = True
                right = False
                LastMove = 'left'
            elif keys[pygame.K_d]:
                left = False
                right = True
                LastMove = 'right'
            else:
                left = False
                right = False
            if not isJump:
                if keys[pygame.K_SPACE]:
                    isJump = True
            if player not in all_sprites and restart_ans:
                focus.restart()
                death.restart()
                camera.update(focus)
                for sprite in all_sprites:
                    camera.apply(sprite)
                player = restart()
            win.blit(game_fon, (0, 0))
            player_group.draw(win)
            damage_group.draw(win)
            tiles_group.draw(win)
            nothing_group.draw(win)
            special_group.draw(win)
            kill_group.draw(win)
            win_group.draw(win)
            all_sprites.update()
            camera.update(focus)
            for sprite in all_sprites:
                camera.apply(sprite)
            font = pygame.font.SysFont('arial', 36)
            text = font.render("Health:" + str(health_point), 1, (255, 200, 0))
            text_x = 60
            text_y = 120
            win.blit(text, (text_x, text_y))
            pygame.display.flip()
            clock.tick(FPS)
        else:
            pygame.mouse.set_visible(True)


if __name__ == "__main__":
    start_screen()
