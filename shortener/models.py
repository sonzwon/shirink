from django.db import models 
from django.contrib.auth.models import AbstractUser

# Create your models here.

class PayPlan(models.Model):
    name = models.CharField(max_length=20)
    price = models.IntegerField()
    update_at = models.DateTimeField(auto_now=True)
    create_at = models.DateTimeField(auto_now_add=True)

class Users(AbstractUser):
    full_name = models.CharField(max_length=30, null=True)
    pay_plan = models.ForeignKey(PayPlan, on_delete=models.DO_NOTHING) 
