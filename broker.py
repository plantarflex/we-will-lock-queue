import socket
from config import BaseConfig
from threading import Thread, Lock, Queue


class Master:
    def __init__(self):
        global greenlight, lock, queue
        greenlight = True
        lock = Lock()
        acquire_queue = Queue()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            while True:
                sock.bind((
                   BaseConfig.VIKI_MASTER_NAME,
                   BaseConfig.VIKI_MASTER_PORT
                   ))
                print('>>>> Waiting for client socket call...')
                sock.listen()
                client_sock, addr = sock.accept()
                print('>>>> Established socket connection with {}'.format(addr))
                sock_thread = Thread(target=self.send_signal, args=(client_sock,))
                sock_thread.start()
                #sock_thread.join()

    def send_signal(self, client_sock):
        while True:
            lock.acquire()
            data = slave.recv(1024)
            print(data)
            if data == 'acquire':
                if greenlight is True:
                    client_sock.send(True)
                    greenlight = False
                else:
                    client_sock.send(False)
            elif data == 'release':
                greenlight = True
            lock.release()



class Slave:
    def __init__(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            while True:
                sock.connect((
                    BaseConfig.VIKI_MASTER_NAME,
                    BaseConfig.VIKI_MASTER_PORT
                    ))
                sock.sendall(msg)
                data = sock.recv(1024)
        print('Received', repr(data))
        return data




