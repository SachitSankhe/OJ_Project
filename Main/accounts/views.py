
from django.forms import ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.password_validation import validate_password,password_validators_help_text_html
# Create your views here.

def home(request):
    return render(request,'accounts/homepage.html')

def registration_page(request):
    context={
        'help_text' : password_validators_help_text_html()
    }
    return render(request,'accounts/register.html',context)


def register(request):
    if request.method == 'POST':
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            user_name = request.POST['username']
            email = request.POST['email']
            pass1 = request.POST['password1']
            pass2 = request.POST['password2']

            if User.objects.filter(username=user_name).exists():
                # print("username not matching")
                messages.error(request,"Username already exists")
                return HttpResponseRedirect('/accounts/register/')


            elif User.objects.filter(email=email).exists():
                # print("email not matching")
                messages.error(request,"Email already exists")
                return HttpResponseRedirect('/accounts/register/')


            elif (pass1!=pass2):
                # print("Password not matching")
                try:
                    validate_password(pass1)
                    messages.error(request,"Password not matching")
                    return HttpResponseRedirect('/accounts/register/')
                except ValidationError as v:
                    messages.error(request,v)
                    return HttpResponseRedirect('/accounts/register/')

            else:
                user = User.objects.create_user(username=user_name,password=pass1,first_name = first_name,last_name=last_name,email=email)
                user.save()
                messages.success(request,'User Created Succesfully.Please login')
                return HttpResponseRedirect(reverse('accounts:login'))
    else:
        return render(request,'accounts/register.html')
def login(request):
    if request.method == 'POST':
        user_name = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username = user_name,password = password)

        if user is not None:
            auth.login(request,user)
            print("User logged in")
            return HttpResponseRedirect(reverse('oj:index'))
        else:
            messages.error(request,'Invalid Credentials!')
            return HttpResponseRedirect('/accounts/login/')
    else:
        print("This is the get request")
        return render(request,'accounts/login.html')

def logout(request):
    auth.logout(request)
    return redirect(reverse('oj:index'))