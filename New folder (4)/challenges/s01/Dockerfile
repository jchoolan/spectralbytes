FROM alpine:3.20

RUN apk add --no-cache openssh-server && \
    adduser -D -s /bin/sh investigator && \
    mkdir -p /run/sshd /home/investigator/evidence && \
    ssh-keygen -A

COPY evidence/ /home/investigator/evidence/
COPY motd /etc/motd

RUN echo 'investigator:GhostPacket2026!' | chpasswd && \
    chown -R root:root /home/investigator/evidence && \
    chmod -R a+rX /home/investigator/evidence

EXPOSE 22

CMD ["/usr/sbin/sshd", "-D", "-e"]
