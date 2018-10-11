from __future__ import unicode_literals
from django.db import models
import re
import bcrypt


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-copyZ0-9._-]+\.[a-zA-Z]+$')
      

class UserManager(models.Manager):
    def create_error_message(self, label, message):
        error = {}
        error["label"]= label
        error["message"]=message
        return error, False

    def basic_validator(self,form_data):
        data_is_valid=True
        errors = []

        if len(form_data['firstname']) < 2:
            error, data_is_valid = self.create_error_message(
                "firstname",
                "First name is required and should be at least 2 characters"
            )
            errors.append(error)
        if len(form_data['firstname']) >100:
            error, data_is_valid = self.create_error_message(
                "firstname",
                "First name must be less than 100 characters"
            )
            errors.append(error)    
        if len(form_data['lastname']) < 2:
            error, data_is_valid = self.create_error_message(
                "lasttname",
                "Last name is required and should be at least 2 characters"
            )
            errors.append(error)
        if len(form_data['lastname']) >100:
            error, data_is_valid = self.create_error_message(
                "lastname",
                "Last name must be less than 100 characters"
            )
            errors.append(error)    
        if not EMAIL_REGEX.match(form_data['email'] ):
            error, data_is_valid = self.create_error_message(
                "email",
                "Invalid email format! Ex: test@test.com" 
            )
            errors.append(error)   
        if len(form_data['password']) < 8:
            error, data_is_valid = self.create_error_message(
                "password",
                "Password is required and should be at least 8 characters"
            )
            errors.append(error) 
        if len(form_data['password']) >100:
            error, data_is_valid = self.create_error_message(
                "password",
                "Password must be less than 100 characters"
            )
            errors.append(error)
        if len(form_data['confirmpw']) < 8:
            error, data_is_valid = self.create_error_message(
                "confirmpw",
                "Password is required and should be at least 8 characters"
            )
            errors.append(error)
        if len(form_data['confirmpw']) >100:
            error, data_is_valid = self.create_error_message(
                "confirmpw",
                "Password must be less than 100 characters"
            )          
            errors.append(error)  
        if(form_data['confirmpw']) != (form_data['password']):
            error, data_is_valid = self.create_error_message(
                "confirmpw",
                "Passwords must match"
            )   
            errors.append(error)     
        if User.objects.filter(email=request.POST['email']).count() >0:
            error, data_is_valid = self.create_error_message(
                "email",
                "Email already exists"
            )   
            errors.append(error) 
           
        return data_is_valid, errors


class User(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    # created_at = models.DateTimeField(auto_now_add = True)
    # updated_at = models.DateTimeField(auto_now = True)

    objects = UserManager()

class QuoteManager(models.Manager):
    def create_error_message(self, label, message):
        error = {}
        error["label"]= label
        error["message"]=message
        return error, False

    def basic_validator(self,form_data):
        data_is_valid=True
        errors = []

        if len(form_data['author']) < 3:
            error, data_is_valid = self.create_error_message(
                "author",
                "Author is required and should be at least 3 characters"
            )
            errors.append(error)    
        if len(form_data['body']) < 10:
            error, data_is_valid = self.create_error_message(
                "body",
                "Quote is required and should be at least 10 characters"
            )
            errors.append(error) 
        return data_is_valid, errors  

class Quote(models.Model):
    body = models.TextField(max_length=255)
    author = models.CharField(max_length=100)
    posted_by= models.ForeignKey(User, related_name="posted_quotes", null=True)
    user= models.ForeignKey(User, related_name="quotes", null=True)

    objects = QuoteManager()

