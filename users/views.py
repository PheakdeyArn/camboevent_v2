from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from content.models import EventDetailPage


@login_required
def profile_view(request):
    return render(request,
                  'account/profile.html',
                  {'section': 'profile'})


@ login_required
def favourite_event_list(request):
    new = EventDetailPage.objects.filter(favourites=request.user)
    return render(request,
                  'account/favourites.html',
                  {'new': new})

@ login_required
def favourite_event_add(request, id):
    post = get_object_or_404(EventDetailPage, id=id)
    if post.favourites.filter(id=request.user.id).exists():
        post.favourites.remove(request.user)
    else:
        post.favourites.add(request.user)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

