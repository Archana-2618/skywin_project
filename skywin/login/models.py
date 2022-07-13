from django.db import models

# Create your models here.



class User(models.Model):
    username = models.CharField(max_length=255, null=False)
    #email = models.EmailField(max_length=255, null=False)
    user_type=models.CharField(max_length=50)
    mobile=models.BigIntegerField(unique=True)
    password = models.CharField(max_length=50)
    confirm_password= models.CharField(max_length=50,null=True)
    ifLogged = models.BooleanField(default=False)
    token = models.CharField(max_length=500, null=True, default="")
    created_date = models.DateTimeField(auto_now=True, null=False, blank=False)
    updated_date = models.DateTimeField(auto_now=True, null=False, blank=False)


    def __str__(self):
        return self.mobile