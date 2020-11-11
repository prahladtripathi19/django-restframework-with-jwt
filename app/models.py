from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.

class Wallet(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	amount = models.IntegerField(default=0)
	credited = models.IntegerField(default=0)
	debited = models.IntegerField(default=0)
	created = models.DateTimeField(auto_now_add=True)

class WalletTranscation(models.Model):
	wallet = models.ForeignKey(Wallet, on_delete= models.CASCADE)
	txntype = models.BooleanField(default = True) # 0 for debit and 1 for credit
	txnamount = models.IntegerField(default=0)
	user_to = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="sendtouser")
	user_from = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="receivedfromuser")
	addSource = models.CharField(max_length=10)
	txndate = models.DateTimeField(default=datetime.now)





