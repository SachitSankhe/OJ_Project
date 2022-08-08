from . import views
from django.urls import path

app_name = 'accounts'

urlpatterns = [
    path("",views.home,name="home"),
    path("register/",views.registration_page,name="registration_page"),
    path("register/submit",views.register,name="register"),
    path("login/",views.login,name="login"),
    path('logout/',views.logout,name='logout'),
]