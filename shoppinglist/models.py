from django.db import models

# Create your models here.
from django.utils import timezone

from groceryapp.settings import AUTH_USER_MODEL

from django.utils.translation import ugettext_lazy as _


class TimestampMixin(models.Model):
    """Add created and modified timestamps to a model."""
    created_at = models.DateTimeField(_('created at'), default=timezone.now)
    modified_at = models.DateTimeField(_('modified_at'), auto_now=True)

    class Meta:
        abstract = True


class ShoppingList(TimestampMixin, models.Model):
    """
    A shoppinglist is a list which contains shoppingitems
    """
    name = models.CharField(_('name'), max_length=128)

    author = models.ForeignKey(AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, related_name='shopping_lists')

    class Meta:
        verbose_name = _('shopping list')
        verbose_name_plural = _('shopping lists')

    def __str__(self):
        return self.name


class ShoppingItem(TimestampMixin, models.Model):
    """
    A shoppingitem is a item which is included in a shoppinglist
    """
    description = models.CharField(_('description'), max_length=256)
    done = models.BooleanField(_('done'), default=False)

    shopping_list = models.ForeignKey(ShoppingList, on_delete=models.CASCADE, related_name='shopping_items')

    class Meta:
        verbose_name = _('shopping item')
        verbose_name_plural = _('shopping items')

    def __str__(self):
        return self.description
