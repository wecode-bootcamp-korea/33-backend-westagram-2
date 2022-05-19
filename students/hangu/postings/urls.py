from django.urls import path

from .views import CommentsView, PostingView #, CommentSearchView

urlpatterns = [
    path('/write', PostingView.as_view()),
    path('/comment/<int:posting_id>', CommentsView.as_view()),
]
