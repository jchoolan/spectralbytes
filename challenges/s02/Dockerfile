FROM spectralbytes-ctf-stage02:latest

USER root

RUN id investigator >/dev/null 2>&1 || useradd -m -s /bin/bash investigator

RUN echo 'investigator:GhostPacket2026!' | chpasswd && \
    mkdir -p /run/sshd /home/investigator/evidence && \
    ssh-keygen -A

COPY evidence/ /home/investigator/evidence/
COPY motd /etc/motd

RUN chown -R root:root /home/investigator/evidence && \
    chmod -R a+rX /home/investigator/evidence && \
    chmod 755 /home/investigator && \
    printf '\nPasswordAuthentication yes\nPermitRootLogin no\n' >> /etc/ssh/sshd_config

EXPOSE 22

CMD ["/usr/sbin/sshd", "-D", "-e"]
