from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from shoppinglist.models import ShoppingList, ShoppingItem


class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingList
        fields = ['id', 'name']


class TemplateItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingItem
        fields = ['id', 'description']

    def save(self, **kwargs):
        shopping_list_id = kwargs.pop('shopping_list_id')
        shopping_list = get_object_or_404(ShoppingList, pk=shopping_list_id)
        kwargs['shopping_list'] = shopping_list
        instance = super(TemplateItemSerializer, self).save(**kwargs)
        return instance
