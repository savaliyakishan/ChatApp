from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
import re,os


@login_required(login_url='/login/')
def messageinfo(request,pk=None):
    if request.user.is_staff == True:
        return redirect('Chat-with-User',pk=pk)
    else:
        messages.error(request,'Not Access!')
        return redirect("logout")
    
# @login_required(login_url='/login/')
# def callinfo(request,sender=None,reciver=None):
#     if request.user.is_staff == True:
#         return render(request,'dashboard/call.html')