from django.urls import include, path
from .views import (
    like_event_add,
    like_scholarship_add
)

urlpatterns = [
    path('like_event/<int:id>', like_event_add, name='like_event_add'),
    path('like_scholarship/<int:id>', like_scholarship_add, name='like_scholarship_add')
]
