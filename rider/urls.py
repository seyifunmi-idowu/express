from django.urls import include, path
from rest_framework.routers import DefaultRouter

import rider.views as views

router = DefaultRouter(trailing_slash=False)

router.register(r"rider/auth", views.RiderAuthViewset, basename="driver-auth-views")


urlpatterns = [path("", include(router.urls))]
