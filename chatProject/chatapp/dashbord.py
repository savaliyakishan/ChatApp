from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import authenticate,logout,login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
import re,os

@login_required(login_url='/login/')
def index(request):
    if request.user.is_staff == True:
        allUserData = User.objects.filter(is_staff=True,is_superuser=False).order_by('id')
        context={
            "userData":allUserData
        }
        return render(request,"dashboard/index.html",context)
    else:
        messages.error(request,'Not Access!')
        return redirect("logout")

@login_required(login_url='/login/')
def profile(request):
    if request.user.is_staff == True:
        if 'updateProfile' in request.POST:
            userUpdatedata=User.objects.get(id=request.user.id)
            if len(request.FILES) != 0:
                if len(userUpdatedata.profileImages) > 0:
                    os.remove(userUpdatedata.profileImages.path)
                    userUpdatedata.profileImages = request.FILES['profile']
            userUpdatedata.username = request.POST['username']
            userUpdatedata.first_name = request.POST['firstname']
            userUpdatedata.last_name = request.POST['lastname']
            userUpdatedata.email = request.POST['email']
            userUpdatedata.gender = request.POST['gender']
            userUpdatedata.phoneNumber = request.POST['phone']
            userUpdatedata.save()
            messages.success(request, 'Update Sucessfully')
            return redirect("Dashbord")
        return render(request,"dashboard/profile.html")
    else:
        messages.error(request,'Not Access!')
        return redirect("logout")