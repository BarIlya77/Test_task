import threading
import time
import queue

from api import add_weather_data
from sql import Weather
from export_xlsx import write_data_xlsx

running = True
sem = threading.Semaphore()
command_queue = queue.Queue()


def fun1():
    global running
    while running:
        sem.acquire()
        add_weather_data(55.69, 37.35)
        sem.release()
        time.sleep(180)


def fun2():
    global running
    while running:
        sem.acquire()
        if not command_queue.empty():
            command = command_queue.get()
            if command == "get data":
                data = Weather.get_data()
                print(write_data_xlsx(data))
        sem.release()
        time.sleep(0.25)


def command_listener():
    while running:
        time.sleep(1)
        command = input("Введите команду: ")
        command_queue.put(command)


thread1 = threading.Thread(target=fun1)
thread2 = threading.Thread(target=fun2)
listener_thread = threading.Thread(target=command_listener)

thread1.start()
thread2.start()
listener_thread.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    running = False

thread1.join()
thread2.join()
listener_thread.join()
