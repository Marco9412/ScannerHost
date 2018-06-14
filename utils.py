
import os
import os.path
import subprocess


def scan(session_id):
    directory = './sessions/%s' % session_id

    if not os.path.isdir(directory):
        os.mkdir(directory)

    num = len(os.listdir(directory))
    proc = subprocess.run(['/bin/bash', '-c', 'scanimage --resolution 300 --format=png > %s/%d.png' % (directory, num)])
    return ('%s/%d.png' % (directory, num)), proc.returncode == 0


def pdf(session_id):
    directory = './sessions/%s' % session_id

    if not os.path.isdir(directory):
        return None, False

    res = ''
    num = len(os.listdir(directory))
    for n in range(0, num):
        res = res + '%s/%d.png ' % (directory, n)

    proc = subprocess.run(['/bin/bash', '-c', 'convert %s %s/document.pdf' % (res, directory)])
    return ('%s/document.pdf' % directory), proc.returncode == 0
