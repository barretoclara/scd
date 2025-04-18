import threading
import time


class BufferMonitor:
    def __init__(self, capacity):
        self.capacity = capacity
        self.buffer = [None] * capacity
        self.in_index = 0
        self.out_index = 0
        self.count = 0
        self.lock = threading.Lock()
        self.not_full = threading.Condition(self.lock)
        self.not_empty = threading.Condition(self.lock)

    def put_res(self, item, pid):
        with self.not_full:
            while self.count == self.capacity:
                print(f"[Produtor {pid}] Esperando (buffer cheio)...")
                self.not_full.wait()
            self.buffer[self.in_index] = item
            print(
                f"[Produtor {pid}] Produziu {item} | Pos: {self.in_index} | Buffer: {self.buffer}")
            self.in_index = (self.in_index + 1) % self.capacity
            self.count += 1
            self.not_empty.notify()

    def get_res(self, cid):
        with self.not_empty:
            while self.count == 0:
                print(
                    f"               [Consumidor {cid}] Esperando (buffer vazio)...")
                self.not_empty.wait()
            item = self.buffer[self.out_index]
            self.buffer[self.out_index] = None
            print(
                f"               [Consumidor {cid}] Consumiu {item} | Pos: {self.out_index} | Buffer: {self.buffer}")
            self.out_index = (self.out_index + 1) % self.capacity
            self.count -= 1
            self.not_full.notify()
            return item


buffer_monitor = BufferMonitor(capacity=5)


def producer(pid):
    for i in range(5):
        item = f"P{pid}-{i}"
        buffer_monitor.put_res(item, pid)
        time.sleep(1)


def consumer(cid):
    for i in range(5):
        buffer_monitor.get_res(cid)
        time.sleep(1.5)


for i in range(4):
    threading.Thread(target=producer, args=(i+1,)).start()
for i in range(4):
    threading.Thread(target=consumer, args=(i+1,)).start()
