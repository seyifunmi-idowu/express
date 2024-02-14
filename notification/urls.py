from django.urls import include, path
from rest_framework.routers import DefaultRouter

from notification import views

router = DefaultRouter(trailing_slash=False)

router.register(
    r"notification", views.NotificationViewset, basename="notification-views"
)


urlpatterns = [path("", include(router.urls))]
