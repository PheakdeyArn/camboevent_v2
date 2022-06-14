from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from content.models import EventDetailPage, ScholarshipDetailPage
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


@login_required
def profile_view(request):
    return render(
        request,
        'account/profile.html',
        {'section': 'profile'}
    )


@ login_required
def favourite_contents(request):
    fav_events = EventDetailPage.objects.filter(favourites=request.user)[:4]
    fav_scholarships = ScholarshipDetailPage.objects.filter(favourites=request.user)[:4]
    return render(
        request,
        'account/favourites.html',
        {'fav_events': fav_events, 'fav_scholarships': fav_scholarships},
    )

@ login_required
def favourite_events(request):
    all_posts = EventDetailPage.objects.filter(favourites=request.user)

    paginator = Paginator(all_posts, 5)
    # Try to get the ?page=x value
    page = request.GET.get("page")
    # category = request.GET.get('category')

    try:
        # If the page exists and the ?page=x is an int
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If the ?page=x is not an int; show the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If the ?page=x is out of range (too high most likely)
        # Then return the last page
        posts = paginator.page(paginator.num_pages)

    return render(
        request,
        'account/all_favourites.html',
        {'posts': posts, 'title': 'Favourite Events'},
    )

@ login_required
def favourite_scholarships(request):
    all_posts = ScholarshipDetailPage.objects.filter(favourites=request.user)

    paginator = Paginator(all_posts, 5)
    # Try to get the ?page=x value
    page = request.GET.get("page")
    # category = request.GET.get('category')

    try:
        # If the page exists and the ?page=x is an int
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If the ?page=x is not an int; show the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If the ?page=x is out of range (too high most likely)
        # Then return the last page
        posts = paginator.page(paginator.num_pages)

    return render(
        request,
        'account/all_favourites.html',
        {'posts': posts, 'title': 'Favourite Scholarships'},
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

