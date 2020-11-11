#urls.py
from django.urls import path
from .views import HelloWord, WalletMoney, WalletPay, TranscationLog, UserWallet

urlpatterns = [

    path('check/', HelloWord.as_view(), name='hello'),
    #path('login/', walletLogin.as_view(), name='hello'),
    path('money/', WalletMoney.as_view(), name='walletmoney'),
    path('pay/', WalletPay.as_view(), name='WalletPay'),
    path('transcations/', TranscationLog.as_view(), name="TranscationLog"),
    path('userwallet/', UserWallet.as_view(), name='UserWallet'),

]