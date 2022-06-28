# Tasks


## Working on in the most recent round
- [x] Entering a number at the start breaks the app, catch that exception
- [x] the daughter's copied note starts off on the same line. Also too many newlines. Start from new line for new notes.
- [x] The completed list time still shows up as a float, change to an int.
- [x] User should only be able to add notes, the notes of a parent become the context of the child. And so on.


## Bugs
- [] Notes being copied to context are not adding to the entire history (see 27/06/22 for eg)
- [x] Asking for extra time and restarting again does not remember the amount of time passed in the previous iteration.
- [x] duplicating is not making a replica, rather it is moving the same event to the next day
- [x] Add ability to explore task, just do a task and add details later

## Simple features
- [] capture last edit time, so if I spend time taking notes or something, the time is accounted for.
- [] Add ability to distribute an event over many days. Eg do twitter writeup 30 mins/day 3 times over 5 days.
- [] Show in the view how many lines of context and/or notes the activity has
- [] Capture streak of the activity
- [] When I add a task, show me number of hours accounted for in the day
- [] Dual thread so that timer stays running and I can take notes
- [] Keep track of number of hours scheduled (so i dont overbook my day)
- [] Rechedule takes current day into account. This becomes confusing. Do reschedule based on the date in the db
- [] Subtask timers i.e show the current subtask and add a timer for that
- [] show how long activity has been paused (used explore track to keep track of that)
- [] Add grouping for tasks so you can drill into a category and finish those first (eg: big tasks, small tasks, break tasks. revenue tasks, etc)

## UI improvements
- [] Show date when you have begun your day since now you can start a previous day
- 

## Complex features
- [] Capture sub tasks while doing main task (start timer for them)
- [] Perform a search inline to bring up the relevant activity, so I can create a daughter of it. Eg: needed to create daughter to check with Naresh next weekend. However I had to find the task tomorrow to do that. Inline search would be helpful.
- [] build simple tkinter ui 1
- [] Use SQL Alchemy --> https://auth0.com/blog/sqlalchemy-orm-tutorial-for-python-developers/
- [] have a graph always visible (analytics graph of your performance)
- [] add task while timer timing down 
- [] Can you start a cursor always from a \t position? SO multiline notes don't look ugly.
- [] Use escape sequences to have a clear screen (specifically escape sequence to clear lines)

## Completed:
- [x] Way to exit out of select id mode 
- [x] Mark a task completed even if timer is running
- [x] Record the task as complete (instead of doing it automatically)
- [x] Record the accurate time to the db (if i run multiple sessions, it should take that into account)
- [x] Mark as running not as completed
- [x] Edit task 
- [x] allow me to duplicate a task to tomorrow
- [x] allow deletion of tasks
- [x] when event is done give user option to add a follow-up event that comes from the previous one. 
- [x] give feedback on task selected that you are starting
- [x] create context table and start capturing the task details there
- [x] enable bulk edit of events
  - [x] Enabled bulk reschedule of events by typing bulk
- [x] When I control break to exit out of a timer, give me my options there - start new task, add related task, mark completed, and so on
- [x] Rough waters, smooth sailing from here on - the peak of anxiety before flow