from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from django.db.models import Q
import re,os


@login_required(login_url='/login/')
def index(request,pk=None):
    if request.user.is_staff == True:
        reciverUerData=None
        messageHistory=None
        if pk is not None :
            reciverUerData = User.objects.get(id=pk)
            messageHistory = messageInfo.objects.filter(senderUserInfo__in=[request.user.id,pk],reciveUserInfo__in=[request.user.id,pk])
        allUserData = User.objects.filter(is_staff=True,is_superuser=False).exclude(id=request.user.id).order_by('id')
        context={
            "userData":allUserData,
            "reciverData":reciverUerData,
            "messagehistory":messageHistory
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

