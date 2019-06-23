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


class ShoppingListQuerySet(models.QuerySet):
    def templates(self):
        return self.filter(is_template=True)

    def lists(self):
        return self.filter(is_template=False)

    def by_author(self, user):
        return self.filter(author=user)

    def co_authored(self, user):
        return user.co_authored_lists.all()


class ShoppingListManager(models.Manager):
    def get_queryset(self):
        return ShoppingListQuerySet(self.model, using=self._db)

    def templates(self):
        return self.get_queryset().templates()

    def lists(self):
        return self.get_queryset().lists()

    def by_author(self, user):
        return self.get_queryset().by_author(user)

    def co_authored(self, user):
        return self.get_queryset().co_authored(user)


class ShoppingList(TimestampMixin, models.Model):
    """
    A shoppinglist is a list which contains shoppingitems
    """
    name = models.CharField(_('name'), max_length=128)
    is_template = models.BooleanField(_('template'), default=False)

    author = models.ForeignKey(AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, related_name='shopping_lists')

    co_authors = models.ManyToManyField(AUTH_USER_MODEL, related_name='co_authored_lists')

    objects = ShoppingListManager()

    class Meta:
        verbose_name = _('shopping list')
        verbose_name_plural = _('shopping lists')

    def __str__(self):
        return self.name

    def to_template(self, name):
        shopping_items = self.shopping_items.all()
        self.id = None
        self.name = name
        self.is_template = True
        self.save()
        for shopping_item in shopping_items:
            shopping_item.duplicate(self)
        return self

    def from_template(self, name):
        shopping_items = self.shopping_items.all()
        self.id = None
        self.name = name
        self.is_template = False
        self.save()
        for shopping_item in shopping_items:
            shopping_item.duplicate(self)
        return self


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

    def duplicate(self, shopping_list):
        self.id = None
        self.shopping_list = shopping_list
        self.save()
        return self
