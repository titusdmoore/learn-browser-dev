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

def valid_entity(test_entity):
    valid_entities = [
        ("&gt;", ">"),
        ("&lt;", "<")
    ]

    for entity_tup in valid_entities: 
        if test_entity == entity_tup[0]:
            return entity_tup[1]
    
    return False

def show(body, raw):
    disable_write = False
    out = ""

    slow = 0
    for i in range(len(body)):
        if body[i] in "<>&;" and not raw:
            if body[i] == "<" or body[i] == "&":
                slow = i
                disable_write = True
                continue
            
            # This has a bug if an entity contains a close tag
            if body[i] == ";":
                entity = valid_entity(body[slow:i+1])
                if entity:
                    out += entity
                else:
                    out += body[slow:i+1]

            disable_write = False
            continue
            
        if disable_write: continue

        out += body[i]

    print(out)

def load (url):
    body = url.request()

    if "http" in url.scheme:
        show(body, url.raw_source)
    elif "file" in url.scheme:
        print(body)
    elif "data" in url.scheme:
        show(body, url.mime_type != "text/html")

def main():
    headers = parse_headers()
    load(URL(sys.argv[1], headers))


if __name__ == "__main__":
    main()
