import paramiko
from multiprocessing import Process, Queue
import datetime
import config
import pickle
import os.path
import math
import re
import discord
import botClient as bc
import asyncio
import time
import threading
import sys
from flask import Flask, request
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route('/lab-information-post', methods=['POST'])
@app.route('/lab-information-post/', methods=['POST'])
def recv_file():
    if 'file' in request.files:
        file = request.files['file']
        if file.filename != '' and file and '.' in file.filename and \
            file.filename.rsplit('.', 1)[1].lower() in ['csv']:
            filename = secure_filename(file.filename)
            try:
                os.mkdir('./uploads')
            except:
                pass
            file.save(os.path.join('./uploads', filename))

class LabScan():
    def __init__(self, configfile):
        self.labs = {}
        self.mins = []
        self.configfile = configfile
        self.bot = None
        self.newLabs = False
        self.lock = threading.Lock()
        self.quit = False
        try:
            labt = pickle.load( open( "./persistence/labs.p", "rb" ) )
            self.lock.acquire()
            self.labs = labt[0]
            self.mins = labt[1]
            self.lock.release()
            print("Labs successfully loaded.")
        except:
            print("No labs to load")
    
    def pollLabs(self):
        sp = 2
        for room in [218,219,220,221,232]:
            print("lab" + str(room) + ":\n  ", end='', flush=True)
            for row in range(1,7):
                print( "  0" + str(row), end='', flush=True)
            print("")
            for column in "abcd":
                print("-" + str(column), end='', flush=True)
                line = ""
                for row in range(1,7):
                    host = "lab{}-{}0{}.cs.curtin.edu.au.".format(room,column,row)
                    self.lock.acquire()
                    self.labs[host] = users
                    self.lock.release()
                    if (users>-1 and users < mini):
                        mini = users
                        mins = []
                    if (users == mini):
                        mins.append(host)
                    line += "  " + str((" ",users)[users!=-1]) + pad(users,sp)
                print(line,flush=True)
        self.lock.acquire()
        self.mins = mins
        max = -1
        for lab in sorted(self.labs,key=self.labs.get):
            if self.labs[lab] > max:
                max = self.labs[lab]
        if max != -1:
            print("Saving up machines to file", flush=True)
            pickle.dump( (self.labs,self.mins), open ("./persistence/labs.p", "wb" ) )
        self.lock.release()
        if self.bot:
            if self.bot.eloop:
                self.bot.eloop.create_task(self.bot.updatePMsg())

def pad(inte,places):
    if inte < 1:
        padding = places-1
    else:
        padding = (places-int(1+math.log10(abs(inte))))
    return " " * padding