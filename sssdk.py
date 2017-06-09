#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import json
from contextlib import contextmanager

__version__ = '0.1.0dev'

TIME_OUT_SEC = 3
BINARY_FORMAT = 'utf8'


def create_sf_socket(sockfile):
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
    sock.settimeout(TIME_OUT_SEC)
    sock.connect(sockfile)
    return sock


def create_hp_socket(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(TIME_OUT_SEC)
    sock.connect((host, int(port)))
    return sock


@contextmanager
def udp_socket(host=None, port=None, sockfile=None):
    sock = create_sf_socket(sockfile) \
        if sockfile else create_hp_socket(host, port)
    try:
        yield sock
    finally:
        sock.close()


class ShadowsocksSDKError(Exception):
    pass


class TransferProtocol(object):
    template = '{command}: {json}'

    @staticmethod
    def ping():
        return str('ping').encode(BINARY_FORMAT)

    @staticmethod
    def add(json_data):
        text = TransferProtocol.template.format(
            command='add',
            json=json.dumps(json_data))
        return text.encode(BINARY_FORMAT)

    @staticmethod
    def remove(json_data):
        text = TransferProtocol.template.format(
            command='remove',
            json=json.dumps(json_data))
        return text.encode(BINARY_FORMAT)


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
            resp_text = self._response(sock).strip()
            if resp_text.decode(BINARY_FORMAT) == 'pong':
                status = True
        return status

    def add_user(self, port, password):
        with udp_socket(*self.args) as sock:
            json_data = {
                'server_port': int(port),
                'password': password
            }
            sock.send(TransferProtocol.add(json_data))
            resp_text = self._response(sock).strip()
            if resp_text.decode(BINARY_FORMAT) != 'ok':
                raise ShadowsocksSDKError('add user error')

    def remove_user(self, port):
        with udp_socket(*self.args) as sock:
            json_data = {
                'server_port': int(port)
            }
            sock.send(TransferProtocol.remove(json_data))
            resp_text = self._response(sock).strip()
            if resp_text.decode(BINARY_FORMAT) != 'ok':
                raise ShadowsocksSDKError('remove user error')
