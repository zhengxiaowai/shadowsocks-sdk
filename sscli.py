#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import argparse

from sssdk import ShadowsocksSDK, __version__


def get_version():
    return __version__


def create_sdk(host, port, sockfile=None):
    return ShadowsocksSDK(host, port, sockfile)


def cli_ping(args):
    ss = create_sdk(args.host, args.port)
    try:
        if ss.ping():
            print('PONG')
    except socket.error:
        print('NOT ACTIVE')


def cli_add(args):
    ss = create_sdk(args.host, args.port)
    ss.add_user(args.server_port, args.password)
    print('Successfully add new users, {}:{}.'.format(
        args.server_port, args.password))


def cli_remove(args):
    ss = create_sdk(args.host, args.port)
    ss.remove_user(args.server_port)
    print('Successfully remove users.')


def main():
    parser = argparse.ArgumentParser(add_help=False)

    #: main command arguments
    parser.add_argument(
        '-h', '--help',
        action='help',
        default=argparse.SUPPRESS,
        help='show sscli usage and message.')
    parser.add_argument(
        '-v', '--version',
        action='version',
        version=get_version(),
        help='show shadowsocks sdk version.')

    subparsers = parser.add_subparsers()
    subparsers.required = True

    #: host and port arguments
    parent_parser = argparse.ArgumentParser(add_help=False)
    parent_parser.add_argument(
        '--host',
        required=True,
        default='127.0.0.1',
        help='shadowsocks server manager bind host, default 127.0.0.1.')
    parent_parser.add_argument(
        '--port',
        required=True,
        default=6001,
        type=int,
        help='shadowsocks server manager bind port, default 6001.')

    #: server_port argument
    server_port_parser = argparse.ArgumentParser(add_help=False)
    server_port_parser.add_argument(
        '--server_port',
        required=True,
        default=9000,
        type=int,
        help='new server_port for new user, default 9000.')

    #: subcommand ping
    ping_parser = subparsers.add_parser(
        'ping',
        parents=[parent_parser],
        help='ping shadowsocks server.')
    ping_parser.set_defaults(func=cli_ping)

    #: subcommand add
    add_parser = subparsers.add_parser(
        'add',
        parents=[parent_parser, server_port_parser],
        help='add new user to shadowsocks server.')

    add_parser.add_argument(
        '--password',
        required=True,
        default='password',
        type=str,
        help='new password for new user, default password.')

    add_parser.set_defaults(func=cli_add)

    #: subcommand remove
    remove_parser = subparsers.add_parser(
        'remove',
        parents=[parent_parser, server_port_parser],
        help='remove a user from shadowsocks server.')

    remove_parser.set_defaults(func=cli_remove)

    args = parser.parse_args()
    try:
        args.func(args)
    except KeyboardInterrupt:
        print('user cancel.')
    except socket.timeout:
        print('Timeout, try again.')


if __name__ == '__main__':
    main()
