from django.shortcuts import render, HttpResponse , redirect
from django.contrib import messages
from .models import *
import bcrypt

def index(request):
    return render(request,'index.html')

def register(request):
    if request.method == 'POST':
        errors = User.objects.register_validation(request.POST)
        if len(errors) > 0:
            for key,value in errors.items():
                messages.error(request,value)
            return redirect("/") 
        else:
            hash_pass = bcrypt.hashpw(request.POST['password'].encode(),bcrypt.gensalt()).decode()
            user = User.objects.create(
                fname = request.POST['fname'],
                lname = request.POST['lname'],
                email = request.POST['email'],
                password = hash_pass
            )
            user.save()
            messages.success(request,"User successfully added!")

            request.session['user_id'] = user.id
            return redirect('/success')
    return redirect('/')

def login(request):
    if request.method == 'POST':
        errors = User.objects.login_validation(request.POST)
        if len(errors) > 0:
            for key,value in errors.items():
                messages.error(request,value)
            return redirect("/")
        else:
            userid = User.objects.get(email__iexact=request.POST['email'])
            request.session['user_id'] = userid.id
            return redirect('/success')

    return redirect('/') 

def success(request):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        'user': User.objects.get(id=request.session['user_id'])
    }
    return render(request,'success.html',context)


def logout(request):
    del request.session['user_id']
    return redirect('/')