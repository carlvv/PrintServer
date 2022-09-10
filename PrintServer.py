import os
import sys
import time
from imap_tools import MailBox, AND
from bs4 import BeautifulSoup


def emailListener(email_server, username, password, sleeptime, email_whitelist, printer):
    while True:
        with MailBox(email_server).login(username, password) as mailbox:
            for msg in mailbox.fetch(AND(seen=False)):
                for currentMail in email_whitelist:
                    if msg.from_ == currentMail:
                        for att in msg.attachments:
                            if att.filename[len(att.filename) - 4:] == ".pdf":
                                print("Printing: " + att.filename + " from " + msg.from_)
                                with open(att.filename, "wb") as binary_file:
                                    binary_file.write(att.payload)
                                os.system(printer.format(att.filename))
        time.sleep(sleeptime)


def main():
    try:
        with open('config.xml', 'r') as f:
            credentials = f.read()
            bs_data = BeautifulSoup(credentials, "lxml")
            if sys.platform == "linux" or sys.platform == "linux2":
                printer = bs_data.find("printer-linux").text
            elif sys.platform == "win32":
                printer = "cmd /c " + os.getcwd() + "\\" + bs_data.find("printer-win").text
        if not os.path.exists("Attachments"):
            os.mkdir("Attachments")
        os.chdir("Attachments")
        emailListener(bs_data.find("server").text,
                      bs_data.find("username").text,
                      bs_data.find("password").text,
                      int(bs_data.find("sleep-time").text),
                      bs_data.find("whitelist").text.strip().split(";"),
                      printer)
    except KeyboardInterrupt:
        exit(0)


if __name__ == '__main__':
    main()
