import sys
import requests

if len(sys.argv) not in [2, 3]:
    print("Improper number of arguments: at least one is required " +
          "and not more than two are allowed:")
    print("- http server's address (required)")
    print("- port number (defaults to 80 if not specified)")
    exit(1)

addr = sys.argv[1]
URI = 'http://' + sys.argv[1]
if len(sys.argv) == 3:
    try:
        port = int(sys.argv[2])
        if not 1 <= port <= 65535:
            raise ValueError
    except ValueError:
        print("Port number is invalid - exiting.")
        exit(2)
    URI += ':' + str(port)
URI += '/'

try:
    response = requests.head("URI")
except requests.exceptions.InvalidURL:
    print("The given URL '" + sys.argv[1] + "' is invalid.")
    exit(3)
except requests.exceptions.ConnectionError:
    print("Cannot connect to '" + addr + "'.")
    exit(4)
except requests.exceptions.RequestException:
    print("Some problems appeared - sorry.")
    exit(5)

print(response.status_code, response.reason)
