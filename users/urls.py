from django.urls import path

from users import views

urlpatterns = [
    path('signin', views.SigninView.as_view()),
    path("signup", views.SignupView.as_view()),
    path("me", views.UserView.as_view())
]
