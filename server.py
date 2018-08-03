# -*- coding:utf-8 -*-
import threading
import logging
from logging import handlers
import os
import ssl
import socket
import urllib
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

###---------------logging
# 获取logger实例，如果参数为空则返回root logger
logger = logging.getLogger(__name__)
# 指定logger输出格式
formatter = logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s')
## 文件日志
#如果没有log文件夹创建
if not os.path.exists('./log'):
    os.makedirs('./log')
logfile = "./log/access.log"
file_handler = handlers.TimedRotatingFileHandler(logfile, when='d', interval=1, backupCount=0, encoding=None, delay=False, utc=False)
file_handler.setFormatter(formatter)  # 可以通过setFormatter指定输出格式
# 控制台日志
console_handler = logging.StreamHandler(sys.stdout)
console_handler.formatter = formatter  # 也可以直接给formatter赋值
# 为logger添加的日志处理器
logger.addHandler(file_handler)
logger.addHandler(console_handler)
# 指定日志的最低输出级别，默认为WARN级别
logger.setLevel(logging.INFO)
#开始记录日志
#logger.info('this is information')
###------------------logging

###图灵数据
def get_computer(data):
    key = 'dfasdfasdfsadfasfsafasfasdfsaf' # 更换成自己申请的
    api = 'http://www.tuling123.com/openapi/api?key='+key+'&info='+data
    response =urllib.urlopen(api).read()
    dic_json = json.loads(response)
    return 'bot:'.decode('utf-8')+dic_json['text']

###本机IP端口
#host = socket.gethostbyname(socket.gethostname())
host = '192.168.0.109'
logger.info('ServerIP: ' + host)
port =8888

###运行socket及从客户端取数据
def socket_service():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 防止socket server重启后端口被占用（socket.error: [Errno 98] Address already in use）
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        ###使用ssl加密 s (s是启动的socket,只要给s使用ssl加一层壳)
        #证书生成命令最好linux服务器下:openssl req -new -x509 -days 365 -nodes -out cert.pem -keyout key.pem
        connstream = ssl.wrap_socket(s, "key.pem", "cert.pem", server_side=True, ssl_version=ssl.PROTOCOL_TLSv1)
        connstream.bind((host, port))
        connstream.listen(10)

    except socket.error as msg:
        print msg
        sys.exit(1)
    logger.info('Waiting connection...')

    #多线程
    while 1:
        conn, addr = connstream.accept()
        t = threading.Thread(target=deal_data, args=(conn, addr))
        t.start()

def deal_data(conn, addr):
    logger.info('Accept new connection from {0}'.format(addr))
    conn.send('Hi, Welcome to the server!')
    while 1:
        data = conn.recv(1024)
        #{0}{1}表示第0个和第1个变量
        logger.info('{0} client send data is {1}'.format(addr, data))
        #time.sleep(1)
        if data == 'exit' or not data:
            logger.info('{0} connection close'.format(addr))
            conn.send('Connection closed!')
            break
        else:
            sp = get_computer(data)
            conn.send('Your:' + data + '\n' + '{0}'.format(sp))
    conn.close()

if __name__ == '__main__':
    socket_service()




