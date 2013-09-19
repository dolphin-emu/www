from annoying.decorators import render_to
from django.conf import settings
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from dolweb.downloads.diggpaginator import DiggPaginator
from dolweb.downloads.models import BranchInfo, DevVersion, ReleaseVersion

import hashlib
import hmac
import multiprocessing

_addbuild_lock = multiprocessing.Lock()

@render_to('downloads-index.html')
def index(request):
    """Displays the downloads index"""

    releases = ReleaseVersion.objects.order_by('-date')
    master_builds = DevVersion.objects.filter(branch='master').order_by('-date')[:10]
    last_master = master_builds[0] if len(master_builds) else None

    return { 'releases': releases, 'master_builds': master_builds,
             'last_master': last_master }

@render_to('downloads-branches.html')
def branches(request):
    """Displays all the visible branches"""

    infos = BranchInfo.objects.filter(visible=True).order_by('name')
    branches = []

    for info in infos:
        branches.append((
            info.name,
            DevVersion.objects.filter(branch=info.name).order_by('-date')[:5]
        ))

    return { 'branches': branches }

@render_to('downloads-view-devrel.html')
def view_dev_release(request, hash):
    release = get_object_or_404(DevVersion, hash=hash)

    return { 'ver': release }

@render_to('downloads-list.html')
def list(request, branch, page):
    if page is None:
        page = 1
    builds = DevVersion.objects.filter(branch=branch).order_by('-date')
    if len(builds) == 0 and branch != 'master':
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
    build_type = request.POST['build_type']
    build_url = request.POST['build_url']
    msg = "%d|%d|%d|%d|%d|%d|%d|%s|%s|%s|%s|%s|%s|%s" % (
        len(branch), len(shortrev), len(hash), len(author), len(description),
        len(build_type), len(build_url),

        branch, shortrev, hash, author, description, build_type, build_url
    )
    hm = hmac.new(settings.DOWNLOADS_CREATE_KEY, msg, hashlib.sha1)
    if hm.hexdigest() != request.POST['hmac']:
        return HttpResponse('Invalid HMAC', status=403)

    # Lock to avoid race conditions
    try:
        _addbuild_lock.acquire()
        # Check if we already have a commit with the same hash
        try:
            build_obj = DevVersion.objects.get(hash=hash)
        except DevVersion.DoesNotExist:
            build_obj = DevVersion()
            build_obj.branch = branch
            build_obj.shortrev = shortrev
            build_obj.hash = hash
            build_obj.author = author
            build_obj.description = description

            # Shorten the description by taking only the first line, truncating it to
            # 250 chars and adding an ellipsis if truncated
            descr_abbrev = description.split('\n')[0]
            if len(descr_abbrev) >= 250:
                descr_abbrev = descr_abbrev[:250] + "..."
            build_obj.description_abbrev = descr_abbrev

        if build_type == 'win32':
            build_obj.win32_url = build_url
        elif build_type == 'win64':
            build_obj.win64_url = build_url
        elif build_type == 'osx':
            build_obj.osx_url = build_url
        elif build_type == 'ubu':
            build_obj.ubu_url = build_url
        else:
            return HttpResponse('Wrong build type', status=400)

        build_obj.save()
        return HttpResponse('OK')
    finally:
        _addbuild_lock.release()

def get_latest(request, branch):
    """Callback used by the emulator to get the latest version on a branch."""

    build = DevVersion.objects.filter(branch=branch).order_by('-date')
    if len(build) == 0:
        raise Http404

    return HttpResponse(build[0].hash)
