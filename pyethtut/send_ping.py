#!/usr/bin/env python3.6

if __name__ == '__main__':
    from ipgetter import myip
    from discovery import EndPoint, PingServer
    my_ip = myip()
    my_endpoint = EndPoint(my_ip, 30303, 30303)
    their_endpoint = EndPoint('127.0.0.1', 30303, 30303)

    server = PingServer(my_endpoint)

    listen_thread = server.udp_listen()
    listen_thread.start()

    server.ping(their_endpoint)
