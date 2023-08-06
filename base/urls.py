from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),
    path('', views.home, name="home"),
    path('set/<str:pk>/', views.set, name="set"),
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),
    path('create-set/', views.createSet, name="create-set"),
    path('update-set/<str:pk>/', views.updateSet, name="update-set"),
    path('delete-set/<str:pk>/', views.deleteSet, name="delete-set"),
    path('delete-card/<str:spk>/<str:cpk>/', views.deleteCard, name="delete-card"),
]