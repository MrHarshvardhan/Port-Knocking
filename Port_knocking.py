#!/usr/bin/env python3

import argparse
from tqdm import tqdm
import socket
import os
import sys
import time

class Knocker:
    def __init__(self, args):
        self.parse_args(args)

    def parse_args(self, args):
        parser = argparse.ArgumentParser(description='Simple port-knocking client written in python3.')
        parser.add_argument('-t', '--timeout', type=int, default=200, help='Timeout in milliseconds.')
        parser.add_argument('-d', '--delay', type=int, default=200, help='Delay in milliseconds between knocks.')
        parser.add_argument('-v', '--verbose', action='store_true', help='Be verbose.')
        parser.add_argument('hosts', nargs='+', help='Hostnames or IP addresses of the hosts to knock on. Supports IPv6.')
        args = parser.parse_args(args)
        self.timeout = args.timeout / 1000
        self.delay = args.delay / 1000
        self.verbose = args.verbose
        self.hosts = args.hosts

    def knock(self, host, port, use_udp):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM if use_udp else socket.SOCK_STREAM)
            s.settimeout(self.timeout)
            socket_address = (host, port)
            if use_udp:
                s.sendto(b'', socket_address)
            else:
                s.connect_ex(socket_address)
            s.close()
            return True
        except Exception as e:
            return False

    def run(self):
        script_directory = os.path.dirname(os.path.abspath(__file__))

        for host in self.hosts:
            result_filename = os.path.join(script_directory, f"knock_results_{host.replace('.', '_')}.txt")
            with open(result_filename, 'w') as result_file:
                print(f"\nKnocking on {host}...")
                for port in tqdm(range(1, 65536), desc=f"Progress for {host}"):
                    success_tcp = self.knock(host, port, False)
                    success_udp = self.knock(host, port, True)
                    
                    result_file.write(f"{host}:{port} - TCP: {'Success' if success_tcp else 'Failed'}, UDP: {'Success' if success_udp else 'Failed'}\n")

                    if not success_tcp and self.verbose:
                        print(f"Failed to knock on {host}:{port} (TCP)")

                    if not success_udp and self.verbose:
                        print(f"Failed to knock on {host}:{port} (UDP)")

                    if self.delay:
                        time.sleep(self.delay)

if __name__ == '__main__':
    knocker = Knocker(sys.argv[1:])
    knocker.run()
