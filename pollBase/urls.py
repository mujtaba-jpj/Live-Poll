
from django.contrib import admin
from django.urls import path
from django.urls import include
from mainPoll import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('poll/', include('mainPoll.urls')),
    path("", views.index, name="home"),
    path('accounts/', include('allauth.urls')),
]
