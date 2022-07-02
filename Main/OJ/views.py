from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect

from OJ.functions import handle_uploaded_file

from .models import Problems
from .forms import FileSubmission
#Create your views here.


def index(request):
    context = {
        'Problem_List' : Problems.objects.order_by('-problem_level')[:5]
    }
    return render(request,'OJ/index.html',context)

def details(request,problem_id):
    problem = get_object_or_404(Problems,pk=problem_id)
    
    return render(request,'OJ/problem_details.html',{'problem': problem })


def submission(request):
    if request.method == 'POST':
        form_1 = FileSubmission(request.POST, request.FILES)
        if form_1.is_valid():    
            form.save()
            handle_uploaded_file(request.FILES['files'])
            return HttpResponseRedirect('File uploaded succesfully')
    else:
        form = FileSubmission()
        return render(request, 'OJ/details.html', {'form': form})

def finalpage(request):
    return render(request,"OJ/submissions.html",{})