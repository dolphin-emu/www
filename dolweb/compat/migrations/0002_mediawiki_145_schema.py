from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('compat', '0001_initial'),
    ]

    # The compat tables are controlled by MediaWiki.  MediaWiki 1.45 has
    # already made these schema changes, so let's record them in Django's
    # migration state without attempting to actually migrate.
    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[],
            state_operations=[
                migrations.CreateModel(
                    name='Content',
                    fields=[
                        ('id', models.BigIntegerField(db_column='content_id', primary_key=True, serialize=False)),
                        ('address', models.CharField(db_column='content_address', max_length=255)),
                    ],
                    options={
                        'verbose_name': 'MediaWiki Content',
                        'verbose_name_plural': 'MediaWiki Contents',
                        'db_table': 'content',
                    },
                ),
                migrations.CreateModel(
                    name='LinkTarget',
                    fields=[
                        ('id', models.BigIntegerField(db_column='lt_id', primary_key=True, serialize=False)),
                        ('namespace', models.IntegerField(db_column='lt_namespace')),
                        ('title_url', models.CharField(db_column='lt_title', max_length=255)),
                    ],
                    options={
                        'verbose_name': 'MediaWiki Link Target',
                        'verbose_name_plural': 'MediaWiki Link Targets',
                        'db_table': 'linktarget',
                        'ordering': ['namespace', 'title_url'],
                    },
                ),
                migrations.CreateModel(
                    name='SlotRole',
                    fields=[
                        ('id', models.IntegerField(db_column='role_id', primary_key=True, serialize=False)),
                        ('name', models.CharField(db_column='role_name', max_length=64)),
                    ],
                    options={
                        'verbose_name': 'MediaWiki Slot Role',
                        'verbose_name_plural': 'MediaWiki Slot Roles',
                        'db_table': 'slot_roles',
                    },
                ),
                migrations.AlterModelOptions(
                    name='categorylink',
                    options={
                        'ordering': ['target__title_url', 'page'],
                        'verbose_name': 'MediaWiki Category Link',
                        'verbose_name_plural': 'MediaWiki Category Links',
                    },
                ),
                migrations.RemoveField(
                    model_name='categorylink',
                    name='cat',
                ),
                migrations.RemoveField(
                    model_name='revision',
                    name='text',
                ),
                migrations.AlterModelTable(
                    name='text',
                    table='text',
                ),
                migrations.CreateModel(
                    name='Slot',
                    fields=[
                        ('revision', models.ForeignKey(db_column='slot_revision_id', on_delete=django.db.models.deletion.PROTECT, primary_key=True, related_name='+', serialize=False, to='compat.Revision')),
                        ('content', models.ForeignKey(db_column='slot_content_id', on_delete=django.db.models.deletion.PROTECT, related_name='+', to='compat.Content')),
                        ('origin', models.ForeignKey(db_column='slot_origin', on_delete=django.db.models.deletion.PROTECT, related_name='+', to='compat.Revision')),
                        ('role', models.ForeignKey(db_column='slot_role_id', on_delete=django.db.models.deletion.PROTECT, related_name='+', to='compat.SlotRole')),
                    ],
                    options={
                        'verbose_name': 'MediaWiki Slot',
                        'verbose_name_plural': 'MediaWiki Slots',
                        'db_table': 'slots',
                    },
                ),
                migrations.AddField(
                    model_name='categorylink',
                    name='target',
                    field=models.ForeignKey(db_column='cl_target_id', on_delete=django.db.models.deletion.PROTECT, related_name='+', to='compat.LinkTarget'),
                ),
            ],
        ),
    ]
