# Copyright (c) 2018 Dolphin Emulator Website Contributors
# SPDX-License-Identifier: MIT

from django.conf import settings
from django.http import HttpResponseBadRequest, HttpResponseNotFound, JsonResponse
from dolweb.downloads.models import DevVersion
from dolweb.update.models import UpdateTrack


def _error_response(code, msg):
    return JsonResponse({"error": msg}, status=code)


def _make_up_to_date_response():
    return JsonResponse({"status": "up-to-date"})


def _get_manifest_url(version, platform):
    first_hash = version.hash[:2]
    second_hash = version.hash[2:4]
    return settings.UPDATE_MANIFEST_URL % (platform,
                                           version.hash[0:2], version.hash[2:4], version.hash[4:])


def _changelog_from_dev_versions_list(versions):
    changelog_entries = []
    for version in versions:
        data = version.description_data
        data['shortrev'] = version.shortrev
        changelog_entries.append(data)
    return changelog_entries


def _changelog_from_update_track(versions):
    changelog_entries = []
    for version in versions:
        data = version.version.description_data
        data['shortrev'] = version.version.shortrev
        data['changelog_html'] = version.changelog_text
        changelog_entries.append(data)
    return changelog_entries


def _serialize_version(version, platform):
    return {
        "hash": version.hash,
        "name": version.shortrev,
        "manifest": _get_manifest_url(version, platform),
    }


def _make_outdated_response(old_version, new_version, platform, changelog):
    return JsonResponse({
        "status": "outdated",
        "content-store": settings.UPDATE_CONTENT_STORE_URL,
        "old": _serialize_version(old_version, platform),
        "new": _serialize_version(new_version, platform),
        "changelog": changelog,
    })


def latest(request, track):
    if track in settings.AUTO_MAINTAINED_UPDATE_TRACKS:
        version = DevVersion.objects.filter(
            branch=settings.AUTO_MAINTAINED_UPDATE_TRACKS[track]).latest(
                'date')
        changelog_html = version.description_data['short_descr']
    else:
        track_obj = UpdateTrack.objects.filter(
            name=track).latest('version__date')
        if track_obj is None:
            return _error_response(404, "No track %r" % track)
        version = track_obj.version
        changelog_html = track_obj.changelog_text

    if version is None:
        return _error_response(404,
                               "No latest version found on track %r" % track)

    artifacts = []
    for art in version.artifacts.all():
        artifacts.append({'system': art.target_system, 'url': art.url})
    data = {
        'shortrev': version.shortrev,
        'hash': version.hash,
        'changelog_html': changelog_html,
        'artifacts': artifacts
    }
    return JsonResponse(data)


def check(request, updater_ver, track, version, platform):
    if updater_ver != "0" and updater_ver != "1":
        return _error_response(400,
                               "Unsupported updater version %r" % updater_ver)

    # Updater API v0 only supports Windows
    if updater_ver == "0":
        platform = "win"
    else:
        if platform != "win" and platform != "macos":
            return _error_response(400,
                                   "Unsupported platform %r" % platform)

    if track in settings.AUTO_MAINTAINED_UPDATE_TRACKS:
        return _check_on_auto_maintained_track(request, track, version, platform)
    else:
        return _check_on_manually_maintained_track(request, track, version, platform)


def _check_on_auto_maintained_track(request, track, version, platform):

    target_system = ('Windows x64' if platform == 'win' else 'macOS')

    # Find the current version and get its release date in order to select all
    # newer versions.

    branch = settings.AUTO_MAINTAINED_UPDATE_TRACKS[track]
    try:
        version = DevVersion.objects.get(branch=branch, hash=version)
    except DevVersion.DoesNotExist:
        return _error_response(404, "No version %r on track %r (branch: %r) for platform %r" %
                               (version, track, branch, platform))

    newer_versions = DevVersion.objects.filter(
        branch=branch,
        date__gt=version.date,
        artifacts__target_system=target_system).order_by('-date')
    if len(newer_versions) == 0:
        return _make_up_to_date_response()
    new_version = newer_versions[0]
    changelog = _changelog_from_dev_versions_list(newer_versions)
    return _make_outdated_response(version, new_version, platform, changelog)


def _check_on_manually_maintained_track(request, track, version, platform):

    target_system = ('Windows x64' if platform == 'win' else 'macOS')

    try:
        version = DevVersion.objects.get(hash=version)
    except DevVersion.DoesNotExist:
        return _error_response(404, "No version %r exists" % version)

    newer_versions = UpdateTrack.objects.filter(
        name=track, version__date__gt=version.date).order_by('-version__date')
    if len(newer_versions) == 0:
        return _make_up_to_date_response()
    new_version = newer_versions[0].version
    if new_version.artifacts.filter(target_system=target_system).count() == 0:
        return _make_up_to_date_response()
    changelog = _changelog_from_update_track(newer_versions)
    return _make_outdated_response(version, new_version, platform, changelog)
