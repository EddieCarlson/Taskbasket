import os
import sys
sys.path.append('/home/ubuntu/ToDoRepo')
sys.path.append('/home/ubuntu/ToDoRepo/lib')
sys.path.append('/home/ubuntu/ToDoRepo/eddietest')
os.environ["DJANGO_SETTINGS_MODULE"] = "eddietest.settings"
from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()
