
FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    openssh-server cron sudo procps && \
    rm -rf /var/lib/apt/lists/*

# Create the low-privilege player account
RUN useradd -m -g operator -s /bin/bash operator && \
    echo 'operator:SpectralS06Lab!' | chpasswd && \
    mkdir -p /run/sshd /opt/spectralbytes/archive

# Install the intentionally vulnerable maintenance script
COPY scripts/maintenance.sh /opt/spectralbytes/maintenance.sh

# The operator can modify a script executed by root
RUN chown operator:operator /opt/spectralbytes/maintenance.sh && \
    chmod 755 /opt/spectralbytes/maintenance.sh

# Create the root-only challenge flag
RUN mkdir -p /root/evidence && \
    printf '%s\n' 'SPECTRAL{root_trust_boundary_broken}' \
    > /root/evidence/flag.txt && \
    chmod 700 /root/evidence && \
    chmod 600 /root/evidence/flag.txt

# Root runs the maintenance script once per minute
RUN printf '%s\n' \
    '* * * * * root /bin/bash /opt/spectralbytes/maintenance.sh' \
    > /etc/cron.d/spectralbytes-maintenance && \
    chmod 644 /etc/cron.d/spectralbytes-maintenance

# Configure SSH
RUN printf '%s\n' \
    'PasswordAuthentication yes' \
    'PermitRootLogin no' \
    'AllowUsers operator' \
    > /etc/ssh/sshd_config.d/ctf.conf

# Player instructions
RUN printf '%s\n' \
    'Welcome to SpectralBytes S06 - Root of the Problem' \
    'Investigate the maintenance process and file permissions.' \
    'Your objective is to recover the protected evidence flag.' \
    > /etc/motd

EXPOSE 22

# Start cron and SSH inside the challenge container
CMD ["/bin/bash", "-c", "cron && exec /usr/sbin/sshd -D -e"]
