FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
        openssh-server tshark wireshark-common file unzip 7zip sudo openssl \
    && rm -rf /var/lib/apt/lists/* \
    && mkdir -p /var/run/sshd \
    && groupadd -f wireshark

RUN useradd -m -s /bin/bash forensics \
    && echo 'forensics:SPECTRAL{S03_nonce_REUSEDCTR}' | chpasswd \
    && usermod -aG wireshark forensics

RUN sed -i 's/^#\?PermitRootLogin.*/PermitRootLogin no/' /etc/ssh/sshd_config \
    && sed -i 's/^#\?PermitEmptyPasswords.*/PermitEmptyPasswords no/' /etc/ssh/sshd_config \
    && sed -i 's/^#\?X11Forwarding.*/X11Forwarding no/' /etc/ssh/sshd_config \
    && sed -i 's/^#\?AllowTcpForwarding.*/AllowTcpForwarding no/' /etc/ssh/sshd_config

COPY challenge/ /home/forensics/challenge/
RUN chown -R root:root /home/forensics/challenge \
    && chmod -R a+rX /home/forensics/challenge \
    && chmod 755 /home/forensics

# SpectralBytes Stage 04 ASCII welcome banner
COPY welcome.txt /etc/spectralbytes-welcome.txt

# Display the banner during interactive SSH sessions
RUN printf '\n# SpectralBytes S04 welcome banner\nif [[ $- == *i* ]]; then\n    cat /etc/spectralbytes-welcome.txt\nfi\n' >> /home/forensics/.bashrc

EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]
