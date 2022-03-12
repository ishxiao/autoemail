#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
file: ipemail.py

Created on Thu Feb 02 11:00:00 2022

@author: Xiao Shang

email: me@ishxiao.com

note: Send new ip to my email.
"""

from urllib.request import urlopen
import re
import smtplib
import sm
import socket

# Setup our login credentials
from_address = [FROM_EMAIL_ADDRESS]
to_address = [TO_EMAIL_ADDRESS]
subject = [EMAIL_SUBJECT]
username = [LOGIN_EMAIL_ACCOUNT]
password = [LOGIN_EMAIL_PASSWORD]

# last_ip path
path_to_last_ip = '/home/ubuntu' #pi
# path_to_last_ip = '/home/ishx/Downloads' # ishx-pc
path_to_tor = '/home/ubuntu' # pi
def get_local_ip():
    url = 'www.baidu.com'
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((url, 0))
        print(f"Our chosen local IP address service is {url}")
        local_ip = s.getsockname()[0]
    except:
        local_ip = "x.x.x.x"
    finally:
        s.close()
    return local_ip

def get_external_ip():
    # Setup where we will get our IP address
    url = 'http://icanhazip.com'
    print(f"Our chosen external IP address service is {url}")

    # Open up the url, then read the contents, and take away our IP address
    request = urlopen(url).read().decode('utf-8')
    # We extract the IP address only
    # remove '\n'
    external_ip = request[:-1]

    return external_ip

def get_ip():
    return get_external_ip(), get_local_ip()

def send_email(ourIP):
    # Body of the email'
    body_text = f"Our IP address is:\nExternal IP: {ourIP[0]}\nLocal IP: {ourIP[1]}\n"
    msg = '\r\n'.join(['To: %s' % to_address, 'From: %s' % from_address, 'Subject: %s' % subject, '', body_text])

    # Actually send the email!
    server = smtplib.SMTP('smtp.qq.com:587')
    server.starttls() # Our security for transmission of credentials
    server.login(username,password)
    server.sendmail(from_address, to_address, msg)
    server.quit()
    print("New IP address has been sent via email!!")

def check_ip():
    # Check to see if our IP address has really changed
    ourIP = list(get_ip())
    print(f"Our IP address is:\nExternal IP: {ourIP[0]}\nLocal IP: {ourIP[1]}")
    # Open up previous IP address (last_ip.txt) and extract contents
    lastIP = []
    with open(path_to_last_ip +'/ipemail/last_ip.txt', 'rt') as last_ip:
        for line in last_ip:
            lastIP.append(line.strip()) # Read the text file
    if lastIP == ourIP:
        print("Our IP address has not changed.")
    else:
        print("We have a new IP address.")
        with open(path_to_last_ip +'/ipemail/last_ip.txt', 'wt') as last_ip:
            for line in ourIP:
                last_ip.write(line+'\n')
        print("We have written the new IP address to the text file.")
        send_email(ourIP)

def main():
    check_ip()

    return 0

if __name__ == '__main__':
    main()
