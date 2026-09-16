FROM debian:bookworm-slim

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        openssh-server \
        ca-certificates \
        file \
        grep \
        findutils \
        coreutils \
        procps \
        iproute2 \
    && rm -rf /var/lib/apt/lists/*

# Create the challenge user.
RUN useradd \
    --create-home \
    --shell /bin/bash \
    --uid 1001 \
    spectral01

# Development password.
# Change this before any real/public deployment.
RUN echo 'spectral01:GhostSignal!01' | chpasswd

# SSH runtime directory.
RUN mkdir -p /run/sshd

# Challenge directories.
RUN mkdir -p \
    /home/spectral01/evidence/archive \
    /home/spectral01/notes

# Copy challenge material.
COPY files/README.txt /home/spectral01/README.txt
COPY files/evidence/ /home/spectral01/evidence/
COPY files/notes/ /home/spectral01/notes/

# Ownership.
RUN chown -R spectral01:spectral01 /home/spectral01

# Normal permissions.
RUN chmod 750 /home/spectral01 \
    && chmod 750 /home/spectral01/evidence \
    && chmod 750 /home/spectral01/evidence/archive \
    && chmod 750 /home/spectral01/notes \
    && chmod 640 /home/spectral01/README.txt \
    && chmod 640 /home/spectral01/evidence/* \
    && chmod 640 /home/spectral01/evidence/archive/* \
    && chmod 640 /home/spectral01/notes/*

# Install our SSH configuration.
COPY sshd_config /etc/ssh/sshd_config

# Generate host keys at image build time.
RUN ssh-keygen -A

EXPOSE 22

COPY entrypoint.sh /entrypoint.sh
RUN chmod 755 /entrypoint.sh

CMD ["/entrypoint.sh"]
