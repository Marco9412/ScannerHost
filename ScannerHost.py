#!/usr/bin/env python3

# ----------------------------------------------------------------------------------------------------------------------
# Scanner Host
# Marco Panato
# 2018-06-14
#
# Simple web app that permit the user to take pictures from a saned scanner and automatically generate pdf.
# ----------------------------------------------------------------------------------------------------------------------


from flask import Flask, session, render_template, redirect, send_from_directory, request
from flask_socketio import SocketIO, emit
import uuid
import utils
import os


app = Flask(__name__, static_url_path='')
app.secret_key = 'A0Zr98j/3YX R~XHH!jmN]LWX/,?RT'  # TODO change me!
socket_io = SocketIO(app)


def get_current_uuid():
    if 'uid' not in session:
        if request.method == 'GET':
            return request.args.get('uid')
        elif request.method == 'POST':
            return request.form['uid']
        else:
            return None
    else:
        return session['uid']


# ----------------------------------------------------------------------------------------------------------------------
# Web sockets
@socket_io.on('scanPlease')
def do_scan_socket():
    if 'uid' in session:
        path, res = utils.scan(str(session['uid']))
        if res:
            emit('scanOk', path)
        else:
            emit('scanErr')
    else:
        emit('scanErr')
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# Browser way
@app.route('/pdf')
def get_pdf():
    current_uid = get_current_uuid()
    if current_uid:
        path, res = utils.pdf(str(current_uid))
        #if res:
        return redirect(path)
    return "Error"


@app.route('/', methods=['GET'])
def hello_world():
    if 'uid' not in session:
        session['uid'] = uuid.uuid4()  # generate random session-id
    return render_template('main.html')


@app.route('/sessions/<path:path>')
def send_image(path):
    return send_from_directory(utils.SESSIONS_FOLDER, path)


@app.route('/documents/<path:path>')
def send_documents(path):
    return send_from_directory(utils.DOCUMENTS_FOLDER, path)
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# External app way
@app.route('/new_session')
def new_session():
    if 'uid' not in session:
        session['uid'] = uuid.uuid4()  # generate random session-id
    return str(session['uid'])


@app.route('/scan')
def do_scan():
    current_uid = get_current_uuid()
    if current_uid:
        path, res = utils.scan(str(current_uid))
        return str(path) if res else '-1'
    return '-2'
# ----------------------------------------------------------------------------------------------------------------------


utils.check_folder()  # create session and documents folders

if __name__ == '__main__':
    port = os.environ['SCANNER_HOST_PORT'] if 'SCANNER_HOST_PORT' in os.environ else '9996'
    socket_io.run(app, host='0.0.0.0', port=int(port))
