from django.urls import path
from . import views

urlpatterns = [
    path('<int:poll_id>', views.poll,name="poll"),
    path('login/', views.LoginUser, name="login-user"),
    path('logout/', views.LogoutUser, name='logout-user'),
    path('create-poll/', views.createPoll, name='create-poll'),
    path('my-polls/',views.myPolls,name="my-polls")
]
