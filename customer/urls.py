from django.urls import include, path
from rest_framework.routers import DefaultRouter

from customer import views

router = DefaultRouter(trailing_slash=False)

router.register(
    r"customer/auth", views.CustomerAuthViewset, basename="customer-auth-views"
)
router.register(r"customer", views.CustomerViewset, basename="customer-views")
router.register(
    r"customer/saved-address",
    views.CustomerAddressViewset,
    basename="customer-address-views",
)


urlpatterns = [path("", include(router.urls))]
