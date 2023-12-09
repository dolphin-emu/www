# Copyright (c) 2018 Dolphin Emulator Website Contributors
# SPDX-License-Identifier: MIT

from annoying.decorators import render_to
from django.conf import settings
from django.core.paginator import EmptyPage
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import cache_control
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.vary import vary_on_headers
from dolweb.downloads.diggpaginator import DiggPaginator
from dolweb.downloads.models import Artifact, BranchInfo, DevVersion, ReleaseVersion
from dolweb.update.models import UpdateTrack

import hashlib
import hmac
import multiprocessing

_addbuild_lock = multiprocessing.Lock()

@cache_control(max_age=15)
@vary_on_headers('User-Agent')
@render_to('downloads-index.html')
def index(request):
    """Displays the downloads index"""

    releases = ReleaseVersion.objects.order_by('-date')
    master_builds = (DevVersion.objects.filter(branch='master')
                                       .order_by('-date')
                                       [:10])
    beta_track = (UpdateTrack.objects.filter(name='beta')
                                     .order_by('-version__date')
                                     [:5])
    beta_builds = [track.version for track in beta_track]
    last_master = master_builds[0] if len(master_builds) else None

    return { 'releases': releases, 'master_builds': master_builds,
             'beta_builds': beta_builds, 'last_master': last_master }

@cache_control(max_age=15)
@vary_on_headers('User-Agent')
@render_to('downloads-branches.html')
def branches(request):
    """Displays all the visible branches"""

    infos = BranchInfo.objects.filter(visible=True).order_by('name')
    branches = []

    for info in infos:
        branches.append((
            info.name, DevVersion.objects.filter(branch=info.name)
                                         .order_by('-date')
                                         [:5]
        ))

    return { 'branches': branches }

@cache_control(max_age=15)
def buildlist(request):
    """Displays a list of builds from buildbot for the bisect tool"""
    master_builds = Artifact.objects.filter(branch='master').order_by('-date')
    builds_list = []
    for build in master_builds:
        rev_info = [build.shortrev,  build.url]
        builds_list.append(rev_info)
    return JsonResponse(builds_list, safe=False)

@vary_on_headers('User-Agent')
@render_to('downloads-view-devrel.html')
def view_dev_release(request, hash):
    release = get_object_or_404(DevVersion, hash=hash)

    return { 'ver': release }

@vary_on_headers('User-Agent')
@render_to('downloads-view-devrel.html')
def view_dev_release_by_name(request, branch, name):
    release = get_object_or_404(DevVersion, branch=branch, shortrev=name)

    return { 'ver': release }

@cache_control(max_age=15)
@vary_on_headers('User-Agent')
@render_to('downloads-list.html')
def list(request, branch, page):
    if page is None:
        page = 1
    builds = DevVersion.objects.filter(branch=branch).order_by('-date')
    if builds.count() == 0 and branch != 'master':
        get_object_or_404(BranchInfo, name=branch)
    pagi = DiggPaginator(builds, 20, body=9, tail=2)

    try:
        page_obj = pagi.page(page)
    except EmptyPage:
        raise Http404

    return { 'branch': branch, 'page': page, 'page_obj': page_obj,
             'pagi': pagi }

@csrf_exempt
def new(request):
    """Callback used by the buildbot to register a new build"""

    if request.method != 'POST':
        raise Http404

    # Check the message signature
    branch = request.POST['branch']
    shortrev = request.POST['shortrev']
    hash = request.POST['hash']
    author = request.POST['author']
    description = request.POST['description']
    target_system = request.POST['target_system']
    build_url = request.POST['build_url']
    user_os_matcher = request.POST['user_os_matcher']
    msg = u"%d|%d|%d|%d|%d|%d|%d|%d|%s|%s|%s|%s|%s|%s|%s|%s" % (
        len(branch), len(shortrev), len(hash), len(author), len(description),
        len(target_system), len(build_url), len(user_os_matcher),

        branch, shortrev, hash, author, description, target_system, build_url,
        user_os_matcher
    )
    hm = hmac.new(settings.DOWNLOADS_CREATE_KEY.encode('ascii'),
                  msg.encode("utf-8"), hashlib.sha1)
    if hm.hexdigest() != request.POST['hmac']:
        return HttpResponse('Invalid HMAC', status=403)

    # Lock to avoid race conditions
    try:
        _addbuild_lock.acquire()

        try:
            build_obj = DevVersion.objects.get(hash=hash)
        except DevVersion.DoesNotExist:
            build_obj = DevVersion()
            build_obj.branch = branch
            build_obj.shortrev = shortrev
            build_obj.hash = hash
            build_obj.author = author
            build_obj.description = description
            build_obj.save()

        try:
            artifact_obj = Artifact.objects.get(
                    version=build_obj, target_system=target_system)
        except Artifact.DoesNotExist:
            artifact_obj = Artifact()
            artifact_obj.version = build_obj
            artifact_obj.target_system = target_system
            artifact_obj.user_os_matcher = user_os_matcher
        artifact_obj.url = build_url
        artifact_obj.save()
    finally:
        _addbuild_lock.release()

    return HttpResponse('OK')

@cache_control(max_age=15)
def get_latest(request, branch):
    """Callback used by the emulator to get the latest version on a branch."""

    build = DevVersion.objects.filter(branch=branch).order_by('-date')
    if len(build) == 0:
        raise Http404

    return HttpResponse(build[0].hash)
