from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import authenticate,logout,login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
import re

def index(request):
    return render(request,'base/index.html')

def userlogin(request):
    if request.method == "POST":
        try:
            username = request.POST['username']
            password = request.POST['password']
            user=authenticate(username=username,password=password)
            if user is not None :
                login(request, user)
                if request.user.is_staff == True:
                    user_obj = User.objects.get(email=request.user.email)
                    user_obj.active_user = True
                    user_obj.save()
                    messages.success(request,"Login SucessFully")
                    return redirect("Dashbord")
            else:
                messages.error(request,"Pelase Ragister First.")
                return redirect("User-Login")
        except Exception as Ex:
            messages.error(request,f"{Ex}")
    return render(request,'base/login.html')
    

def ragister(request):
    userRagister=User()
    if request.method == "POST":
        try:
            password = request.POST['password']
            repassword = request.POST['repassword']
            if password != repassword:
                messages.error(request,'Password Not Match?')
                return render(request,'base/ragister.html')
            conform_password = re.search("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,}$", password)
            if conform_password is None:
                messages.error(request,'Password Not Valid follow Formate(Capital,small,numeric,special characters)')
                return render(request,'base/ragister.html')
            userRagister.first_name = request.POST['firstname']
            userRagister.last_name = request.POST['lastname']
            userRagister.username = request.POST['username']
            userRagister.phoneNumber = request.POST['phone']
            userRagister.email = request.POST['email']
            if len(request.FILES) == 0:
                userRagister.profileImages = 'images/defultprofile.png'
            else:
                userRagister.profileImages = request.FILES['profile']
            userRagister.gender = request.POST['gender']
            userRagister.is_staff=True
            userRagister.set_password(password)
            userRagister.save()
        except Exception as Ex:
            messages.error(request,f"{Ex}")
            return render(request,'base/ragister.html')
        messages.success(request,"Ragister Sucessfully")
        return redirect('User-Login')
    else:
        return render(request,'base/ragister.html')

def userLogout(request):
    try:
        user_obj = User.objects.get(email=request.user.email)
        user_obj.active_user = False
        user_obj.save()
        logout(request)
    except Exception:
        pass
    messages.success(request,"Logout Sucessfully!")
    return redirect('/login/')
