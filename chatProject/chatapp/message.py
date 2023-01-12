from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
import re,os


@login_required(login_url='/login/')
def messageinfo(request,pk=None):
    if request.user.is_staff == True:
        if 'sendMessage' in request.POST:
            reciver_user = User.objects.get(id=pk)
            messageData = messageInfo()
            messageData.senderUserInfo = request.user.id
            messageData.reciveUserInfo = reciver_user
            messageData.message = request.POST['messagecontain']
            messageData.save()
            return redirect('Chat-with-User',pk=pk)
    else:
        messages.error(request,'Not Access!')
        return redirect("logout")