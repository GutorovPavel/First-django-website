from django.urls import path
from .views import *

urlpatterns = [
    path('home/', Home.as_view(), name='index'),
    path('register/', Register.as_view(), name='register'),
    path('', Login.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    # path('top/', index, name='top'),
    path('addpost/',  AddPost.as_view(), name='addpost'),
    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),
    path('category/<slug:category_slug>/', ShowCategory.as_view(), name='category')
]
