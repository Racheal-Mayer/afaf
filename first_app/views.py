from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
import bcrypt
from .models import *

def index(request):
    context = {
        "register" : Register.objects.all()
    }
    return render(request, "index.html", context)

def adduser(request):
    errors = Register.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        newuser = Register.objects.create(fname=request.POST['fname'],
        lname= request.POST['lname'], 
        email = request.POST['email'], 
        password = pw_hash)
        request.session['loggedinID'] = newuser.id
        messages.success(request, "User successfully Entered!")
        return redirect('/')

def login(request):
        errors = Register.objects.validator(request.POST)
        if len(errors) > 0:
                for key, value in errors.items():
                    messages.error(request, value)
                return redirect('/')
        user = Register.objects.filter(email=request.POST['email'])
        logged_user= user[0]
        request.session['loggedinID'] = logged_user.id
        return redirect('/success')

def success(request):
    if 'loggedinID' not in request.session:
        return redirect('/')
    loggedinuser = Register.objects.get(id= request.session['loggedinID'])
    context = {
        "loggedinuser" : loggedinuser,
        "myquotes" : Quote.objects.filter(Q(uploader = loggedinuser) | Q(favoritor = loggedinuser)),
        'notmyquotes' : Quote.objects.exclude(Q(uploader = loggedinuser) | Q(favoritor = loggedinuser))
    }
    return render(request,"success.html", context)

def addquote(request):
        #handle form info such as validating form info and adding the item to database.
    print(request.POST)
    # send form info to validtor in models
    validationErrors = Quote.objects.validateItem(request.POST)
    if len(validationErrors)>0:
        for key,value in validationErrors.items():
            messages.error(request, value)
        return redirect("/success")
        # get the logged in user so we can assign the items uploaded to that user object
    loggedinuser = Register.objects.get(id=request.session['loggedinID'])
    #create item in data base if there are no validation errors
    newquote = Quote.objects.create(quotes= request.POST['Quote'], quotedby = request.POST['quotedby'], uploader = loggedinuser)
    return redirect ("/success")

def edit(request,quote_id):
    context = {
        "quote_id" : quote_id
    }
    return render(request, "edit.html", context)

def process_edit(request, quote_id):
    errors = Quote.objects.validateItem(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/edit/{quote_id}')
    else:
    # use id to grab quote
        quote_to_edit = Quote.objects.get(id=quote_id)
        quote_to_edit.quotes = request.POST['Quote']
        quote_to_edit.save()
        messages.success(request, "Quote successfully Entered!")
        return redirect('/success')

def deletequote(request, quoteId):
    quote = Quote.objects.get(id= quoteId)
    quote.delete()
    return redirect ("/success")

def show (request, uploaderId):
    user = Register.objects.get(id=uploaderId)
    context = {
        "Quote" : Quote.objects.filter(uploader=user),
        "user" : user
    }
    return render(request, "show.html", context)

def addToFav (request, quoteId):
    loggedinuser = Register.objects.get(id=request.session['loggedinID'])
    quote = Quote.objects.get(id= quoteId)
    quote.favoritor.add(loggedinuser)
    return redirect ("/success")

##REMOVING JOIN LIKE UNLIKING A POST!!!
def removefromFav(request, quoteId):
    loggedinuser = Register.objects.get(id=request.session['loggedinID'])
    quote = Quote.objects.get(id= quoteId)
    quote.favoritor.remove(loggedinuser)
    return redirect ("/success")
#.REMOVE & .ADD ARE THE ONLY DIFFERENCE
#BRINGING IN THE LOGGED IN USER IN SESSION & THE ITEM THAT ID LIKED

def destroy(request):
    request.session.clear()
    return redirect("/")

