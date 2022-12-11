from typing import Container
from django.contrib import messages
from django.contrib.auth.models import User
import subprocess
import docker
from django.urls import reverse
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import Problem, Solution, TestCase

from django.utils import timezone
# Create your views here.


global con_id 

def index(request):
    context = {
        'Problem_List': Problem.objects.order_by('-problem_level')[:5]
    }
    return render(request, 'OJ/index.html', context)


@login_required
def details(request, problem_id):
    problem = get_object_or_404(Problem, pk=problem_id)
    return render(request, 'OJ/problem_details.html', {'problem': problem})

    
@login_required
def submission(request, problem_id):
    if request.method == 'POST':
        upload_file = request.FILES.get('problem_code')
        if upload_file != None:
            filename = upload_file.name
            if filename.endswith('.cpp'):
                user = request.user
                client = docker.from_env()
                gcc_image = "gcc:latest"
                # print(con_id)
                try:
                    print("inside try")
                    # Start docker desktop don't change anything
                    container:Container = client.containers.get(container_id=user.username)
                    if(container.status!='running'):
                        container.start()
                except Exception as e:
                    print(e)
                    container = client.containers.run(gcc_image,detach=True,tty=True,name = user.username)
                    # print(con_id)
 
                

                with open(f'OJ/codeFiles/sample.cpp', 'wb+') as destination:
                    for chunk in upload_file.chunks():
                        user_code = chunk
                        destination.write(chunk)
                subprocess.run(['docker','cp','OJ/codeFiles/sample.cpp',container.id+":a.cpp"])

                # compile_com = "g++ OJ\codeFiles\sample.cpp -o OJ\codeFiles\output.exe"
                # run_com = "OJ\codeFiles\output.exe"
                try:   
                    subprocess.run(['docker','exec',container.id,'bash','-c','g++ a.cpp'],timeout=3)
                    try:
                        testcases = TestCase.objects.filter(problem_id=problem_id)
                        flag = True
                        for testcase in testcases:
                            # subprocess.run(['docker','cp',user_code,container.id+":a.cpp"])
                            with open(f'OJ/codeFiles/input.txt', '+w') as destination:
                                destination.write(testcase.input)
                            subprocess.run(['docker','cp','OJ/codeFiles/input.txt',container.id+":input.txt"])
                            subprocess.run(['docker','exec',container.id,'bash','-c','./a.out < input.txt > output.txt'],timeout=2)
                            subprocess.run(['docker','cp',container.id+':output.txt','OJ/codeFiles/output.txt'],timeout=5)
                            # op = subprocess.run(run_com, input=testcase.input, capture_output=True, timeout=1, text=True)
                            with open(f'OJ/codeFiles/output.txt', 'r') as destination:  
                                op = destination.read()
                            sample_out = testcase.output
                            print(op)
                            # curr_op = op.stdout
                            curr_op = ' '.join(op.strip().splitlines())
                            print(curr_op)
                            print(op)
                            if(curr_op!=sample_out):
                                flag = False
                                break
                        
                        if(flag):
                            print("Correct Answer")
                            verdict = "AC"
                        else:
                            print("Wrong Answer")
                            verdict="WA"
                    except subprocess.TimeoutExpired:
                        container:Container = client.containers.get(container_id=user.username)
                        container.stop()
                        print("Timeout (TLE)")
                        verdict = "TLE"

                except subprocess.CalledProcessError:
                    print("Compilation Error")
                    verdict = "Compilation Error"
                finally:
                    sol = Solution()
                    sol.user = request.user
                    sol.problem_id = Problem.objects.get(pk=problem_id)
                    sol.problem_code = user_code
                    sol.submitted_at = timezone.now()
                    sol.Verdict = verdict
                    sol.save()
                    messages.success(request, "File Uploaded Succesfully")
                    return HttpResponseRedirect(reverse('oj:leaderboard'))
            else:
                messages.warning(request, "Wrong File Uploaded")
                return HttpResponseRedirect(f'/OJ/problems/{problem_id}/')
        else:
            messages.error(request, "File not added")
            return HttpResponseRedirect(f'/OJ/problems/{problem_id}/')


@login_required
def leaderboard(request):
    context = {
        'sol': Solution.objects.filter(user=request.user).order_by('-submitted_at')[:10],
    }
    return render(request, 'OJ/finalpage.html', context)
