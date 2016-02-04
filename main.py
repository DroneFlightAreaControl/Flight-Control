#!/usr/bin/python

import socket  # Networking support
import signal  # Signal support (server shutdown on signal receive)
import time    # Current time
import re
from geopy.distance import vincenty
from threading import Thread



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
					response_content = str(droneWrangler.GetDrones()).replace('\'',"\"")
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
            "name":"Up North",
            "lat":32.23241348,
            "lon":-110.95213205,
            "type":10,
			 "description":'Asshole finder 7k',
            "number":13
            },
			{
            "name":"East",
            "lat":32.23194156,
            "lon":-110.94964296,
            "type":10,
			 "description":'Asshole finder 7k',
            "number":12
            },
			{
            "name":"east mall",
            "lat":32.23070729,
            "lon":-110.94895631,
            "type":10,
			 "description":'Asshole finder 7k',
            "number":11
            },
            {
            "name":"First task",
            "lat":32.23191077,
            "lon":-110.95214788,
            "type":10,
			 "description":'Asshole finder 7k',
            "number":10
            },
            {
            "name":"second task",
            "lat":32.23187868,
            "lon":-110.95184747,
            "type":10,
			 "description":'Asshole finder 7k',
            "number":9
            }
        ]
		}


	def run(self):
		while True:
			for i, task in enumerate(self.tasks['tasks']):
				#Remove task if number is zero indacating it is a compleated task
				if task['number'] == 0:
					print str(task)
					del self.tasks['tasks'][i]
	def GetTasks(self):
		return str(self.tasks)
	def NumTasks(self):
		return len(tasks['tasks'])
	def AddTask(self,Name,lat,lon,Type,Description,Number):
		#add task if number is not zero it is an edit
		if Number != 0:
			for i, task in enumerate(self.tasks['tasks']):
				if int(task['number']) == int(Number):
					del self.tasks['tasks'][i]
				#if len name is less than 2 then it is a removal so we skip the addition of the task
				if len(Name) < 2:
					return True
		self.taskindex += 1
		self.tasks['tasks'].append({"name":str(Name),"lat":lat,"lon":lon,"type":Type,"description":Description,"number":self.taskindex})
	def GetTask(self,lat,lon):
		dist = [0,-1]
		#Returns the closest task to a position
		for task in self.tasks['tasks']:
				assigned_tasks = droneWrangler.GetAssignedTasks()
				assigned_tasks.append(0)
				valid = True
				#checking if it is already assigned
				for x in assigned_tasks:
					if task['number'] == x:
						valid = False
				if (valid) and ((dist[0] == 0) or (vincenty((task['lat'],task['lon']), (lat,lon)).meters < dist[1])):
					dist = [task['number'],vincenty((task['lat'],task['lon']), (lat,lon)).meters]
		return dist[0]
	def FinishTask(self,num):
		for i, task in enumerate(self.tasks['tasks']):
			if int(task['number']) == num:
				task['number'] = 0
				del self.tasks['tasks'][i]
	def GetTaskByNum(self,num):
		for task in self.tasks['tasks']:
			if int(task['number']) == int(num):
				return task
		return None
		
class DroneDaymon(Thread):
	from dronekit import connect, VehicleMode, LocationGlobal, LocationGlobalRelative
	from pymavlink import mavutil # Needed for command message definitions
	import time
	import math
	def __init__(self, name, port=14550):
		from dronekit import connect, VehicleMode, LocationGlobal, LocationGlobalRelative
		super(DroneDaymon, self).__init__()
		self.daemon = True
		self.cancelled = False
		from dronekit import connect
		self.name = name
		self.mission = 0
		self.home = LocationGlobalRelative(32.23190435,-110.95272724, 30)
		#self.data = mavutil.mavlink_connection('udpin:0.0.0.0:'+str(port), planner_format=False,
        #                          notimestamps=True,
        #                          robust_parsing=True)
		self.vehicle = connect("0.0.0.0:"+str(port), wait_ready=True)
	
	def get_distance_metres(self, aLocation1, aLocation2):
		"""
		Returns the ground distance in metres between two LocationGlobal objects.
		This method is an approximation, and will not be accurate over large distances and close to the 
		earth's poles. It comes from the ArduPilot test code: 
		https://github.com/diydrones/ardupilot/blob/master/Tools/autotest/common.py
		"""
		import math
		dlat = aLocation2.lat - aLocation1.lat
		dlong = aLocation2.lon - aLocation1.lon
		return math.sqrt((dlat*dlat) + (dlong*dlong)) * 1.113195e5
	
	def arm_and_takeoff(self, aTargetAltitude):
		"""
		Arms vehicle and fly to aTargetAltitude.
		"""
		from dronekit import VehicleMode
		print "Basic pre-arm checks"
		# Don't let the user try to arm until autopilot is ready
		while not self.vehicle.is_armable:
			print " Waiting for vehicle to initialise..."
			time.sleep(1)
	
			
		print "Arming motors"
		# Copter should arm in GUIDED mode
		self.vehicle.mode    = VehicleMode("GUIDED")
		self.vehicle.armed   = True    
	
		while not self.vehicle.armed:      
			print " Waiting for arming..."
			time.sleep(1)
	
		print "Taking off!"
		self.vehicle.simple_takeoff(aTargetAltitude) # Take off to target altitude
	
		# Wait until the vehicle reaches a safe height before processing the goto (otherwise the command 
		#  after Vehicle.simple_takeoff will execute immediately).
		while True:
			print " Altitude: ", self.vehicle.location.global_relative_frame.alt      
			if self.vehicle.location.global_relative_frame.alt>=aTargetAltitude*0.95: #Trigger just below target alt.
				print "Reached target altitude"
				break
			time.sleep(1)
	
	def get_mission(self):
		if handler.GetTask(self.vehicle.location.global_frame.lat,self.vehicle.location.global_frame.lon) == 0:
			#no tasks go home
			print self.name+" Has no tasks going home"
			self.vehicle.simple_goto(self.home)
			while True:
				targetLocation = self.home
				remainingDistance=self.get_distance_metres(self.vehicle.location.global_relative_frame, targetLocation)
				droneWrangler.Update(self.name,lat=self.vehicle.location.global_frame.lat,lon=self.vehicle.location.global_frame.lon)
				print "Distance to target: ", remainingDistance
				time.sleep(1)
				if remainingDistance<=4: #Just below target, in case of undershoot.
					print "Reached target"
					break
			while handler.GetTask(self.vehicle.location.global_frame.lat,self.vehicle.location.global_frame.lon) == 0:
				print "waiting for mission"
				droneWrangler.Update(self.name,lat=self.vehicle.location.global_frame.lat,lon=self.vehicle.location.global_frame.lon)
				pass #wait until there is a mission to do
			self.arm_and_takeoff(30)
			self.mission =handler.GetTask(self.vehicle.location.global_frame.lat,self.vehicle.location.global_frame.lon)
				
	
	def run(self):
		time.sleep(5)
		from dronekit import LocationGlobal, LocationGlobalRelative
		while True:
			time.sleep(1)
			print "getting misssion"
			if self.mission == 0:
				self.get_mission()
			self.mission = int(handler.GetTask(self.vehicle.location.global_frame.lat,self.vehicle.location.global_frame.lon))
			print "Assigned Task "+str(handler.GetTaskByNum(self.mission))
			targetLocation = LocationGlobalRelative(float(handler.GetTaskByNum(self.mission)['lat']), float(handler.GetTaskByNum(self.mission)['lon']), 30)
			self.arm_and_takeoff(30)
			self.vehicle.simple_goto(targetLocation)
			while True:
				self.remainingDistance=self.get_distance_metres(self.vehicle.location.global_relative_frame, targetLocation)
				droneWrangler.Update(self.name,lat=self.vehicle.location.global_frame.lat,lon=self.vehicle.location.global_frame.lon)
				print "Distance to target: ", self.remainingDistance
				if self.remainingDistance<=4: #Just below target, in case of undershoot.
					print "Reached target"
					break
				time.sleep(1)
			handler.FinishTask(self.mission)
			self.mission = 0
		
		
	
class DroneHandler(Thread):
	
	def __init__(self):
		super(DroneHandler, self).__init__()
		self.daemon = True
		self.cancelled = False
		drone1 = DroneDaymon('First name',port=14570)
		drone2 = DroneDaymon('second name',port=14550)
		drone1.start()
		drone2.start()
		self.drones = {"drones":[
					{
					"name":"First name",
					"lat":32.231153299999995,
					"lon":-110.9509174,
					"batt":10,
					"taskName":"Asshole finder 9k",
					"taskNumber":0,
					},
					{
					"name":"Second name",
					"lat":32.231153299999995,
					"lon":-110.9509174,
					"batt":50,
					"taskName":"Asshole finder 8k",
					"taskNumber":0,
					}
				]
			}
	
	def run(self):
		pass #no-op
		
	def GetAssignedTasks(self):
		tasks = []
		for drone in self.drones['drones']:
			if drone['taskNumber'] != 0:
				tasks.append(drone['taskNumber'])
		return tasks
	def Update(self, name, lat, lon):
		for i, drone in enumerate(self.drones['drones']):
			if drone['name'] == name:
				drone['lat'] = lat
				drone['lon'] = lon
	def GetDrones(self):
		return str(self.drones)
 

print ("Starting web server")
my_class = Server(port = 80)
droneWrangler = DroneHandler()
handler = TaskHandler()
handler.start()
droneWrangler.start()
my_class.start()

while True:
	#print handler.GetTask(29.3,-111)
	time.sleep(1)