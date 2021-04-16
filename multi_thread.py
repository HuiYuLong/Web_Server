from socket import *
import os
import threading
import time

def handle_error(msg, start_time, end_time):
    try:
        items = msg.decode().split('\n')
        print("*** msg: ***\n", msg)

    # Parse the Request
        request_line = items[0]
        print("*** request_line: ***\n", request_line)

        is_304 = False
        for item in items:
            if 'If-Modified-Since' in item:
                is_304 = True

        items = request_line.split()
        # Request Method
        method = items[0]
        # Request URL
        url = items[1]
        # Protocol Version
        version = items[2]
        url = os.getcwd() + url
            
        if method != 'GET':
            print("wrong method")
            response = 'HTTP/1.1 400 Bad request\nConnection: close\n\n'
        elif version.startswith('HTTP') is False:
            print("wrong version")
            response = 'HTTP/1.1 400 Bad request\nConnection: close\n\n'
        # Check existence
        elif not os.path.exists(url):  
            print(url)           
            response = 'HTTP/1.1 404 Not Found\nConnection: close\n\n'
        # Check if modified
        elif is_304:
            response = 'HTTP/1.1 304 Not Modified\nConnection: close\n\n'
        elif end_time-start_time > 5:
            response = 'HTTP/1.1 408 Request Timed Out\nConnection: close\n\n'

        else:
            response = 'HTTP/1.1 200 OK\nConnection: keep-alive\nContent-Type: text/html\n\n'   
            with open(url, 'r') as f:
                response += f.read()  
    except Exception as e:
        print(e)
        response = 'HTTP/1.1 400 Bad request\nConnection: close\n\n'

    return response

def start_server(port: int) -> 'socket':

    # Create TCP SOCKET for server
    s = socket(AF_INET, SOCK_STREAM)

    # Bind Local Server's ID and Port
    try:
        s.bind(('127.0.0.1', port))
        print('server starts at port: ', port)
    except:
        s.bind(('127.0.0.1', 13000))
        print('server starts at port: ', 13000)

    # Listening
    s.listen(1000)
    return s

class WordThread(threading.Thread):
    """
    Request thread handling
    """
    def __init__(self, client_socket, start_time, end_time):
        threading.Thread.__init__(self)
        self.socket = client_socket
        self.start_time = start_time
        self.end_time = end_time

    def run(self):
        print(self.getName() + " thread start")
        print('The server thread ID: %d' % (threading.current_thread().ident))
        # str(self.socket.getsockname())
        # receive message
        msg = self.socket.recv(1024)
        if not msg:
            print('error: no msg')
            server_socket.close()
            return False

        response = handle_error(msg, self.start_time, self.end_time)
        print(response)

        self.socket.send(response.encode('utf-8'))
        self.socket.close()
        print(self.getName() + " thread exit")


def handle_request(server_socket):
    # Handle request from client
    while True:
        # Wait for client connection
        start_time = time.time()
        # time.sleep(6)
        client_socket, addr = server_socket.accept()
        end_time = time.time()

        # Create a thread
        thread = WordThread(client_socket, start_time, end_time)
        if not thread:
            continue
        thread.start()


if __name__ == '__main__':
    server_socket = start_server(12000)
    print('The server is ready to receive')
    handle_request(server_socket)
