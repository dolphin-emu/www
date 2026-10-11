# Copyright (c) 2018 Dolphin Emulator Website Contributors
# SPDX-License-Identifier: MIT

from zinnia.views.mixins.entry_preview import EntryPreviewMixin

# TODO(delroth): Ugly. Should really authenticate these requests, but we don't
# have a nice SSO story at the moment.
del EntryPreviewMixin.get_object
