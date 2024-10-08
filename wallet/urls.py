from django.urls import include, path
from rest_framework.routers import DefaultRouter

import wallet.views as views

router = DefaultRouter(trailing_slash=False)

router.register(r"bank", views.BankViewset, basename="bank-views")
router.register(r"card", views.CardViewset, basename="card-views")
router.register(r"paystack", views.PaystackViewset, basename="paystack-views")
router.register(r"wallet", views.WalletViewset, basename="wallet-views")


urlpatterns = [path("", include(router.urls))]
