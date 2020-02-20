import socket
from threading import Thread
from queue import Queue
from config import Config


class SocketMaster:
    ACQUIRE = b'0'
    RELEASE = b'1'
    LOCK = b'2'
    def __init__(self, host, port):
        self.acq = Queue()
        self.client_socks = []
        self.flag = True
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((host, port))
        self.sock.listen()
        Thread(target=self.accept, args=()).start()
        Thread(target=self.listen, args=()).start()
        Thread(target=self.send, args=()).start()

    def accept(self):
        while True:
            print('>>>> Waiting for client socket call...')
            client_sock, addr = self.sock.accept()
            print('>>>> Established socket connection with {}'.format(addr))
            self.client_socks.append(client_sock)

    def listen(self):
        while True:
            for client_sock in self.client_socks:
                try:
                    data = client_sock.recv(1)
                    print(data)
                    if data == self.ACQUIRE:
                        self.acq.put(client_sock)
                        continue
                    elif data == self.RELEASE:
                        print('>>>> {} releases lock'.format(client_sock))
                        self.flag = True
                        continue
                    else:
                        continue
                except Exception as e:
                    print(e)
                    continue

    def send(self):
        while True:
            if self.flag is True and not self.acq.empty():
                try:
                    client_sock = self.acq.get()
                    client_sock.sendall(self.LOCK)
                    print('>>>> {} acquires lock'.format(client_sock))
                    self.flag = False
                    self.acq.task_done()
                except Exception as e:
                    print(e)
                    continue


def run():
    master = SocketMaster(
        Config.SOCKET_MASTER_NAME,
        Config.SOCKET_MASTER_PORT
        )


if __name__ == '__main__':
    run()

