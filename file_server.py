import json
import socket
import ssl

rsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock = ssl.wrap_socket(rsock, server_side=True, certfile="cert.pem", keyfile="key.pem",
                       ssl_version=ssl.PROTOCOL_TLSv1_2)

sock.bind(("192.168.0.108", 60))
sock.listen()

client, addr = sock.accept()

with open("config.json", "r") as config:
    file_name = json.load(config)

file = open(file_name["file"], "wb")
data = client.recv(2048)

while data:
    file.write(data)
    data = client.recv(2048)

file.close()
sock.close()