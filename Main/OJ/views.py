from django.shortcuts import render
from django.http import HttpResponse

from .models import Problems
#Create your views here.

def index(request):
    context = {
        'Problem_List' : Problems.objects.order_by('-problem_level')[:5]
    }
    return render(request,'OJ\index.html',context)