from django.contrib import admin
from . import models
# from mptt.admin import MPTTModelAdmin

# admin.site.register(models.CommentEvent, MPTTModelAdmin)

from .models import EventLikes, ScholarshipLikes


class EventLikesAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'post',
        'status',
        'created_at',
        'updated_at'
    )


class ScholarshipLikesAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'post',
        'status',
        'created_at',
        'updated_at'
    )


admin.site.register(EventLikes, EventLikesAdmin)
admin.site.register(ScholarshipLikes, ScholarshipLikesAdmin)

