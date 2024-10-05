
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

app_name ="Home"

urlpatterns = [
    path("", views.index, name="home"),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('activate/<uidb64>/<token>/', views.activate_account, name='activate'),
    path('chat/', views.chat_view, name="chat"),
    path("logout/", views.custom_logout, name="logout"),


]