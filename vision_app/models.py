from django.db import models
import re
from datetime import datetime

class UserManage(models.Manager):
    def validatorReg(self, postData):
        errors = {}
        if postData['username']:
            if not postData['username'].isalpha():
                errors['user_name_alpha'] = 'User name must contain letters only'
            if len(postData['username']) < 2:
                errors['len_user_name'] = 'User name should be longer than 2 letters'
        else:
            errors['null_user_name'] = 'You have to enter a User name'

        if postData['email']:
            EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
            if not EMAIL_REGEX.match(postData['email']):               
                errors['email'] = "Invalid email address!"
            elif User.objects.filter(email=postData['email']).exists():
                errors['email_unique'] = "This email is already registered"
        else:
            errors['null_email'] = 'You have to enter an email'
        
        if postData['password']:
            if len(postData['password']) < 5:
                errors['len_password'] = 'Password should be longer than 5 characters'
        else:
            errors['null_password'] = 'You have to enter a password'
        
        if postData['c_password']:
            if len(postData['c_password']) < 5:
                errors['len_c_password'] = 'Password should be longer than 5 characters'
            elif postData['c_password'] != postData['password']:
                errors['c_password'] = 'Your two passwords do not match'
        else:
            errors['null_c_password'] = 'You have to enter a confirmation password'
        return errors
    
    def validatorLog(self, postData):
        errors = {}
        if postData['log_email']:
            EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
            if not EMAIL_REGEX.match(postData['log_email']):               
                errors['email'] = "Invalid email address!"
        else:
            errors['null_email'] = 'You have to enter an email'
        
        if postData['log_password']:
            if len(postData['log_password']) < 5:
                errors['len_password'] = 'Password should be longer than 5 characters'
        else:
            errors['null_password'] = 'You have to enter a password'
        return errors
    
    def vaildatorlog(self,postData):
        error={}
        if postData['log_email']:
            EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
            if not EMAIL_REGEX.match(postData['log_email']):               
                error['email'] = "Invalid email address!"
        else :
            error['null_email'] = 'You have to enter an email'
        
        if postData['log_password']:
            if len(postData['log_password']) <5 :
                error['len_password'] = 'password should be longer than 6 letters'
        else :
            error['null_password'] = 'You have to enter an password'
        return error  



class User(models.Model):
    username= models.CharField(max_length=45)
    email = models.EmailField(max_length=225, unique=True)
    password = models.CharField(max_length=45) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManage()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class Category(models.Model):
    name = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Desgin(models.Model):
    title = models.CharField(max_length=45)
    image_url = models.TextField(max_length=225) 
    user_uploaded = models.ForeignKey(User, related_name="designs_uploaded", on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name="designs", on_delete=models.CASCADE)
    who_liked_it = models.ManyToManyField(User, related_name="liked_designs", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    text = models.TextField(max_length=225)
    user = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)
    design = models.ForeignKey(Desgin, related_name="comments", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.text}"