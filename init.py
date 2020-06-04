import random
import math

random.seed()

class expando:
    pass

def create_ball(weight, diametr, x, y, xspeed, yspeed):  # хранение всех параметров шара
    ball = expando()
    ball.weight = weight   # вес
    ball.radius = diametr//2   # радиус
    ball.x = x   # абсцисса
    ball.y = y   # ордината
    ball.xspeed = xspeed  # скорость по х
    ball.yspeed = yspeed  # скорость по у
    ball.draw = None   # для отрисовки шара
    ball.collisions = 0   # количество столкновений для отметания лишних событий из очереди
    ball.index_in_queue = None   # индекс события с шаром в общей очереди
    ball.queue = None  # частная очередь
    ball.time = 0  # последнее обновление координат
    return ball

def preset_pyramid(): # разбиение бильярдной пирамиды
    diametr = 50
    weight = 1
    ball0 = create_ball(weight, diametr, 400, 25, 0, 2)
    ball1 = create_ball(weight, diametr, 400, 300, 0, 0)
    ball2 = create_ball(weight, diametr, 372.5, 355, 0, 0)
    ball3 = create_ball(weight, diametr, 427.5, 355, 0, 0)
    ball4 = create_ball(weight, diametr, 345, 410, 0, 0)
    ball5 = create_ball(weight, diametr, 400, 410, 0, 0)
    ball6 = create_ball(weight, diametr, 455, 410, 0, 0)
    ball7 = create_ball(weight, diametr, 317.5, 465, 0, 0)
    ball8 = create_ball(weight, diametr, 372.5, 465, 0, 0)
    ball9 = create_ball(weight, diametr, 427.5, 465, 0, 0)
    ball10 = create_ball(weight, diametr, 482.5, 465, 0, 0)
    ball11 = create_ball(weight, diametr, 290, 520, 0, 0)
    ball12 = create_ball(weight, diametr, 345, 520, 0, 0)
    ball13 = create_ball(weight, diametr, 400, 520, 0, 0)
    ball14 = create_ball(weight, diametr, 455, 520, 0, 0)
    ball15 = create_ball(weight, diametr, 510, 520, 0, 0)
    timestep = 1
    balls = [ball0, ball1, ball2, ball3, ball4, ball5, ball6, ball7, ball8, ball9, ball10, ball11, ball12, ball13, ball14, ball15]
    return balls, timestep, (800, 600)

def preset_brown(): # симуляция броуновской пирамиды
    ball = create_ball(20, 20, 400, 300, 0, 0)
    balls = [ball]
    y = 3
    while y < 290:
        for x in range(3, 790, 15):
            ball = create_ball(1, 4, x, y, random.gauss(0, 3), random.gauss(0, 3))
            balls.append(ball)
        y += 200
    y = 313
    while y < 590:
        for x in range(3, 790, 15):
            ball = create_ball(1, 4, x, y, random.gauss(0, 3), random.gauss(0, 3))
            balls.append(ball)
        y += 200

    timestep = 1
    return balls, timestep, (800, 600)

def preset_diffusion():
    balls = []
    for y in range(26, 285, 51):
        ball = create_ball(100000, 50, 400, y, 0, 0)
        balls.append(ball)
    for y in range(420, 574, 51):
        ball = create_ball(100000, 50, 400, y, 0, 0)
        balls.append(ball)
    for y in range(3, 590, 100):
        for x in range(3, 370, 10):
            ball = create_ball(1, 4, x, y, random.gauss(0, 1), random.gauss(0, 1))
            balls.append(ball)
    return balls, 1, (800, 600)

def user_input(file_adr):
    file = open(file_adr)
    string = file.readline()
    sizex = ''
    sizey = ''
    for i in range(len(string)):
        if string[i] != ' ':
            sizex += string[i]
        else:
            sizey = string[i+1:len((string))]
            break
    if sizex == '' or sizey == '':
        return None, None, None
    size = (int(sizex), int(sizey))
    balls = []

    string = file.readline()
    while string != '':
        weight = ''
        diametr = ''
        x = ''
        y = ''
        xspeed = ''
        yspeed = ''

        i = 0
        while i < len(string) and string[i] != ' ':
            weight += string[i]
            i += 1
        i += 1
        while i < len(string) and string[i] != ' ':
            diametr += string[i]
            i += 1
        i += 1
        while i < len(string) and string[i] != ' ':
            x += string[i]
            i += 1
        i += 1
        while i < len(string) and string[i] != ' ':
            y += string[i]
            i += 1
        i += 1
        while i < len(string) and string[i] != ' ':
            xspeed += string[i]
            i += 1
        i += 1
        while i < len(string) and string[i] != ' ':
            yspeed += string[i]
            i += 1

        if weight == '' or diametr == '' or x == '' or y == '' or xspeed == '' or yspeed == '':
            return None, None, None

        ball = create_ball(int(weight), int(diametr), int(x), int(y), int(xspeed), int(yspeed))
        balls.append(ball)

        string = file.readline()

    v2max = 0
    for i in range(len(balls)):
        if balls[i].x < balls[i].radius or balls[i].x > size[0] - balls[i].radius or balls[i].y < balls[i].radius or balls[i].y > size[1] - balls[i].radius:
            return None, None, None
        v2 = balls[i].xspeed**2 + balls[i].yspeed**2
        if v2 > v2max:
            v2max = v2
        for j in range(i+1, len(balls)):
            if ((balls[i].x - balls[j].x)**2 + (balls[i].y - balls[j].y)**2) < (balls[i].radius + balls[j].radius)**2:
                return None, None, None

    v2max = (math.sqrt(v2max))
    for i in range(len(balls)):
        balls[i].xspeed = balls[i].xspeed / v2max
        balls[i].yspeed = balls[i].yspeed / v2max

    return balls, 1, size






