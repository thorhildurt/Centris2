#The amazing centris 2.0
import requests
from getpass import getpass
from bs4 import BeautifulSoup


#TODO:
#- api
#+list all courses your taking (centris2 currentcourses, allcourses)
#+list all your assignments (due assignments, all assignents)
#+get info about assignment
#+get your timetible
#+submit solution

#- turtle shell fyrir CLI



def store_pass():
	with open('supersecure', 'w') as f:
		f.write(getpass())

def password():
	return open('supersecure').read()

r = requests.get('https://myschool.ru.is/myschool', auth=('thorhildurt15', password()))
#print(r.content.decode('utf-8'))
soup = BeautifulSoup(r.text, 'html.parser')
list = soup.find_all('table')
for i in list:
	print(i)
title = soup.find('title').string
print(title)
#print(type(r.text))
#store_pass()
