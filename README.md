# SpectralBytes — Operation Ghost Packet

A six-stage cybersecurity Capture The Flag (CTF) environment built using Docker, Docker Compose, and CTFd.

## Project Overview

Operation Ghost Packet is a hands-on cybersecurity training environment designed to demonstrate security vulnerabilities, investigation techniques, and exploitation concepts.

The platform consists of six challenge stages deployed in isolated Docker containers. CTFd provides the web interface for challenge descriptions, hints, flag submissions, and scoring.

## Technologies Used

- Docker and Docker Compose
- CTFd
- PostgreSQL
- Redis
- Linux containers
- SSH
- Python
- Wireshark and PCAP analysis

## Challenge Stages

| Stage | Topic | Access |
|---|---|---|
| S01 | Initial investigation | SSH — Port 2231 |
| S02 | Steganography and evidence investigation | SSH — Port 2232 |
| S03 | Cryptography — AES-CTR nonce reuse | SSH — Port 2233 |
| S04 | Network forensics — PCAP analysis | SSH — Port 2234 |
| S05 | Web application security | HTTP — Port 8055 |
| S06 | Linux privilege escalation | SSH — Port 2236 |

The stages are designed to form a connected challenge sequence.

## Requirements

Before running the project, install:

1. Git
2. Docker Desktop with Docker Compose
3. WSL 2, if required by Docker Desktop on Windows

## Installation

Clone the repository:

```powershell
git clone https://github.com/jchoolan/spectralbytes.git
cd spectralbytes
```

Ensure Docker Desktop is running.

Check the Docker installation:

```powershell
docker --version
docker compose version
```

Configure any required environment variables before starting the containers.

**Important:** The CTFd service uses a custom Docker image, `spectralbytes-ctfd:postgres`. This image must be available locally or have a working build configuration before starting the full environment.

Build and start the containers:

```powershell
docker compose up -d --build
```

Check their status:

```powershell
docker compose ps
```

## Accessing the Platform

Open CTFd in your browser:

**http://localhost:8090**

The web application for Stage 05 is available at:

**http://localhost:8055**

SSH challenge services use ports 2231, 2232, 2233, 2234, and 2236.

Use the credentials provided by the challenge instructions.

## Restoring CTFd

The Git repository contains the application source and Docker configuration. It does not automatically include the configured CTFd PostgreSQL database.

To reproduce the original challenge descriptions, flags, hints, and other CTFd settings, an administrator must restore a compatible CTFd backup.

CTFd backup files should be transferred privately and must not be committed to this repository.

## Docker Commands

Start:

```powershell
docker compose up -d
```

Stop:

```powershell
docker compose down
```

View container status:

```powershell
docker compose ps
```

View logs:

```powershell
docker compose logs --tail=50
```

Rebuild:

```powershell
docker compose up -d --build
```

Avoid running `docker compose down -v` unless you intentionally want to remove persistent volumes, including database data.

## Project Structure

```text
spectralbytes-ctf/
├── challenges/
│   ├── s01/
│   ├── s02/
│   ├── s03/
│   ├── s04/
│   ├── s05/
│   └── s06/
├── compose.yaml
├── .gitignore
└── README.md
```

## Security Notice

This repository is intended for authorized educational use.

The challenge source code may contain embedded flags, passwords, and other solution-related information. Keep the repository private while the challenges are in use.

Do not commit administrator secrets, production credentials, database exports, or player information.

## Team

Developed by the SpectralBytes project team for cybersecurity education and practical security assessment.
