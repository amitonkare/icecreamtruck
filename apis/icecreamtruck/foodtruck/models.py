from django.db import models


class Flavour(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class FoodItem(models.Model):
    name = models.CharField(max_length=255)
    flavours = models.ManyToManyField(Flavour, through="FoodItemFlavour", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class FoodItemFlavour(models.Model):
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    flavour = models.ForeignKey(Flavour, on_delete=models.CASCADE)
    price = models.FloatField()

    def __str__(self):
        return f"{self.food_item.name} | {self.flavour.name} | Price: {self.price}"


class Truck(models.Model):
    name = models.CharField(max_length=255)
    owner = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_truck_items(self):
        return Inventory.objects.filter(truck=self).order_by("food_item_flavour")


class Inventory(models.Model):
    food_item_flavour = models.ForeignKey(FoodItemFlavour, on_delete=models.CASCADE)
    truck = models.ForeignKey(Truck, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    date = models.DateField()

    def __str__(self):
        return f"{self.food_item.name} | {self.flavour.name} | {self.truck.name} | Quantity: {self.quantity}"


    class Meta:
        ordering = ["quantity"]


class Order(models.Model):
    truck = models.ForeignKey(Truck, on_delete=models.CASCADE)
    total_price = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id} | {self.truck.name} | {self.total_price}"

    def get_order_items(self):
        return self.items


class OrderItems(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    food_item_flavour = models.ForeignKey(FoodItemFlavour, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.order.id} | {self.flavour.name} | {self.food_item.name}"
