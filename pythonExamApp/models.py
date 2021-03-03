from django.db import models
from datetime import date
import re
import bcrypt
# Create your models here.

class UserManager(models.Manager):
	
	def UserValidator(self, formInputs):
		today = date.today()
		EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
		emailTaken = User.objects.filter(email = formInputs['formEmail'])
		errors = {}
		if len(formInputs['formEmail'])==0:
			errors['emailnotempty'] = 'The email field cannot be empty.'
		elif not EMAIL_REGEX.match(formInputs['formEmail']):       
			errors['email'] = "Invalid email address!"
		elif len(emailTaken)>0:
			errors['takenemail'] = "This email is already taken, please try again."
		if len(formInputs['formFirstName'])==0:
			errors['FirstNameRequired'] = "First name is required."
		elif len(formInputs['formFirstName'])<3:
			errors['FirstNameLonger'] = "The first name must be 2 characters long."
		if len(formInputs['formLastName'])==0:
			errors['LastNameRequired'] = "First name is required."
		elif len(formInputs['formLastName'])<3:
			errors['LastNameLonger'] = "The first name must be 2 characters long."
		if formInputs['formPassword']==0:
			errors['noPass'] = "Password is required."
		elif len(formInputs['formPassword'])<8:
			errors['tooshort'] = "Passwords must be at least 8 characters long."
		if formInputs['formPassword'] != formInputs['formPasswordConfirm']:
			errors['mismatch'] = "Passwords do not match."
		return errors

	def loginValidator(self, formInputs):
		errors = {}
		matchingEmail = User.objects.filter(email = formInputs['emailLogin'])
		if len(matchingEmail)==0:
			errors['missingEmail'] = "This email is not found, please register first."
		elif not bcrypt.checkpw(formInputs['passwordLogin'].encode(), matchingEmail[0].password.encode()):
			errors['badpassword'] = "Incorrect password"
		return errors

class User(models.Model):
	firstName = models.CharField(max_length=255)
	lastName = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = UserManager()

class Quotes(models.Model):
	author = models.CharField(max_length=255)
	description = models.CharField(max_length=255)
	uploaded_by = models.ForeignKey(User, related_name='favBook', on_delete = models.CASCADE)
	users_who_like = models.ManyToManyField(User, related_name= 'lotsBooks')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

