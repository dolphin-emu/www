from django.conf import settings
from django.http import Http404, HttpResponse

import base64
import subprocess

def make_401_response():
    response = HttpResponse()
    response.status_code = 401
    response['WWW-Authenticate'] = 'Basic realm="Dolphin mgmt interface"'
    return response

def run_command(request, cmd):
    if 'HTTP_AUTHORIZATION' not in request.META:
        return make_401_response()

    auth = request.META['HTTP_AUTHORIZATION'].split()
    if len(auth) != 2:
        return make_401_response()

    if auth[0].lower() != 'basic':
        return make_401_response()

    authenticator = base64.b64decode(auth[1]).decode('utf-8').split(':')
    if tuple(authenticator) not in settings.MGMT_AUTHORIZED_USERS:
        return make_401_response()

    return HttpResponse(subprocess.check_output(cmd, shell=True), 'text/plain')
