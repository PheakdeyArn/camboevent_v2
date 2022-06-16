from django.urls import include, path
from .views import (
    like_blog_add
)

urlpatterns = [
    path('like_blog/<int:id>', like_blog_add, name='like_blog_add')
]


