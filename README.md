Dolphin Emulator Official Website
=================================

https://dolphin-emu.org/

Technologies: Django (Python 3), HTML and CSS, using Twitter Bootstrap.

Author: mostly Pierre Bourdon (delroth@dolphin-emu.org).

Translations are handled via Transifex, see:
    https://www.transifex.com/projects/p/dolphin-emu/resource/website/

Quick overview
--------------

5 important applications:
 * Downloads: serves the list of downloads, revision info, branch list, etc.
   Gets requests from the Buildbot when a build is complete and updates its
   internal database.
 * Compat: serves the compatibility list, which gets its data from the Dolphin
   Wiki (https://wiki.dolphin-emu.org/) and from a MongoDB database containing
   game banners (fetched and used to generate an image atlas regularly).
 * Docs: serves the FAQ (stored internally in a database, with a dynamic i18n
   translation layer) and the guides (stored in the Dolphin Wiki).
 * Media: serves the screenshot gallery.
 * Homepage: serves the homepage.
 * Update: serves update metadata information to users.

Licensing
---------

Code is licensed under the MIT license: do whatever you want with it. Images
are licensed under the CC-by-sa license: if you want to use them, please
attribute them to us and redistribute them under the same license.
