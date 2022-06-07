from django.urls import include, path

from .views import profile_view, favourite_event_add, favourite_event_list, favourite_scholarship_add

urlpatterns = [
    path('', include('allauth.urls')),
    path('profile/', profile_view, name='account_profile'),
    path('profile/favourite_events/', favourite_event_list, name='favourite_event_list'),
    path('fav_event/<int:id>', favourite_event_add, name='favourite_event_add'),
    path('fav_scholarship/<int:id>', favourite_scholarship_add, name='favourite_scholarship_add'),

]