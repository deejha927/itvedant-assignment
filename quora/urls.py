from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .views import *

urlpatterns = [
    path("", LoginView.as_view(), name="login-view"),
    path("register/", RegisterView.as_view(), name="register-view"),
    path("logout/", LogoutView.as_view(), name="logout-view"),
    path("feed/", MessageView.as_view(), name="question-view"),
    path("answer/<int:id>/", CommentView.as_view(), name="answer-view"),
    path("like/<int:id>/", LikeView.as_view(), name="like-view"),
    path("posts/", UserPostView.as_view(), name="user-post-view"),
    path("posts/<int:id>/", csrf_exempt(UserPostView.as_view()), name="user-post-view"),
    path("postslike/<int:id>/", MessageLikeView.as_view(), name="message-like-view"),
]
