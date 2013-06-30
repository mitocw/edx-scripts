#!/usr/bin/python
#
# File:   edxStudioDownloader.py
# Date:   28-Apr-13
# Author: I. Chuang <ichuang@mit.edu>
#
# download course .tar.gz files from edX Studio
#
# Put username and passsword in config.py; eg
#    username = "me"
#    password = "my password"
# 
# Put course list in courses.py, eg:
#    courses  = [ 'HarvardX/ER22x/2013_Spring',]


import os, sys
import time
import requests
from courses import *
from config import *

def login(ses, username, pw):
    url = 'https://studio.edx.org/signin'
    r1 = ses.get(url)
    csrf = ses.cookies['csrftoken']
    url2 = 'https://studio.edx.org/login_post'
    headers = {'X-CSRFToken':csrf,
               'Referer': 'https://studio.edx.org/signin'}
    r2 = ses.post(url2, data={'email': username, 'password': pw}, headers=headers)
    if not r2.status_code==200:
        print "Login failed!"
        print r2.text
    
def do_download(ses, course_id):

    print "Downloading tar.gz for %s" % (course_id)

    url = 'https://studio.edx.org/%s/%s/generate_export/%s' % tuple(course_id.split('/'))
    r3 = ses.get(url)

    dt = time.ctime(time.time()).replace(' ','_').replace(':','')
    fn = 'COURSE-%s___%s.tar.gz' % (course_id.replace('/','__'),dt)

    open(fn, 'w').write(r3.content)
    print "--> %s" % (fn)
    return fn

#-----------------------------------------------------------------------------

ses = requests.session()
login(ses, username, password)

for cid in courses:
    do_download(ses, cid)

