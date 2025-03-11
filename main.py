import sys
from url import URL

def parse_headers():
    headers = {
        "Connection": "close",
        "User-Agent": "TDX_Net/0.0",
    }

    # Protect indexing out of range
    if len(sys.argv) <= 1: return headers

    for arg in sys.argv[1:]:
        if ":" in arg:
            key, value = arg.split(":", 1)
            headers[key] = value

    return headers


def show(body):
    in_tag = False
    for c in body:
        if c == "<":
            in_tag = True
        elif c == ">":
            in_tag = False
        elif not in_tag:
            print(c, end="")

def load (url):
    body = url.request()

    if "http" in url.scheme:
        show(body)
    elif "file" in url.scheme:
        print(body)

def main():
    headers = parse_headers()
    load(URL(sys.argv[1], headers))


if __name__ == "__main__":
    main()
