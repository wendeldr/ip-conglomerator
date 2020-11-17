#!/usr/bin/env python3

#./client.py 127.0.0.1 65432 search needle

from getmac import get_mac_address
import sys
import socket
import selectors
import traceback
import uuid
import libclient

sel = selectors.DefaultSelector()

def create_request(action='update'):
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    return dict(
        type="text/json",
        encoding="utf-8",
        content=dict(action=action, hostname=hostname, ip=local_ip, mac=get_mac_address()),
    )


def start_connection(key, host, port, request):
    addr = (host, port)
    print("starting connection to", addr)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(False)
    sock.connect_ex(addr)
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    message = libclient.Message(key, sel, sock, addr, request)
    sel.register(sock, events, data=message)


if len(sys.argv) < 3 or len(sys.argv) > 6:
    print("usage:", sys.argv[0], "<host> <port> <password> <optional-action (list)>")
    sys.exit(1)


host, port, password = sys.argv[1], int(sys.argv[2]), sys.argv[3]
print(password)
if len(sys.argv) == 5:
    request = create_request(sys.argv[4])
else:
    request = create_request()

start_connection(password, host, port, request)

try:
    while True:
        events = sel.select(timeout=1)
        for key, mask in events:
            message = key.data
            try:
                message.process_events(mask)
            except Exception:
                print(
                    "main: error: exception for",
                    f"{message.addr}:\n{traceback.format_exc()}",
                )
                message.close()
        # Check for a socket being monitored to continue.
        if not sel.get_map():
            break
except KeyboardInterrupt:
    print("caught keyboard interrupt, exiting")
finally:
    sel.close()
