import socket, ssl, pprint, time

HOST = '192.168.0.109'
PORT = 9999
BUFSIZE = 1024
ADDR = (HOST, PORT)

# socket create success
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# require a certificate from the server
ssl_sock = ssl.wrap_socket(s, ca_certs="cert.pem", cert_reqs=ssl.CERT_REQUIRED)
# socket connect success
ssl_sock.connect(ADDR)

# note that closing the SSLSocket will also close the underlying socket
pprint.pprint(ssl_sock.getpeercert())

while True:
    data = raw_input('> ')
    if not data:
        break
    ssl_sock.send(data)
    data = ssl_sock.recv(BUFSIZE)
    if not data:
        break
    print data
ssl_sock.close()