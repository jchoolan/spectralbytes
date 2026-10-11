# S03 Reset / Recovery

## Normal reset

```powershell
docker compose down
docker compose up -d --build
docker compose ps
```

Confirm the service is `healthy`, then test:

```powershell
ssh crypto@localhost -p 2223
```

## Full image rebuild

```powershell
docker compose down --remove-orphans
docker image rm spectralbytes-s03:release
docker compose build --no-cache
docker compose up -d
docker compose ps
```

## Incident procedure

1. Stop the S03 service:
   `docker compose down`
2. Preserve relevant Docker/container logs and timestamps.
3. Recreate from the pinned source/image.
4. Run the automated tests.
5. Verify SSH authentication and the intended player path.
6. Reopen the challenge only after health/isolation checks pass.
