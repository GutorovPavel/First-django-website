from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView
from django.views.generic.edit import FormMixin

from .models import *
from .forms import *
from .utils import *

# Create your views here.


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
        return Artist.objects.filter(is_published=True)


class ShowCategory(DataMixin, ListView):
    model = Artist
    template_name = 'app/index.html'
    context_object_name = 'artists'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=main + context['artists'][0].category.name,
                                      cat_selected=context['artists'][0].category_id)
        context.update(c_def)
        return context

    def get_queryset(self):
        return Artist.objects.filter(category__slug=self.kwargs['category_slug'], is_published=True)


class ShowPost(DataMixin, FormMixin, DetailView):
    model = Artist
    template_name = 'app/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    form_class = CommentForm

    def get_success_url(self):
        return reverse('post', kwargs={'slug': self.object.slug})

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm(initial={'post': self.object})
        c_def = self.get_user_context(title=main + context['post'].nick,
                                      comments=Comment.objects.filter(post__slug=self.kwargs['post_slug']))
        context.update(c_def)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.post = Artist.objects.get(slug=self.kwargs['post_slug'])
        obj.save()
        return super().form_valid(form)


class AddPost(DataMixin, CreateView):
    model = Artist
    form_class = AddPostForm
    template_name = 'app/addpost.html'
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







