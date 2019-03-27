# Copyright (c) 2019 Dolphin Emulator Website Contributors
# SPDX-License-Identifier: MIT

from django.http import HttpResponseBadRequest, HttpResponseNotFound, JsonResponse
from django.conf import settings

import time
import random
import re

secret_chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
secret_length = 10

session_valid_keys = ['name', 'region', 'game', 'password', 'method', 'server_id', 'version', 'player_count', 'in_game', 'port']

sessions = {}
sessions_last_cleanup = 0

def _validate_session(session):
    # Abort if an unsupported field is provided
    for key in session:
        if key not in session_valid_keys:
            return False

    # Check if all fields are provided
    for key in session_valid_keys:
        if key not in session:
            return False

    if not 0 < len(session['name']) <= settings.SESSION_MAX_NAME_LENGTH:
        return False

    if not (session['password'] == '1' or session['password'] == '0'):
        return False

    if not (session['in_game'] == '1' or session['in_game'] == '0'):
        return False

    if not 0 < int(session['port']) <= 65355:
        return False

    return True

def _sessions_cleanup():
    to_delete = []
    for key in sessions:
        if time.time() - sessions[key]['timestamp'] > settings.SESSION_TIMEOUT_SECONDS:
            to_delete.append(key)

    for key in to_delete:
        del sessions[key]

def _filter_string(sessions, key, value, match = False):
    filtered_sessions = []

    for session in sessions:
        if match:
            if re.match('.*' + value + '.*', session[key]):
                filtered_sessions.append(session)
        else:
            if session[key] == value:
                filtered_sessions.append(session)


    return filtered_sessions

def _bad_method():
    return JsonResponse({'status': 'BAD_METHOD'})

def _bad_version():
    return JsonResponse({'status': 'BAD_VERSION'})

def generate_secret():
    secret = ''

    random.seed()

    for _ in range(10):
        secret += random.choice(secret_chars)

        if secret in sessions:
            return generate_secret()

    return secret


def session_list(request, api_ver):
    if request.method != 'GET':
        return _bad_method()

    if api_ver != '0':
        return _bad_version()

    global sessions_last_cleanup

    if time.time() - sessions_last_cleanup > settings.SESSION_CLEANUP_INTERVAL:
        _sessions_cleanup()
        sessions_last_cleanup = time.time()

    filtered_sessions = list(sessions.values())

    if 'name' in request.GET:
        filtered_sessions = _filter_string(filtered_sessions, 'name', request.GET['name'], True)

    if 'game' in request.GET:
        filtered_sessions = _filter_string(filtered_sessions, 'game', request.GET['game'], True)

    if 'password' in request.GET:
        filtered_sessions = _filter_string(filtered_sessions, 'password', request.GET['password'])

    if 'region' in request.GET:
        filtered_sessions = _filter_string(filtered_sessions, 'region', request.GET['region'])

    if 'version' in request.GET:
        filtered_sessions = _filter_string(filtered_sessions, 'version', request.GET['version'])

    if 'in_game' in request.GET:
        filtered_sessions = _filter_string(filtered_sessions, 'in_game', request.GET['in_game'])

    return JsonResponse({'status': 'OK', 'sessions': filtered_sessions})

def session_add(request, api_ver):
    if request.method != 'GET':
        return _bad_method()

    if api_ver != '0':
        return _bad_version()

    if not _validate_session(request.GET):
        return JsonResponse({'status': 'INVALID_SESSION_DATA' })

    session = request.GET.dict()

    session['timestamp'] = time.time()
    session['password'] = bool(int(session['password']))
    session['in_game'] = bool(int(session['in_game']))
    session['player_count'] = int(session['player_count'])
    session['port'] = int(session['port'])

    secret = generate_secret()

    sessions[secret] = session

    return JsonResponse({'status': 'OK', 'secret': secret})

def session_remove(request, api_ver):
    if request.method != 'GET':
        return _bad_method()

    if api_ver != '0':
        return _bad_version()

    secret = request.GET['secret']

    if secret not in sessions:
        return JsonResponse({'status': 'SESSION_NOT_FOUND'})

    del sessions[secret]

    return JsonResponse({'status': 'OK'})

def session_active(request, api_ver):
    if request.method != 'GET':
        return _bad_method()

    if api_ver != '0':
        return _bad_version()

    secret = request.GET['secret']

    if secret not in sessions:
        return JsonResponse({'status': 'SESSION_NOT_FOUND'})


    sessions[secret]['timestamp'] = time.time()

    if 'player_count' in request.GET:
        sessions[secret]['player_count'] = int(request.GET['player_count'])

    if 'in_game' in request.GET:
        sessions[secret]['in_game'] = bool(int(request.GET['in_game']))

    if 'game' in request.GET:
        sessions[secret]['game'] = request.GET['game']

    return JsonResponse({'status': 'OK'})
