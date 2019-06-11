from django.contrib import admin

# Register your models here.
from shoppinglist.models import ShoppingItem, ShoppingList

admin.site.register(ShoppingItem)
admin.site.register(ShoppingList)
