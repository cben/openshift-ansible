# This file is not part of openshift-ansible code, it's mounted into awx
# and just happens to be written in Python.  Based on
# https://github.com/ansible/awx/blob/1.0.3/installer/openshift/templates/configmap.yml.j2
# pylint: skip-file

import os
import socket
ADMINS = ()

# Container environments don't like chroots
AWX_PROOT_ENABLED = False

#Autoprovisioning should replace this
CLUSTER_HOST_ID = socket.gethostname()
SYSTEM_UUID = '00000000-0000-0000-0000-000000000000'

REMOTE_HOST_HEADERS = ['HTTP_X_FORWARDED_FOR']

CELERY_TASK_QUEUES += (Queue(CLUSTER_HOST_ID, Exchange(CLUSTER_HOST_ID), routing_key=CLUSTER_HOST_ID),)
CELERY_TASK_ROUTES['awx.main.tasks.cluster_node_heartbeat'] = {'queue': CLUSTER_HOST_ID, 'routing_key': CLUSTER_HOST_ID}
CELERY_TASK_ROUTES['awx.main.tasks.purge_old_stdout_files'] = {'queue': CLUSTER_HOST_ID, 'routing_key': CLUSTER_HOST_ID}
STATIC_ROOT = '/var/lib/awx/public/static'
PROJECTS_ROOT = '/var/lib/awx/projects'
JOBOUTPUT_ROOT = '/var/lib/awx/job_status'
SECRET_KEY = file('/etc/tower/SECRET_KEY', 'rb').read().strip()
ALLOWED_HOSTS = ['*']
INTERNAL_API_URL = 'http://127.0.0.1:8052'
AWX_TASK_ENV['HOME'] = '/var/lib/awx'
SERVER_EMAIL = 'root@localhost'
DEFAULT_FROM_EMAIL = 'webmaster@localhost'
EMAIL_SUBJECT_PREFIX = '[AWX] '
EMAIL_HOST = 'localhost'
EMAIL_PORT = 25
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = False

LOGGING['handlers']['console'] = {
    '()': 'logging.StreamHandler',
    'level': 'DEBUG',
    'formatter': 'simple',
}

LOGGING['loggers']['django.request']['handlers'] = ['console']
LOGGING['loggers']['rest_framework.request']['handlers'] = ['console']
LOGGING['loggers']['awx']['handlers'] = ['console']
LOGGING['loggers']['awx.main.commands.run_callback_receiver']['handlers'] = ['console']
LOGGING['loggers']['awx.main.commands.inventory_import']['handlers'] = ['console']
LOGGING['loggers']['awx.main.tasks']['handlers'] = ['console']
LOGGING['loggers']['awx.main.scheduler']['handlers'] = ['console']
LOGGING['loggers']['django_auth_ldap']['handlers'] = ['console']
LOGGING['loggers']['social']['handlers'] = ['console']
LOGGING['loggers']['system_tracking_migrations']['handlers'] = ['console']
LOGGING['loggers']['rbac_migrations']['handlers'] = ['console']
LOGGING['loggers']['awx.isolated.manager.playbooks']['handlers'] = ['console']
LOGGING['handlers']['callback_receiver'] = {'class': 'logging.NullHandler'}
LOGGING['handlers']['fact_receiver'] = {'class': 'logging.NullHandler'}
LOGGING['handlers']['task_system'] = {'class': 'logging.NullHandler'}
LOGGING['handlers']['tower_warnings'] = {'class': 'logging.NullHandler'}
LOGGING['handlers']['rbac_migrations'] = {'class': 'logging.NullHandler'}
LOGGING['handlers']['system_tracking_migrations'] = {'class': 'logging.NullHandler'}
LOGGING['handlers']['management_playbooks'] = {'class': 'logging.NullHandler'}

DATABASES = {
    'default': {
        'ATOMIC_REQUESTS': True,
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': "awx",
        'USER': "awx",
        'PASSWORD': os.getenv('DATABASE_PASSWORD'),
        'HOST': "postgresql",
        'PORT': "5432",
    }
}
CELERY_BROKER_URL = 'amqp://{}:{}@{}:{}/{}'.format(
    "awx",
    "abcdefg",
    "localhost",
    "5672",
    "awx")
CHANNEL_LAYERS = {
    'default': {'BACKEND': 'asgi_amqp.AMQPChannelLayer',
                'ROUTING': 'awx.main.routing.channel_routing',
                'CONFIG': {'url': CELERY_BROKER_URL}}
}
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '{}:{}'.format("localhost", "11211")
    },
    'ephemeral': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    },
}
