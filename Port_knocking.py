#!/usr/bin/env python3

import argparse
import socket
import sys
import time

class Knocker(object):
    def __init__(self, args: list):
        self._parse_args(args)

    def _parse_args(self, args: list):
        parser = argparse.ArgumentParser(description='Simple port-knocking client written in python3.\n'
                                                     'See more at https://github.com/grongor/knock')

        parser.add_argument('-t', '--timeout', type=int, default=200,
                            help='How many milliseconds to wait on a hanging connection. Default is 200 ms.')
        parser.add_argument('-d', '--delay', type=int, default=200,
                            help='How many milliseconds to wait between each knock. Default is 200 ms.')
        parser.add_argument('-u', '--udp', help='Use UDP instead of TCP by default.', action='store_true')
        parser.add_argument('-v', '--verbose', help='Be verbose.', action='store_true')
        parser.add_argument('host', help='Hostname or IP address of the host to knock on. Supports IPv6.')
        parser.add_argument('ports', metavar='port[:protocol]', nargs='*',
                            help='Port(s) to knock on, protocol (tcp, udp) is optional. If not provided, knocks on all ports.')

        args = parser.parse_args(args)
        self.timeout = args.timeout / 1000
        self.delay = args.delay / 1000
        self.default_udp = args.udp
        self.ports = args.ports
        self.verbose = args.verbose

        self.address_family, _, _, _, ip = socket.getaddrinfo(
            host=args.host,
            port=None,
            flags=socket.AI_ADDRCONFIG
        )[0]
        self.ip_address = ip[0]

        if not self.ports:
            # If no specific ports are provided, knock on all ports (65535)
            self.ports = [str(port) for port in range(1, 65536)]

    def _log_result(self, result):
        with open("open_ports.txt", "a") as f:
            f.write(result + '\n')

    def knock(self):
        last_index = len(self.ports) - 1
        for i, port in enumerate(self.ports):
            use_udp = self.default_udp
            if port.find(':') != -1:
                port, protocol = port.split(':', 2)
                if protocol == 'tcp':
                    use_udp = False
                elif protocol == 'udp':
                    use_udp = True
                else:
                    error = 'Invalid protocol "{}" given. Allowed values are "tcp" and "udp".'
                    raise ValueError(error.format(protocol))

            if self.verbose:
                print('hitting %s %s:%d' % ('udp' if use_udp else 'tcp', self.ip_address, int(port)))

            s = socket.socket(self.address_family, socket.SOCK_DGRAM if use_udp else socket.SOCK_STREAM)
            s.setblocking(False)

            socket_address = (self.ip_address, int(port))
            result = f'Port {port} on {self.ip_address} is closed'
            try:
                if use_udp:
                    s.sendto(b'', socket_address)
                    result = f'Port {port} on {self.ip_address} is open'
                else:
                    s.connect_ex(socket_address)
                    result = f'Port {port} on {self.ip_address} is open'
            except Exception as e:
                pass
            finally:
                s.close()

            if self.verbose:
                print(result)

            if "open" in result:
                self._log_result(result)

            if self.delay and i != last_index:
                time.sleep(self.delay)


if __name__ == '__main__':
    Knocker(sys.argv[1:]).knock()
