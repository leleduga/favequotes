from __future__ import unicode_literals
from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
from django.contrib.auth import logout
import bcrypt

def index(request):
    if "errors" in request.session:
        errors=request.session["errors"]
        del request.session["errors"]
    else:
        errors=[]    
    context={
        "errors":errors
    }
    return render(request, 'exam2app/index.html', context)

def register(request):
    data_is_valid, errors = User.objects.basic_validator(request.POST)
    print ('data is valid',data_is_valid)
    print (errors)
    if  data_is_valid:    
        user=User.objects.create(
            firstname=request.POST["firstname"],
            lastname=request.POST["lastname"],
            email=request.POST["email"],
            password = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt()),
        )
        request.session['firstname'] = request.POST['firstname']
        request.session['lastname']=request.POST['lastname']
        request.session['email']=request.POST['email']
    
        return redirect('/dashboard')
    else:
        request.session["errors"]=errors
        return redirect('/') 
    if User.objects.filter(email=request.POST['email']).count()>0:
        request.session["errors"]=errors
        print("Duplicate Email")   
        return redirect('/')   
    else:
        redirect('/dashboard') 

def validate_login(request):
    try:
        user = User.objects.get( email=request.POST["email"] )
        isValid = bcrypt.checkpw( request.POST["password"].encode() , user.password.encode() )
        print(isValid)
 
        if isValid:
            print("PASSWORDS MATCH")
            return redirect("/dash")
        else:
            print("NO MATCH")
            messages.add_message( request, messages.ERROR, "Invalid Credentials!" )
            return redirect("/")
    except:
        messages.add_message( request, messages.ERROR, "No user with this email was found!" )
        return redirect("/")

def dash(request):
    allquotes= Quote.objects.all().order_by("-id")[:3]
    myquotes= Quote.objects.all().order_by("-id")[3:]

    context= {
        "allquotes":allquotes,
        "myquotes":myquotes,
    }
    return render(request,"exam2app/dash.html", context)

def userquotes(request):
    # quote=Quote.objects.get(id=id)
    # context={
    #     "quote":quote,
    #     "user": user
    # }
    return render(request, 'exam2app/userquotes.html')

def editacct(request):
    # user=User.objects.get(id=id)
    # context={
    #     "user":user
    # }
    return render(request, 'exam2app/editacct.html')

def logout(request):    
    del request.session["email"]
    return render(request, 'exam2app/logout.html')
