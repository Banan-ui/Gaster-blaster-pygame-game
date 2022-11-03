from random import randint
import pygame as pg
import sys


pg.init()
W = 900
H = 600
dist = 120 #Отступ от края окна до арены

ORANGE = (255, 165, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

seconds = 0
minutes = 0
timer = "00:00"

sides = ("left", "right", "up", "down")
crash = 0
next_frame = 0

transparency = 255 #Прозрачность выстрела


sc = pg.display.set_mode((W, H))

# FONT AND TIMER
font = pg.font.SysFont('arial', 50, bold=True)
# font = pg.font.Font('Excelsior 3.01 Regular.ttf', 50) #Recomended font (install and write path)

surf_font = font.render("Contain", True, WHITE , ORANGE) #Создание поверхности с таймером
rect_font = surf_font.get_rect(center = (W/2, 40))
# print(pg.font.get_fonts()) #Все шрифты в системе

#TIMERS
pg.time.set_timer(pg.USEREVENT, 760) #Таймер спавна
pg.time.set_timer(pg.USEREVENT + 3, 1000) #Таймер таймер

class Soul(): #Класс персонажа
    def __init__(self, surf):
        self.image = surf
        self.mask = pg.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center = (W/2, H/2))

        #Размеры картинки
        self.x = self.image.get_size()[0]
        self.y = self.image.get_size()[1]

        self.cent_pos = [int(self.rect.x + self.x/2),  int(self.rect.y + self.y/2)] #Центральная точка
        self.speed = 3 #Скорость передвежения

    def left(self):
        if self.rect.x > dist+3:
            self.rect.x -= self.speed
            self.cent_pos[0] -= self.speed


    def right(self):
        if self.rect.x < W-dist-self.x-2:
            self.rect.x += self.speed
            self.cent_pos[0] += self.speed

    def up(self):
        if self.rect.y > dist+4:
            self.rect.y -= self.speed
            self.cent_pos[1] -= self.speed

    def down(self):
        if self.rect.y < H-dist-self.y-2:
            self.rect.y += self.speed
            self.cent_pos[1] += self.speed


class Gb_ph1(pg.sprite.Sprite):
    def __init__(self, side, p_pos, surf_1, surf_2):
        pg.sprite.Sprite.__init__(self)
        self.player_pos = p_pos
        self.side = side
        # print(side)

    #ОБЧИСЛЕНИЕ ОБЩЕГО УГЛА, КАТЕТОВ, ТОЧЕК
        if self.side == "left": #Если левая сторона спавна
            self.spawn_pos = (int(dist/2), randint(dist, H-dist)) #Точка спавна
            self.cross_pos = (int(dist/2), self.player_pos[1]) #Точка пересечения между точкой спавна и точкой перебывания игрока, прямой угол
            self.applied = abs(self.cross_pos[1] - self.spawn_pos[1]) #Прилагающий катет
            self.opposite = abs(self.cross_pos[0] - self.player_pos[0]) #Противоположный катет
            self.demo_angle = 90 # Угол поворота картинки без дополнительного угла
            if self.spawn_pos[1] < self.player_pos[1]: # В зависимости от положения игрока (Выше или ниже точки спавна обьекта)
                self.f = "-"
            else:
                self.f = "+"

        elif self.side == "right":
            self.spawn_pos = (int(W-dist/2), randint(dist, H-dist))
            self.cross_pos = (int(W-dist/2), self.player_pos[1])
            self.applied = abs(self.cross_pos[1] - self.spawn_pos[1])
            self.opposite = abs(self.cross_pos[0] - self.player_pos[0])
            self.demo_angle = 270
            if self.spawn_pos[1] > self.player_pos[1]:
                self.f = "-"
            else:
                self.f = "+"

        elif self.side == "up":
            self.spawn_pos = (randint(dist, W-dist), int(dist/2))
            self.cross_pos = (self.player_pos[0], int(dist/2))
            self.applied = abs(self.spawn_pos[0] - self.cross_pos[0])
            self.opposite = abs(self.cross_pos[1] - self.player_pos[1])
            self.demo_angle = 0
            if self.spawn_pos[0] > self.player_pos[0]:
                self.f = "-"
            else:
                self.f = "+"

        elif self.side == "down":
            self.spawn_pos = (randint(dist, W-dist), int(H-dist/2))
            self.cross_pos = (self.player_pos[0], int(H-dist/2))
            self.applied = abs(self.spawn_pos[0] - self.cross_pos[0])
            self.opposite = abs(self.cross_pos[1] - self.player_pos[1])
            self.demo_angle = 180
            if self.spawn_pos[0] < self.player_pos[0]:
                self.f = "-"
            else:
                self.f = "+"

    # ОПРЕДЕЛЕНИЕ УГЛА НАКЛОНА
        if self.applied == 0:
            self.angle_of_slope = 0 #Дополнительный угол наклона
        else:
            self.ratio = self.opposite / self.applied
            if self.ratio > 5.6713:
                self.angle_of_slope = 5 #Дополнительный угол наклона
            elif self.ratio <= 5.6713 and self.ratio > 1.7321:
                self.angle_of_slope = 20
            elif self.ratio <= 1.7321 and self.ratio > 0.8390:
                self.angle_of_slope = 40
            elif self.ratio <= 0.8390 and self.ratio > 0.364:
                self.angle_of_slope = 60
            elif self.ratio <= 0.364:
                self.angle_of_slope = 80
            # print("Соотношение: ", self.ratio)

        if self.f == "+":
            self.finale_angle = self.demo_angle + self.angle_of_slope
        elif self.f == "-":
            self.finale_angle = self.demo_angle - self.angle_of_slope
        # print(self.finale_angle)

    #СОЗДАНИЕ И РАЗМЕЩЕНИЕ ПОВЕРХНОСТИ
        self.image = pg.transform.rotate(surf_1 , self.finale_angle)
        self.image_2 = pg.transform.rotate(surf_2 , self.finale_angle)
        self.rect = self.image.get_rect(center = self.spawn_pos)
        self.add(Blasters)

    def triangle_draw(self):
        pg.draw.line(sc, ORANGE, self.spawn_pos, self.player_pos) #Гипотенуза
        pg.draw.line(sc, GREEN, self.spawn_pos, self.cross_pos) #Приялягающий катет
        pg.draw.line(sc, BLUE, self.cross_pos, self.player_pos) #Противоположный катет

    def del_from_group(self):
        self.kill()


class Gb_ph2(pg.sprite.Sprite):
    def __init__(self, spawn_pos, surf, angle, group):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.rotate(surf, angle)
        self.mask = pg.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center = spawn_pos)

        self.image.set_alpha(255)
        self.add(group)


Blasters = pg.sprite.Group() #Группа

#Обьект класса Soul, основной игрок
player = Soul(pg.image.load("Soul.png").convert_alpha())

#Инициализация изображений
gblaster_png_1 = pg.image.load('GB_phase1.png').convert_alpha()
gblaster_png_2 = pg.image.load('GB_phase2.png').convert_alpha()
blaster_png = pg.image.load('fire.png').convert_alpha()

#Обьекты класса Gb_ph1
gb_1 = 0
gb_2 = 0

CONST_1 = 0
CONST_2 = 0
spawn = 1 #Показывает номер спавневшегося обьекта (всего 2)
offset_access = 0 #Наличие столкновения


# SOUNDS
first_sound = pg.mixer.Sound('gaster_blaster_first.wav')
sound1 = pg.mixer.Sound('gaster_blaster.wav')
sound2 = pg.mixer.Sound('hit.wav')
sound3 = pg.mixer.Sound('destruction.wav')

len_sound3 = sound3.get_length() #Время проигрывания

pg.mixer.music.load('MEGALOVANIA.mp3') #Загрузка файла с музыкой 
pg.mixer.music.play(-1) #Запуск проигрывания (-1) - Зацикливание проигрывания, (1) - проиграеться 2 раза
pg.mixer.music.set_volume(1) #Громкость

while 1:
    for i in pg.event.get():
        if i.type == pg.QUIT:
            sys.exit()

        elif i.type == pg.USEREVENT and crash == 0: #Создание обьектов класса Gb_ph1 по таймеру
            if spawn == 1: #Спавн обьекта 1
                # print("spawn obg_1")
                if CONST_1 == 1:
                    gb_1.kill()
                    GB_phase2.kill()
                    pg.time.set_timer(pg.USEREVENT+2, 500, True)
                else:
                    CONST_1 = 1

                offset_access = 0
                transparency_access = 0
                transparency = 255
                gb_1 = Gb_ph1(sides[randint(0, 3)], player.cent_pos, gblaster_png_1, gblaster_png_2)

                spawn = 2

            elif spawn == 2: #Спавн обьекта 2
                # print("spawn obg_2")
                if CONST_2 == 1:
                    gb_2.kill()
                    GB_phase2.kill()
                else:
                    CONST_2 = 1

                offset_access = 0
                transparency_access = 0
                transparency = 255
                gb_2 = Gb_ph1(sides[randint(0, 3)], player.cent_pos, gblaster_png_1, gblaster_png_2)

                pg.time.set_timer(pg.USEREVENT+1, 500, True)
                spawn = 1

            first_sound.play()
            first_sound = sound1

        elif i.type == pg.USEREVENT+1 and crash == 0: #Обновление обьекта gb_1, созданте обьекта класса Gb_ph2
            gb_1.image = gb_1.image_2
            GB_phase2 = Gb_ph2(gb_1.spawn_pos, blaster_png, gb_1.finale_angle, Blasters)
            offset_access = 1

        elif i.type == pg.USEREVENT+2 and crash == 0:#Обновление обьекта gb_2, созданте обьекта класса Gb_ph2
            gb_2.image = gb_2.image_2
            GB_phase2 = Gb_ph2(gb_2.spawn_pos, blaster_png, gb_2.finale_angle, Blasters)
            offset_access = 1

        elif i.type == pg.USEREVENT + 3 and crash == 0: #Событие таймера
            if seconds == 59:
                seconds = 0
                minutes += 1
            else:
                seconds += 1

            if seconds < 10:
                timer = f"0{minutes}:0{seconds}"
                # print("One")
            else:
                timer = f"0{minutes}:{seconds}"
                # print("Two")

        elif i.type == pg.USEREVENT + 4: #Событие "Крушения души"
            player.image = pg.image.load("Soul_end.png").convert_alpha()
            player.rect.x = player.rect.x - 1
            sound3.play()
            pg.time.set_timer(pg.USEREVENT + 5, int(round(len_sound3, 3) * 1000), 1)

        elif i.type == pg.USEREVENT + 5: #Выход из игры
            print('Game over')
            sys.exit()

    #OFFSET AND TRANSPARENCY
    if offset_access == 1 and crash == 0: # Проверка на столкновения и прозрачность
        if pg.sprite.collide_mask(player, GB_phase2) != None: #Проверка масок на столкновения используя названия спрайтов
            pg.mixer.music.stop()
            crash = 1 #CRASH START

        if transparency_access < 5: # Создание анимации прозрачности бластера
            transparency_access += 1
        else:
            transparency = transparency - 40 # -40 прозрачность
            GB_phase2.image.set_alpha(transparency) #Установка прозрачности
        

        #ВТОРОЙ СПОСОБ ПРОВЕРКИ СТОЛКНОВЕНИЙ (Ручной подсчет)
        # offset = (int(GB_phase2.rect.x - player.rect.x), int(GB_phase2.rect.y - player.rect.y))
        # if player.mask.overlap_area(GB_phase2.mask, offset) > 0:
            # print("Game Over")


    #УПРАВЛЕНИЕ
    keys = pg.key.get_pressed()
    if keys[pg.K_LEFT] and crash == 0:
        player.left()
    elif keys[pg.K_RIGHT] and crash == 0:
        player.right()

    if keys[pg.K_UP] and crash == 0:
        player.up()
    elif keys[pg.K_DOWN] and crash == 0:
        player.down()


#*****************************************************
# ОТРИСОВКА

    sc.fill(BLACK)

    surf_font = font.render(timer, True, WHITE)
    sc.blit(surf_font, rect_font)

    if next_frame < 5:
        Blasters.draw(sc)

    elif next_frame == 20:
        pg.mixer.stop()
        sound2.play()
        pg.time.set_timer(pg.USEREVENT+4, 1000, True)

    if crash == 1 and next_frame != 21:
        next_frame += 1

    #ПРЯМОУГОЛЬНИК АРЕНЫ
    # pg.draw.rect(sc, WHITE, (120, 120, W-240, H-240), 6)
    pg.draw.line(sc, WHITE, (dist, dist), (dist, H-dist), 6) #Left
    pg.draw.line(sc, WHITE, (W-dist, dist), (W-dist, H-dist), 6) #Right

    pg.draw.line(sc, WHITE, (dist-2, dist), (W-dist+3, dist), 6) #Up
    pg.draw.line(sc, WHITE, (dist-2, H-dist), (W-dist+3, H-dist), 6) #Bottom
    
    # gb_1.triangle_draw()
    sc.blit(player.image, player.rect)

    pg.display.update()
    pg.time.delay(10)






