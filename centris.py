#The amazing centris 2.0
import requests
from getpass import getpass
from bs4 import BeautifulSoup
from prettytable import PrettyTable


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
#store_pass()

soup = BeautifulSoup(r.text, 'html.parser')

url = 'https://myschool.ru.is/myschool/' #the baseurl

for link in soup.find_all('a'):
    if link.text == 'Verkefni':
    	url += link.get('href') #create url for Verkefni

res = requests.get(url, auth=('thorhildurt15', password())) #new requests with the new url
projectsoup = BeautifulSoup(res.text, 'html.parser')
proj = projectsoup.find('div', {'class': 'ruContentPage'})

tables = proj.find_all('table')
nextassignments = tables[0]

tableheader = nextassignments.find_all('th')
tablerows=nextassignments.find_all('td')

x = PrettyTable() #create new pretty table method

field = []
for data in tableheader:
	field.append(data.text)
x.field_names = field

row = []
num = 0
for data in tablerows:
	row.append(data.text)
	if num == 4:
		x.add_row(row)
		row = []
		num = 0
	else:
		num += 1
	

print(x.get_string())



#TEST STUFF
#---------------
#print(children)
#print(children.text) ## next assignments
#children = proj.findChildren()
#for i in Children:
#	print(i)



#print(soup2.table)
#store_pass(
    	

#print(soup.get_text())

#print(type(r.text))
