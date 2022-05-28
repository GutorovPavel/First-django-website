from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView

from .models import *
from .forms import *

# Create your views here.

main = 'RAP NEWS:  '


menu = [
    {'title': 'Новая статья', 'url_name': 'addpost'},
]


# class Home(ListView):
#     model = Artist
#     template_name = 'app/index.html'
#     context_object_name = 'artists'
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)  # получение уже заданного контекста
#         context['menu'] = menu
#         context['title'] = main + 'Home'
#         return context


def index(request):
    context = {
        'menu': menu,
        'artists': Artist.objects.all(),
        'cats': Category.objects.all(),
        'cat_selected': 0,
    }
    return render(request, 'app/index.html', context=context)


def show_category(request, category_slug):
    artists = Artist.objects.filter(category__slug=category_slug)
    cats = Category.objects.all()

    context = {
        'artists': artists,
        'cats': cats,
        'menu': menu,
        'cat_selected': category_slug,
    }

    return render(request, 'app/index.html', context=context)


def show_post(request, post_slug):
    post = get_object_or_404(Artist, slug=post_slug)
    cats = Category.objects.all()

    context = {
        'post': post,
        'cats': cats,
        'menu': menu,
        'cat_selected': post.category_id,
    }

    return render(request, 'app/post.html', context=context)


def add_post(request):
    form = AddPostForm()

    if request.method == "POST":
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')

    context = {
        'form': form,
        'menu': menu,
        'title': 'Новая статья'
    }

    return render(request, 'app/addpost.html', context=context)

def register_page(request):
    form = RegisterUserForm()

    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, user + ' is successfully registered!')
            return redirect('login')

    context = {
        'menu': menu,
        'title': "Registration",
        'form': form,
    }
    return render(request, 'app/register.html', context=context)


# def login_user(request):
#     form = LoginForm()
#
#     if request.method == "POST":
#         form = LoginForm(request.POST)
#
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#
#             user = authenticate(request, username=username, password=password)
#
#             if user is not None:
#                 login(request, user)
#                 return redirect('index')
#             else:
#                 messages.info(request, 'Username or Password is incorrect')
#                 return redirect('login')
#
#     context = {
#         'menu': menu,
#         'title': 'Authentication',
#         'form': form
#     }
#     return render(request, 'app/login.html', context=context)


class DataMixin:

    def get_user_context(self, **kwargs):
        context = kwargs
        categories = Category.objects.all()
        context['menu'] = menu
        context['categories'] = categories
        return context


class LoginUser(DataMixin, LoginView):
    form_class = LoginForm
    template_name = 'app/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))


def logout_user(request):
    logout(request)
    return redirect('login')
