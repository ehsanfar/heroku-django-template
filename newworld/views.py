from django.shortcuts import render, HttpResponseRedirect, Http404
from django.http import HttpResponse



# from .models import Greeting

# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, 'index.html')


# def list(request):
#     # return HttpResponse('Hello from Python!')
#     return render(request, 'list.html')




	# context = {}
	# template = "list.html"
	# return render(request, template, context)