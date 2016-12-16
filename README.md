# Centris 2.0 
##API and a command line interface for MySchool
Command line interface for myschool.ru.is. Instead of going to www.myschool.ru.is you can get various info from your myschool account by only using the command line on your local computer.

##Features
+ Get your timetable for the current week
+ View all your courses that you are enrolled in
+ View upcoming assignments and deadline
+ View all assignments for the semester with grade
+ View specific assignments by course
+ View the lunch today at Málið 
+ View the menu for all week at Málið
+ login 
+ logout

##How to run
+ Make sure that Python3 is installed
+ Install the PyPI packages listed in requirements.txt
+ Unzip the project to your favorite directory
+ Then run some commands in the command line window on your local computer (see below)

##Commands
To get all available commands for the API run:
``` python3 centris.py -h ```

###list of commands
+ timetable
+ courses
+ assignments [-a] [-d] [-c 'specific course string' ]
+ logout
+ login
+ lunch [-t] [-w]

##Examples
### Use Python3 for mac/linux and use py for windows
+ Get your timetable:
``` python3 centris.py timetable ```
+ Check out what is for lunch today:
``` python3 centris.py lunch -d ```
+ Check all assignments and grades in the course PRLA (Python):
``` python3 centris.py assignments -c PRLA ```
