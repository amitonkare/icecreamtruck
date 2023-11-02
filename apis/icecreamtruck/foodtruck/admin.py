from django.contrib import admin

from foodtruck.models import *


admin.site.register(Flavour)
admin.site.register(FoodItem)
admin.site.register(Inventory)
admin.site.register(Order)
admin.site.register(OrderItems)
admin.site.register(Truck)
