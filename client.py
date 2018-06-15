# -*- coding:utf-8 -*-

import socket
import ssl
import pprint
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#服务器IP及端口
host = '192.168.0.109'
port = 8888

def socket_client():

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #使用ssl加密 s
    #证书生成命令最好linux服务器下:openssl req -new -x509 -days 365 -nodes -out cert.pem -keyout key.pem
    ssl_sock = ssl.wrap_socket(s, ca_certs="cert.pem", cert_reqs=ssl.CERT_REQUIRED)
    ssl_sock.connect((host,port))

    print ssl_sock.recv(1024)
    #打印密钥信息
    pprint.pprint(ssl_sock.getpeercert())
    while 1:
        cmd = raw_input('please input line:')
        if cmd == 'quit':
            break
        elif cmd == '':
            continue
        ssl_sock.sendall(cmd)
        data = ssl_sock.recv(1024)
        # print unicode转一下,否则使用Pyinstaller转成exe时会出现中文乱码
        print unicode(data)
    ssl_sock.close()

if __name__ == '__main__':
    socket_client()