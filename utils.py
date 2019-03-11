
import os
import os.path
import subprocess

# Or can be the name of the scanner to use to speedup scanning
# The name can be extracted by executing 'scanimage -L'
SCANNER_DEVICE = None  #'epson2:libusb:001:003'

BASEPATH = os.environ['SCANNER_HOST_BASEPATH'] if 'SCANNER_HOST_BASEPATH' in os.environ else '.'
SESSIONS_SUFFIX = '/sessions'
DOCUMENTS_SUFFIX = '/documents'

SESSIONS_FOLDER = BASEPATH + SESSIONS_SUFFIX
DOCUMENTS_FOLDER = BASEPATH + DOCUMENTS_SUFFIX


def check_folder():
    if not os.path.isdir(SESSIONS_FOLDER):
        os.mkdir(SESSIONS_FOLDER)
    if not os.path.isdir(DOCUMENTS_FOLDER):
        os.mkdir(DOCUMENTS_FOLDER)


def scan(session_id):
    directory = '%s/%s' % (SESSIONS_FOLDER, session_id)
    returnurl = '%s/%s' % (SESSIONS_SUFFIX, session_id)

    if not os.path.isdir(directory):
        os.mkdir(directory)

    num = len(os.listdir(directory))
    if SCANNER_DEVICE:
        proc = subprocess.run(
            ['/bin/sh', '-c', 'scanimage --resolution 300 -d %s --format=png > %s/%d.png'
             % (SCANNER_DEVICE, directory, num)])
        return ('%s/%d.png' % (returnurl, num)), proc.returncode == 0
    else:
        proc = subprocess.run(['/bin/bash', '-c', 'scanimage --resolution 300 --format=png > %s/%d.png'
                               % (directory, num)])
        return ('%s/%d.png' % (returnurl, num)), proc.returncode == 0


def pdf(session_id):
    directory = '%s/%s' % (SESSIONS_FOLDER, session_id)
    output = '%s/%s' % (DOCUMENTS_FOLDER, session_id)
    returnurl = '%s/%s' % (DOCUMENTS_SUFFIX, session_id)

    if not os.path.isdir(directory):
        return None, False
    if not os.path.isdir(output):
        os.mkdir(output)

    res = ''
    num = len(os.listdir(directory))
    for n in range(0, num):
        res = res + '%s/%d.png ' % (directory, n)

    proc = subprocess.run(['/bin/sh', '-c', 'convert %s %s/document.pdf' % (res, output)])
    return ('%s/document.pdf' % returnurl), proc.returncode == 0

