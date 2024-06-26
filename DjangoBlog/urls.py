"""DjangoBlog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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

from api import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    # path('db/', views.db), # 创建一些数据

    path('api/blog/', views.BlogView.as_view()),
    path('api/blog/<int:pk>/', views.BlogDetailView.as_view()),
    path('api/comment/<int:blog_id>/', views.CommentView.as_view()),

    path('api/register/', views.RegisterView.as_view()),
    path('api/login/', views.LoginView.as_view()),

    path('api/favor/', views.FavorView.as_view()),

]
