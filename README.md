## WE WILL LOCK QUEUE

---

* Communication between remote processes via TCP socket
* Socket Master maintains...
    * socket server
    * global queue of socket slaves
    * state object whether to call ACK
    * broadcaster to call ACK to all slaves
* Socket Slave maintains ...
    * socket client
    * wait loop for master's acquire-ACK call
* Implemented to mock multiprocessing.Lock
* (future) may use celery or redis instead of global queue object for more stable operation


* If you are a python lover, you would probably know this multithreading pattern

```python
from threading import Lock, Thread
from concurrent.futures import ThreadPoolExecutor

def func(thread_name, lock):
    lock.acquire()
    print('{} acquired lock!'.format(thread_name))
    cnt += 1
    lock.release()
    print('{} released lock!'.format(thread_name))


def run_threads():
    lock = Lock()
    global cnt
    cnt = 0
    with ThreadPoolExecutor(max_workers=5) as executor:
        for thread_idx in range(5):
            executor.submit(
                func,
                thread_idx+1,
                lock
            )

def run_accordingly():
    lock = Lock()
    global cnt
    cnt = 0
    th1 = Thread(target=func, args(1,lock))
    th2 = Thread(target=func, args(1,lock))
    th1.start()
    th2.start()
    th1.join()
    th2.join()

```


* or this pattern implemented in muliprocessing could be like below

```python
from multiprocessing import Lock
from concurrent.futures import ProcessPoolExecutor

def func(process_name, lock):
    lock.acquire()
    print('{} acquired lock!'.format(process_name))
    cnt += 1
    lock.release()
    print('{} released lock!'.format(process_name))


def run_processes():
    lock = Lock()
    global cnt
    cnt = 0
    with ProcessPoolExecutor(max_workers=5) as executor:
        for process_idx in range(5):
            executor.submit(
                func,
                process_idx+1,
                lock
            )
```

* What if processes of completely different context, even with different python forked by irrelevent different mother processes should communicate?
* Probably you would like something like below

```python
from we_will_lock_you import Lock
from multiprocessing import Process

def func(process_name, lock):
    lock.acquire()
    print('{} acquired lock!'.format(process_name))
    cnt += 1
    lock.release()
    print('{} released lock!'.format(process_name))


def run_process():
    lock = Lock(remote='<REMOTE_PROCESS_INFO>')
    global cnt
    cnt = 0
    p1 = Process(target=func, args=(1, lock))
    p1.start()
    p1.join()
    
```
