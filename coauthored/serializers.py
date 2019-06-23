from rest_framework import serializers

from shoppinglist.models import ShoppingList


class AddUserToCoAuthorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingList
        fields = ['id', 'coauthors']