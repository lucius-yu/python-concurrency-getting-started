# threading_queue_example.py
# use queue implement consumer and proceducer in 2 threads

import time
from threading import Thread
from queue import Queue


def generate_item(item_no):
  time.sleep(1)
  print("item_{} generated".format(item_no))
  return "item_{}".format(item_no)

def process_item(item):
  time.sleep(2)
  print("{} processed".format(item))

def producer(queue):
  for i in range(10):
    item = generate_item(i)
    queue.put(item)

def consumer(queue):
  while True:
    item = queue.get()
    process_item(item)

item_queue = Queue(maxsize=20)

t_producer = Thread(target=producer, args=(item_queue, ))
t_consumer = Thread(target=consumer, args=(item_queue, ))

t_producer.start()
t_consumer.start()

t_producer.join()
t_consumer.join()