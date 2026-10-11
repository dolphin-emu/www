from django.db import migrations


def move_content_type(apps, schema_editor):
    # Preserve existing series permissions and admin log references.
    content_types = apps.get_model('contenttypes', 'ContentType').objects.using(
        schema_editor.connection.alias)
    content_types.filter(app_label='blog', model='blogseries').update(
        app_label='zinnia')


class Migration(migrations.Migration):
    dependencies = [
        ('blog', '0001_initial'),
        ('zinnia', '0010_blogseries_entry_fields'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.RunPython(move_content_type),
        # The table stays in place; only the model's app ownership changes.
        migrations.SeparateDatabaseAndState(
            state_operations=[migrations.DeleteModel(name='BlogSeries')],
        ),
    ]
