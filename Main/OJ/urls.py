from django.urls import path

from . import views

app_name = 'oj'

urlpatterns = [
    path('problems/', views.index , name = 'index'),
    path('problems/<int:problem_id>/', views.details, name = 'details'),
    path('problems/<int:problem_id>/submit/', views.submission, name='submission'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
]