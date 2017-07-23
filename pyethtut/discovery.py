import socket
import threading
import time
import struct
import rlp
from crypto import keccak256
from secp256k1 import PrivateKey
from ipaddress import ip_address

from typing import Union


class EndPoint(object):
    def __init__(self, address: Union[str, int], udpPort: int, tcpPort: int):
        self.address = ip_address(address)
        self.udpPort = udpPort
        self.tcpPort = tcpPort

    def pack(self):
        return [self.address.packed,
                struct.pack(">H", self.udpPort),
                struct.pack(">H", self.tcpPort)]


class PingNode(object):
    packet_type = b'\x01'
    version = b'\x03'

    def __init__(self, endpoint_from: EndPoint, endpoint_to: EndPoint):
        self.endpoint_from = endpoint_from
        self.endpoint_to = endpoint_to

    def pack(self):
        return [self.version,
                self.endpoint_from.pack(),
                self.endpoint_to.pack(),
                struct.pack(">I", int(time.time()) + 60)]


class PingServer(object):
    def __init__(self, my_endpoint: EndPoint):
        self.endpoint = my_endpoint

        # get private key
        with open('priv_key', 'r') as priv_key_file:
            priv_key_serialized = priv_key_file.read()
        self.priv_key = PrivateKey()  # type: PrivateKey
        self.priv_key.deserialize(priv_key_serialized)

        # init socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('0.0.0.0', self.endpoint.udpPort))

    def wrap_packet(self, packet):
        payload = packet.packet_type + rlp.encode(packet.pack())
        sig = self.priv_key.ecdsa_sign_recoverable(keccak256(payload), raw=True)
        sig_serialized = self.priv_key.ecdsa_recoverable_serialize(sig)
        payload = b''.join([sig_serialized[0], str.encode(chr(sig_serialized[1])),
                            payload])

        payload_hash = keccak256(payload)
        return payload_hash + payload

    def udp_listen(self):
        def receive_ping():
            print("listening...")
            data, addr = self.sock.recvfrom(1024)
            print("received message[", addr, "]")

        return threading.Thread(target=receive_ping)

    def ping(self, endpoint: EndPoint):
        ping = PingNode(self.endpoint, endpoint)
        message = self.wrap_packet(ping)
        print("sending ping...")
        self.sock.sendto(message, (endpoint.address.exploded, endpoint.udpPort))
