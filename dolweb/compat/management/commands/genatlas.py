# Copyright (c) 2018 Dolphin Emulator Website Contributors
# SPDX-License-Identifier: MIT

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from dolweb.compat.models import Page
from PIL import Image
from io import BytesIO

import binascii
import collections
import hashlib
import os
import os.path
import pymongo
import string

BANNER_WIDTH = 96
BANNER_HEIGHT = 32
MAX_ATLAS_HEIGHT = 32 * 50

PLACEHOLDER = '''
iVBORw0KGgoAAAANSUhEUgAAAGAAAAAgCAIAAABiouoDAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJ
bWFnZVJlYWR5ccllPAAAARlJREFUeNrU2U0KhDAMBWAn1I0w4MrzemRhQNBuJugF+pPkvb51KM1H
FyH97Ps+GeU4jvM8Syq/T2rP/z0pqVyWZV1Xk6ZksoveSW9m2ypWxxjIzwilYw/kYQTUcQGyNcLq
eAFZGcF1HIH6jRh0fIF6jEh03IHajHh0NGnyz9tDyQypLvd9X9dFohPxgmrfEZVOHFCVEY9OKJCV
UaRONFC/UbAOAKjHKF4HA9RmBNGBAb1G8zwXFmslRAcJpCNPzrmwWCtr90djA7kuzIYHam4VYiSj
6KCMZCAdiJGMpRNvJGw6KSUqI6HS0Wlw2za/vyNGoIbtl+v/GhdQ826Qx0gIdaiMhFOHx0hodUiM
hFmHwUjIdeBGfwEGADC2MM78PI3uAAAAAElFTkSuQmCC
'''

mongo = pymongo.MongoClient(settings.BNR_MONGO_HOST)
db = mongo[settings.BNR_MONGO_DBNAME]
db.authenticate(settings.BNR_MONGO_USER, settings.BNR_MONGO_PASSWORD)

ALL_BANNER_GAMEIDS = None
def get_all_bnr_gameids():
    global ALL_BANNER_GAMEIDS

    if ALL_BANNER_GAMEIDS is not None:
        return ALL_BANNER_GAMEIDS

    ALL_BANNER_GAMEIDS = set()
    for blob in db.blobs.find({}, { 'unique_id': 1 }):
        uid = ''.join(map(chr, blob['unique_id']))
        ALL_BANNER_GAMEIDS.add(uid)
    return ALL_BANNER_GAMEIDS

def country_key(gameid):
    if gameid[3] == 'E':
        return 0
    elif gameid[3] == 'P':
        return 1
    else:
        return 2

def get_gameids(letter):
    # Select all gameids redirecting to pages starting with that letter
    if letter == '#':
        cond = "pl.pl_title SIMILAR TO '[^a-zA-Z]%%'"
    else:
        cond = "pl.pl_title LIKE '%s%%%%'" % letter

    gameids = Page.objects.raw('''
        SELECT gp.page_id, gp.page_title, pl.pl_title AS link_to
            FROM page gp
            LEFT JOIN pagelinks pl on pl.pl_from = gp.page_id
            WHERE gp.page_is_redirect = 1
                AND gp.page_namespace = 0
                AND LENGTH(gp.page_title) = 6
                AND pl.pl_namespace = 0
                AND %s
    ''' % cond)

    title_gameids = collections.defaultdict(list)
    for gid in gameids:
        if not gid.title_url.isalnum():
            continue
        hash = hashlib.sha1(gid.link_to.encode('utf-8')).hexdigest()[:8]
        title_gameids[hash].append(gid.title_url.upper())

    # Prefer in that order: US, EU, JP, then whatever
    for li in title_gameids.values():
        li.sort(key=country_key)

    # Match the gameids with the banners
    bnr_gameids = get_all_bnr_gameids()

    res = {}
    for (hash, gids) in title_gameids.items():
        # Find first matching gid in gameids
        matching_gid = None
        for gid in gids:
            if gid in bnr_gameids:
                matching_gid = gid
                break
        else:
            # "Fuzzy" match: bruteforce the region
            pattern = gids[0][:3] + "%s" + gids[0][4:]
            for l in string.ascii_uppercase:
                gid = pattern % l
                if gid in bnr_gameids:
                    matching_gid = gid
                    break
        if matching_gid is None:
            continue
        res[matching_gid] = hash

    return res

def download_all_banners(gameids):
    res = {}
    gameids_ord = [[ord(c) for c in gid] for gid in gameids]
    for blob in db.blobs.find({ 'unique_id': { '$in': gameids_ord }}):
        gid = ''.join(map(chr, blob['unique_id']))
        img = blob['image']
        res[gid] = img
    return res

def generate_coords(gameids):
    # Start at (0, 32) to leave space for a transparent (empty) banner
    cx, cy = 0, 32
    w, h = 96, 32
    coords = {}
    for gid in gameids:
        w = max(cx + BANNER_WIDTH, w)
        h = max(cy + BANNER_HEIGHT, h)

        coords[gid] = (cx, cy)

        cy += BANNER_HEIGHT
        if cy > MAX_ATLAS_HEIGHT:
            cx += BANNER_WIDTH
            cy = 0

    return (w, h), coords

def generate_css(ident, coords, gameids):
    start = 'td.banner div.bnr{background-image:url("%sbnr/atlas-%s.png")}' % (settings.MEDIA_URL, ident.replace('#', '%23'))
    chunks = [start]
    for gid in gameids:
        hash = gameids[gid]
        s = '.bnr-%(hash)s{background-position:%(x)dpx %(y)dpx}'
        s %= { 'hash': hash, 'x': -coords[gid][0], 'y': -coords[gid][1] }
        chunks.append(s)
    return ''.join(chunks)

def needs_update(ident, css):
    path = os.path.join(settings.MEDIA_ROOT, 'bnr', 'atlas-%s.css' % ident)
    if not os.path.exists(path):
        return True
    prev_css = open(path).read()

    hash = hashlib.sha1(css.encode('utf-8')).hexdigest()
    prev_hash = hashlib.sha1(prev_css.encode('utf-8')).hexdigest()

    return (hash != prev_hash)

def generate_image_map(size, coords):
    im = Image.new("RGBA", size)
    gameids = coords.keys()
    banners = download_all_banners(gameids)

    sio = BytesIO(binascii.a2b_base64(PLACEHOLDER))
    sio.seek(0)
    placeholder = Image.open(sio)
    im.paste(placeholder, (0, 0, 96, 32))

    pix = im.load()

    for gid, (ox, oy) in coords.items():
        data = iter(banners[gid])
        for y in range(32):
            for x in range(96):
                pix[x + ox, y + oy] = (next(data), next(data), next(data), 255)

    return im

def update_atlas(ident, img, css):
    base = os.path.join(settings.MEDIA_ROOT, 'bnr')
    if not os.path.exists(base):
        os.mkdir(base)

    css_path = os.path.join(base, 'atlas-%s.css' % ident)
    img_path = os.path.join(base, 'atlas-%s.png' % ident)

    open(css_path + '.new', 'w').write(css)
    img.save(img_path + '.new', 'PNG')

    os.rename(css_path + '.new', css_path)
    os.rename(img_path + '.new', img_path)

def generate_atlas(ident, gameids):
    size, coords = generate_coords(gameids)
    css = generate_css(ident, coords, gameids)
    if needs_update(ident, css):
        img = generate_image_map(size, coords)
        update_atlas(ident, img, css)

class Command(BaseCommand):
    def handle(self, *args, **options):
        for l in '#' + string.ascii_uppercase:
            print('Generating atlas for: %r' % l)
            generate_atlas(l, get_gameids(l))
