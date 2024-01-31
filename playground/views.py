from django.shortcuts import render
from project.models import Project, Task

from project.models import Session
from post.models import Vouch, Tag
import json

# Create your views here.
def play (request):
    return render(request, 'play.html', {'name': 'Mosh'})
