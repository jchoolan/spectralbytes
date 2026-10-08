
FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    openssh-server python3 ca-certificates && \
    rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash forensics && \
    echo 'forensics:SpectralS04Lab!' | chpasswd && \
    mkdir -p /run/sshd /home/forensics/evidence && \
    chown -R root:root /home/forensics/evidence && \
    chmod 755 /home/forensics/evidence

COPY evidence/ghost_traffic.pcap /home/forensics/evidence/ghost_traffic.pcap

RUN chmod 644 /home/forensics/evidence/ghost_traffic.pcap && \
    printf '%s\n' \
    'Welcome to SpectralBytes S04 - Ghost Traffic' \
    'Investigate the capture in ~/evidence/ghost_traffic.pcap' \
    'Use Wireshark to recover the transferred archive.' \
    > /etc/motd && \
    printf '%s\n' \
    'PasswordAuthentication yes' \
    'PermitRootLogin no' \
    'AllowUsers forensics' \
    > /etc/ssh/sshd_config.d/ctf.conf

EXPOSE 22

CMD ["/usr/sbin/sshd", "-D", "-e"]
