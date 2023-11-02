from datetime import datetime
from django.core.management.base import BaseCommand, CommandError

from foodtruck.models import FoodItemFlavour, Truck, Inventory


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            food_item_flavours = FoodItemFlavour.objects.all()

            for fif in food_item_flavours:
                Inventory.objects.create(
                    food_item_flavour=fif,
                    truck=Truck.objects.get(pk=1),
                    quantity=20,
                    date=datetime.now().date(),
                )

            print("Inventory Updated!")

        except Exception as e:
            print("Inventory not Updated!", e)
            raise CommandError(e)
