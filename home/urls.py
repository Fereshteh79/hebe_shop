from django.core.cache import cache
from django.urls import path
from django.views.decorators.cache import cache_page

from . import views

app_name = 'home'
urlpatterns = [
    path('', cache_page(60* 1)(views.Home.as_view()), name='home')
]