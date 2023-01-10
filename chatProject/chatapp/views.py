from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import authenticate,logout,login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
import re

def home(request):
    if request.method == "POST":
        try:
            username = request.POST['username']
            password = request.POST['password']
            user=authenticate(username=username,password=password)
            if user is not None:
                messages.success(request,"Login SucessFully")
                return redirect("Home")
        except Exception as Ex:
            messages.error(request,f"{Ex}")
    return render(request,'base/login.html')

def ragister(request):
    userRagister=User()
    if request.method == "POST":
        try:
            password = request.POST['password']
            # repassword = request.POST['repassword']
            # if password != repassword:
            #     messages.error(request,'Password Not Match?')
            #     return render(request,'base/ragister.html')
            # conform_password = re.search("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,}$", password)
            # if conform_password is None:
            #     messages.error(request,'Password Not Valid?')
            #     return render(request,'base/ragister.html')
            userRagister.first_name = request.POST['firstname']
            userRagister.last_name = request.POST['lastname']
            userRagister.username = request.POST['username']
            userRagister.phoneNumber = request.POST['phone']
            userRagister.email = request.POST['email']
            userRagister.profileImages = request.FILES['profile']
            userRagister.gender = request.POST['gender']
            userRagister.set_password(password)
            userRagister.save()
        except Exception as Ex:
            messages.error(request,f"{Ex}")
            return render(request,'base/ragister.html')
        messages.success(request,"Ragister Sucessfully")
        return render(request,'base/login.html')
    else:
        return render(request,'base/ragister.html')