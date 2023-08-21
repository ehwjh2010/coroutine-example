# -*- coding: utf-8 -*-
import time
import socket
from selectors import DefaultSelector, EVENT_WRITE, EVENT_READ

selector = DefaultSelector()
stopped = False
elements = [i for i in range(10)]
elements_copy = [0 for _ in range(10)]


class Crawler:
    def __init__(self, e):
        self.url = '/'
        self.sock = None
        self.response = b''
        self.count = 1
        self.e = e

    def fetch(self):
        self.sock = socket.socket()
        self.sock.setblocking(False)
        try:
            self.sock.connect(('www.baidu.com', 80))
        except BlockingIOError:
            pass
        selector.register(self.sock.fileno(), EVENT_WRITE, self.connected)

    def connected(self, key, mask):
        selector.unregister(key.fd)
        get = 'GET {0} HTTP/1.0\r\nHost: www.baidu.com\r\n\r\n'.format(self.url)
        self.sock.send(get.encode('ascii'))
        selector.register(key.fd, EVENT_READ, self.read_response)

    def read_response(self, key, mask):
        global stopped
        # 如果响应大于4KB，下一次循环会继续读
        chunk = self.sock.recv(4096)

        if chunk:
            self.response += chunk
        else:
            selector.unregister(key.fd)
            elements_copy[self.e] = self.e
            print(self.url, self.count, len(self.response))
            if elements_copy == elements:
                stopped = True
        self.count += 1


def loop():
    while not stopped:
        # 阻塞, 直到一个事件发生
        events = selector.select()
        for event_key, event_mask in events:
            callback = event_key.data
            callback(event_key, event_mask)


if __name__ == '__main__':
    start = time.time()
    for ele in elements:
        crawler = Crawler(ele)
        crawler.fetch()
    loop()
    print(time.time() - start)
