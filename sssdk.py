#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import json
from contextlib import contextmanager


def create_sf_socket(sockfile):
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
    sock.connect(sockfile)
    return sock

def create_hp_socket(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect((host, int(port)))
    return sock

@contextmanager
def udp_socket(host=None, port=None, sockfile=None):
    sock = create_sf_socket(sockfile) if sockfile else create_hp_socket(host, port)
    try:
        yield sock
    finally:
        sock.close()

class ShadowsocksSDKError(Exception):
    pass

class TransferProtocol(object):
    def __init__(self):
        self.template = b'{command}: {json}'
    
    @staticmethod
    def ping():
        return b'ping'
    
    @staticmethod
    def add(self, json):
        return self.template.format('add', json=json.dumps(json))
    
    @staticmethod
    def remove(self, json):
        return self.template.format('remove', json=json.dumps(json))

class ShadowsocksSDK(object):
    def __init__(self, host, port, sockfile=None):
        self.host = host
        self.port = port
        self.sockfile = sockfile
        self.args = [host, port, sockfile]
    
    def _response(self, sock, size=1506):
        return sock.recv(1506)

    def ping(self):
        status = False
        with udp_socket(*self.args) as sock:
            sock.send(TransferProtocol.ping())
            if self._response(sock).strip() == 'pong':
                status = True
        return status
    
    def add_user(self, port, password):
        with udp_socket(*self.args) as sock:
            json_data = {
                'server_port': port,
                'password': password
            }
            sock.send(TransferProtocol.add(json_data))
            if self._response(sock).strip() != 'ok':
                raise ShadowsocksSDKError('add user error')
    
    def remove_user(self, port):
        with udp_socket(*self.args) as sock:
            json_data = {
                'server_port': port
            }
            sock.send(TransferProtocol.remove(json_data))
            if self._response(sock).strip() != 'ok':
                raise ShadowsocksSDKError('remove user error')

    def stat(self):
        with udp_socket(*self.args) as sock:
            while True:
                yield self._response(sock).strip()

if __name__ == '__main__':
    ss = ShadowsocksSDK('43.245.223.215', '6001')
    print(ss.ping())