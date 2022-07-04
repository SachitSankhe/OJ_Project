from multiprocessing import context
from django.urls import reverse
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect

from .models import Problem
from .models import Solution

from .forms import FileSubmission
from django.utils import timezone
#Create your views here.


def index(request):
    context = {
        'Problem_List' : Problem.objects.order_by('-problem_level')[:5]
    }
    return render(request,'OJ/index.html',context)

def details(request,problem_id):
    problem = get_object_or_404(Problem,pk=problem_id)
    return render(request,'OJ/problem_details.html',{'problem': problem })


def submission(request,problem_id):
    if request.method == 'POST':
        form_1 = FileSubmission(request.POST,request.FILES)
        if form_1.is_valid:
            file = request.FILES.get('problem_code')
            with open(f'OJ/codeFiles/sample.cpp', 'wb+') as destination:  
                for chunk in file.chunks():  
                    destination.write(chunk)  
            sol = Solution()
            sol.problem_id = Problem.objects.get(pk=problem_id)
            sol.problem_code = 'OJ/codeFiles/sample.cpp'
            sol.submitted_at = timezone.now()
            sol.Verdict = "AC"
            sol.save()
            return HttpResponseRedirect(reverse('oj:leaderboard'))
        else:
            form_2 = FileSubmission()
            return HttpResponseRedirect('OJ/problem_details.html')
    else:
        return HttpResponse("Not Saved")

def leaderboard(request):
    context = {
        'sol' : Solution.objects.all().order_by('-submitted_at')[:10],
    }
    return render(request,'OJ/finalpage.html',context)

