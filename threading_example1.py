import threading
import time

def do_some_work(val):
  print("doing some work in thread")
  time.sleep(1)
  print("echo : {}".format(val))
  return

# main thread
val = "text"
t = threading.Thread(target=do_some_work, args=(val,))
t.start()
print("suspend execution in main thread")
t.join()
print("continoue execution in main thread")
