from operator import itemgetter

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from datetime import datetime, timedelta
import random

from eddietest.messages.models import Message
from eddietest.messages.models import Task
from eddietest.messages.models import Kind
from eddietest.messages.models import User

def defaults(): #creates the default user, all users' defaultKinds start as his
	defu = User()
	defu.name = 'RED UNICORN'
	defu.code = 'REDUNICORN'
	defu.save()
	defaultKinds = ['School', 'Work', 'Household', 'Social']
	for k in defaultKinds:
		newKind = Kind()
		newKind.name = k
		newKind.save()
		defu.defaultKinds.add(newKind)
	defu.save()
	return None

def root(request):
	if('REDUNICORN' not in [u.code for u in User.objects.all()]): #if default user doesn't exist
		defaults()

	if request.method == 'GET': 
		return render_to_response('root.html', context_instance=RequestContext(request))
	
	if request.method == 'POST':
		u = User()
		u.save()
		u.name = request.POST.get('name')		
		run = True
		while run:
			newCode = ''
			for i in range(10):
				newCode += str(random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789$-_.+!*'))
			run = newCode in [user.code for user in User.objects.all()] #must generate a unique code before exiting
		u.code = newCode 
		u.defaultKinds = User.objects.get(code='REDUNICORN').defaultKinds.all()
		u.save()
		return HttpResponseRedirect('user/'+u.code)

def index(request, userID):
	return dispTasks(request, userID, None, True)

def dispTasks(request, userID, kindType, dispAll):
	user = User.objects.get(code=userID)
	a = None
	if request.method == 'POST':
		a = request.POST.get('which')
    	if a != None:
			Task.objects.get(pk=a).delete()
	defKinds = [k.name for k in user.defaultKinds.all()]
	tempKinds = set([t.kind for t in user.tasks.all()]).difference(set(defKinds))
	tasks = user.tasks.all();
	if kindType:
		tasks = user.tasks.filter(kind=kindType)
	stasks = [Task.objects.get(pk=T[2]) for T in sorted([(t.dateDue, t.priority, t.pk) for t in tasks], key=itemgetter(0,1))]	
	return render_to_response('index2.html', {'tasks': stasks, 'defKinds': defKinds , 'tempKinds': tempKinds, 'user' : user}, context_instance=RequestContext(request))

def add(request, userID):
	user = User.objects.get(code=userID)
	error = None
	
	if request.method == 'POST':
		t = Task()
		t.caption = request.POST.get('Caption:')
		t.elaboration = request.POST.get('notes')
		t.priority = int(request.POST.get('priority'))
		if request.POST.get('radio2') == '1':
			t.dateDue = datetime(datetime.now().year, datetime.now().month, datetime.now().day, 23, 59, 59, 0)
		else:
			month = int(request.POST.get('month'))
			day = int(request.POST.get('day'))
			time = request.POST.get('time').split(':')
			#t.dateDue = datetime(datetime.now.year 
			t.dateDue = datetime(datetime.now().year, int(request.POST.get('month')), int(request.POST.get('day')), int(request.POST.get('time').split(':')[0]), int(request.POST.get('time').split(':')[1]), 0, 0)
			if t.dateDue - datetime.now() < timedelta(0):
				t.dateDue = datetime(t.dateDue + timedelta(1))
			
		kindtype = request.POST.get('oldkind')
		if kindtype != '0':
			t.kind = kindtype;
			#t.kind = Kind.objects.get(pk=kindtype).name
		else:
			t.kind = request.POST.get('New kind:')		

		t.save()
		user.tasks.add(t)
		user.save() 
        
		if not t.caption or not t.dateDue or not  t.priority:
			error = 'Fill out all fields!'
        
	months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
	times = []
	monthlist = range(1,13)
	days = range(1,32)
	kinds = set([t.kind for t in user.tasks.all()])
	for i in range(24):
		times.append(str(i)+':00')
		times.append(str(i)+':30')
	defaultKinds = [k for k in user.defaultKinds.all()]
	return render_to_response('add3.html', {'error' : error, 'months' : months, 'monthlist' : monthlist, 'days' : days, 'times' : times, 'kinds' : kinds, 'defaultKinds': defaultKinds, 'userID' : userID}, context_instance=RequestContext(request))
	
def task(request, userID, taskID):
	user = User.objects.get(code=userID)
	task = Task.objects.get(pk=taskID)
	kinds = [t.kind for t in user.tasks.all()]
	return render_to_response('task.html', {'task' : task, 'kinds' : kinds, 'time' : t.dateDue - datetime.now(), 'userID' : user.code}, context_instance=RequestContext(request))

def kind(request):
    k = Kind()
    k.name = request.POST.get('kind')
    k.save()

