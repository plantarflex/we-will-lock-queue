import socket
from threading import Thread, Queue


class ThreadedMaster:
    def __init__(self, host, port):
        global acq, client_socks
        acq = Queue()
        client_socks = []
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((host, port))
        sock.listen()
        Thread(target=self.listen, args=(sock,)).start()
        Thread(target=self.handle_clients, args=()).start()

    def listen(self, sock):
        while True:
            print('>>>> Waiting for client socket call...')
            client_sock, addr = sock.accept()
            print('>>>> Established socket connection with {}'.format(addr))
            client_socks.append(client_sock)

    # TODO
    def handle_client(self, client_sock, lock):
        while True:
            data = client_sock.recv(1024)
            print(data)
            if data == 'acquire':
                if acq.empty():
                    client_sock.sendall(True)
                    continue
                acq.put(client_sock)
            elif data == 'release':
                new_client_sock = acq.get()
                self.broadcast(new_client_sock)
                acq.task_done()
            else:
                self.broadcast()
                continue

    def broadcast(self, except_=None):
        for client_sock in self.client_socks:
            if client_sock == except_:
                client_sock.sendall(True)
            else:
                client_sock.sendall(False)


class SlaveLock:
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while True:
            try:
                self.sock.connect((host, port))
                break
            except:
                continue

    def acquire(self):
        self.sock.sendall('acquire')
        while True:
            data = self.sock.recv(1024)
            print(data)
            if bool(data) is True:
               return True

    def release(self):
        self.sock.sendall('release')



