#!/bin/sh

set -eu

# Make sure runtime directory exists.
mkdir -p /run/sshd

# Make sure SSH host keys exist.
ssh-keygen -A >/dev/null 2>&1 || true

# Start SSH in the foreground.
exec /usr/sbin/sshd -D -e
