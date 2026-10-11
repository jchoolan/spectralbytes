FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        openssh-server \
        steghide \
        libimage-exiftool-perl \
        file \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash investigator && \
    echo 'investigator:SPECTRAL{spectral_ghost_47}' | chpasswd && \
    mkdir -p /run/sshd /home/investigator/evidence && \
    ssh-keygen -A

COPY evidence/ /home/investigator/evidence/
COPY motd /etc/motd

RUN chown -R root:root /home/investigator/evidence && \
    chmod -R a+rX /home/investigator/evidence && \
    chmod 755 /home/investigator && \
    printf '\nPasswordAuthentication yes\nPermitRootLogin no\nAllowUsers investigator\n' \
        >> /etc/ssh/sshd_config

EXPOSE 22

CMD ["/usr/sbin/sshd", "-D", "-e"]