from django.urls import path
from news import views

urlpatterns=[ 
    path('', views.index, name = "home"),
    path('login',views.login_view,name="login"),
     path('logout',views.logout_view,name="logout"),
     path('register',views.register,name="register"),
]