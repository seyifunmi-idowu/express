from django.urls import include, path
from rest_framework.routers import DefaultRouter

import order.views as views

router = DefaultRouter(trailing_slash=False)

router.register(r"vehicles", views.VehicleViewset, basename="vehicle-views")


urlpatterns = [path("", include(router.urls))]
