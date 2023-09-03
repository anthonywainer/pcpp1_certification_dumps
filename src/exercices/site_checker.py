import sys
import socket

if len(sys.argv) not in [2, 3]:
    print("Improper number of arguments: at least one is required" +
          "and not more than two are allowed:")
    print("- http server's address (required)")
    print("- port number (defaults to 80 if not specified)")
    exit(1)

addr = sys.argv[1]
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if len(sys.argv) == 3:
    try:
        port = int(sys.argv[2])
        if not 1 <= port <= 65535:
            raise ValueError
    except ValueError:
        print("Port number is invalid - exiting.")
        exit(2)
else:
    port = 80

try:
    sock.connect((addr, port))
except socket.timeout:
    print("The server" + addr + "seems to be dead - sorry.")
    exit(3)
except socket.gaierror:
    print("Server address" + addr + "is invalid or malformed - sorry.")
    exit(4)

request = b"HEAD / HTTP/1.0\r\nHost: " + \
          bytes(addr, "utf8") + \
          b"\r\nConnection:close\r\n\r\n"

sock.send(request)
answer = sock.recv(100).decode("utf8")
sock.shutdown(socket.SHUT_RDWR)
sock.close()
print(answer[:answer.find('\r')])
