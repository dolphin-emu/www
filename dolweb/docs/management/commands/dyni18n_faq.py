from django.conf import settings
from django.core.management.base import BaseCommand

import os
import os.path
import requests

def get_resource_url():
    return 'https://www.transifex.com/api/2/project/%s/resource/%s/' % (
        settings.TRANSIFEX_PROJECT, settings.TRANSIFEX_FAQ_RESOURCE
    )

def get_all_langs():
    details = requests.get(get_resource_url() + '?details',
                           auth=(settings.TRANSIFEX_USER, settings.TRANSIFEX_PASSWORD))
    details = details.json()

    for lang in details['available_languages']:
        if lang['code'] != details['source_language_code']:
            yield lang['code']

def download_translation(lang):
    po = requests.get(get_resource_url() + 'translation/%s/' % lang,
                      auth=(settings.TRANSIFEX_USER, settings.TRANSIFEX_PASSWORD))
    po = po.json()

    if not os.path.exists(settings.DYNI18N_PATH):
        os.makedirs(settings.DYNI18N_PATH)
    path = os.path.join(settings.DYNI18N_PATH, 'dolweb.docs.faq.%s.po' % lang)
    open(path + '.tmp', 'w').write(po['content'].encode('utf-8'))
    os.rename(path + '.tmp', path)

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        for lang in get_all_langs():
            download_translation(lang)
