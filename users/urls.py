from django.urls import include, path

from .views import (
    profile_view,
    favourite_event_add,
    favourite_contents,
    favourite_scholarship_add,
    favourite_events,
    favourite_scholarships
)

urlpatterns = [
    path('', include('allauth.urls')),
    path('profile/', profile_view, name='account_profile'),
    path('profile/favourite_contents/', favourite_contents, name='favourite_contents'),
    path('profile/favourite_events/', favourite_events, name='favourite_events'),
    path('profile/favourite_shcolarships/', favourite_scholarships, name='favourite_scholarships'),
    path('fav_event/<int:id>', favourite_event_add, name='favourite_event_add'),
    path('fav_scholarship/<int:id>', favourite_scholarship_add, name='favourite_scholarship_add'),

]