from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.db.models import Q
from django.views import View
from .modelForms import *


class RegisterView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            form = RegistrationForm()
            return render(request, "user/register.html", {"form": form})
        return redirect("/feed")

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")
        return render(request, "user/register.html", {"form": form})


class LoginView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, "user/login.html", {})
        return redirect("/feed")

    def post(self, request):
        data = request.POST
        context = {"message": None}
        user = authenticate(request, username=data["username"], password=data["password"])
        if user is not None:
            login(request, user)
            return redirect("/feed")
        else:
            context["message"] = "Email or password wrong."
        return render(request, "user/login.html", context)


class LogoutView(LoginRequiredMixin, View):
    login_url = "/"

    def get(self, request):
        logout(request)
        return redirect("/")


class MessageView(LoginRequiredMixin, View):
    login_url = "/"

    def get(self, request):
        questions = (
            Message.objects.prefetch_related("comments__likes", "message_like")
            .filter(Q(active=True) & ~Q(author=request.user.id))
            .order_by("-created_at")
        )
        user_likes = MessageLike.objects.filter(user=request.user).values_list("message", flat=True)
        form = MessageForm()
        ansForm = CommentForm()
        return render(
            request,
            "question/home.html",
            {"form": form, "questions": questions, "answer": ansForm, "user_likes": user_likes},
        )

    def post(self, request):
        data = request.POST.copy()
        data["author"] = request.user.id
        form = MessageForm(data)
        if form.is_valid():
            form.save()
            return redirect("/feed")


class CommentView(LoginRequiredMixin, View):
    login_url = "/"

    def post(self, request, id):
        data = request.POST.copy()
        data["author"] = request.user.id
        data["message"] = id
        form = CommentForm(data)
        if form.is_valid():
            form.save()
            return redirect("/feed")


class LikeView(LoginRequiredMixin, View):
    login_url = "/"

    def get(self, request, id):
        comment = get_object_or_404(Comment, id=id)  # Get the answer object
        if comment.author == request.user:
            return JsonResponse({"message": "You cannot like your own answer."}, status=403)
        likeExist = Like.objects.filter(user=request.user.id, comment=id)
        if likeExist.exists():
            likeExist.delete()
            return JsonResponse({"message": "Like has been Removed", "liked": False})
        data = {"user": request.user.id, "comment": id}
        form = LikeForm(data)
        if form.is_valid():
            form.save()
            return JsonResponse({"message": "Liked the answer", "liked": True})
        return JsonResponse({"message": "Something went wrong"}, status=400)


class UserPostView(LoginRequiredMixin, View):
    login_url = "/"

    def get(self, request):
        posts = (
            Message.objects.prefetch_related(
                "message_like",
            )
            .filter(active=True, author=request.user.id)
            .order_by("-id")
        )
        return render(request, "post/myPost.html", {"data": posts})

    def delete(self, request, id):
        try:
            post = Message.objects.get(id=id, author=request.user.id)
            post.delete()
            return JsonResponse({"message": "Post has been removed"}, status=200)
        except:
            return JsonResponse({"message": "Post not found"}, status=404)


class MessageLikeView(LoginRequiredMixin, View):
    login_url = "/"

    def get(self, request, id):
        try:
            likeExist = MessageLike.objects.filter(user=request.user.id, message=id)
            if likeExist.exists():
                likeExist.delete()
                return JsonResponse({"message": "Like has been Removed", "liked": False}, status=200)
            data = {"user": request.user.id, "message": id}
            form = MessageLikeForm(data)
            if form.is_valid():
                form.save()
                return JsonResponse({"message": "Liked the Post", "liked": True}, status=201)
            return JsonResponse({"message": "Something went wrong"}, status=400)
        except:
            return JsonResponse({"message": "Post not found"}, status=404)
