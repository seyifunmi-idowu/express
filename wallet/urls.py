from django.urls import include, path
from rest_framework.routers import DefaultRouter

import wallet.views as views

router = DefaultRouter(trailing_slash=False)

router.register(r"wallet", views.WalletViewset, basename="wallet-views")


urlpatterns = [path("", include(router.urls))]
