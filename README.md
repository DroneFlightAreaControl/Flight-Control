# DroneFlightAreaControl
A multilayered drone and airspace managment system. 

## Top Layer:
Web interface for visulasing drone locations and tasks, along with task managment
Goals for compleation:
* Show current location of drones with interpolation of position (based on speed and heading)
* Show current tasks in a list, as well as in a map view
* Issue new tasks by clicking on the map and selecting a task type

## Managment layer
Middle layer arbatrating between the web interface and the drones handles tasks as well as task assigment
Goals for compleation:
* have a task list of arbatary tasks with there metadata
* Handle task asigment to drones in an effective manor 
* Monitior and assign tasks to drones based on current status (distance battery life ect...)

## Drone managment daymon 
Middle layer is spun up for every drone and handles Managment layer to drone layer one task at a time
* Handle comunacation from the Managment layer
* Holds data about the drone including state position battery status ect...
* Handles single tasks for drones

## Optional area denyance  module
* connects to common drones over wifi and 3dr modules
* Commands them to land and turn off or other area denyal tenqueks
* Protcting an area from others
