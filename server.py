import socket
import threading
import sys
import pickle

class Service():
	"""docstring for Service"""
	def __init__(self, host="localhost", port=4000):

		self.clients = []

		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.bind((str(host), int(port)))
		self.sock.listen(10)
		self.sock.setblocking(False)

		accept = threading.Thread(target=self.acceptCon)
		proccessing = threading.Thread(target=self.proccessingCon)
		
		accept.daemon = True
		accept.start()

		proccessing.daemon = True
		proccessing.start()

		while True:
			msg = input('-->')
			if msg == 'quit':
				self.sock.close()
				sys.exit()
			else:
				pass


	def msg_to_all(self, msg, client):
		for c in self.clients:
			try:
				if c != client:
					c.send(msg)
			except:
				self.clients.remove(c)

	def acceptCon(self):
		while True:
			try:
				conn, addr = self.sock.accept()
				conn.setblocking(False)
				self.clients.append(conn)
			except:
				pass

	def proccessingCon(self):
		while True:
			if len(self.clients) > 0:
				for c in self.clients:
					try:
						data = c.recv(1024)
						if data:
							self.msg_to_all(data,c)
					except:
						pass


s = Service()