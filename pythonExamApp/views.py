from django.shortcuts import render, redirect
from django.contrib import messages	
from . models import *
import bcrypt

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import messages	
from . models import *
import bcrypt

# Create your views here.
def index (request):
	return render(request,'index.html')

def register(request):
	errorsFromValidator = User.objects.UserValidator(request.POST)
	
	if len(errorsFromValidator)>0:
		for key, value in errorsFromValidator.items():   messages.error(request, value)
		return redirect('/')
	
	encryptedPW = bcrypt.hashpw(request.POST['formPassword'].encode(), bcrypt.gensalt()).decode()

	newUser = User.objects.create(firstName = request.POST['formFirstName'], lastName = request.POST['formLastName'], email = request.POST['formEmail'], password = encryptedPW)
	
	request.session['loggedInUserID'] = newUser.id
	
	return redirect ('/')

def login(request):
	errorsFromValidator = User.objects.loginValidator(request.POST)
	if len(errorsFromValidator)>0:
		for key, value in errorsFromValidator.items():   messages.error(request, value)
		return redirect('/')
	matchingEmail = User.objects.filter(email = request.POST['emailLogin'])
	request.session['loggedInUserID'] = matchingEmail[0].id
		
	return redirect('/viewQuotes')

def logout(request):
	request.session.clear()    
	return redirect('/')

def viewQuotes (request):
	if 'loggedInUserID' not in request.session:
		messages.error(request, 'You must be logged in')
		return redirect('/')
	context = {
		'loggedInUser': User.objects.get(id = request.session['loggedInUserID']),
		'allQuotes' : Quotes.objects.all(),
		'allUsers' : User.objects.all()
		
      }
	return render(request, 'quotes.html', context)

def userQuotes (request):
	if 'loggedInUserID' not in request.session:
		messages.error(request, 'You must be logged in')
		return redirect('/')
	context = {
		'loggedInUser': User.objects.get(id = request.session['loggedInUserID']),
		'allQuotes' : Quotes.objects.all(),
		'allUsers' : User.objects.all()
	}
	return render(request, 'quoteInfo.html', context)

def addQuote(request):
	Quotes.objects.create(author=request.POST["formAuthor"], description=request.POST["formDesc"], uploaded_by = User.objects.get(id = request.session['loggedInUserID']))
	return redirect('/viewQuotes')

def oneQuote(request, oneQuoteID):
	context = {
			'oneQuote': Quotes.objects.get(id = oneQuoteID),
			'loggedInUser': User.objects.get(id = request.session['loggedInUserID']),
			'allUsers' : User.objects.all(),
   			'allQuotes' : Quotes.objects.all(),
      		
	}
	return render(request, 'quoteInfo.html', context)

def newLike(request, oneQuoteID):
	this_user = User.objects.get(id=request.session['loggedInUserID'])
	this_quote = Quotes.objects.get(id=oneQuoteID)
	
	this_quote.users_who_like.add(this_user)
	
	return redirect('/viewQuotes')

def unLike(request, oneUserID):
	this_user = User.objects.get(id=request.session['loggedInUserID'])
	this_quote = Quotes.objects.get(id=oneUserID)
	this_quote.users_who_like.remove(this_user)
	
	return redirect('/viewQuotes')

def deleteQuote(request, oneQuoteID):
	b = Quotes.objects.get(id = oneQuoteID)
	b.delete()
	return redirect('/viewQuotes')

def updateQuote(request, oneQuoteID):
	b = Quotes.objects.get(id = oneQuoteID)
	b.author = request.POST['editAuthor']
	b.description = request.POST['editDescription']
	b.save()
	return redirect('/viewQuotes')

def viewAccount (request, oneUserID):
	if 'loggedInUserID' not in request.session:
		messages.error(request, 'You must be logged in')
		return redirect('/')
	context = {
		'loggedInUser': User.objects.get(id = request.session['loggedInUserID']),
		'allQuotes' : Quotes.objects.all(),
		'allUsers' : User.objects.all()
	}
	return render (request, 'editaccount.html',context)

def editAccount (request, oneUserID):
	b = User.objects.get(id = oneUserID)
	b.firstName = request.POST['editFirstName']
	b.lastName = request.POST['editLastName']
	b.email = request.POST['editEmail']
	b.save()
	return redirect('/viewQuotes')