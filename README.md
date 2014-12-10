udp\_healther
=============

Simple python script to help monitor UDP services using TCP healthchecks.

Overview
========

Lets say you've got a service listening on UDP port 1234. You would like to load balance across multiple servers running the service. With UDP you're probably not going to get a reply. You could also check the entire box is up using an ICMP healthcheck.

This tool takes a different approach. Running the script on the same box as the service, it will look to see if something is listening on the chosen UDP port. If it is, then this tool opens up a TCP port that can be used for health checks.

Installation
============

TODO - this needs to be run as a service...

Usage
========

    $ ./udp_healther.py
    Usage: udp_healther.py <udp_port> <tcp_port>

Example
=======

We're going to use netcat as our service that listens on UDP port 6000. We want our healthcheck to test TCP port 5000.

First lets run the tool

    $ ./udp_healther.py 6000 5000
    Starting UDP Healther. Looking for udp port 6000 and running tcp on port 5000
    UDP listener not found. Waiting...

Now start netcat

    $ nc -l -u -p 6000

The tool output will now be

    $ ./udp_healther.py 6000 5000
    Starting UDP Healther. Looking for udp port 6000 and running tcp on port 5000
    UDP listener not found. Waiting...
    UDP listener found, starting TCP listener

Test the TCP connection:

    $ nc localhost 5000
    OK

The tool output will now be:

    $ ./udp_healther.py 6000 5000
    Starting UDP Healther. Looking for udp port 6000 and running tcp on port 5000
    UDP listener not found. Waiting...
    UDP listener found, starting TCP listener
    Got a connection from ('127.0.0.1', 53269)

If we stop the netcat listen we will see

    $ ./udp_healther.py 6000 5000
    Starting UDP Healther. Looking for udp port 6000 and running tcp on port 5000
    UDP listener not found. Waiting...
    UDP listener found, starting TCP listener
    Got a connection from ('127.0.0.1', 53269)
    UDP listener gone, killing TCP listener
