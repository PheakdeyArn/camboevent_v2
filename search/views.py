from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.template.response import TemplateResponse

from wagtail.core.models import Page
from wagtail.search.models import Query

from blog.models import BlogCategory, BlogDetailPage, BlogTag


def get_recent_blogs(limit_top=5, exclude_news=True, only_news_blog=False):
    try:
        # note -> use [::-1] instead of reversed:

        if only_news_blog:
            try:
                news_cat = BlogCategory.objects.get(name='news')
                news_cat_id = news_cat.id

                if limit_top:
                    blogs = BlogDetailPage.objects.filter(categories=news_cat_id).live().public().order_by(
                        'published_datetime')[:limit_top][::-1]
                else:
                    blogs = BlogDetailPage.objects.filter(categories=news_cat_id).live().public().order_by(
                        'published_datetime')[:][::-1]
                return blogs
            except BlogCategory.DoesNotExist:
                return None

        if exclude_news:
            news_cat = BlogCategory.objects.get(name='news')
            news_cat_id = news_cat.id
            blog_detail_results = BlogDetailPage.objects.filter(~Q(categories=news_cat_id)).live().public().order_by(
                'published_datetime')[:limit_top][::-1]
        else:
            # meaning get all blogs from all categories including news.
            blog_detail_results = BlogDetailPage.objects.all().live().public().order_by('published_datetime')[:limit_top][::-1]

        return blog_detail_results
    except BlogTag.DoesNotExist:
        return None


def search(request):
    search_query = request.GET.get('query', None)
    page = request.GET.get('page', 1)

    # Search
    if search_query:
        search_results = Page.objects.live().search(search_query)
        query = Query.get(search_query)

        # Record hit
        query.add_hit()
    else:
        search_results = Page.objects.none()

    # Pagination
    paginator = Paginator(search_results, 10)
    try:
        search_results = paginator.page(page)
    except PageNotAnInteger:
        search_results = paginator.page(1)
    except EmptyPage:
        search_results = paginator.page(paginator.num_pages)

    return TemplateResponse(request, 'search/search.html', {
        'search_query': search_query,
        'search_results': search_results,
    })
