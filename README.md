# shadowsocks-sdk
the sdk canhelp you to manage your shadowsocks sever

# Usage

- sdk usage
- cli usage

```
pip install shadowsocks-sdk
```

## SDK Usage

```
ss = ShadowsocksSDK('127.0.0.1', 6001)
print(ss.ping())
ss.add_user('9000', 'password')
ss.remove_user('9000')
```

## CLI Usage

```
usage: sscli [-h] [-v] {ping,add,remove} ...

positional arguments:
  {ping,add,remove}
    ping             ping shadowsocks server.
    add              add new user to shadowsocks server.
    remove           remove a user from shadowsocks server.

optional arguments:
  -h, --help         show sscli usage and message.
  -v, --version      show shadowsocks sdk version.
```

### ping usage

```
usage: sscli ping [-h] --host HOST --port PORT

optional arguments:
  -h, --help   show this help message and exit
  --host HOST  shadowsocks server manager bind host, default 127.0.0.1.
  --port PORT  shadowsocks server manager bind port, default 6001.

```

### add usage

```
usage: sscli add [-h] --host HOST --port PORT --server_port SERVER_PORT
                 --password PASSWORD

optional arguments:
  -h, --help            show this help message and exit
  --host HOST           shadowsocks server manager bind host, default
                        127.0.0.1.
  --port PORT           shadowsocks server manager bind port, default 6001.
  --server_port SERVER_PORT
                        new server_port for new user, default 9000.
  --password PASSWORD   new password for new user, default password.
```

### remove usage 

```
usage: sscli remove [-h] --host HOST --port PORT --server_port SERVER_PORT

optional arguments:
  -h, --help            show this help message and exit
  --host HOST           shadowsocks server manager bind host, default
                        127.0.0.1.
  --port PORT           shadowsocks server manager bind port, default 6001.
  --server_port SERVER_PORT
                        new server_port for new user, default 9000.
```

# LICENSE

MIT
