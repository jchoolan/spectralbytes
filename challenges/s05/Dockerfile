
FROM python:3.12-slim

WORKDIR /app

RUN groupadd --system ctf && \
    useradd --system --gid ctf --home-dir /app ctf

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app/main.py /app/main.py
COPY app/theme.py /app/theme.py

RUN chown -R ctf:ctf /app

USER ctf

ENV PYTHONUNBUFFERED=1

EXPOSE 5000

CMD ["python", "main.py"]
