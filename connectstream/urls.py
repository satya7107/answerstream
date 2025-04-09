from django.urls import path
from . import views
from .views import login_view, register
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', views.home, name='home'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('ask/', views.ask_question, name='ask_question'),
    path('answer/<int:question_id>/', views.submit_answer, name='submit_answer'),
    path('like/<int:answer_id>/', views.like_answer, name='like_answer'),
   
]
