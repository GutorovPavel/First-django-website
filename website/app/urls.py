from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('register/', register_page, name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('top/', index, name='top'),
    path('addpost/', add_post, name='addpost'),
    path('post/<slug:post_slug>/', show_post, name='post'),
    path('category/<slug:category_slug>/', show_category, name='category')
]
