#The amazing centris 2.0
import requests
from getpass import getpass
from bs4 import BeautifulSoup
from prettytable import PrettyTable
from datetime import datetime
import argparse
import re
from pathlib import Path

#args = parser.parse_args()
#downl = args.downl_folder
#dest = args.dest_folder


#TODO:
#- api
#+list all courses your taking (centris2 currentcourses, allcourses) X
#+list all your assignments (due assignments) X
#+list all your assignments (finished assignments) X
#+get info about assignment ~
#+get your timetible X
#+submit solution ~
#+get lunch X
#only get assignment form one course
#student lists
#finished courses
#2f1

#COMMANDS:
#+timetable
# proj (default = allt)
#+ -d proj x
#+ -a proj x
#courses (current)
# -f courses
# -a courses
# -c courses

#- turtle shell fyrir CLI
def login(args):
	store_user()
	store_pass()
	
def store_pass():
	with open('supersecure', 'w') as f:
		f.write(getpass())

def password():
	return open('supersecure').read()

def username():
	return open('user').read()

def store_user():
	with open('user', 'w') as f:
		x = input("Username: ")
		f.write(x)

url = 'https://myschool.ru.is/myschool/' #the baseurl

def islogedin():
	try:
		username()
		password()
	except:
		print('Hey cutie! You must be logged in <3')
		login(None)

def getcourses():
	r = requests.get('https://myschool.ru.is/myschool', auth=(username(), password()))
	soup = BeautifulSoup(r.text, 'html.parser')

	courselink = ''
	for link in soup.find_all('a'):
		if link.text == 'Námskeið':
			courselink = url + link.get('href')

	r = requests.get(courselink, auth=(username(), password()))
	coursesoup = BeautifulSoup(r.text, 'html.parser')

	links = coursesoup.find_all('span', title = True)
	
	list = []
	for i in links:
		list.append(i['title'])
		
	return list

#My courses
def courses(args):
	islogedin()
	
	r = requests.get('https://myschool.ru.is/myschool', auth=(username(), password()))
	soup = BeautifulSoup(r.text, 'html.parser')

	courses = soup.find_all('center')
	tablecontent = courses[1]
	x = tablecontent.find('table')
	tableheader = x.find('th')
	y = PrettyTable()
	y.field_names = tableheader

	allcourses = getcourses()
	
	clean = []
	for i in allcourses:
		string = re.sub('\n', '', i)
		cleanstring = re.sub('\.[0-9]+', '', string)
		clean.append(re.sub('\r', ' ', cleanstring))

	list = []
	for i in clean:
		list.append(i)
		y.add_row(list)
		list = []

	print(y.get_string())

#timetable
def timetable(args):
	islogedin()

	r = requests.get('https://myschool.ru.is/myschool', auth=(username(), password()))
	soup = BeautifulSoup(r.text, 'html.parser')

	for link in soup.find_all('a'):
		if link.text == 'Stundatafla':
			timetable = url + link.get('href') #create url for Verkefni

	res = requests.get(timetable, auth=(username(), password())) 
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
def dueass():
	islogedin()

	r = requests.get('https://myschool.ru.is/myschool', auth=(username(), password()))
	soup = BeautifulSoup(r.text, 'html.parser')

	for link in soup.find_all('a'):
		if link.text == 'Verkefni':
			dueproject = url + link.get('href') #create url for Verkefni

	res = requests.get(dueproject, auth=(username(), password())) #new requests with the new url
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

#print pretty table for all assignments in one course
def ass(url):

	res = requests.get(url, auth=(username(), password()))
	projectsoup = BeautifulSoup(res.text, 'html.parser')

	ttables = projectsoup.find_all('center') 

	ttlist = []
	for i in ttables:
		ttlist.append(i.table)

	ttablelist = []
	for i in ttlist:
		ttablelist.append(i.find('table'))

	tableheader = ttablelist[0].find('tr')

	m = PrettyTable()

	header = tableheader.find_all('th')
	headerlist = []
	for i in header:
		headerlist.append(i.text)
	m.field_names = headerlist

	rows = []
	for i in ttablelist:
		rows += i.find_all('tr')

	for row in rows:
		if row.find('td'):
			list = row.find_all('td')
			data = []
			for i in list:
				data.append(i.text)
			while len(data) < 7:
				data.append('')
			m.add_row(data)


	title = projectsoup.find('span', {'class':'ruContent'})
	print()
	print(title.text)
	print(m.get_string())

def allcourselink():
	r = requests.get('https://myschool.ru.is/myschool', auth=(username(), password()))
	soup = BeautifulSoup(r.text, 'html.parser')

	courselink = ''
	for link in soup.find_all('a'):
		if link.text == 'Námskeið':
			courselink = url + link.get('href') #create url for Verkefni

	res = requests.get(courselink, auth=(username(), password()))
	projectsoup = BeautifulSoup(res.text, 'html.parser')

	proj = projectsoup.find('td', {'class': 'ruRight'})

	for link in projectsoup.find_all('a'):
		if link.text == 'Verkefni *':
			courselink = url + link.get('href')

	#test new link
	res = requests.get(courselink, auth=(username(), password()))
	projectsoup = BeautifulSoup(res.text, 'html.parser')

	newlinks = projectsoup.find('div', {'id': 'ruTabsNewcontainer'})
	tablist = newlinks.find_all('a')
	return tablist

def allassignments():
	tablist = allcourselink()

	#print all assignments
	for i in tablist:
		ass(url + i.get('href'))

def assignments(args):
	islogedin()
	if args.all:
		allassignments()
	elif args.due:
		dueass()
	elif args.course:
		course(args.course)
	else:
		dueass()


def logout(args):
	if Path('supersecure').exists():
		Path('supersecure').unlink()
	if Path('user').exists():
		Path('user').unlink()

def lunch(args):
	r = requests.get('https://myschool.ru.is/myschool', auth=(username(), password()))
	soup = BeautifulSoup(r.text, 'html.parser')

	for link in soup.find_all('a'):
		if link.text == 'MÁLIÐ':
			menulink = link.get('href') #create url for Verkefni

	res = requests.get(menulink)
	menusoup = BeautifulSoup(res.text, 'html.parser')

	x = menusoup.find_all('div',{'class': 'wpb_wrapper'})

	menuweek = []
	for i in menusoup.find_all('div',{'class': 'wpb_wrapper'}):
		if i.find('div',{'class': 'menu-text'}):
			data = []
			for k in i.find_all('div',{'class': 'menu-text'}):
				data.append(k)
			menuweek.append(data)

	if args.today:
		menutoday(menuweek)
	elif args.week:
		allweekmenu(menuweek)
	else:
		menutoday(menuweek)


def allweekmenu(menuweek):

	days = ['Mánudagur', 'Þriðjudagur', 'Miðvikudagur', 'Fimmtudagur', 'Föstudagur']

	count = 0
	print('-------------------------------------------------')
	for day in menuweek:
		print('{:^40}'.format('*** ' + days[count] + ' ***'))
		print()
		for i in day:
			print(i.find('div', {'class': 'menu-title'}).text)
			print('-> '+i.find('div', {'class': 'menu-desc'}).text)
			print()
		print('-------------------------------------------------')
		print()
		count += 1

def menutoday(menuweek):

	days = ['Mánudagur', 'Þriðjudagur', 'Miðvikudagur', 'Fimmtudagur', 'Föstudagur']
	x = datetime.today().weekday()

	if x == 6 or x == 7:
		print('No lunch today :-(')
	else:
		print('{:^40}'.format('*** ' + days[x] + ' ***'))
		print()
		for i in menuweek[x]:
			print(i.find('div', {'class': 'menu-title'}).text)
			print('-> '+i.find('div', {'class': 'menu-desc'}).text)
			print()

def course(string):
	courselist = getcourses()
	splitlist = []
	for i in courselist:
		splitlist.append(re.split('-|\.', i))

	courses = [i[2] for i in splitlist ]

	if string in courses:
		tablist = allcourselink()
		for i in tablist:
			if string in i.parent['title']:
				ass(url + i.get('href'))
	else:
		print('Please insert one of the following commands: ')
		for i in courses:
			print(i, end=', ')





#ARGSPARSERS

parser = argparse.ArgumentParser(
	description="Get stuff from myschool")

subparsers = parser.add_subparsers()

parser_timetable = subparsers.add_parser('timetable', help='shows your current timetable from myschool')
parser_timetable.set_defaults(func=timetable)

parser_courses = subparsers.add_parser('courses', help='shows your current courses')
parser_courses.set_defaults(func=courses)

parser_assignments = subparsers.add_parser('assignments', help='shows your upcoming assignment by default, add -a for all assignments, add -c "abbreviation for coursename"')
parser_assignments.add_argument('-a', '--all', action='store_true', help='shows all your assignments for this semester')
parser_assignments.add_argument('-d', '--due', action='store_true', help='shows your comming up assignments')
parser_assignments.add_argument('-c','--course', metavar='STRING', default ='', type=str, help='shows all your assignments for specified course: type -c "abbreviation for coursename"')

parser_assignments.set_defaults(func=assignments)

parser_timetable = subparsers.add_parser('logout', help='logout from your account')
parser_timetable.set_defaults(func=logout)

parser_timetable = subparsers.add_parser('login', help='login to your myschool acc')
parser_timetable.set_defaults(func=login)

parser_menu = subparsers.add_parser('lunch', help='shows the menu from the cafeteria in HR. shows the lunch today by default')
parser_menu.add_argument('-t', '--today', action='store_true', help='show the today\'s lunch at málið in HR')
parser_menu.add_argument('-w', '--week', action='store_true', help='show the lunch for the week at málið in HR')
parser_menu.set_defaults(func=lunch)

args = parser.parse_args()
args.func(args)


