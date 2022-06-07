from django.urls import include, path

from .views import profile_view

urlpatterns = [
    path('/', include('allauth.urls')),
    path('/profile/', profile_view, name='account_profile'),

]