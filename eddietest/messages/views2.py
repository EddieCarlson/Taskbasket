from operator import itemgetter

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext



from eddietest.messages.models import Message
#from eddietest.messages.models import Kind
from eddietest.messages.models import Task

def index(request):

    if request.method == 'POST':
        a = int(request.POST.get('which'))
	Task.objects.get(pk=a).delete()    
    	
    stasks = []
    ftasks = []
    tasks = Task.objects.all()
    for t in tasks:
	stasks.append(((t.caption), (t.priority), (t.pk)))
    sorted(stasks, key=itemgetter(1))	
    
    for t in stasks:
	ftasks.append(Task.objects.all().get(pk=t[2]))
    return render_to_response('index.html', {'tasks': ftasks, }, context_instance=RequestContext(request))

def add(request):
    error = None
    if request.method == 'POST':
	t = Task()
        t.caption = request.POST.get('Caption:')
	t.elaboration = request.POST.get('Full Description:')
	t.priority = int(request.POST.get('Priority(0 highest):'))
        
	t.save();
        
        if not t.caption or not t.elaboration or t.priority == '':
		error = 'Fill out all fields!'
            
    return render_to_response('add.html', {'error' : error}, context_instance=RequestContext(request))

def task(request, task_id):
    t = Task.objects.get(pk=int(task_id))
    return render_to_response('task.html', {'task' : t}, context_instance=RequestContext(request))
