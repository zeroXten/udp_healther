#!/usr/bin/env python

from multiprocessing import Process
import time
import socket
import sys
import signal

def signal_handler(signum, frame):
    print "Exiting..."
    sys.exit(0)

def tcp_listen(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        s.bind((ip, int(port)))
        s.listen(5)
        while 1:
            conn, addr = s.accept()
	    print "Got a connection from", addr
            conn.send("OK\n")
            conn.close()
    except:
        print "Cant bind to socket"

def found_udp(port):
    found = False

    for line in open("/proc/net/udp").readlines():
        local_address = line.split()[1].split(":")
        if len(local_address) == 2 and int(local_address[1], 16) == int(port):
            found = True
            break
    return found

if len(sys.argv) != 3:
    print "Usage: udp_healther.py <udp_port> <tcp_port>"
    sys.exit(1)

ip = '0.0.0.0'
(udp_port, tcp_port) = sys.argv[1:]
delay = 1

signal.signal(signal.SIGINT, signal_handler)

just_started = True
proc = None
print "Starting UDP Healther. Looking for udp port %s and running tcp on port %s" % (udp_port, tcp_port)
while 1:
    if not proc:
        if found_udp(udp_port):
            print "UDP listener found, starting TCP listener"
            proc = Process(target=tcp_listen, args=(ip, tcp_port))
            proc.start()
        elif just_started:
            print "UDP listener not found. Waiting..."

    if proc and not found_udp(udp_port):
        print "UDP listener gone, killing TCP listener"
        proc.terminate()
        proc.join()
        proc = None

    just_started = False
    time.sleep(delay)
