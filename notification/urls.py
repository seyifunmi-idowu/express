from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=False)

# router.register(r"notification", views.RiderViewset, basename="notification-views")


urlpatterns = [path("", include(router.urls))]
