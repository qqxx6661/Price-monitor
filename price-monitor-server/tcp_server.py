# -*- coding: utf-8 -*-
import socket
import threading
from send_email import SendEmail
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('0.0.0.0', 2333))
s.listen(5)  # 等待连接的最大数量
print('Waiting for connection...')


def tcplink(sock, addr):
    print('Accept new connection from %s:%s...' % addr)
    sock.send(b'Welcome to the price-monitor price-monitor-server!')
    while True:
        data = sock.recv(1024)
        data_plain = data.decode('utf-8')  # byte转str
        print('client message: %s' % data_plain)
        if data_plain == 'email':
            sock.send(b'Ready!')
            send_email = SendEmail('111', 'wo', 'ni', 'zhuti', 'yangzd1993@foxmail.com')
            send_email.send()
        elif not data or data_plain == 'exit':
            break
        sock.send(('Hello, %s!' % data.decode('utf-8')).encode('utf-8'))
    sock.close()
    print('Connection from %s:%s closed.' % addr)

while True:
    # 接受一个新连接:
    sock, addr = s.accept()
    # 创建新线程来处理TCP连接:
    t = threading.Thread(target=tcplink, args=(sock, addr))
    t.start()
