from django.contrib import admin
from .models import BlogLikes

# Register your models here.
class BlogLikesAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'blog',
        'status',
        'created_at',
        'updated_at'
    )


admin.site.register(BlogLikes, BlogLikesAdmin)
