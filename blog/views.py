from django.contrib import auth
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import PostForm, SigninForm, SignupForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.http.response import HttpResponseRedirect
from django.urls.base import reverse
from django.contrib.auth import logout


# Create your views here.

def firstpage(request):
    return render(request, 'blog/j2kbfirstpage.html')


def homepage(request):
    return render(request, 'blog/homepage.html')


def about_us(request):
    return render(request, 'blog/j2kbaboutus.html')


def contact_us(request):
    return render(request, 'blog/j2kbcontactus.html')


def photopage(request):
    return render(request, 'blog/j2kbphotopage.html')


def memo(request):
    return render(request, 'blog/j2kbmemopage.html')


def todolist(request):
    return render(request, 'blog/j2kbtodolistpage.html')


def generalforum(request):
    return render(request, 'blog/j2kbgeneralforum.html')


def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user.get_username()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})


@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)


@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author == User.objects.get(username = request.user.get_username()):
        post.delete()
        return post_list(request)


def signup(request):
    if request.method == "GET":
        return render(request, 'registration/signup.html', {'f': SignupForm()})

    elif request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['password'] == form.cleaned_data['password_check']:
                new_user = User.objects.create_user(form.cleaned_data['username'],
                                                    form.cleaned_data['email'],
                                                    form.cleaned_data['password'])
                new_user.last_name = form.cleaned_data['last_name']
                new_user.first_name = form.cleaned_data['first_name']
                new_user.save()

                return redirect('homepage')

            else:
                return render(request, 'registration/signup.html', {'f': form,
                                                                    'error': '입력하신 비밀번호와 다릅니다.'})
        else:
            return render(request, 'registration/signup.html', {'f': form})


def signin(request):
    if request.method == "GET":
        return render(request, 'registration/signin.html', {'f': SigninForm()})

    elif request.method == "POST":
        form = SigninForm(request.POST)
        id = request.POST['username']
        pw = request.POST['password']
        u = authenticate(username=id, password=pw)

        if u:
            auth.login(request, user=u)
            return HttpResponseRedirect(reverse('homepage'))
        else:
            return render(request, 'registration/signin.html', {'f': form, 'error': '아이디나 비밀번호가 일치하지 않습니다.'})


def signout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('first_page'))
