import socket
from time import sleep
from threading import Thread

class SocketSlave:
    ACQUIRE = b'0'
    RELEASE = b'1'
    LOCK = b'2'
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while True:
            print('Searching for socket server at {}:{}'.format(host, port))
            try:
                self.sock.connect((host, port))
                print('Connected to socket server')
                break
            except:
                continue

    def acquire(self):
        self.sock.sendall(self.ACQUIRE)
        while True:
            print('Waiting for lock')
            data = self.sock.recv(1)
            if data == self.LOCK:
                print('acquired lock')
                return True

    def release(self):
        print('releasing lock')
        self.sock.sendall(self.RELEASE)

    def test(self):
        cnt = 1
        while True:
            self.acquire()
            print('TRY {}'.format(cnt))
            cnt += 1
            sleep(3)
            self.release()


def test():
    slave = SocketSlave('master', 9999)
    slave.test()


if __name__ == '__main__':
    test()

