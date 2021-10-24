from django.urls import path
from news import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[ 
    path('', views.index, name = "home"),
    path('login',views.login_view,name="login"),
     path('logout',views.logout_view,name="logout"),
     path('register',views.register,name="register"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)