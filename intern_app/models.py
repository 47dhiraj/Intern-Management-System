from email.policy import default
from django.db import models

from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)

from rest_framework_simplejwt.tokens import RefreshToken

from django.db.models.signals import post_save
from django.dispatch import receiver

from datetime import datetime


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):                                      
        if username is None:
            raise TypeError('User should have a username')
        if password is None:
            raise TypeError('Password should not be none')
        if email is None:
            raise TypeError('User should have a Email')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)      
        user.save()                                                                           
        return user                                                                            

    def create_superuser(self, username, email, password=None):                                 
        user = self.create_user(username, email, password, )                                     
        user.is_superuser = True
        user.is_staff = True
        user.is_supervisor = True
        user.is_intern = False
        user.save()                                                                             
        return user                                                                            


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True, db_index=True)                     
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    is_verified = models.BooleanField(default=False)                                            
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_supervisor = models.BooleanField(default=False)
    is_intern = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add =True)                                        
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'                                                                   
    REQUIRED_FIELDS = ['username']                                                              

    objects = UserManager()                                                                     

    def __str__(self):
        return self.email

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)                                                  
        }


@receiver(post_save, sender=User) 
def user_post_save_receiver(sender, instance, created, *args, **kwargs): 
    if created:
        instance.is_active = True
        instance.is_verified = True
        instance.save()

class Task(models.Model):
    tasktitle = models.CharField(max_length=300, unique=True, db_index=True)
    assignee = models.ForeignKey(User, on_delete=models.SET_NULL, null = True, blank = True, related_name='assignee')
    assignor = models.ForeignKey(User, on_delete=models.SET_NULL, null = True, blank = True, related_name='assignor')
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add =True)                                        
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering: ['-updated_at']

    def __str__(self):
        return self.tasktitle



class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null = True, blank = True, related_name='attendant')
    status = models.BooleanField(default=True)
    date = models.DateField(auto_now_add=True)
    work_start_time = models.TimeField(default=datetime.now().time())
    work_end_time = models.TimeField(default=datetime.now().time())                                        
    
    class Meta:
        ordering: ['-date']

    def __str__(self):
        return self.user.username + ' ' + str(self.date)
