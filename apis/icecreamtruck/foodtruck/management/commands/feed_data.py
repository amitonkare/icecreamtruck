import json
from pathlib import Path
from django.core.management.base import BaseCommand, CommandError

from foodtruck.models import FoodItem, Flavour, FoodItemFlavour, Truck


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            BASE_DIR = Path(__file__).resolve().parent.parent.parent
            flavours = open(BASE_DIR / "fixtures/flavours.json").read()

            flavours = json.loads(flavours)

            flavours_objs = Flavour.objects.bulk_create(
                Flavour(**flavour) for flavour in flavours
            )
            flavour_obj_dict = {}
            for flavour in flavours_objs:
                flavour_obj_dict[flavour.name] = flavour

            food_items = open(BASE_DIR / "fixtures/fooditems.json").read()

            food_item_objs = {}
            food_item_flavours = []
            for food_item in json.loads(food_items):
                if food_item["name"] not in food_item_objs:
                    food_item_objs[food_item["name"]] = FoodItem.objects.create(name=food_item["name"])

                food_item_flavours.append(
                    FoodItemFlavour(
                        food_item=food_item_objs[food_item["name"]],
                        flavour=flavour_obj_dict[food_item["flavours"]],
                        price=food_item["price"]
                    )
                )

            FoodItemFlavour.objects.bulk_create(food_item_flavours)

            Truck.objects.create(name="Truck 1", address="E-Street", owner="Owner 1")
            print("Data Created!")
        except Exception as e:
            import traceback
            traceback.print_exc()
            print("Data not Created!", e)
            raise CommandError(e)
