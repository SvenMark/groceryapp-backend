from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from shoppinglist.models import ShoppingList, ShoppingItem
from shoppinglist.serializers import ShoppingListSerializer, ShoppingItemSerializer, ShoppingListTemplateSerializer


class ShoppingListViewSet(viewsets.ModelViewSet):
    serializer_class = ShoppingListSerializer

    def get_queryset(self):
        return ShoppingList.objects.lists().by_author(self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'])
    def to_template(self, request, pk=None):
        serializer = ShoppingListTemplateSerializer(data=request.data)
        if serializer.is_valid():
            try:
                shopping_list = ShoppingList.objects.get(pk=pk)
                shopping_template = shopping_list.to_template(name=serializer.data['name'])
                return Response(ShoppingListSerializer(shopping_template).data, status=status.HTTP_201_CREATED)
            except ObjectDoesNotExist:
                return Response({'error': 'shopping list does not exist'}, status=status.HTTP_404_NOT_FOUND)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ShoppingItemViewSet(viewsets.ModelViewSet):
    serializer_class = ShoppingItemSerializer

    def get_queryset(self):
        return ShoppingItem.objects.filter(shopping_list=self.kwargs['shopping_list_pk']).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(shopping_list_id=self.kwargs['shopping_list_pk'])

    def perform_update(self, serializer):
        serializer.save(shopping_list_id=self.kwargs['shopping_list_pk'])
