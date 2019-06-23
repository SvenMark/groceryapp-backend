from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from shoppinglist.models import ShoppingList, ShoppingItem
from shoppinglist.serializers import ShoppingListTemplateSerializer, ShoppingListSerializer
from templating.serializers import TemplateSerializer, TemplateItemSerializer


class TemplateViewSet(viewsets.ModelViewSet):
    serializer_class = TemplateSerializer

    def get_queryset(self):
        return ShoppingList.objects.templates().by_author(self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, is_template=True)

    @action(detail=True, methods=['post'])
    def from_template(self, request, pk=None):
        serializer = ShoppingListTemplateSerializer(data=request.data)
        if serializer.is_valid():
            try:
                shopping_template = ShoppingList.objects.get(pk=pk)
                shopping_list = shopping_template.from_template(name=serializer.data['name'])
                return Response(ShoppingListSerializer(shopping_list).data, status=status.HTTP_201_CREATED)
            except ObjectDoesNotExist:
                return Response({'error': 'shopping list does not exist'}, status=status.HTTP_404_NOT_FOUND)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TemplateItemViewSet(viewsets.ModelViewSet):
    serializer_class = TemplateItemSerializer

    def get_queryset(self):
        return ShoppingItem.objects.filter(shopping_list=self.kwargs['shopping_list_pk']).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(shopping_list_id=self.kwargs['shopping_list_pk'])
