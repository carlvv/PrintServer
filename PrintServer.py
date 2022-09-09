import os
import sys
import time
from imap_tools import MailBox, A
from bs4 import BeautifulSoup

email_server = ""
username = ""
password = ""
email_whitelist = []
printer = ""
sleeptime = 0


def emailListener():
    while True:
        with MailBox(email_server).login(username, password) as mailbox:
            for msg in mailbox.fetch(A(seen=False)):
                for currentMail in email_whitelist:
                    if msg.from_ == currentMail:
                        for att in msg.attachments:
                            if att.filename[len(att.filename) - 4:] == ".pdf":
                                print("Printing: " + att.filename + " from " + msg.from_)
                                with open(att.filename.join(), "wb") as binary_file:
                                    binary_file.write(att.payload)
                                os.system(printer.format(att.filename))
        time.sleep(sleeptime)


try:
    with open('config.xml', 'r') as f:
        credentials = f.read()
        Bs_data = BeautifulSoup(credentials, "lxml")
        email_server = Bs_data.find("server").text
        username = Bs_data.find("username").text
        password = Bs_data.find("password").text
        sleeptime = int(Bs_data.find("sleeptime").text)
        email_whitelist = Bs_data.find("whitelist").text.strip().split(";")
        if sys.platform == "linux" or sys.platform == "linux2":
            printer = Bs_data.find("printer-linux").text
        elif sys.platform == "win32":
            printer = Bs_data.find("printer-win").text
    os.chdir("Attachments")
    emailListener()
except KeyboardInterrupt:
    exit(0)
