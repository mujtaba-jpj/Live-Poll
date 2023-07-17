
from django.contrib import admin
from django.urls import path
from django.urls import include
from graphs import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('poll/', include('graphs.urls')),
    path("", views.index, name="home"),
    path('accounts/', include('allauth.urls')),
]
