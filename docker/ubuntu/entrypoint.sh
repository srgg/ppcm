#!/bin/bash

# generate host keys if not present
#ssh-keygen -A

systemctl enable ssh
# do not detach (-D), log to stderr (-e), passthrough other arguments
exec /usr/sbin/sshd -D -e "$@"
