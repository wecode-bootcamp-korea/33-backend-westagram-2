from django.urls import path
from postings.views import PostingView, PostingSearchView

urlpatterns = [
    path('/post', PostingView.as_view()),
    path('/search/<int:user_id>', PostingSearchView.as_view()),
    ]