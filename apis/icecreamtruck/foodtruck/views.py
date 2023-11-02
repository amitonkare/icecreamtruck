import traceback
from datetime import datetime
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework import status as http_status
from django.db.models import Sum

from foodtruck.serializers import (
    FlavourSerializer,
    FoodItemFlavourSerializer,
    FoodItemSerializer,
    InventorySerializer,
    TruckDetailsSerializer,
    TruckSerializer,
    OrderSerializer,
)

from foodtruck.models import (
    FoodItem,
    Flavour,
    FoodItemFlavour,
    Truck,
    Inventory,
    Order,
    OrderItems,
)
from foodtruck.helpers import check_inventory, create_order


class OrderViewSet(viewsets.ViewSet):
    queryset = Order.objects.all().order_by("-created_at")
    permission_classes = [AllowAny]

    @action(detail=False, methods=["get"])
    def get_orders(self, request):
        """
        Get all orders sorted descendign by created dates
        """
        try:
            orders = Order.objects.all().order_by("-created_at")
            return Response(
                {"orders": OrderSerializer(orders, many=True).data},
                status=http_status.HTTP_200_OK,
            )
        except APIException as e:
            traceback.print_exc()
            return Response(
                {"detail": "Internal Server Error"},
                status=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=False, methods=["post"])
    def buy_food(self, request):
        """
        Create an order with food items for the given truck.
        """
        try:
            payload = request.data
            if len(payload["items"]) == 0:
                return Response(
                    {"detail": "Empty Order"},
                    status=http_status.HTTP_422_UNPROCESSABLE_ENTITY,
                )

            if not Truck.objects.filter(id=payload["truck"]).exists():
                return Response(
                    {"detail": "Invalid Truck"},
                    status=http_status.HTTP_422_UNPROCESSABLE_ENTITY,
                )

            available = check_inventory(payload["items"], payload["truck"])

            if available:
                order, total_price = create_order(payload)
                return Response(
                    {
                        "order_id": order.id,
                        "total_price": total_price,
                        "message": "Enjoy!",
                    },
                    status=http_status.HTTP_201_CREATED,
                )
            else:
                return Response(
                    {"detail": "Insufficient inventory", "message": "Sorry!"},
                    status=http_status.HTTP_422_UNPROCESSABLE_ENTITY,
                )
        except APIException as e:
            traceback.print_exc()
            return Response(
                {"detail": "Internal Server Error"},
                status=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        except Exception as e:
            traceback.print_exc()
            return Response(
                {"detail": "Internal Server Error"},
                status=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=False, methods=["get"])
    def todays_collection(self, request):
        """
        Return todays total collection from orders.
        """
        try:
            today_start = datetime.now().replace(
                hour=0, minute=0, second=0, microsecond=0
            )
            q = Order.objects.filter(
                created_at__gte=today_start,
            ).aggregate(todays_collection=Sum("total_price"))
            return Response(
                {"total_collection": q["todays_collection"]},
                status=http_status.HTTP_200_OK,
            )
        except APIException as e:
            traceback.print_exc()
            return Response(
                {"detail": "Internal Server Error"},
                status=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class InventoryViewSet(viewsets.ViewSet):
    queryset = Order.objects.all().order_by("-created_at")
    permission_classes = [AllowAny]

    @action(detail=False, methods=["post"])
    def get_inventory(self, request):
        """
        Get inventory for a given date
        """
        try:
            payload = request.data
            inventory = Inventory.objects.filter(
                truck=payload["truck"],
                date=datetime.strptime(payload["date"], "%Y-%m-%d"),
            ).prefetch_related("food_item_flavour")
            return Response(
                {"inventory": InventorySerializer(inventory, many=True).data},
                status=http_status.HTTP_200_OK,
            )
        except APIException as e:
            traceback.print_exc()
            return Response(e.detail, status=e.status_code)
        except Exception as e:
            traceback.print_exc()
            return Response(
                "Something went wrong",
                status=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class FlavourViewSet(viewsets.ModelViewSet):
    queryset = Flavour.objects.all()
    serializer_class = FlavourSerializer
    permission_classes = [AllowAny]


class FoodItemViewSet(viewsets.ModelViewSet):
    queryset = FoodItem.objects.all()
    serializer_class = FoodItemSerializer
    permission_classes = [AllowAny]


class FoodItemFlavourViewSet(viewsets.ModelViewSet):
    queryset = FoodItemFlavour.objects.all()
    serializer_class = FoodItemFlavourSerializer
    permission_classes = [AllowAny]


class TruckViewSet(viewsets.ViewSet):
    queryset = Truck.objects.all()
    serializer_class = TruckSerializer
    permission_classes = [AllowAny]

    @action(detail=True, methods=["get"])
    def details(self, request, pk):
        """
        Get details of a truck with its food items.
        """
        try:
            data = TruckDetailsSerializer(get_object_or_404(Truck,pk=pk)).data
            return Response(data, status=http_status.HTTP_200_OK)
        except APIException as e:
            traceback.print_exc()
            return Response({"detail": str(e)}, status=http_status.HTTP_500_INTERNAL_SERVER_ERROR)
