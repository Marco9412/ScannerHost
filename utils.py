
import os
import os.path
import subprocess


def check_folder():
    if not os.path.isdir('./sessions'):
        os.mkdir('./sessions')
    if not os.path.isdir('./documents'):
        os.mkdir('./documents')


def scan(session_id):
    directory = './sessions/%s' % session_id

    if not os.path.isdir(directory):
        os.mkdir(directory)

    num = len(os.listdir(directory))
    proc = subprocess.run(['/bin/bash', '-c', 'scanimage --resolution 300 --format=png > %s/%d.png' % (directory, num)])
    return ('%s/%d.png' % (directory, num)), proc.returncode == 0


def pdf(session_id):
    directory = './sessions/%s' % session_id
    output = './documents/%s' % session_id

    if not os.path.isdir(directory):
        return None, False
    if not os.path.isdir(output):
        os.mkdir(output)

    res = ''
    num = len(os.listdir(directory))
    for n in range(0, num):
        res = res + '%s/%d.png ' % (directory, n)

    proc = subprocess.run(['/bin/bash', '-c', 'convert %s %s/document.pdf' % (res, output)])
    return ('%s/document.pdf' % output), proc.returncode == 0
