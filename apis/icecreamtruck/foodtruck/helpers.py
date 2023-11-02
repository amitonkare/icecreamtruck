from datetime import datetime

from foodtruck.models import (
    Flavour,
    FoodItemFlavour,
    Inventory,
    Order,
    Truck,
    FoodItem,
    OrderItems,
)


def check_inventory(items, truck):
    availability = []
    for item in items:
        available = Inventory.objects.filter(
            truck=truck,
            food_item_flavour=item["food_item_flavour"],
            date=datetime.now(),
            quantity__gte=int(item["quantity"]),
        ).exists()
        availability.append(available)
    if len(availability) and all(availability):
        return True
    return False


def create_order(payload):
    try:
        total_price = 0.0
        order = Order.objects.create(truck=Truck.objects.get(pk=payload["truck"]))
        food_items = {}

        for item in payload["items"]:
            OrderItems.objects.create(
                order=order,
                food_item_flavour=FoodItemFlavour.objects.filter(
                    pk=item["food_item_flavour"]
                ).first(),
                quantity=item["quantity"],
            )
            food_items[int(item["food_item_flavour"])] = item["quantity"]

        food_item_flavours = FoodItemFlavour.objects.filter(id__in=food_items.keys())
        for food_item_flavour in food_item_flavours:
            total_price += food_item_flavour.price * int(
                food_items[food_item_flavour.id]
            )
            inventory = Inventory.objects.get(
                truck=order.truck,
                food_item_flavour=food_item_flavour,
                date=order.created_at.date(),
            )
            inventory.quantity -= int(food_items[food_item_flavour.id])
            inventory.save()

        order.total_price = total_price
        order.save()

        return order, total_price
    except Exception as e:
        raise
