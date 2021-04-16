import socket
import threading
import random

lock = threading.Semaphore(1)

def request(threadId):
	global lock

	# Create a client socket
	clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
	# Connect to the server
	clientSocket.connect(("127.0.0.1",13000))

	# Send data to server
	# Send a proper request - return OK code
	ok_request = 'GET /test.html HTTP/1.1\r\n\r\n'
	# Send a coditional request - return Not Modified message
	coditional_request = 'GET /test.html HTTP/1.1\r\nIf-Modified-Since: 2021-04-12'
	# Send a POST request - return 400 BAD request
	bad_request = 'POST /test.html HTTP/1.1\r\n\r\n'
	# Request for a non-exist web page
	non_exist_request = 'GET /nonexist.html HTTP/1.1\r\n\r\n'

	requests = [ok_request, coditional_request, bad_request, non_exist_request]

	request = random.choice(requests)
	# Random choose a request and send it to server side
	clientSocket.send(request.encode())

	# Receive data from server
	dataFromServer = clientSocket.recv(1024)

	lock.acquire()
	print(dataFromServer.decode())
	lock.release()
	clientSocket.close()

def main():
	threads = list()
	numThreads = 10
	for i in range(numThreads):
		thread = threading.Thread(target=request, args=[i+1])
		threads.append(thread)
		thread.start()
	for thread in threads:
		thread.join()

if __name__ == "__main__":
	main()