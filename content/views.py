from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from .models.like import EventLikes, ScholarshipLikes
from django.contrib.auth.decorators import login_required
from content.models import EventDetailPage, ScholarshipDetailPage

# Create your views here.
@ login_required
def like_event_add(request, id):
    get_like = EventLikes.objects.filter(post_id=id, user=request.user)
    post = get_object_or_404(EventDetailPage, id=id)

    if not get_like:
        new_obj = EventLikes(post=post, user=request.user, status=True)
        new_obj.save()
        return HttpResponseRedirect(request.META['HTTP_REFERER'])

    if get_like[0].status:
        get_like[0].status = False
    else:
        get_like[0].status = True

    get_like[0].save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])



@ login_required
def like_scholarship_add(request, id):
    get_like = ScholarshipLikes.objects.filter(post_id=id, user=request.user)
    post = get_object_or_404(ScholarshipDetailPage, id=id)

    if not get_like:
        new_obj = ScholarshipLikes(post=post, user=request.user, status=True)
        new_obj.save()
        return HttpResponseRedirect(request.META['HTTP_REFERER'])

    if get_like[0].status:
        get_like[0].status = False
    else:
        get_like[0].status = True

    get_like[0].save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])
