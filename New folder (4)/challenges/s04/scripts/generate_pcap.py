
from pathlib import Path
from io import BytesIO
from zipfile import ZipFile, ZIP_DEFLATED
from scapy.all import IP, TCP, Raw, wrpcap

BASE = Path(__file__).resolve().parent.parent
EVIDENCE = BASE / "evidence"
EVIDENCE.mkdir(parents=True, exist_ok=True)

FLAG = "SPECTRAL{ghost_traffic_recovered}"

# Build the ZIP file that players must recover.
buffer = BytesIO()

with ZipFile(buffer, "w", ZIP_DEFLATED) as archive:
    archive.writestr(
        "incident_report.txt",
        "SPECTRALBYTES INCIDENT RESPONSE\n"
        "Case: Ghost Packet\n"
        "Recovered evidence confirms an unauthorized transfer.\n"
        f"Evidence flag: {FLAG}\n"
    )
    archive.writestr(
        "transfer_notes.txt",
        "Source: GATEWAY-7\n"
        "Archive: incident-transfer-archive.zip\n"
        "Next investigation: S05 internal incident portal\n"
    )

zip_data = buffer.getvalue()

client = "192.168.56.20"
server = "192.168.56.10"
client_port = 49152
server_port = 80

client_seq = 1000
server_seq = 5000

packets = []

def packet(src, dst, sport, dport, seq, ack, flags, payload=b""):
    p = IP(src=src, dst=dst) / TCP(
        sport=sport,
        dport=dport,
        seq=seq,
        ack=ack,
        flags=flags
    )
    if payload:
        p = p / Raw(load=payload)
    packets.append(p)

# TCP handshake
packet(client, server, client_port, server_port, client_seq, 0, "S")
packet(server, client, server_port, client_port, server_seq, client_seq + 1, "SA")
packet(client, server, client_port, server_port, client_seq + 1, server_seq + 1, "A")

request = (
    b"GET /incident-transfer-archive.zip HTTP/1.1\r\n"
    b"Host: gateway-7.internal\r\n"
    b"User-Agent: IncidentSync/1.0\r\n"
    b"Connection: close\r\n\r\n"
)

packet(
    client, server, client_port, server_port,
    client_seq + 1, server_seq + 1, "PA", request
)

client_next = client_seq + 1 + len(request)

packet(
    server, client, server_port, client_port,
    server_seq + 1, client_next, "A"
)

response = (
    b"HTTP/1.1 200 OK\r\n"
    b"Content-Type: application/zip\r\n"
    + f"Content-Length: {len(zip_data)}\r\n".encode()
    + b"Content-Disposition: attachment; filename=\"incident-transfer-archive.zip\"\r\n"
    + b"Connection: close\r\n\r\n"
    + zip_data
)

server_next = server_seq + 1

# Segment the HTTP response into TCP packets.
for offset in range(0, len(response), 1000):
    chunk = response[offset:offset + 1000]
    packet(
        server, client, server_port, client_port,
        server_next, client_next, "PA", chunk
    )
    server_next += len(chunk)

packet(
    client, server, client_port, server_port,
    client_next, server_next, "A"
)

packet(
    server, client, server_port, client_port,
    server_next, client_next, "FA"
)

packet(
    client, server, client_port, server_port,
    client_next, server_next + 1, "FA"
)

packet(
    server, client, server_port, client_port,
    server_next + 1, client_next + 1, "A"
)

output = EVIDENCE / "ghost_traffic.pcap"
wrpcap(str(output), packets)

print(f"PCAP created: {output}")
print(f"Packets: {len(packets)}")
print(f"Embedded ZIP size: {len(zip_data)} bytes")
