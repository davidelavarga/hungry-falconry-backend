"""hungryFalconryRest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken import views as rest_views

from hfr_app import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('hello/', views.HelloView.as_view(), name='hello'),
    url(r'^api-token-auth/', rest_views.obtain_auth_token),
    path('feeders/', views.FeederList.as_view()),
    path('feeders/<int:pk>/', views.FeederDetail.as_view()),
    path('feeders/<int:pk>/schedules/', views.ScheduleList.as_view()),
    path('feeders/<int:pk>/schedules/<slug_scheduler>/', views.ScheduleDetail.as_view()),
]
