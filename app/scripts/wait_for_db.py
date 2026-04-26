from __future__ import annotations

import os
import socket
import sys
import time

import psycopg

DB_HOST = os.getenv("OPENMAP_DB_HOST", "db")
DB_PORT = int(os.getenv("OPENMAP_DB_PORT", "5432"))
DB_NAME = os.getenv("OPENMAP_DB_NAME", "openmap")
DB_USER = os.getenv("OPENMAP_DB_USER", "postgres")
DB_PASSWORD = os.getenv("OPENMAP_DB_PASSWORD", "postgres")
DNS_TIMEOUT_SECONDS = int(os.getenv("OPENMAP_DB_DNS_TIMEOUT", "60"))
CONNECTION_TIMEOUT_SECONDS = int(os.getenv("OPENMAP_DB_CONN_TIMEOUT", "60"))


def wait_for_dns() -> None:
    for attempt in range(1, DNS_TIMEOUT_SECONDS + 1):
        try:
            socket.gethostbyname(DB_HOST)
            return
        except Exception as exc:
            print(f"[wait-dns] host '{DB_HOST}' not resolvable ({exc}), retry {attempt}/{DNS_TIMEOUT_SECONDS}")
            time.sleep(1)

    sys.exit(f"db DNS resolution failed for host '{DB_HOST}' after {DNS_TIMEOUT_SECONDS}s")


def wait_for_connection() -> None:
    dsn = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    for attempt in range(1, CONNECTION_TIMEOUT_SECONDS + 1):
        try:
            with psycopg.connect(dsn, connect_timeout=2):
                return
        except Exception as exc:
            print(f"[wait-db] db not ready ({exc}), retry {attempt}/{CONNECTION_TIMEOUT_SECONDS}")
            time.sleep(1)

    sys.exit(f"db connection failed after {CONNECTION_TIMEOUT_SECONDS}s")


def main() -> None:
    wait_for_dns()
    wait_for_connection()
    print("[wait-db] database is reachable")


if __name__ == "__main__":
    main()
