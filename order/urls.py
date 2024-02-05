from django.urls import include, path
from rest_framework.routers import DefaultRouter

import order.views as views

router = DefaultRouter(trailing_slash=False)

router.register(r"maps", views.MapsViewset, basename="maps-views")
router.register(
    r"order/customer", views.CustomerOrderViewset, basename="customer-order-views"
)
router.register(r"order/rider", views.RiderOrderViewset, basename="rider-order-views")
router.register(r"vehicles", views.VehicleViewset, basename="vehicle-views")


urlpatterns = [path("", include(router.urls)), path("map", views.view_map, name="map")]
