from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from django.shortcuts import render

# Create your views here.
def index(request):
    now = datetime.now()

    return render(
        request,
        "Project3App2/index.html",
        {
            'title': "The internet",
            'message': "The internethmmmm",
            'content': " is: " + now.strftime("%A, %d, %B, %Y at %X")     
        }
        )
