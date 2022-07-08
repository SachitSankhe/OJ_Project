from django.contrib import messages
import subprocess
from django.urls import reverse
from django.shortcuts import get_object_or_404, render
from django.http import  HttpResponseRedirect

from .models import Problem
from .models import Solution

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
        file = request.FILES.get('problem_code')
        if file!=None:
            filename = file.name
            if filename.endswith('.cpp'):
                with open(f'OJ/codeFiles/sample.cpp', 'wb+') as destination:  
                    for chunk in file.chunks():  
                        destination.write(chunk)  

                compile_com = "g++ OJ\codeFiles\sample.cpp -o OJ\codeFiles\output.exe"
                run_com = "OJ\codeFiles\output.exe"
                try:
                    subprocess.run(compile_com,shell=True,check=True,timeout=5)
                    try:
                        with open("OJ\codeFiles\input.txt","r") as i:
                            op = subprocess.run(run_com,stdin=i,capture_output=True,check=True,timeout=1,text=True)
                    
                        out = 'OJ\codeFiles\sample_output.txt'
                        with open(out) as f:
                            sample_out = f.read()

                        if(op.stdout==sample_out):
                            verdict = 'AC'
                        else:
                            verdict='WA'
                        
                    except subprocess.TimeoutExpired:
                        verdict = "Timeout (TLE)"
                    

                except subprocess.CalledProcessError as e:
                    if e.returncode!=0:
                        verdict = "Compilation Error"
                finally:
                    sol = Solution()
                    sol.problem_id = Problem.objects.get(pk=problem_id)
                    sol.problem_code = 'OJ\codeFiles\sample.cpp'
                    sol.submitted_at = timezone.now()
                    sol.Verdict = verdict
                    sol.save()
                    messages.success(request,"File Uploaded Succesfully")
                    return HttpResponseRedirect(reverse('oj:leaderboard'))
            else:
                messages.warning(request,"Wrong File Uploaded")
                return HttpResponseRedirect(f'/OJ/problems/{problem_id}/')
            
        else:
            messages.error(request,"File not added")
            return HttpResponseRedirect(f'/OJ/problems/{problem_id}/')

def leaderboard(request):
    context = {
        'sol' : Solution.objects.all().order_by('-submitted_at')[:10],
    }
    return render(request,'OJ/finalpage.html',context)

