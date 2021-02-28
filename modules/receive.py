import os
import socket
import json
import configparser

config = configparser.ConfigParser()
config.read(os.path.dirname(os.path.dirname(__file__)) + '\\config.ini', encoding='GB18030')

ListenSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ListenSocket.bind((config.get('network','LISTEN_IP'), config.getint('network','LISTEN_PORT')))
ListenSocket.listen(100)

HttpResponseHeader = '''HTTP/1.1 200 OK
Content-Type: text/html
'''

def request_to_json(msg):
    for i in range(len(msg)):
        if msg[i]=="{" and msg[-1]=="}":
            return json.loads(msg[i:])
    return None

#需要循环执行，返回值为json格式
def rev_msg():# json or None
    Client, Address = ListenSocket.accept()
    Request = Client.recv(1024).decode(encoding='utf-8')
    #print(Request)
    rev_json=request_to_json(Request)
    Client.sendall((HttpResponseHeader).encode(encoding='utf-8'))
    Client.close()
    return rev_json