from django.urls import path

from . import views

urlpatterns = [
    path('problems/', views.index , name = 'index')
]
