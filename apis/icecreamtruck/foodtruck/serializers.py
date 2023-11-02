from foodtruck.models import (
    FoodItemFlavour,
    Inventory,
    Flavour,
    FoodItem,
    Order,
    OrderItems,
    Truck,
)
from rest_framework import serializers


class InventorySerializer(serializers.ModelSerializer):
    food_item = serializers.ReadOnlyField(source="food_item_flavour.food_item.name")
    flavour = serializers.ReadOnlyField(source="food_item_flavour.flavour.name")

    class Meta:
        model = Inventory
        fields = "__all__"


class FlavourSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flavour
        fields = "__all__"


class FoodItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodItem
        fields = "__all__"
        depth = 1


class TruckSerializer(serializers.ModelSerializer):

    class Meta:
        model = Truck
        fields = "__all__"

class TruckDetailsSerializer(serializers.ModelSerializer):
    items = InventorySerializer(source="get_truck_items", many=True)

    class Meta:
        model = Truck
        fields = "__all__"


class FoodItemFlavourSerializer(serializers.ModelSerializer):
    food_item_name = serializers.ReadOnlyField(source="food_item.name")
    flavour_name = serializers.ReadOnlyField(source="flavour.name")

    class Meta:
        model = FoodItemFlavour
        fields = "__all__"


class OrderItemSerialzer(serializers.ModelSerializer):
    food_item_flavour = FoodItemFlavourSerializer()

    class Meta:
        model = OrderItems
        exclude = ["order"]


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerialzer(source="get_order_items", many=True)
    truck_name = serializers.ReadOnlyField(source="truck.name")

    class Meta:
        model = Order
        fields = "__all__"
