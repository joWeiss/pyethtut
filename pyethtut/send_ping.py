#!/usr/bin/env python3.6

if __name__ == '__main__':
    from ipgetter import myip
    from discovery import EndPoint, PingServer
    my_ip = myip()
    my_endpoint = EndPoint(my_ip, 30303, 30303)
    # ping to ethereum foundation go bootnode
    # see https://ocalog.com/post/18/
    their_endpoint = EndPoint('52.16.188.185', 30303, 30303)

    server = PingServer(my_endpoint)

    listen_thread = server.udp_listen()
    listen_thread.start()

    server.ping(their_endpoint)
