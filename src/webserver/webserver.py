import json
import bottle
from database import dbHandler
from scraper import spiderworker
from coursegraph import build_graph
from bottle import request
from coursegraph.userpreferences import UserPrefs

setup = False
dbHandler.init(setup)
scraperWorker = spiderworker.SpiderWorker()
if setup:
	scraperWorker.start()


def selectedCourses():
	semester = request.forms.get("semester")
	mandatory_subjects = request.forms.get("mandatory_subjects")
	mandatory_available_courses = request.forms.get("mandatory_available_courses")
	elective_subjects = request.forms.get("elective_subjects")
	elective_available_courses = request.forms.get("elective_available_courses")
	campus_pref = request.forms.get("campus_pref")
	morning_class_pref = request.forms.get("morning_class_pref")
	afternoon_class_pref = request.forms.get("afternoon_class_pref")
	evening_class_pref = request.forms.get("evening_class_pref")
	yes_day_off = request.forms.get("yes_day_off")
	no_day_off = request.forms.get("no_day_off")
	monday_off = request.forms.get("monday_off")
	tuesday_off = request.forms.get("tuesday_off")
	wednesday_off = request.forms.get("wednesday_off")
	thursday_off = request.forms.get("thursday_off")
	friday_off = request.forms.get("friday_off")
	no_instruct_method_pref = request.forms.get("no_instruct_method_pref")
	in_class_delivery_pref = request.forms.get("in_class_delivery_pref")
	online_delivery_pref = request.forms.get("online_delivery_pref")
	CRN1 = request.forms.get("CRN1")
	CRN2 = request.forms.get("CRN2")
	CRN3 = request.forms.get("CRN3")
	CRN4 = request.forms.get("CRN4")
	CRN5 = request.forms.get("CRN5")

	UserPrefs.semester = semester
	
	if yes_day_off == 'on':
		UserPrefs.MaximizeDaysOff = True
	elif no_day_off == 'on':
		UserPrefs.MaximizeDaysOff = False
	
	if monday_off == 'on':
		UserPrefs.PreferredDaysOff.append(1,6)

	if tuesday_off == 'on':
		UserPrefs.PreferredDaysOff.append(2,7)

	if wednesday_off == 'on':
		UserPrefs.PreferredDaysOff.append(3,8)

	if thursday_off == 'on':
		UserPrefs.PreferredDaysOff.append(4,9)

	if friday_off == 'on':
		UserPrefs.PreferredDaysOff.append(5,10)


@bottle.route('/')
def index():
    return bottle.static_file('input.html', root='static/')

@bottle.route('/stylesheet.css')
def style():
	return bottle.static_file('stylesheet.css', root='static/')

@bottle.route('/input.js')
def input():
    return bottle.static_file('input.js', root='static/')

@bottle.route('/input_form', method="POST")
def getCalendar():
	#Now begin the process of querying the db
	semester = request.forms.get("semester")
	mandatory_selected_courses = request.forms.getall("mandatory_selected_courses")
	elective_selected_courses = request.forms.getall("elective_selected_courses")
	selectedCourses()

	inputdict = {
		'SEMESTER': semester,
		'MCOURSES' : mandatory_selected_courses,
		'ECOURSES' : elective_selected_courses
	}

	courses, ecourses = dbHandler.grabCourses(inputdict)
	w1, w2 = build_graph.graph_optimize(courses+ecourses)
	templ = open('public_html/cal.tmpl','r').read()
	
	return bottle.template(templ, w1=w1, w2=w2)

@bottle.route('/getAvailableCourses')
def getAvailCourses():
	return json.dumps(dbHandler.getAvailableCourses())

bottle.run(host='', port=8080)
if setup:
	scraperWorker.end()
	scraperWorker.join()