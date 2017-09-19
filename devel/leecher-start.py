# -*- coding: utf-8 -*-

__author__ = 'ogaidukov'

import subprocess
import sys
import os

# explicit path to celery executable as workaround for pyenv's shims and PuCharm strange behavior
celery_exec = os.path.join(os.path.dirname(sys.executable), 'celery')

if __name__ == "__main__":
    subprocess.call([celery_exec, 'worker', '-B', '-E',
                     '--config=leecher_celery_conf',
                     '--schedule=../tmp/celerybeat-schedule',
                     '--autoreload'])
