from rest_framework import serializers
from rest_framework.exceptions import NotFound

from django.shortcuts import get_list_or_404, get_object_or_404

from shoppinglist.models import ShoppingList, ShoppingItem


class ShoppingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingList
        fields = ['id', 'name']


class ShoppingItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingItem
        fields = ['id', 'description']

    def save(self, **kwargs):
        shopping_list_id = kwargs.pop('shopping_list_id')
        shopping_list = get_object_or_404(ShoppingList, pk=shopping_list_id)
        kwargs['shopping_list'] = shopping_list
        instance = super(ShoppingItemSerializer, self).save(**kwargs)
        return instance
