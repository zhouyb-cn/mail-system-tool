from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('handle/result', views.handleResult, name='handle.result'),
]