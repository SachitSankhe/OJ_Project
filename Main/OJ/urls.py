from django.urls import path

from . import views

app_name = 'oj'

urlpatterns = [
    path('problems/', views.index , name = 'index'),
    path('<int:problem_id>/', views.details, name = 'details'),
    path('submission', views.submission,name='submission'),
]
