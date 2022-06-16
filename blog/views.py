from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from .models.like import BlogLikes
from django.contrib.auth.decorators import login_required
from blog.models import BlogDetailPage

# Create your views here.
@ login_required
def like_blog_add(request, id):

    print("%%%%%%%%%%%%%%%%%%%werwerwer")
    get_like = BlogLikes.objects.filter(blog_id=id, user=request.user)
    get_blog = get_object_or_404(BlogDetailPage, id=id)

    if not get_like:
        print("User not like is post: ")
        new_obj = BlogLikes(blog=get_blog, user=request.user, status=True)
        new_obj.save()
        return HttpResponseRedirect(request.META['HTTP_REFERER'])

        # new_obj = BlogLikes(blog=)

    if get_like[0].status:
        get_like[0].status = False
        get_like[0].save()
    else:
        get_like[0].status = True
        get_like[0].save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])

