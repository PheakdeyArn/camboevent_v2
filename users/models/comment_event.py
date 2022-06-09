from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

# from content.models import EventDetailPage
from users.models import User


class CommentEvent(MPTTModel):

    post = models.ForeignKey('content.EventDetailPage',
                             on_delete=models.CASCADE,
                             related_name='events_comments')
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User, related_name='user_comment_event', on_delete=models.CASCADE)
    parent = TreeForeignKey('self', on_delete=models.CASCADE,
                            null=True, blank=True, related_name='children')
    email = models.EmailField()
    content = models.TextField()
    publish = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    class MPTTMeta:
        order_insertion_by = ['publish']

    def __str__(self):
        return self.name