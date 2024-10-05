# urls.py

from django.urls import path
from .views import project_list, create_project, join_project,project_detail
app_name= "Collaboration"

   
urlpatterns = [
    path('', project_list, name='project_list'),
    path('create/', create_project, name='create_project'),
    path('join/<int:project_id>/', join_project, name='join_project'),
    path('project/<int:project_id>/', project_detail, name='project_detail'),
]

