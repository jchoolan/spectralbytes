# SpectralBytes S03 â€” Nonce Once

## Challenge
Cryptography / Programming â€” 200 points.

S03 demonstrates AES-CTR keystream reuse. Two telemetry records use the same
key and initial counter. The participant recovers the second plaintext with
XOR and extracts the flag.

## Player access

SSH:
- Host: localhost (development)
- Port: 2223
- Username: crypto
- Password: SpectralS03Lab!

In the final CTF deployment, replace `localhost` with the approved challenge
host and publish only the assigned SSH port. The container SSH daemon listens on 2223.

## Player files

- `data/ciphertexts.json`
- `scripts/supporting_info.txt`
- `scripts/solve_hint.txt`
- `scripts/checker.py`

The AES key is not present in the player container.

## Intended player path

1. SSH to S03.
2. Inspect both ciphertext records.
3. Confirm the nonce is identical.
4. Read the supporting information for the known plaintext.
5. Recover the reused keystream:
   `keystream = ciphertext_A XOR known_plaintext_A`
6. Recover plaintext B:
   `plaintext_B = ciphertext_B XOR keystream`
7. Extract the `SPECTRAL{...}` flag.
8. Optionally validate the recovered plaintext prefix with `checker.py`.
9. Submit the exact flag in CTFd.

## Facilitator-only files

`facilitator/generate.py` and `facilitator/solve_s03.py` must never be copied
into the player image or player release ZIP.

## Build / run

```powershell
docker compose build
docker compose up -d
docker compose ps
```

Expected state: `healthy`.

## Reset

```powershell
docker compose down
docker compose up -d --build
docker compose ps
```

## Stop

```powershell
docker compose down
```

## Security notes

- Dedicated non-root `crypto` user.
- Root SSH login disabled.
- TCP/agent/X11/tunnel forwarding disabled.
- No Docker socket or host volume is mounted.
- Challenge network is Docker `internal: true`, so container-initiated
  Internet egress is denied.
- CPU, memory, PID and log limits are configured.
- Root filesystem is read-only; `/run` and `/tmp` are tmpfs.
- All Linux capabilities are dropped.
- `no-new-privileges` is enabled.
