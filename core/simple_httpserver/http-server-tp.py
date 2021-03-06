#!/usr/bin/env python
#coding:utf-8

'''线程池版本
'''

import socket
import os
import sys
import signal
import Queue
import threading

'''
GET /index.html HTTP/1.1
Host: 54.222.146.205:8000
'''

resp = '''HTTP/1.1 200 OK\r\nContent-Length: 15\r\n\r\n<h1>zhengyscn</h1>'''

def worker():
    while True:
        conn = q.get() # 堵塞
        output = ''
        while '\r\n\r\n' not in output:
            recv_data = conn.recv(1)
            output += recv_data
        print 'url: ', output.split('\n')[0].split()[1]
        conn.sendall(resp)
        conn.close()
        q.task_done()


q = Queue.Queue()
for i in range(6):
     t = threading.Thread(target=worker)
     t.daemon = True
     t.start()

signal.signal( signal.SIGCHLD, signal.SIG_IGN )

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', 8000))
# backlog等于5，表示内核已经接到了连接请求，但服务器还没有调用accept进行处理的连接个数最大为5
# 这个值不能无限大，因为要在内核中维护连接队列
s.listen(5) #backlog

while True:
    conn, addr = s.accept()
    q.put(conn)
