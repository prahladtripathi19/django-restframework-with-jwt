from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import exceptions
from rest_framework.permissions import IsAuthenticated
from .models import Wallet, WalletTranscation
from django.contrib.auth.models import User
from rest_framework.pagination import PageNumberPagination
from app.pagination import PaginationHandlerMixin
from .serializers import WalletTranscationSerializer, WalletSerializer
from django.db.models import Sum
import datetime

# Create your views here.
class BasicPagination(PageNumberPagination):
    page_size_query_param = 1

class HelloWord(APIView):
	permission_classes = (IsAuthenticated,)
	
	def get(self, request):
		content = {'message': 'Hello, World!=='+self.request.user.email}
		return Response(content)

class WalletMoney(APIView):
	permission_classes = (IsAuthenticated,)
	def get(self, request):
		wallet = Wallet.objects.filter(user=request.user.id)
		if wallet:
			return JsonResponse({"current_balance":wallet[0].amount})
		else:
			return JsonResponse({"current_balance":0})

	def post(self, request):
		amount = request.data.get('amount')
		#source = request.data.get("source")
		walletobj = Wallet.objects.filter(user=request.user.id)
		if amount is not None:
			if walletobj:
				wallet = walletobj[0]
				wallet.amount = wallet.amount + int(amount)
				wallet.credited = wallet.credited + int(amount)
				wallet.save()
			else:
				wallet = Wallet()
				wallet.user = request.user
				wallet.amount = int(amount)
				wallet.credited = int(amount)
				wallet.save()
			txn = WalletTranscation()
			txn.wallet = wallet
			txn.txnamount = int(amount)
			txn.addSource = "CC/DC/NB"
			txn.save()
			return JsonResponse({"message":"added successfully", "current_balance":wallet.amount})
		else:
			return JsonResponse({"message":"incorect input provided"})
class WalletPay(APIView):
	permission_classes = (IsAuthenticated,)
	
	def post(self, request):
		amount = request.data.get('amount')
		user_id = request.data.get("user")
		if amount is not None and user_id is not None:
			print(amount, user_id)
			#import pdb;
			#pdb.set_trace()
			walletobj = Wallet.objects.filter(user=request.user.id)
			if walletobj:
				wallet = walletobj[0]
				if wallet.amount >= int(amount):
					try:
						userobj = User.objects.get(id=user_id)
						wallet.amount = wallet.amount - int(amount)
						wallet.debited = wallet.debited + int(amount)
						wallet.save()

						txn = WalletTranscation()
						txn.wallet = wallet
						txn.txnamount = int(amount)
						txn.sent_to = userobj
						txn.txntype = False
						txn.save()
						return JsonResponse({"message":"send successfully", "current_balance":wallet.amount})
					except:
						raise
						return JsonResponse({"message":"Receiver not exist"})
				else:
					return JsonResponse({"message":"Not have enough balance to send money!. Please add money and try again"})
			else:
				JsonResponse({"message":"Please add Balance to your wallet"})
		
		else:
			return JsonResponse({"message":"incorect input provided"})

class TranscationLog(APIView, PaginationHandlerMixin):
	permission_classes = (IsAuthenticated,)
	pagination_class = BasicPagination
	serializer_class = WalletTranscationSerializer
	def get(self, request):
		wallet = Wallet.objects.filter(user=request.user.id)
		if wallet:
			instance = WalletTranscation.objects.filter(wallet=wallet[0].id)
			page = self.paginate_queryset(instance)
			if page is not None:
				serializer = self.get_paginated_response(self.serializer_class(page,
			many=True).data)
			else:
				serializer = self.serializer_class(instance, many=True)
			return Response(serializer.data)
		else:
			return JsonResponse({"message":"no record exist"})
class UserWallet(APIView):
	permission_classes = (IsAuthenticated,)
	def get(self, request):
		wallet = Wallet.objects.filter(user=request.user.id)
		if wallet:
			today = datetime.date.today()  #wallet = wallet[0].id, 
			wt = WalletTranscation.objects.filter(wallet__id = wallet[0].id, txndate__year=today.year, txndate__month=today.month).values("txntype").annotate(txnamount =Sum('txnamount'))
			contextdict = {}
			contextdict["walletId"] = wallet[0].id
			contextdict["username"] = wallet[0].user.username
			contextdict["current_balance"] = wallet[0].amount
			
			for wallettxn in wt:
				if wallettxn["txntype"]:
					contextdict["amount_added"] = wallettxn["txnamount"]
				else:
					contextdict["amount_paid"] = wallettxn["txnamount"]
			return JsonResponse(contextdict)
		else:
			return JsonResponse({"current_balance":0})


