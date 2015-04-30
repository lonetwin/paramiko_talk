"""
A stub SFTP server for demonstrating a sftp-dropbox bridge
"""

import os
import stat
from paramiko import ServerInterface, SFTPServerInterface, SFTPServer, \
                     SFTPAttributes, AUTH_SUCCESSFUL, OPEN_SUCCEEDED
from paramiko.common import o666

import logging
import urllib3
urllib3.disable_warnings()

from dropbox import client

log = logging.getLogger()

class StubServer (ServerInterface):
    def check_auth_password(self, username, password):
        # all are allowed
        return AUTH_SUCCESSFUL

    def check_channel_request(self, kind, chanid):
        return OPEN_SUCCEEDED


class StubSFTPServer (SFTPServerInterface):
    ROOT = ''
    TOKEN_FILE = "token_store.txt"

    def __init__(self, *args, **kwargs):
        super(StubSFTPServer, self).__init__(*args, **kwargs)

        serialized_token = open(self.TOKEN_FILE).read()
        access_token = serialized_token[len('oauth2:'):]
        self.api_client = client.DropboxClient(access_token)
        self.current_path = self.ROOT


    def list_folder(self, path):
        """list files in current remote directory"""

        try:
            resp = self.api_client.metadata(self.current_path)
            log.info('[+] Got response %s..', str(resp)[:40])
            if 'contents' in resp:
                out = []
                for f in resp['contents']:
                    attr = SFTPAttributes()
                    attr.filename = os.path.basename(f['path'])
                    if f['is_dir']:
                        attr.st_mode = (stat.S_IFDIR | stat.S_IRWXU)
                    else:
                        attr.st_mode = (stat.S_IFREG | stat.S_IRWXU)
                    attr.st_size = f['bytes']
                    out.append(attr)
        except OSError as e:
            return SFTPServer.convert_errno(e.errno)

        return out
