import socket
import ssl
import threading

import app

rsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock = ssl.wrap_socket(rsock, server_side=True, certfile="cert.pem", keyfile="key.pem", ssl_version=ssl.PROTOCOL_TLSv1_2)

sock.bind(("192.168.0.108", 80))
sock.listen()

t = threading.Thread(target=app.time_check)
t.setDaemon(True)
t.start()

while True:
    client, addr = sock.accept()
    print(addr)
    while True:
        try:
            request = client.recv(2048).decode()
            if not request: break

            app.execute_request(request)

        except ConnectionResetError:
            break
    client.close()
