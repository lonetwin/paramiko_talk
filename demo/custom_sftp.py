#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import socket
import logging

import paramiko

from stub_sftp import StubServer, StubSFTPServer

HOST, PORT = 'localhost', 8022
KEYFILE = './test_rsa.key'

def main():
    paramiko.common.logging.basicConfig(level=logging.INFO)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)

    conn, addr = server_socket.accept()

    host_key = paramiko.RSAKey.from_private_key_file(KEYFILE)
    transport = paramiko.Transport(conn)
    transport.add_server_key(host_key)
    transport.set_subsystem_handler(
        'sftp', paramiko.SFTPServer, StubSFTPServer)

    server = StubServer()
    transport.start_server(server=server)

    channel = transport.accept()
    while transport.is_active():
        time.sleep(1)

if __name__ == '__main__':
    main()
