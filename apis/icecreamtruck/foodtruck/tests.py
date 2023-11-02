from datetime import datetime
import json
from pathlib import Path
import pytest
from django.test import TestCase, Client
from rest_framework import status as http_status

from foodtruck.models import Flavour, FoodItem, FoodItemFlavour, Truck, Inventory


class TestOrderViewSet(TestCase):
    def setUp(self) -> None:
        self.api_url = "http://localhost:8000/v1"
        self.c = Client()

        BASE_DIR = Path(__file__).resolve().parent
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

        truck = Truck.objects.create(name="Truck 1", address="E-Street", owner="Owner 1")

        food_item_flavours = FoodItemFlavour.objects.all()

        for fif in food_item_flavours:
            Inventory.objects.create(
                food_item_flavour=fif,
                truck=truck,
                quantity=20,
                date=datetime.now().date(),
            )


    # can retrieve all orders
    def test_retrieve_all_orders(self):
        response = self.c.get("/v1/order/get_orders/")
        # Check that the response status code is 200 OK
        assert response.status_code == http_status.HTTP_200_OK

        # Check that the response data contains the expected key "orders"
        assert "orders" in response.data

        # Check that the response data is a list
        assert isinstance(response.data["orders"], list)

    # can create a new order
    def test_create_new_order(self):
        payload = {
            "items": [
                {"food_item_flavour": 1, "quantity": 2},
                {"food_item_flavour": 2, "quantity": 3},
            ],
            "truck": 1,
        }

        response = self.c.post(
            "/v1/order/buy_food/", payload, content_type="application/json"
        )

        # Check that the response status code is 201 CREATED
        assert response.status_code == http_status.HTTP_201_CREATED

        # Check that the response data contains the expected keys "order_id", "total_price", and "message"
        assert "order_id" in response.data
        assert "total_price" in response.data
        assert "message" in response.data

    # can retrieve today's total collection
    def test_retrieve_todays_total_collection(self):
        # Make a GET request to retrieve today's total collection
        # response = order_viewset.todays_collection(request=None)
        response = self.c.get(
            "/v1/order/todays_collection/"
        )
        # Check that the response status code is 200 OK
        assert response.status_code == http_status.HTTP_200_OK

        # Check that the response data contains the expected key "total_collection"
        assert "total_collection" in response.data

    # empty order returns 422
    def test_empty_order_returns_422(self):
        # Create a mock request payload with an empty order
        payload = {"items": [], "truck": 1}

        # Make a POST request with an empty order
        response = self.c.post(
            "/v1/order/buy_food/", payload, content_type="application/json"
        )

        # Check that the response status code is 422 UNPROCESSABLE ENTITY
        assert response.status_code == http_status.HTTP_422_UNPROCESSABLE_ENTITY

        # Check that the response data contains the expected key "detail"
        assert "detail" in response.data

    # insufficient inventory returns 422
    def test_insufficient_inventory_returns_422(self):
        fif_id = FoodItemFlavour.objects.all().first().id
        truck_id = Truck.objects.all().first().id
        payload = {"items": [{"food_item_flavour": fif_id, "quantity": 25}], "truck": truck_id}

        # Make a POST request with insufficient inventory
        response = self.c.post(
            "/v1/order/buy_food/", payload, content_type="application/json"
        )

        # Check that the response status code is 422 UNPROCESSABLE ENTITY
        assert response.status_code == http_status.HTTP_422_UNPROCESSABLE_ENTITY

        # Check that the response data contains the expected keys "detail" and "message"
        assert "detail" in response.data
        assert "message" in response.data

    # invalid truck id returns 500
    def test_invalid_truck_id_returns_500(self):
        fif_id = FoodItemFlavour.objects.all().first().id
        payload = {"items": [{"food_item_flavour": fif_id, "quantity": 2}], "truck": 9999}
        response = self.c.post(
            "/v1/order/buy_food/", payload, content_type="application/json"
        )
        # Check that the response status code is 500 INTERNAL SERVER ERROR
        assert response.status_code == http_status.HTTP_422_UNPROCESSABLE_ENTITY

        # Check that the response data contains the expected key "detail"
        assert "detail" in response.data
