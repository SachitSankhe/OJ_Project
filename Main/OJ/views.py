from django.contrib import messages
from django.contrib.auth.models import User
import subprocess
from django.urls import reverse
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import Problem, Solution, TestCase

from django.utils import timezone
# Create your views here.


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
        file = request.FILES.get('problem_code')
        if file != None:
            filename = file.name
            if filename.endswith('.cpp'):
                with open(f'OJ/codeFiles/sample.cpp', 'wb+') as destination:
                    for chunk in file.chunks():
                        destination.write(chunk)

                compile_com = "g++ OJ\codeFiles\sample.cpp -o OJ\codeFiles\output.exe"
                run_com = "OJ\codeFiles\output.exe"
                try:
                    subprocess.run(compile_com, shell=True,
                                       check=True, timeout=3)
                    try:
                        testcases = TestCase.objects.all().filter(problem_id=problem_id)
                        flag = True
                        for testcase in testcases:
                            op = subprocess.run(run_com, input=testcase.input, capture_output=True, check=True, timeout=1, text=True)
                            sample_out = testcase.output
                            curr_op = op.stdout.strip()
                            curr_op = ' '.join(curr_op.splitlines())
                            print(curr_op)
                            if(curr_op!=sample_out):
                                flag = False
                                break
                        # flag = True
                        # for i in range(0,len(sample_out)):
                        #     if curr_op[i] != '\n':
                        #         if(curr_op[i] != sample_out[i]):
                        #             flag = False
                        # for i in range(0,len(sample_out)):
                        #     print("curr_op: ",curr_op[i]," ", "sample_out: ",sample_out[i])
                        #     print()
                        # print(sample_out)
                        # print(curr_op)
                        if(flag):
                            print("Correct Answer")
                            verdict = "AC"
                        else:
                            print("Wrong Answer")
                            verdict="WA"
                    except subprocess.TimeoutExpired:
                        print("Timeout (TLE)")
                        verdict = "TLE"

                except subprocess.CalledProcessError as e:
                    if e.returncode != 0:
                        print("Compilation Error")
                        verdict = "Compilation Error"
                finally:
                    sol = Solution()
                    sol.user = request.user
                    sol.problem_id = Problem.objects.get(pk=problem_id)
                    with open(f'OJ/codeFiles/sample.cpp', 'r') as destination:
                        sol.problem_code = destination.read()
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
