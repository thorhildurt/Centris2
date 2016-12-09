#The amazing centris 2.0
import requests
from getpass import getpass
from bs4 import BeautifulSoup
from prettytable import PrettyTable
from datetime import datetime


#TODO:
#- api
#+list all courses your taking (centris2 currentcourses, allcourses) X
#+list all your assignments (due assignments) X
#+list all your assignments (finished assignments)
#+get info about assignment
#+get your timetible X
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

#My courses

courses = soup.find_all('center')
tablecontent = courses[1]
x = tablecontent.find('table')
tableheader = x.find('th')
rows = x.find_all('tr')
y = PrettyTable()
y.field_names = tableheader

print(type(rows))
courselist = []
for i in rows:
	if i.find('td'):
		courselist.append(i.find('td')['title'])

list = []
for data in courselist[:-1]:
	list.append(data)
	y.add_row(list)
	list = []

print(y.get_string())

#timetable

for link in soup.find_all('a'):
    if link.text == 'Stundatafla':
    	timetable = url + link.get('href') #create url for Verkefni


res = requests.get(timetable, auth=('thorhildurt15', password())) 
timetablesoup = BeautifulSoup(res.text, 'html.parser')
timetable = timetablesoup.find('div', {'class': 'ruContentPage'})

rows = timetable.find_all('tr')
allrows = []
for i in rows:
	allrows.append(i)

cleanrows = allrows[1:]

m = PrettyTable()
tableheader = cleanrows[0].find_all('th')
tabledate = cleanrows[1].find_all('th')

field = []
count = 0
for data in tableheader:
	field.append(data.text[0:3] + ' - ' + tabledate[count].text)
	count = count + 1
m.field_names = field

for row in cleanrows[2:-3]:

	list = row.find_all('td')
	data = []
	for i in list:
		data.append(i.text.strip('\n'))
	m.add_row(data)

print(m.get_string())


#Due assignments

for link in soup.find_all('a'):
    if link.text == 'Verkefni':
    	dueproject = url + link.get('href') #create url for Verkefni

res = requests.get(dueproject, auth=('thorhildurt15', password())) #new requests with the new url
projectsoup = BeautifulSoup(res.text, 'html.parser')
proj = projectsoup.find('div', {'class': 'ruContentPage'})

tables = proj.find_all('table')

def printtable(html, n):
	tableheader = html.find_all('th')
	tablerows=html.find_all('td')

	x = PrettyTable() #create new pretty table method

	field = []
	for data in tableheader:
		field.append(data.text)
	x.field_names = field

	row = []
	num = 0
	for data in tablerows:
		row.append(data.text)
		if num == n:
			x.add_row(row)
			row = []
			num = 0
		else:
			num += 1
		
	print(x.get_string())

printtable(tables[0], 4)

y = PrettyTable()

tableheader = tables[1].find_all('th')
rows = tables[1].find_all('tr')

#field = []
#for i in tableheader:
#	field.append(i.text)
#print(field)

#header = ''
#list = []
#tempcolumn = ''
#count = 0
#for j in rows:
#	if j.find('th'):
#		if count >= 1:
#			y.add_column(tempcolumn, list)
#		tempcolumn = j.text
#		list = []
#		count += 1
#	if not j.find('th'):
#		list.append(j.find('td'))

#y.add_column(tempcolumn, list)

#t = PrettyTable() #create new pretty table method

#for i in rows:
#	if i.find('th'):
#		print(i.text)
		#t.field_names = i.text
	#else:
	#	t.add_row(i.text)




#x.field_names = field	
#x.add_row(row)


#print(t.get_string())
	
#for i in rows:

#	j = i.find('td')
#	if j:
#		print(j.text)








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
