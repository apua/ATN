#!/usr/bin/env python

import sys
import subprocess as sp

if len(sys.argv) == 2:
    app_name = sys.argv[1].rstrip('/')
else:
    exit(f'usage: python {__file__} {{app_name}}')

sp.run(f'm={app_name}/migrations; if [ -e $m ]; then rm -r $m; fi', shell=True)
sp.run(f'./manage.py makemigrations {app_name}', shell=True)
sp.run(f'./manage.py migrate {app_name}', shell=True)
