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
		a = request.POST.get('todelete')
    	if a != None:
			Task.objects.get(pk=int(a)).delete()
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
	
	times = []
	kinds = set([t.kind for t in user.tasks.all()])
	for i in range(24):
		times.append(str(i)+':00')
		times.append(str(i)+':30')
	defaultKinds = [k for k in user.defaultKinds.all()]

	if request.method == 'POST':
		t = Task()
		t.caption = request.POST.get('Caption:')
		t.elaboration = request.POST.get('notes')
		t.priority = int(request.POST.get('priority'))
		time = request.POST.get('time')
		
	
		if(time):
			hourmin = time.split(':')
			time = [int(hourmin[0]), int(hourmin[1]), 0, 0]
		else:
			time = [23,59,59,0] #if no time specified, assume end of day(23:59)
		moretime = timedelta(0);
		if(request.POST.get('usecal')=="0"):
			year = datetime.now().year
			month = datetime.now().month
			day = datetime.now().day
			ezdate = int(request.POST.get('radio2'))-1
			if(ezdate==0 or ezdate==1):
				moretime = timedelta(ezdate)
			if(ezdate==2):
				moretime = timedelta((4-datetime.today().weekday())%7) #day difference to friday
			#else if(ezdate==4):
			#	t.isGoal = true
		else:
			caldate = request.POST.get('caldate').split('/')
			month = int(caldate[0])
			day = int(caldate[1])
			year = int(caldate[2])
		t.dateDue = datetime(year, month, day, time[0], time[1], time[2], time[3]) + moretime
			

			
		kindtype = request.POST.get('oldkind')
		if kindtype != '0':
			t.kind = kindtype;
			#t.kind = Kind.objects.get(pk=kindtype).name
		else:
			t.kind = request.POST.get('newkind')		
		
		if(not t.kind or not t.caption):
			return render_to_response('add3.html', {'error' : "fill out all fields!", 'times' : times, 'kinds' : kinds, 'defaultKinds': defaultKinds, 'userID': userID}, context_instance=RequestContext(request))		
		else: 
			t.save()
			user.tasks.add(t)
			user.save() 
			dispTasks(request,userID,None,True)

        
	return render_to_response('add3.html', {'error' : error, 'times' : times, 'kinds' : kinds, 'defaultKinds': defaultKinds, 'userID' : userID}, context_instance=RequestContext(request))
	
def task(request, userID, taskID):
	user = User.objects.get(code=userID)
	task = Task.objects.get(pk=taskID)
	kinds = [t.kind for t in user.tasks.all()]
	return render_to_response('task.html', {'task' : task, 'kinds' : kinds, 'time' : t.dateDue - datetime.now(), 'userID' : user.code}, context_instance=RequestContext(request))

def kind(request):
    k = Kind()
    k.name = request.POST.get('kind')
    k.save()

