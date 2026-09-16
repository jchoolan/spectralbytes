# SpectralBytes – Operation Ghost Packet

IE3132 CTF Play Box (SSH-style challenges)

## Current Status
- S01 (First Signal) – working SSH challenge box

## How to run S01
```bash
docker compose up -d --build s01
ssh -p 2221 spectral01@127.0.0.1
# password: GhostSignal!01
