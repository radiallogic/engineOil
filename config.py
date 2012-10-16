#!/usr/bin/env python
# version 2.1

class config:
    def __init__(self):
        self.backupDir = "/mnt/usb"
        self.servers = {'svn.foo.local':['/usr/local/foo_Repos'], 'mail.foo.local':['/etc/','/vmail/mail/'] , 'nagios.foo.com':['/etc/']}
        self.databases = {'wiki.foo.local':{'user':'','pass':'','databases':'--all-databases'},
                            'blog.foo.local':{'user':'','pass':'','databases':'--all-databases'}}
