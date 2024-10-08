"""latiphonics URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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

from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from rest_framework import routers
from latiphonicsapi.views import check_user, register_user, delete_user, get_user, update_user, SymbolView, AddSymbolToListView, LearningItemSymbolView, LearningSymbolView,  NoteView

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'symbol',SymbolView, basename='symbol')
router.register(r'add-symbol',AddSymbolToListView, basename='add-symbol')
router.register(r'learn-item-symbol', LearningItemSymbolView, basename='learn-item-symbol')
router.register(r'learning-symbol', LearningSymbolView, basename='learning-symbol')
router.register(r'note', NoteView, basename='note')


urlpatterns = [
    path('', include(router.urls)),
    path("admin/", admin.site.urls),
    path("register", register_user),
    path('checkuser', check_user, name='check_user'),
    path('delete_user', delete_user),
    path('get_user', get_user),
    path('update_user', update_user)

]
