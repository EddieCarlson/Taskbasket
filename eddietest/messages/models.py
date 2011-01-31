from django.db import models
from datetime import datetime


class Message(models.Model):
    message = models.CharField(max_length=200)
    
    def __unicode__(self):
        return self.message 



class Kind(models.Model):
    name = models.CharField(max_length=50)
    dateMade = models.DateTimeField(auto_now_add=True)
      
    def __unicode__(self):
		return self.name



class Task(models.Model):
    dateMade = models.DateTimeField(auto_now_add=True)
    dateLastChanged = models.DateTimeField(auto_now=True)
    dateDue = models.DateTimeField()
    priority = models.IntegerField()
    caption = models.CharField(max_length=50)
    elaboration = models.CharField(max_length=5000)
    kind = models.CharField(max_length=20)
	#kind = models.ForeignKey(Kind)
    
    def __unicode__(self):
		return self.caption

       
class User(models.Model):
	name = models.CharField(max_length=30)
	tasks = models.ManyToManyField(Task, blank=True, null=True)
	code = models.CharField(max_length=10)
  	defaultKinds = models.ManyToManyField(Kind, blank=True, null=True) 

	def __unicode__(self):
		return self.name
