# Monkey patches for "better" locale support.

from django.conf.urls import patterns
from django.core.urlresolvers import LocaleRegexURLResolver

def my_i18npatterns(prefix, *args):
    pattern_list = patterns(prefix, *args)
    return pattern_list + [LocaleRegexURLResolver(pattern_list)]
