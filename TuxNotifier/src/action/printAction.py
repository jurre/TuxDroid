'''
Created on May 12, 2011

@author: marthyn
'''
from time import strftime
from pymongo import Connection

class PrintAction():

    def __init__(self, text, type):
        
        self.connect("mongo.wtstest.com", 27017)
        
        self.date = strftime("%Y-%m-%d")
        self.time = strftime("%H:%M:%S")
        
        if type == "system":
            self.system_msg(text)
        elif type == "job_status":
            self.job_status_msg(text)
        elif type == "tux_speak":
            self.tux_speak_msg(text)
        print text
    
    """Function to put a system message into the MongoDB"""
    def system_msg(self, text):
        tabel = self.db.system_messages
        text = text.replace("\n", " ")
        text = text.replace("\r", " ")
        record = {"Date": self.date,
                  "Time": self.time,
                  "Message": text}
        tabel.insert(record)
    
    """Function to put a job status into the MongoDB"""
    def job_status_msg(self, text):
        tabel = self.db.jobs
        textArray = text.split("\n")
        record = {"Name": textArray[0].split(" ")[1],
                  "BuildNumber": textArray[1].split(" ")[2],
                  "Date": textArray[3].split(" ")[1],
                  "Time": textArray[4].split(" ")[1],
                  "Status": textArray[2].split(" ")[1]}
        tabel.insert(record)
    
    """Function to put a line of text that tux says into the MongoDB"""
    def tux_speak_msg(self, text):
        tabel = self.db.tuxSpeak
        text = text.replace("\n", " ")
        text = text.replace("\r", " ")
        record = {"Date": self.date,
                  "Time": self.time,
                  "Message": text}
        tabel.insert(record)
    
    """Connect to the MongoDB"""
    def connect(self, url, port):
        connection = Connection(url, port)
        self.db=connection.tuxdroid
        
        
    
        