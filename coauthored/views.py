from rest_framework import viewsets
from rest_framework.decorators import action

from coauthored.serializers import AddUserToCoAuthorsSerializer
from shoppinglist.models import ShoppingList
from shoppinglist.serializers import ShoppingListSerializer


class CoAuthoredListViewSet(viewsets.ModelViewSet):
    serializer_class = ShoppingListSerializer

    def get_queryset(self):
        return ShoppingList.objects.lists().co_authored(self.request.user).order_by('-created_at')

    @action(detail=False, methods=['post'])
    def add_to_list(self, request):
        serializer = AddUserToCoAuthorsSerializer(data=request.data)
        pass

