# Copyright (c) 2018 Dolphin Emulator Website Contributors
# SPDX-License-Identifier: MIT

from fabric import task

_HOSTS = ["dolphin-emu@ssh-dolphin-emu.alwaysdata.net"]

def deploy(c, root, branch):
    activate = "source /home/dolphin-emu/venv/www/bin/activate"
    with c.cd(root):
        c.run("git fetch")
        c.run("git checkout %s" % branch)
        c.run("git reset --hard origin/%s" % branch)
        c.run(activate + " && pip install -r requirements.txt")
        c.run(activate + " && python manage.py collectstatic --noinput")
        with c.cd("dolweb"):
            c.run("msgfmt localefixes/locale/ko/LC_MESSAGES/django.po -o "
                       "localefixes/locale/ko/LC_MESSAGES/django.mo")
            c.run(activate + " && django-admin compilemessages")
    c.run("scripts/restart-apps.sh")

@task(hosts=_HOSTS)
def deploy_stable(c):
    deploy(c, "/home/dolphin-emu/apps/www", "stable")

@task(hosts=_HOSTS)
def deploy_dev(c):
    deploy(c, "/home/dolphin-emu/apps/devwww", "master")
