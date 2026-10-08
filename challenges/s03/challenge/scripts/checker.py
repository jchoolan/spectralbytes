import sys

EXPECTED_PREFIX = (
    b"ROUTE: S05-PORTAL / "
    b"internal-incident-portal / "
)

MAX_INPUT_BYTES = 70


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 checker.py <recovered_plaintext_hex>")
        sys.exit(1)

    candidate_hex = sys.argv[1]

    try:
        recovered = bytes.fromhex(candidate_hex)
    except ValueError:
        print("REJECTED: malformed hex input")
        sys.exit(1)

    if len(recovered) > MAX_INPUT_BYTES:
        print("REJECTED: input exceeds maximum allowed length")
        sys.exit(1)

    if not recovered.startswith(EXPECTED_PREFIX):
        print("REJECTED: recovered plaintext prefix is incorrect")
        sys.exit(1)

    print("ACCEPTED: recovered plaintext prefix is valid")
    print("Next step: inspect the recovered plaintext for the S03 flag.")


if __name__ == "__main__":
    main()
