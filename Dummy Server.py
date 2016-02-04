#!/usr/bin/python

import socket  # Networking support
import signal  # Signal support (server shutdown on signal receive)
import time    # Current time
import re
from threading import Thread

drones = {"drones":[
            {
            "name":"First name",
            "lat":32.231153299999995,
            "lon":-110.9509174,
            "batt":10,
            "taskName":"Asshole finder 9k",
            "taskNumber":10,
            },
            {
            "name":"second name",
            "lat":31.231153299999995,
            "lon":-110.9509174,
            "batt":50,
            "taskName":"Asshole finder 8k",
            "taskNumber":9,
            },
            {
            "Name":"Thurd name",
            "lat":30.231153299999995,
            "lon":-110.9509174,
            "bat":100,
            "taskName":"Asshole finder 7k",
            "taskNumber":8,
            }
        ]
	}
	
tasks = {"tasks":[
            {
            "Name":"First task",
            "lat":32.231153299999995,
            "lon":-110.9509174,
            "type":10,
            "name":"Asshole finder 9k",
            "number":0,
            },
            {
            "Name":"second task",
            "lat":31.231153299999995,
            "lon":-110.9509174,
            "type":10,
            "name":"Asshole finder 8k",
            "number":9,
            },
            {
            "name":"Thurd task",
            "lat":30.231153299999995,
            "lon":-110.9509174,
            "type":10,
            "name":"Asshole finder 7k",
            "number":8,
            }
        ]
		}

class Server(Thread):
 """ Class describing a simple HTTP server objects."""

 def __init__(self, port = 80):
	super(Server, self).__init__()
	self.daemon = True
	self.cancelled = False
	""" Constructor """
	self.host = ''   # <-- works on all avaivable network interfaces
	self.port = port
	self.www_dir = 'www' # Directory where webpage files are stored

 def activate_server(self):
     
     self._wait_for_connections()

 def shutdown(self):
     """ Shut down the server """
     try:
         print("Shutting down the server")
         s.socket.shutdown(socket.SHUT_RDWR)

     except Exception as e:
         print("Warning: could not shut down the socket. Maybe it was already closed?",e)

 def _gen_headers(self,  code):
     """ Generates HTTP response Headers. Ommits the first line! """

     # determine response code
     h = ''
     if (code == 200):
        h = 'HTTP/1.1 200 OK\n'
     elif(code == 404):
        h = 'HTTP/1.1 404 Not Found\n'

     # write further headers
     current_date = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
     h += 'Date: ' + current_date +'\n'
     h += 'Server: Simple-Python-HTTP-Server\n'
     h += 'Connection: close\n\n'  # signal that the conection wil be closed after complting the request

     return h

 def run(self):
     """ Attempts to aquire the socket and launch the server """
     self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
     try: # user provided in the __init__() port may be unavaivable
         self.socket.bind((self.host, self.port))

     except Exception as e:
		print("ERROR: Failed to acquire sockets for ports ", user_port, " and 8080. ")
		print("Try running the Server in a privileged user mode.")
		import sys
		sys.exit(1)

     print ("Server successfully acquired the socket with port:", self.port)
     while True:
         self.socket.listen(3) # maximum number of queued connections

         conn, addr = self.socket.accept()
         # conn - socket to client
         # addr - clients address

         print("Got connection from:", addr)

         data = conn.recv(1024) #receive data from client
         string = bytes.decode(data) #decode it to string

         #determine request method  (HEAD and GET are supported)
         request_method = string.split(' ')[0]
         print ("Method: ", request_method)
         #print ("Request body: ", string)

         if (request_method == 'GET'):
             try:
				print 'Request:'+re.findall(ur'\?(.*) HTTP', string)[0]
				get_type = re.findall(ur'\?(.*) HTTP', string)[0]
             except IndexError:
				get_type = "no"
             if get_type in 'drones':
					response_headers = self._gen_headers( 200)
					response_content = str(drones).replace('\'',"\"")
             elif get_type in 'tasks':
				response_headers = self._gen_headers( 200)
				response_content = handler.GetTasks().replace('\'',"\"")
             elif len(get_type.split(',')) == 6:
				response_headers = self._gen_headers( 200)
				handler.AddTask(get_type.split(',')[0],get_type.split(',')[1],
								get_type.split(',')[2],get_type.split(',')[3],
								get_type.split(',')[4],get_type.split(',')[5])
				response_content = "Yay!"
             else:
					response_headers = self._gen_headers( 404)
					response_content = b"<html><body><p>"+str("no")+"</p><p>Python HTTP server</p></body></html>"
             server_response =  response_headers.encode() # return headers for GET and HEAD
             if (request_method == 'GET'):
                 server_response +=  response_content  # return additional conten for GET only

             conn.send(server_response)
             print ("Closing connection with client")
             conn.close()

         else:
             print("Unknown HTTP request method:", request_method)

class TaskHandler(Thread):
	
	def __init__(self):
		super(TaskHandler, self).__init__()
		self.daemon = True
		self.cancelled = False
		self.taskindex = 10
		self.tasks = {"tasks":[
            {
            "name":"First task",
            "lat":32.231153299999995,
            "lon":-110.9509174,
            "type":10,
			'description':'Asshole finder 7k',
            "number":0
            },
            {
            "name":"second task",
            "lat":31.231153299999995,
            "lon":-110.9509174,
            "type":10,
			'description':'Asshole finder 7k',
            "number":9
            },
            {
            "name":"Thurd task",
            "lat":30.231153299999995,
            "lon":-110.9509174,
            "type":10,
			'description':'Asshole finder 7k',
            "number":8
            }
        ]
		}


	def run(self):
		while True:
			time.sleep(10)
			for i, task in enumerate(self.tasks['tasks']):
				#Remove task if number is zero indacating it is a compleated task
				if task['number'] == 0:
					print str(task)
					del self.tasks['tasks'][i]
	def GetTasks(self):
		return str(self.tasks)
	def AddTask(self,Name,lat,lon,Type,Description,Number):
		if Number != 0:
			for i, task in enumerate(self.tasks['tasks']):
				if int(task['number']) == int(Number):
					del self.tasks['tasks'][i]
				if len(Name) < 2:
					return True
					
		self.taskindex += 1
		self.tasks['tasks'].append({"name":str(Name),"lat":lat,"lon":lon,"type":Type,"description":Description,"number":self.taskindex})
 

print ("Starting web server")
my_class = Server(port = 80)
my_class.start()
handler = TaskHandler()
handler.start()

while True:
	#print handler.GetTasks()
	time.sleep(1)