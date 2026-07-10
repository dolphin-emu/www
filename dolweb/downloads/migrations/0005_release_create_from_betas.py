from django.db import migrations

def create_releases_for_betas(apps, schema_editor):
    UpdateTrack = apps.get_model('update', 'UpdateTrack')
    ReleaseVersion = apps.get_model('downloads', 'ReleaseVersion')
    Artifact = apps.get_model('downloads', 'Artifact')

    for track in UpdateTrack.objects.filter(name='beta'):
        build_obj = track.version

        new_build_obj = ReleaseVersion()
        new_build_obj.shortrev = build_obj.shortrev
        new_build_obj.hash = build_obj.hash
        new_build_obj.is_tagged = False
        new_build_obj.save()

        # Update this separately to avoid running into auto_now_add.
        new_build_obj.date = build_obj.date
        new_build_obj.save()

        for artifact_obj in Artifact.objects.filter(version=build_obj):
            new_artifact_obj = Artifact()
            new_artifact_obj.version = new_build_obj
            new_artifact_obj.target_system = artifact_obj.target_system
            new_artifact_obj.user_os_matcher = artifact_obj.user_os_matcher
            new_artifact_obj.url = artifact_obj.url
            new_artifact_obj.save()

class Migration(migrations.Migration):

    dependencies = [
        ('downloads', '0004_release_add_tagged'),
        ('update', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_releases_for_betas),
    ]
