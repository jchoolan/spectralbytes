import json
import subprocess
import sys
from pathlib import Path
import tempfile

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "challenge" / "data" / "ciphertexts.json"
CHECKER = ROOT / "challenge" / "scripts" / "checker.py"
SUPPORT = ROOT / "challenge" / "scripts" / "supporting_info.txt"
PLAYER = ROOT / "player_release"

EXPECTED_PREFIX = b"ROUTE: S05-PORTAL / internal-incident-portal / "
EXPECTED_PLAINTEXT = (
    EXPECTED_PREFIX + b"SPECTRAL{S03_nonce_REUSEDCTR}"
)


def load():
    data = json.loads(DATA.read_text(encoding="utf-8"))
    assert len(data["records"]) == 2
    return data["records"]


def recover(records):
    a, b = records
    c1 = bytes.fromhex(a["ciphertext"])
    c2 = bytes.fromhex(b["ciphertext"])
    known = (
        b"ROUTE: S04-PCAP / GATEWAY-7 / "
        b"incident-transfer-archive.zip / "
        b"XXXXXXXXXXXXXXXXXXX"
    )
    ks = bytes(c ^ p for c, p in zip(c1, known))
    return bytes(c ^ k for c, k in zip(c2, ks))


def test_structure():
    a, b = load()
    assert a["nonce"] == b["nonce"]
    assert len(bytes.fromhex(a["ciphertext"])) == 81
    assert len(bytes.fromhex(b["ciphertext"])) == 76
    assert SUPPORT.exists()


def test_reference_recovery():
    records = load()
    assert recover(records) == EXPECTED_PLAINTEXT


def test_unique_nonce_negative_fixture():
    records = load()
    a = dict(records[0])
    b = dict(records[1])
    b["nonce"] = "ffeeddccbbaa99887766554433221100"
    assert a["nonce"] != b["nonce"]

    c1 = bytes.fromhex(a["ciphertext"])
    c2 = bytes.fromhex(b["ciphertext"])
    known = (
        b"ROUTE: S04-PCAP / GATEWAY-7 / "
        b"incident-transfer-archive.zip / "
        b"XXXXXXXXXXXXXXXXXXX"
    )
    ks = bytes(c ^ p for c, p in zip(c1, known))
    recovered = bytes(c ^ k for c, k in zip(c2, ks))
    assert not recovered.startswith(EXPECTED_PREFIX)


def run_checker(value):
    return subprocess.run(
        [sys.executable, str(CHECKER), value],
        capture_output=True,
        text=True,
        check=False,
    )


def test_checker_malformed():
    r = run_checker("NOT_HEX")
    assert r.returncode != 0
    assert "REJECTED: malformed hex input" in r.stdout


def test_checker_overlong():
    # 77 bytes = 154 hex characters
    r = run_checker("00" * 77)
    assert r.returncode != 0
    assert "REJECTED: input exceeds maximum allowed length" in r.stdout

def test_checker_accepts_expected_prefix():
    r = run_checker(EXPECTED_PREFIX.hex())
    assert r.returncode == 0
    assert "ACCEPTED" in r.stdout


def test_player_release_contains_no_facilitator_solver():
    assert not (PLAYER / "generate.py").exists()
    assert not (PLAYER / "solve_s03.py").exists()
    assert not (PLAYER / "facilitator").exists()


if __name__ == "__main__":
    import traceback
    failures = 0
    for name in [
        "test_structure",
        "test_reference_recovery",
        "test_checker_malformed",
        "test_checker_overlong",
        "test_checker_accepts_expected_prefix",
        "test_player_release_contains_no_facilitator_solver",
    ]:
        try:
            globals()[name]()
            print(f"PASS {name}")
        except Exception:
            failures += 1
            print(f"FAIL {name}")
            traceback.print_exc()
    raise SystemExit(1 if failures else 0)
