from django.urls import path

from .views import PostingView

urlpatterns = [
    path('/write', PostingView.as_view())
]
