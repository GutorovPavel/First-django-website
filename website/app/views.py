import asyncio
import logging

from asgiref.sync import sync_to_async
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.views.generic.edit import FormMixin, FormView
from hitcount.views import HitCountDetailView

from .models import *
from .forms import *
from .utils import *

# Create your views here.

logger = logging.getLogger('django')


@sync_to_async
def get_published_posts():
    return Artist.objects.filter(is_published=True)


@sync_to_async
def get_category_posts(category_slug):
    return Artist.objects.filter(category__slug=category_slug, is_published=True)


@sync_to_async
def get_post_comments(post_slug):
    return Comment.objects.filter(post__slug=post_slug, user__blocked=False)


class Home(DataMixin, ListView):
    model = Artist
    template_name = 'app/index.html'
    context_object_name = 'artists'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)  # получение уже заданного контекста
        c_def = self.get_user_context(title=main + 'Home')
        context.update(c_def)
        return context

    def get_queryset(self):
        return asyncio.run(get_published_posts())


class ShowCategory(DataMixin, ListView):
    model = Artist
    template_name = 'app/index.html'
    context_object_name = 'artists'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=main + context['artists'][0].category.name,
                                      cat_selected=context['artists'][0].category_id)
        context.update(c_def)
        return context

    def get_queryset(self):
        return asyncio.run(get_category_posts(self.kwargs['category_slug']))


class ShowPost(DataMixin, HitCountDetailView):
    model = Artist
    template_name = 'app/post.html'
    slug_url_kwarg = 'post_slug'
    count_hit = True

    context_object_name = 'post'

    form = CommentForm

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            post = self.get_object()
            form.instance.user = request.user
            form.instance.post = post
            form.save()

            return redirect(reverse('post', kwargs={'post_slug': post.slug}))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form
        c_def = self.get_user_context(title=main + context['post'].nick,
                                      comments=asyncio.run(get_post_comments(self.kwargs['post_slug'])))
        context.update(c_def)
        return context


class AddPost(DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'app/addpost.html'
    success_url = reverse_lazy('index')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=main + 'Новая статья')
        context.update(c_def)
        return context

class UpdatePost(DataMixin, UpdateView):
    model = Artist
    form_class = AddPostForm
    slug_url_kwarg = 'post_slug'
    template_name = 'app/updatepost.html'
    success_url = reverse_lazy('index')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=main + 'Новая статья')
        context.update(c_def)
        return context


class DeletePost(DataMixin, DeleteView):
    model = Artist
    slug_url_kwarg = 'post_slug'
    template_name = 'app/deletepost.html'
    success_url = reverse_lazy('index')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=main + 'Новая статья')
        context.update(c_def)
        return context

#
# def index(request):
#     context = {
#         'menu': menu,
#         'artists': Artist.objects.all(),
#         'cats': Category.objects.all(),
#         'cat_selected': 0,
#     }
#     return render(request, 'app/index.html', context=context)
#
#
# def show_category(request, category_slug):
#     artists = Artist.objects.filter(category__slug=category_slug)
#     cats = Category.objects.all()
#
#     context = {
#         'artists': artists,
#         'cats': cats,
#         'menu': menu,
#         'cat_selected': category_slug,
#     }
#
#     return render(request, 'app/index.html', context=context)
#
#
# def show_post(request, post_slug):
#     post = get_object_or_404(Artist, slug=post_slug)
#     cats = Category.objects.all()
#
#     context = {
#         'post': post,
#         'cats': cats,
#         'menu': menu,
#         'cat_selected': post.category_id,
#     }
#
#     return render(request, 'app/post.html', context=context)
#
#
# def add_post(request):
#     form = AddPostForm()
#
#     if request.method == "POST":
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('index')
#
#     context = {
#         'form': form,
#         'menu': menu,
#         'title': 'Новая статья'
#     }
#
#     return render(request, 'app/addpost.html', context=context)
#
#
# def register_page(request):
#     form = RegisterUserForm()
#
#     if request.method == "POST":
#         form = RegisterUserForm(request.POST)
#         if form.is_valid():
#             form.save()
#             user = form.cleaned_data.get('username')
#             messages.success(request, user + ' is successfully registered!')
#             return redirect('login')
#
#     context = {
#         'menu': menu,
#         'title': "Registration",
#         'form': form,
#     }
#     return render(request, 'app/register.html', context=context)


class Register(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'app/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=main + 'Регистрация')
        context.update(c_def)
        return context


class Login(DataMixin, LoginView):
    form_class = LoginForm
    template_name = 'app/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=main + "Авторизация")
        context.update(c_def)
        return context

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
            return redirect('index')
        else:
            messages.success(self.request, 'Error, Try again')
            return redirect('login')


def logout_user(request):
    logout(request)
    return redirect('login')







