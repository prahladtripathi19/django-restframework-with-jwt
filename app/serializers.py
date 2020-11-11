from rest_framework import serializers
from .models import Wallet, WalletTranscation

class WalletTranscationSerializer(serializers.ModelSerializer):
	class Meta:
		model = WalletTranscation
		fields = ["id","wallet","txntype","txnamount","user_to","user_from","addSource","txndate"]

class WalletSerializer(serializers.ModelSerializer):
	class Meta:
		model = Wallet
		fields = ["id","amount","credited","debited","created"]