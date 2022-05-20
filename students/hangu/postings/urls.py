from django.urls import path

from .views import CommentsView, LikeCountView, PostingView 

urlpatterns = [
    path('/write', PostingView.as_view()),
    path('/comment/<int:posting_id>', CommentsView.as_view()),
    path('/likecount/<int:posting_id>', LikeCountView.as_view()),
]
