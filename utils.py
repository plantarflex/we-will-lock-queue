import socket
import os


def get_base_directory():
    return os.path.dirname(os.path.abspath(__file__))


def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    ip_address = s.getsockname()[0]
    s.close()
    return ip_address


def chunks(_list, n):
    for i in range(0, len(_list), n):
        yield _list[i:i+n]
