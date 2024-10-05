from django.urls import path, include
from . import views
app_name ="Colaborate"
urlpatterns = [
  path("",views.colaborate, name="colaborate"),

]
