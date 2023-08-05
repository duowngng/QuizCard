from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('set/<str:pk>/', views.set, name="set"),
    path('create-set/', views.createSet, name="create-set"),
    path('update-set/<str:pk>/', views.updateSet, name="update-set"),
    path('delete-set/<str:pk>/', views.deleteSet, name="delete-set"),
]