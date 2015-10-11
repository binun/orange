#!/usr/bin/python

import socket
import sys
import atexit
from conf import read_conf_file

def cleanup():
    global sock
    sock.close()
'''
def recv_end(the_socket,End):
	total_data=[]
	data=''
	while True:
		data=the_socket.recv(8192)
		if End in data:
			total_data.append(data[:data.find(End)])
			break
		total_data.append(data)
		if len(total_data)>1:
			last_pair=total_data[-2]+total_data[-1]
			if End in last_pair:
				total_data[-2]=last_pair[:last_pair.find(End)]
				total_data.pop()
				break
	return ''.join(total_data)
'''

host=read_conf_file('amm.conf','coordinator','host','localhost')
port=int(read_conf_file('amm.conf','coordinator','port','6666'))

print(host)
print(port)
atexit.register(cleanup)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print('starting up...')
sock.bind((host,port))
#sock.listen(1)

while True:
	data, address = sock.recvfrom(4096)
	
	print('connection from {0}'.format(address))
	#data = connection.recv(BUFFER)
	#data = recv_end(connection,'MSGEND')
	if data:
		print("received data:", data)
		
sock.close()	
	 
