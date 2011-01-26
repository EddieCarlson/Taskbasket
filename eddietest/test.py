
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext


from operator import itemgetter

from messages.models import Message
#from eddietest.messages.models import Kind
from messages.models import Task

stasks = []
ftasks = []
tasks = Task.objects.all()
for t in tasks:
    stasks.append(((t.caption), (t.priority), (t.pk)))
sorted(stasks, key=itemgetter(1))	

for t in stasks:
    ftasks.append(Task.objects.all().get(pk=t[2]))

for t in ftasks:
    t
