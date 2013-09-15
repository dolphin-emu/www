from django.db.models.signals import post_save
from zinnia.models import Entry
from zinnia.managers import PUBLISHED
from dolweb.blog.models import ForumThreadForEntry


def create_dolphin_forum_thread(sender, instance, **kwargs):
    if instance.status != PUBLISHED:
        return

    thread, created = ForumThreadForEntry.objects.get_or_create(entry=instance)
    if not created:
        return

    # TODO: call MyBB script to get thread ID
    # forum_thread_id = get_shit_done(instance)
    forum_thread_id = 1337
    thread.thread_id = forum_thread_id
    thread.save()


post_save.connect(create_dolphin_forum_thread, sender=Entry)
