from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.exceptions import NotFound

from shoppinglist.models import ShoppingList, ShoppingItem
from shoppinglist.serializers import ShoppingListSerializer, ShoppingItemSerializer


class ShoppingListViewSet(viewsets.ModelViewSet):
    serializer_class = ShoppingListSerializer

    def get_queryset(self):
        return ShoppingList.objects.all().order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ShoppingItemViewSet(viewsets.ModelViewSet):
    serializer_class = ShoppingItemSerializer

    def get_queryset(self):
        return ShoppingItem.objects.filter(shopping_list=self.kwargs['shopping_list_pk']).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(shopping_list_id=self.kwargs['shopping_list_pk'])

    def perform_update(self, serializer):
        serializer.save(shopping_list_id=self.kwargs['shopping_list_pk'])
