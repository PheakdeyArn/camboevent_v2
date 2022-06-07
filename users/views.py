from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from content.models import EventDetailPage, ScholarshipDetailPage


@login_required
def profile_view(request):
    return render(
        request,
        'account/profile.html',
        {'section': 'profile'}
    )


@ login_required
def favourite_event_list(request):
    fav_events = EventDetailPage.objects.filter(favourites=request.user)
    fav_scholarships = ScholarshipDetailPage.objects.filter(favourites=request.user)
    return render(
        request,
        'account/favourites.html',
        {'fav_events': fav_events, 'fav_scholarships': fav_scholarships},
    )

@ login_required
def favourite_event_add(request, id):
    post = get_object_or_404(EventDetailPage, id=id)
    if post.favourites.filter(id=request.user.id).exists():
        post.favourites.remove(request.user)
    else:
        post.favourites.add(request.user)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@ login_required
def favourite_scholarship_add(request, id):
    post = get_object_or_404(ScholarshipDetailPage, id=id)
    if post.favourites.filter(id=request.user.id).exists():
        post.favourites.remove(request.user)
    else:
        post.favourites.add(request.user)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

