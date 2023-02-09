from django.shortcuts import render
import re
from django.shortcuts import render,redirect,HttpResponseRedirect,HttpResponse

from django.contrib import messages
from django.contrib.auth.models import User 
from .models import Profile
from django.urls import reverse
# Create your views here.

from rest_framework import viewsets
from .serializers import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = UserSerializer
 
def signup(request):
    user = User.objects.all()
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass')
        pass2 = request.POST.get('pass1')
        if email in user:
            messages.error(request,"Email is already taken")
        elif(re.search(regex,email)):   
                if pass1==pass2:
                    u = User.objects.create(username=name,first_name=name,email=email,password=pass1)
                    u.save()
                    return render(request,'login.html')
                else:
                    messages.error(request,"Password does not match")
        else:
            messages.error(request,"Please Enter Valid Email")
            
    return render(request, 'register.html')

def login(request):
    user = User.objects.all()
    if request.method == 'POST':
        email = request.POST.get('email')
        pass1 = request.POST.get('pass')
        for u in user:
            if email==u.email:
                if pass1==u.password:
                    uid = u.id
                    request.session["uid"]=uid
                    return HttpResponseRedirect('login/myprofile/')
                else:
                    messages.error(request,"Password is incorrect")
                    
            else:
                messages.error(request,"Email or Password is incorrect")
                
    return render(request,'login.html')

def myprofile(request):
    if request.session.get("uid") is None:
        return HttpResponseRedirect(reverse('login'))
    else:
        uid =request.session["uid"]
        user = User.objects.get(id=uid)
        return render(request,'profile.html',{'user':user})

def adddetails(request):
    uid =request.session["uid"]
    user = User.objects.get(id=uid)
    profile, created = Profile.objects.get_or_create(user=user)
    if request.method == 'POST':
        image = request.FILES.get('profile')
        designation = request.POST.get('designation')
        company = request.POST.get('company')
        if image:
            if image.size > 1024 * 1024:
                messages.error(request,"Image size should be less than 1 MB")
            else:
                profile.image = image
                profile.designation = designation
                profile.company = company
                profile.save()
                return HttpResponseRedirect(reverse('myprofile'))
        else:
            messages.error(request, "Please select Image")

    return render(request,'adddetails.html')

def logout(request):
    request.session["uid"]=None
    return HttpResponseRedirect(reverse('login'))