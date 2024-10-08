from django.urls import include, path
from rest_framework.routers import DefaultRouter

import authentication.views as views

router = DefaultRouter(trailing_slash=False)

router.register(r"auth", views.AuthViewset, basename="auth-views")
router.register(r"user", views.UserViewset, basename="users-views")


urlpatterns = [path("", include(router.urls))]
