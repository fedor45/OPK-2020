class expando():
    pass

def create_heap(n): # создаем кучу
    heap = expando()
    heap.arr = [None]*n
    heap.size = 0
    return heap

# РАЗДЕЛ ДЛЯ ОСНОВНОЙ ОЧЕРЕДИ

def app(heap, event, balls): # добавляем элемент в очередь
    heap.arr[heap.size] = event
    heap.size += 1
    i = heap.size - 1
    if i % 2 == 0:
        prev = (i - 2) // 2
    else:
        prev = (i - 1) // 2
    while prev >= 0 and heap.arr[prev].time > heap.arr[i].time:
        balls[heap.arr[prev].i].index_in_queue = i
        heap.arr[prev], heap.arr[i] = heap.arr[i], heap.arr[prev]
        i = prev
        if i % 2 == 0:
            prev = (i - 2) // 2
        else:
            prev = (i - 1) // 2
    balls[heap.arr[i].i].index_in_queue = i

def get_first(heap, balls):  #забираем первый элемент в очереди (он удаляется)
    first = heap.arr[0]
    balls[first.i].index_in_queue = None
    heap.size -= 1
    heap.arr[0], heap.arr[heap.size] = heap.arr[heap.size], heap.arr[0]
    heap.arr[heap.size] = None
    ind = 0
    if heap.size == 0:
        return first
    balls[heap.arr[0].i].index_in_queue = 0
    next1 = 2 * ind + 1
    next2 = 2 * ind + 2
    while next2 < heap.size and (
            heap.arr[ind].time > heap.arr[next1].time or heap.arr[ind].time > heap.arr[next2].time):
        if heap.arr[next1].time > heap.arr[next2].time:
            balls[heap.arr[next2].i].index_in_queue = ind
            heap.arr[next2], heap.arr[ind] = heap.arr[ind], heap.arr[next2]
            ind = next2
            next1 = 2 * ind + 1
            next2 = 2 * ind + 2
        else:
            balls[heap.arr[next1].i].index_in_queue = ind
            heap.arr[next1], heap.arr[ind] = heap.arr[ind], heap.arr[next1]
            ind = next1
            next1 = 2 * ind + 1
            next2 = 2 * ind + 2
    if next1 < heap.size and heap.arr[ind].time > heap.arr[next1].time:
        balls[heap.arr[next1].i].index_in_queue = ind
        heap.arr[next1], heap.arr[ind] = heap.arr[ind], heap.arr[next1]
        ind = next1
    balls[heap.arr[ind].i].index_in_queue = ind
    return first


def change_element(heap, new_event, ind, balls):   #меняем элемент по индексу на новый
    heap.arr[ind] = new_event
    if ind % 2 == 0:
        prev = (ind - 2) // 2
    else:
        prev = (ind - 1) // 2
    while prev >= 0 and heap.arr[prev].time > heap.arr[ind].time:
        balls[heap.arr[prev].i].index_in_queue = ind
        heap.arr[prev], heap.arr[ind] = heap.arr[ind], heap.arr[prev]
        ind = prev
        if ind % 2 == 0:
            prev = (ind - 2) // 2
        else:
            prev = (ind - 1) // 2
    next1 = 2*ind + 1
    next2 = 2*ind + 2
    while next2 < heap.size and (heap.arr[ind].time > heap.arr[next1].time or heap.arr[ind].time > heap.arr[next2].time):
        if heap.arr[next1].time > heap.arr[next2].time:
            balls[heap.arr[next2].i].index_in_queue = ind
            heap.arr[next2], heap.arr[ind] = heap.arr[ind], heap.arr[next2]
            ind = next2
            next1 = 2*ind + 1
            next2 = 2*ind + 2
        else:
            balls[heap.arr[next1].i].index_in_queue = ind
            heap.arr[next1], heap.arr[ind] = heap.arr[ind], heap.arr[next1]
            ind = next1
            next1 = 2 * ind + 1
            next2 = 2 * ind + 2
    if next1 < heap.size and heap.arr[ind].time > heap.arr[next1].time:
        balls[heap.arr[next1].i].index_in_queue = ind
        heap.arr[next1], heap.arr[ind] = heap.arr[ind], heap.arr[next1]
        ind = next1
    balls[heap.arr[ind].i].index_in_queue = ind

def delete(heap, ind, balls): # удаляем элемент по индексу
    balls[heap.arr[ind].i].index_in_queue = None
    heap.arr[ind], heap.arr[heap.size - 1] = heap.arr[heap.size - 1], heap.arr[ind]
    heap.size -= 1
    heap.arr[heap.size] = None
    if ind % 2 == 0:
        prev = (ind - 2) // 2
    else:
        prev = (ind - 1) // 2
    while prev >= 0 and heap.arr[prev].time > heap.arr[ind].time:
        balls[heap.arr[prev].i].index_in_queue = ind
        heap.arr[prev], heap.arr[ind] = heap.arr[ind], heap.arr[prev]
        ind = prev
        if ind % 2 == 0:
            prev = (ind - 2) // 2
        else:
            prev = (ind - 1) // 2
    next1 = 2 * ind + 1
    next2 = 2 * ind + 2
    while next2 < heap.size and (
            heap.arr[ind].time > heap.arr[next1].time or heap.arr[ind].time > heap.arr[next2].time):
        if heap.arr[next1].time > heap.arr[next2].time:
            balls[heap.arr[next2].i].index_in_queue = ind
            heap.arr[next2], heap.arr[ind] = heap.arr[ind], heap.arr[next2]
            ind = next2
            next1 = 2 * ind + 1
            next2 = 2 * ind + 2
        else:
            balls[heap.arr[next1].i].index_in_queue = ind
            heap.arr[next1], heap.arr[ind] = heap.arr[ind], heap.arr[next1]
            ind = next1
            next1 = 2 * ind + 1
            next2 = 2 * ind + 2
    if next1 < heap.size and heap.arr[ind].time > heap.arr[next1].time:
        balls[heap.arr[next1].i].index_in_queue = ind
        heap.arr[next1], heap.arr[ind] = heap.arr[ind], heap.arr[next1]
        ind = next1
    balls[heap.arr[ind].i].index_in_queue = ind

# РАЗДЕЛ ДЛЯ ЧАСТНОЙ ОЧЕРЕДИ КАЖДОГО ШАРА

def app_self_queue(heap, event): # добавляем элемент в очередь
    heap.arr[heap.size] = event
    heap.size += 1
    i = heap.size - 1
    if i % 2 == 0:
        prev = (i - 2) // 2
    else:
        prev = (i - 1) // 2
    while prev >= 0 and heap.arr[prev].time > heap.arr[i].time:
        heap.arr[prev], heap.arr[i] = heap.arr[i], heap.arr[prev]
        i = prev
        if i % 2 == 0:
            prev = (i - 2) // 2
        else:
            prev = (i - 1) // 2

def del_first(heap):  # удаляем первый элемент в очереди
    first = heap.arr[0]
    heap.size -= 1
    heap.arr[0], heap.arr[heap.size] = heap.arr[heap.size], heap.arr[0]
    heap.arr[heap.size] = None
    ind = 0
    next1 = 2 * ind + 1
    next2 = 2 * ind + 2
    while next2 < heap.size and (
            heap.arr[ind].time > heap.arr[next1].time or heap.arr[ind].time > heap.arr[next2].time):
        if heap.arr[next1].time > heap.arr[next2].time:
            heap.arr[next2], heap.arr[ind] = heap.arr[ind], heap.arr[next2]
            ind = next2
            next1 = 2 * ind + 1
            next2 = 2 * ind + 2
        else:
            heap.arr[next1], heap.arr[ind] = heap.arr[ind], heap.arr[next1]
            ind = next1
            next1 = 2 * ind + 1
            next2 = 2 * ind + 2
    if next1 < heap.size and heap.arr[ind].time > heap.arr[next1].time:
        heap.arr[next1], heap.arr[ind] = heap.arr[ind], heap.arr[next1]
        ind = next1
    return first
