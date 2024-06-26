"""
URL configuration for My_Blog_Site project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from blog import views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include

urlpatterns = [
    path('admin/', admin.site.urls,name='admin'),
    path('',views.IndexView,name='index'),
    path('register/',views.UserRegister,name='register'),
    path('details/<int:pk>',views.BlogDetailView,name='detail'),
    path('profile/',views.UserProfile,name='profile'),
    path('logout/',views.UserLogout,name="logout"),
    path('login/',views.UserLogin,name='login'),
    path('dashboard/',views.Dashboard,name='dashboard'),
    path('post/',include('blog.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)