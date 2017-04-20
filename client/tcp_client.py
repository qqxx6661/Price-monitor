# -*- coding: utf-8 -*-
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 建立连接:
s.connect(('115.159.190.214', 2333))
# 接收欢迎消息:
print(s.recv(1024).decode('utf-8'))
while True:
    data_plain = input('Please type a message:')
    data = str.encode(data_plain)  # 将str转为byte
    if data_plain == 'exit':
        s.send(data)
        break
    s.send(data)
    print(s.recv(1024).decode('utf-8'))
s.close()