from django.urls import path

from users.views import SignupView, LoginView, FollowView

urlpatterns = [
    path('/signup', SignupView.as_view()),
    path('/login', LoginView.as_view()),
    path('/follow/<int:user_id>', FollowView.as_view()),
]
