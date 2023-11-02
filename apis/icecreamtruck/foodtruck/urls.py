from django.urls import path
from django.urls import include
from rest_framework.routers import DefaultRouter
from foodtruck import views


app_name = "foodtruck"
router = DefaultRouter()
router.register(r'order', views.OrderViewSet)
router.register(r'inventory', views.InventoryViewSet)
router.register(r'flavour', views.FlavourViewSet)
router.register(r'food_item', views.FoodItemViewSet)
router.register(r'food_item_flavours', views.FoodItemFlavourViewSet)
router.register(r'truck', views.TruckViewSet)


urlpatterns = [
    path("", include(router.urls)),
]
