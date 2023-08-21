# -*- coding: utf-8 -*-
import time
import socket
from concurrent import futures


def blocking_way():
    sock = socket.socket()
    # blocking
    sock.connect(('www.baidu.com', 80))
    request = f'GET / HTTP/1.0\r\nHost: www.baidu.com\r\n\r\n'
    sock.send(request.encode('ascii'))
    response = b''
    chunk = sock.recv(4096)
    while chunk:
        response += chunk
        # blocking
        chunk = sock.recv(4096)
    sock.close()
    return response


def thread_way():
    workers = 10
    with futures.ThreadPoolExecutor(workers) as executor:
        futs = {executor.submit(blocking_way) for _ in range(workers)}
    return len([fut.result() for fut in futs])


def progress_way():
    workers = 10
    with futures.ProcessPoolExecutor(workers) as executor:
        futs = {executor.submit(blocking_way) for _ in range(workers)}
    return len([fut.result() for fut in futs])


def sync_way():
    res = 0
    for _ in range(10):
        blocking_way()
        res += 1
    return res


def main():
    start = time.time()
    print(sync_way())
    print(time.time() - start)


if __name__ == '__main__':
    main()
