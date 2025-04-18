import threading
import time

BUFFER_SIZE = 5
buffer = [None] * BUFFER_SIZE
in_index = 0
out_index = 0

empty = threading.Semaphore(BUFFER_SIZE)
full = threading.Semaphore(0)
mutex = threading.Semaphore(1)


def producer(pid):
    global buffer, in_index
    for i in range(5):
        item = f"P{pid}-{i}"
        empty.acquire()
        mutex.acquire()
        buffer[in_index] = item
        print(
            f"[Produtor {pid}] Produziu {item} | Pos: {in_index} | Buffer: {buffer}")
        in_index = (in_index + 1) % BUFFER_SIZE
        mutex.release()
        full.release()
        time.sleep(1)


def consumer(cid):
    global buffer, out_index
    for i in range(5):
        full.acquire()
        mutex.acquire()
        item = buffer[out_index]
        buffer[out_index] = None
        print(
            f"               [Consumidor {cid}] Consumiu {item} | Pos: {out_index} | Buffer: {buffer}")
        out_index = (out_index + 1) % BUFFER_SIZE
        mutex.release()
        empty.release()
        time.sleep(1.5)


for i in range(2):
    threading.Thread(target=producer, args=(i+1,)).start()
for i in range(2):
    threading.Thread(target=consumer, args=(i+1,)).start()
