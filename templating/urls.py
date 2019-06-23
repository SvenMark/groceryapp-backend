"""shoppinglist URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from rest_framework_nested import routers
from templating.views import TemplateItemViewSet, TemplateViewSet

router = routers.SimpleRouter()
# no prefix because it is handled in the urlconfig
router.register(r'', TemplateViewSet, base_name='ShoppingItem')

shopping_list_router = routers.NestedSimpleRouter(router, r'', lookup='shopping_list')
shopping_list_router.register(r'templateitems', TemplateItemViewSet, base_name='ShoppingItem')

urlpatterns = router.urls + shopping_list_router.urls
