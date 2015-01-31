from fabric.api import *

env.user = 'dolphin-emu'
env.hosts = ['ssh.alwaysdata.com']

def deploy(root, branch):
    activate = "source /home/dolphin-emu/venv/new-www/bin/activate"
    with cd(root):
        run("git fetch")
        run("git checkout %s" % branch)
        run("git reset --hard origin/%s" % branch)
        run(activate + " && pip install -r requirements.txt")
        run(activate + " && python manage.py collectstatic --noinput")
        with cd("dolweb"):
            run("msgfmt localefixes/locale/ko/LC_MESSAGES/django.po -o "
                       "localefixes/locale/ko/LC_MESSAGES/django.mo")
            run(activate + " && django-admin.py compilemessages")
    run("scripts/restart-apps.sh")

def deploy_stable():
    deploy("/home/dolphin-emu/apps/www", "stable")

def deploy_dev():
    deploy("/home/dolphin-emu/apps/devwww", "master")
