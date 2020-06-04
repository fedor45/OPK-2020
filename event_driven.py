import math
import binary_heap as bh

class expando():
    pass

def create_event(time, type, i, icollisions,  j = None, jcollisions = None):  # хранение параметров события
    event = expando()
    event.time = time  # время события с начала отсчета
    event.type = type  # тип частица-частица, частица-стена
    event.i = i  # 1 шар
    event.icollisions = icollisions # соударения 1 шара для отметания ложных событий
    event.j = j # 2 шар
    event.jcollisions = jcollisions # аналогично 1
    return event

def predict_collision_wall(size, ball1): # рассчет времени и типа события частица-стена
    dt = -1
    type = 'vertical'
    if ball1.xspeed > 0:
        dt = (size[0] - ball1.radius - ball1.x) / ball1.xspeed
    elif ball1.xspeed < 0:
        dt = (ball1.radius - ball1.x) / ball1.xspeed
    if ball1.yspeed > 0:
        dt1 = (size[1] - ball1.radius - ball1.y) / ball1.yspeed
        if dt1 < dt or dt == -1:
            type = 'horizontal'
            dt = dt1
    elif ball1.yspeed < 0:
        dt1 = (ball1.radius - ball1.y) / ball1.yspeed
        if dt1 < dt or dt == -1:
            type = 'horizontal'
            dt = dt1
    return dt, type

def predict_collision_particles(ball1, ball2, sim_time): # рассчет времени события частица-частица
    dx = (sim_time - ball2.time) * ball2.xspeed
    dy = (sim_time - ball2.time) * ball2.yspeed
    dvdr = ((ball2.x + dx) - ball1.x) * (ball2.xspeed - ball1.xspeed) + ((ball2.y + dy) - ball1.y) * (ball2.yspeed - ball1.yspeed)
    d = dvdr ** 2 - ((ball2.xspeed - ball1.xspeed) ** 2 + (ball2.yspeed - ball1.yspeed) ** 2) * (
                ((ball2.x + dx) - ball1.x) ** 2 + ((ball2.y + dy) - ball1.y) ** 2 - (ball1.radius + ball2.radius) ** 2)
    if dvdr >= 0 or d < 0:
        return -1, None
    dt = (-1) * ((dvdr + math.sqrt(d)) / ((ball2.xspeed - ball1.xspeed) ** 2 + (ball2.yspeed - ball1.yspeed) ** 2))
    return dt, 'particles'

def collision_resolve_wall(type, ball1): # изменнеие скорости шара после удара об стену
    if type == 'vertical':
        ball1.xspeed *= (-1)
        return True
    elif type == 'horizontal':
        ball1.yspeed *= (-1)
        return True
    return False

def collision_resolve_particles(ball1, ball2): # изменение скоростей шаров после соударения
    Je = 2 * ball1.weight * ball2.weight * (
            (ball2.x - ball1.x) * (ball2.xspeed - ball1.xspeed) + (ball2.y - ball1.y) * (
            ball2.yspeed - ball1.yspeed))
    sigma = ball1.radius + ball2.radius
    Je = Je / (sigma * (ball1.weight + ball2.weight))
    ball1.xspeed += Je * (ball2.x - ball1.x) / (sigma * ball1.weight)
    ball2.xspeed -= Je * (ball2.x - ball1.x) / (sigma * ball2.weight)
    ball1.yspeed += Je * (ball2.y - ball1.y) / (sigma * ball1.weight)
    ball2.yspeed -= Je * (ball2.y - ball1.y) / (sigma * ball2.weight)
    return True

def start_simulation(size, graph, balls): # формирование очередей и отрисовка шаров
    n = len(balls)
    simulation = expando()
    simulation.queue = bh.create_heap(n)
    simulation.time = 0
    for i in range(n):
        balls[i].queue = bh.create_heap(n)
        dt_wall, type = predict_collision_wall(size, balls[i])
        if dt_wall == -1:
            continue
        bh.app_self_queue(balls[i].queue, create_event(dt_wall, type, i, 0))
        for j in range(n):
            dt, type = predict_collision_particles(balls[i], balls[j], 0)
            if dt != -1 and dt < dt_wall:
                bh.app_self_queue(balls[i].queue, create_event(dt, type, i, 0, j, 0))

    for ball in balls:
        if ball.queue.arr[0] != None:
            bh.app(simulation.queue, ball.queue.arr[0], balls)

    for ball in balls:
        ball.draw = graph.DrawPoint((ball.x, ball.y), ball.radius*2, color='white')
    return simulation


def simulation_move(simulation, time_step, size, graph, balls): # рассчет следующего кадра
    timestep = time_step
    while timestep > 0:    # ПРОВЕРКА НА БЛИЖАЙШЕЕ СОУДАРЕНИЕ
        if simulation.queue.arr[0].time > simulation.time + timestep:
            simulation.time += timestep
            break


        dt = simulation.queue.arr[0].time - simulation.time
        timestep -= dt
        simulation.time += dt

        # ПРОВЕРКА НА ЛОЖНОСТЬ СОБЫТИЯ

        if simulation.queue.arr[0].type == 'particles' and \
                (balls[simulation.queue.arr[0].i].collisions != simulation.queue.arr[0].icollisions or balls[simulation.queue.arr[0].j].collisions != simulation.queue.arr[0].jcollisions):

            bh.del_first(balls[simulation.queue.arr[0].i].queue)
            bh.change_element(simulation.queue, balls[simulation.queue.arr[0].i].queue.arr[0], 0, balls)

        else:
            event = bh.get_first(simulation.queue, balls)
            if event.type == 'particles':
                # ОБНОВЛЕНИЕ КООРДИНАТ ШАРОВ ДЛЯ ПРОСЧЕТА ИЗМЕНЕНИЯ СКОРОСТЕЙ

                graph.MoveFigure(balls[event.i].draw, (time_step - timestep) * balls[event.i].xspeed,
                                 (time_step - timestep) * balls[event.i].yspeed)
                graph.MoveFigure(balls[event.j].draw, (time_step - timestep) * balls[event.j].xspeed,
                                 (time_step - timestep) * balls[event.j].yspeed)

                balls[event.i].x += (simulation.time - balls[event.i].time) * balls[event.i].xspeed
                balls[event.i].y += (simulation.time - balls[event.i].time) * balls[event.i].yspeed
                balls[event.i].time = simulation.time
                balls[event.j].x += (simulation.time - balls[event.j].time) * balls[event.j].xspeed
                balls[event.j].y += (simulation.time - balls[event.j].time) * balls[event.j].yspeed
                balls[event.j].time = simulation.time

                # ИЗМЕНЕНИЕ СКОРОСТЕЙ, ОБНОВЛЕНИЕ ОЧЕРЕДЕЙ

                collision_resolve_particles(balls[event.i], balls[event.j])
                balls[event.i].collisions += 1
                balls[event.j].collisions += 1
                balls[event.i].queue = bh.create_heap(len(balls))
                balls[event.j].queue = bh.create_heap(len(balls))

                # ПРЕДСКАЗАНИЕ СЛЕДУЮЩИХ СТОЛКНОВЕНИЙ

                dt_wall, type = predict_collision_wall(size, balls[event.i])
                if dt_wall != -1:
                    bh.app_self_queue(balls[event.i].queue,
                                      create_event(dt_wall + simulation.time, type, event.i, balls[event.i].collisions))
                    for ind in range(event.i):
                        dt, type = predict_collision_particles(balls[event.i], balls[ind], simulation.time)
                        if dt != -1 and dt < dt_wall:
                            bh.app_self_queue(balls[event.i].queue,
                                              create_event(dt + simulation.time, type, event.i,
                                                           balls[event.i].collisions, ind, balls[ind].collisions))

                    for ind in range(event.i + 1, len(balls)):
                        dt, type = predict_collision_particles(balls[event.i], balls[ind], simulation.time)
                        if dt != -1 and dt < dt_wall:
                            bh.app_self_queue(balls[event.i].queue,
                                              create_event(dt + simulation.time, type, event.i,
                                                           balls[event.i].collisions, ind, balls[ind].collisions))

                    bh.app(simulation.queue, balls[event.i].queue.arr[0], balls)

                dt_wall, type = predict_collision_wall(size, balls[event.j])
                if dt_wall != -1:
                    bh.app_self_queue(balls[event.j].queue,
                                      create_event(dt_wall + simulation.time, type, event.j, balls[event.j].collisions))
                    for ind in range(event.j):
                        dt, type = predict_collision_particles(balls[event.j], balls[ind], simulation.time)
                        if dt != -1 and dt < dt_wall:
                            bh.app_self_queue(balls[event.j].queue,
                                              create_event(dt + simulation.time, type, event.j,
                                                           balls[event.j].collisions, ind, balls[ind].collisions))

                    for ind in range(event.j + 1, len(balls)):
                        dt, type = predict_collision_particles(balls[event.j], balls[ind], simulation.time)
                        if dt != -1 and dt < dt_wall:
                            bh.app_self_queue(balls[event.j].queue,
                                              create_event(dt + simulation.time, type, event.j,
                                                           balls[event.j].collisions, ind, balls[ind].collisions))

                if balls[event.j].index_in_queue != None:
                    if balls[event.j].queue.size != 0:
                        bh.change_element(simulation.queue, balls[event.j].queue.arr[0], balls[event.j].index_in_queue,
                                          balls)
                    else:
                        bh.delete(simulation.queue, balls[event.j].index_in_queue, balls)
                elif balls[event.j].queue.size != 0:
                    bh.app(simulation.queue, balls[event.j].queue.arr[0], balls)

            else:
                # ОБНОВЛЕНИЕ

                balls[event.i].x += (simulation.time - balls[event.i].time) * balls[event.i].xspeed
                balls[event.i].y += (simulation.time - balls[event.i].time) * balls[event.i].yspeed
                balls[event.i].time = simulation.time

                # ИЗМЕНЕНИЕ

                collision_resolve_wall(event.type, balls[event.i])
                balls[event.i].collisions += 1
                balls[event.i].queue = bh.create_heap(len(balls))

                # ПРЕДСКАЗАНИЕ

                dt_wall, type = predict_collision_wall(size, balls[event.i])
                if dt_wall != -1:
                    bh.app_self_queue(balls[event.i].queue,
                                      create_event(dt_wall + simulation.time, type, event.i, balls[event.i].collisions))
                    for ind in range(event.i):
                        dt, type = predict_collision_particles(balls[event.i], balls[ind], simulation.time)
                        if dt != -1 and dt < dt_wall:
                            bh.app_self_queue(balls[event.i].queue,
                                              create_event(dt + simulation.time, type, event.i,
                                                           balls[event.i].collisions,
                                                           ind, balls[ind].collisions))

                    for ind in range(event.i + 1, len(balls)):
                        dt, type = predict_collision_particles(balls[event.i], balls[ind], simulation.time)
                        if dt != -1 and dt < dt_wall:
                            bh.app_self_queue(balls[event.i].queue,
                                              create_event(dt + simulation.time, type, event.i,
                                                           balls[event.i].collisions,
                                                           ind, balls[ind].collisions))

                    bh.app(simulation.queue, balls[event.i].queue.arr[0], balls)

    # ОТРИСОВКА НОВОГО КАДРА

    delta = simulation.time - time_step


    for ball in balls:
        if ball.time <= delta:
            graph.MoveFigure(ball.draw, ball.xspeed * time_step, ball.yspeed * time_step)
        else:
            graph.MoveFigure(ball.draw, ball.xspeed * (simulation.time - ball.time), ball.yspeed * (simulation.time - ball.time))
