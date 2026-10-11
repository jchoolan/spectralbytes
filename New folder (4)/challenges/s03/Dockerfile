FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        openssh-server \
        python3 \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash crypto

RUN mkdir -p /home/crypto/data /home/crypto/scripts /run/sshd

COPY challenge/data/ciphertexts.json /home/crypto/data/ciphertexts.json
COPY challenge/scripts/checker.py /home/crypto/scripts/checker.py
COPY challenge/scripts/solve_hint.txt /home/crypto/scripts/solve_hint.txt
COPY challenge/scripts/supporting_info.txt /home/crypto/scripts/supporting_info.txt

RUN chown -R root:root /home/crypto/data /home/crypto/scripts && \
    chmod 755 /home/crypto/data /home/crypto/scripts && \
    chmod 644 /home/crypto/data/ciphertexts.json \
              /home/crypto/scripts/*.txt \
              /home/crypto/scripts/checker.py

RUN echo 'crypto:SPECTRAL{hidden_in_plain_sight}' | chpasswd && \
    printf '%s\n' \
      'PermitRootLogin no' \
      'PasswordAuthentication yes' \
      'KbdInteractiveAuthentication no' \
      'UsePAM no' \
      'AllowUsers crypto' \
      'X11Forwarding no' \
      'AllowTcpForwarding no' \
      'AllowAgentForwarding no' \
      'PermitTunnel no' \
      'GatewayPorts no' \
      'PermitUserEnvironment no' \
      >> /etc/ssh/sshd_config

RUN ssh-keygen -A

EXPOSE 22

HEALTHCHECK --interval=10s --timeout=3s --start-period=5s --retries=3 \
  CMD python3 -c "import socket; s=socket.socket(); s.settimeout(2); s.connect(('127.0.0.1',22)); s.close()"

CMD ["/usr/sbin/sshd", "-D", "-e"]

# SpectralBytes Stage 03 welcome banner
COPY welcome.txt /etc/spectralbytes-welcome.txt

RUN printf '\n# Display SpectralBytes welcome message for interactive SSH sessions\nif [[ $- == *i* ]]; then\n    cat /etc/spectralbytes-welcome.txt\nfi\n' >> /home/crypto/.bashrc
