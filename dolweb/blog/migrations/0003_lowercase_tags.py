from django.db import migrations


def lowercase_tags(apps, schema_editor):
    database = schema_editor.connection.alias
    tags = apps.get_model('tagging', 'Tag').objects.using(database)
    items = apps.get_model('tagging', 'TaggedItem').objects.using(database)
    entries = apps.get_model('zinnia', 'Entry').objects.using(database)

    for tag in tags.order_by('pk').iterator():
        name = tag.name.lower()
        if name == tag.name:
            continue
        canonical = tags.filter(name=name).exclude(pk=tag.pk).first()
        if canonical is None:
            tags.filter(pk=tag.pk).update(name=name)
            continue
        for content_type_id, object_id in items.filter(
                tag_id=tag.pk).values_list('content_type_id', 'object_id'):
            items.get_or_create(tag_id=canonical.pk,
                                content_type_id=content_type_id,
                                object_id=object_id)
        tags.filter(pk=tag.pk).delete()

    for entry_id, tags_string in entries.values_list('pk', 'tags').iterator():
        if tags_string and tags_string != tags_string.lower():
            entries.filter(pk=entry_id).update(tags=tags_string.lower())


class Migration(migrations.Migration):
    dependencies = [
        ('blog', '0002_move_blogseries_to_zinnia'),
        ('zinnia', '0011_blogseries_verbose_names'),
        ('tagging', '0003_adapt_max_tag_length'),
    ]

    operations = [
        migrations.RunPython(lowercase_tags, migrations.RunPython.noop),
    ]
