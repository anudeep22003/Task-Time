Process

NL what the program does
- Allow me to create a activity
  - created_by
  - parent activity 
  - task/activity 
  - time set for this 
  - context
  - status - completed/running/not started
  - start_time
  - end_time
  - actual_time
  - overage_time
- I switch on a particular task, leading to the stopwatch starting 
  - when done, ring notification
  - allow me to continue if I need extra time
  - allow me to take break and start the break timer
- A stopwatch can create a break activity 
- User input thread:
  - start an activity that you have added or
  - start an unscheduled activity
  - see all in progress parents
  - see progress so far
  - add task for today  / tomorrow / some date 


- Stopwatch class --> that will be a single stopwatch object
- Activity - that will be required by stopwatch object to figure out timebound for the activity
- Activity creator (that creates an activity and adds to the database)
  - created by user 
  - created by stopwatch (breaks)
    - parent will be the master class 

Structure
- db_interface.py 
  - initialize db class
  - load and interface with db class 
- activity.py
  - activity creator class
    - create activity 
  - activity interfacer (interfae that allows activtiy creation)
    - optional input of parent activity 
- stopwatch.py
  - run stopwatch 
- User_interfacer.py
  - orchestrate the user's input
- session_manager.py
  - code to manage sessions
  - will have links to the objects like activity, stopwatch and so on
- main.py
  - thread the application 



Improvements:
- [x] Way to exit out of select id mode 
- [] add task while timer timing down 
- [x] Mark a task completed even if timer is running
- [x] Record the task as complete (instead of doing it automatically)
- [] Record the accurate time to the db (if i run multiple sessions, it should take that into account)
- [x] Mark as running not as completed
- [x] Edit task 
- [] give feedback on task selected that you are starting
- [] keep track of number of hours scheduled (so i dont overbook my day)
- [] have a graph always visible 
- [-] create context table and start capturing the task details there
    - the table is created but the context is not being captured. However the options are there.
- [] enable bulk edit of events
- [] build simple tkinter ui 1
- [] when event is done give user option to add a follow-up event that comes from the previous one. 