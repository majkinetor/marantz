#!/usr/bin/python3
# -*- coding:utf-8 -*-
import os
import sys
import telnetlib
import signal
import time
import re

from flask import Flask
from flask.globals import request
from flask import render_template

app=Flask(__name__)
app.secret_key = '2d9-E2.)f&é,A5754f54g6$p@fpa+zSU03êû9_'

def signal_handler(signal, frame):
    print('You pressed Ctrl+C!')
    sys.exit(0)

def get_status():
    for x in range(0,3):
        try:
            tn.open(MARANTZ_IP, 23, 5)
            break;
        except Exception as err:
            if x == 3: 
                print("Telnet connection error", err)
                return
            #Telnet connection error, retrying after 100ms
            time.sleep(0.1)

    res = b''
    tn.read_eager()

    tn.write(b'PW?\r')
    res += tn.read_until(b"\r")
    tn.read_eager()

    tn.write(b'SI?\r')
    res += tn.read_until(b"\r")
    tn.read_eager()

    tn.write(b'MU?\r')
    res += tn.read_until(b"\r")
    tn.read_eager()

    tn.write(b'MV?\r')
    res += tn.read_until(b"\r")
    tn.read_eager()

    tn.close()
    return MARANTZ_IP + ' ' + re.sub('\r', ' ', res.decode('ASCII'))

def send_command( command ):
    # print('COMMAND: ', command)

    for x in range(0,3):
        try:
            tn.open(MARANTZ_IP, 23, 5)
            break;
        except Exception as err:
            if x == 3: 
                print("Telnet connection error", err)
                return
            #Telnet connection error, retrying after 100ms
            time.sleep(0.1)

    tn.write(command.encode('ASCII'))

    res = b''
    while True:
        r = tn.read_until(b"\r",0.2) #marantz responds after max 200ms
        if r == b'' : break
        res = res + r

    # print('RES: ', res, "\n")
    tn.close()
    return res.decode('ASCII')

@app.route('/')
def index():
    return render_template("index.html", status=get_status())

@app.route('/command')
def command():
    cmd=request.args['cmd'].upper()
    arg=request.args['arg'].upper()
    command = cmd + arg + "\r"
    send_command(command)
    return "OK"

# ----------------------------------------------------
with open(sys.path[0] + '/marantz.pid', "w") as pid_file:
    pid_file.write( str(os.getpid()) )

signal.signal(signal.SIGINT, signal_handler)

tn = telnetlib.Telnet()
MARANTZ_IP = os.environ.get("MARANTZ_IP")
if MARANTZ_IP is None:
    sys.exit('MARANTZ_IP environment variable is not set')
print("MARANTZ IP:", MARANTZ_IP)

if __name__=='__main__':
    app.run("0.0.0.0")
