import ssl
import sys
import threading
import websocket

url = "wss://nb-1be3782a8afd3ad5.cohort.htb/terminal/ws"

# Create WebSocket connection with SSL disabled
ws = websocket.create_connection(
    url,
    sslopt={"cert_reqs": ssl.CERT_NONE}
)

def receive():
    """Continuously read and print responses from the server."""
    while True:
        try:
            data = ws.recv()
            if isinstance(data, bytes):
                data = data.decode("utf-8", errors="replace")
            # Print without adding extra newline (like real terminal)
            sys.stdout.write(data)
            sys.stdout.flush()
        except Exception as e:
            print(f"\n[!] Connection closed: {e}")
            break

# Start receiver thread
thread = threading.Thread(target=receive, daemon=True)
thread.start()

# Main loop: read user input and send with '\n'
try:
    for line in sys.stdin:
        # Strip trailing \r or \n, then append exactly one '\n'
        command = line.rstrip("\r\n") + "\n"
        ws.send(command)
except KeyboardInterrupt:
    print("\n[!] Exiting...")
finally:
    try:
        ws.close()
    except:
        pass
