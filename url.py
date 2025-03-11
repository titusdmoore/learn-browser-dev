import socket
import ssl
import os

class URL:
    def __init__(self, url, headers):
        self.headers = headers
        self.scheme, url = url.split("://", 1)

        if "http" in self.scheme:
            # Default to SSL, else fallback to HTTP
            self.port = 443
            if self.scheme == "http":
                self.port = 80

            # Ensure that the url has a path to prevent undefined behavior in split or headers
            if "/" not in url:
                url = url + "/"

            self.host, url = url.split("/", 1)
            self.path = "/" + url

            # Adds support for custom ports specified in URL
            if ":" in self.host:
                self.host, port = self.host.split(":", 1)
                self.port = int(port)
        elif "file" in self.scheme:
            self.path = url

    def handle_http_request(self):
        s = socket.socket(
            family=socket.AF_INET,
            type=socket.SOCK_STREAM,
            proto=socket.IPPROTO_TCP,
        )
        s.connect((self.host, self.port))

        if self.scheme == "https":
            ctx = ssl.create_default_context()
            s = ctx.wrap_socket(s, server_hostname=self.host)

        request = "GET {} HTTP/1.1\r\n".format(self.path)
        request += "HOST: {}".format(self.host)
        for key, value in self.headers.items():
            request += "\n{}: {}".format(key, value)
        request += "\r\n"
        request += "\r\n"
        s.send(request.encode("utf8"))

        # Start Handle Response Section
        response = s.makefile("r", encoding="utf8", newline="\r\n")

        statusline = response.readline()
        version, status, explanation = statusline.split(" ", 2)

        # Parse Headers
        response_headers = {}
        while True:
            line = response.readline()

            # Reached End of Headers block
            if line == "\r\n": break
            header, value = line.split(":", 1)
            response_headers[header.casefold()] = value.strip()

        assert "transfer-encoding" not in response_headers
        assert "content-encoding" not in response_headers

        # Get body of response
        content = response.read()
        s.close()
        # End Handle Response Section

        return content

    def handle_file_request(self):
        if os.path.isfile(self.path):
            f = open(self.path, "r")
            content = f.read()
            f.close()
            return content
        
        return "File not found at path: {}".format(self.path)

    def handle_data_request(self):
        print("data request")

    def request(self):
        match self.scheme:
            case "file":
                return self.handle_file_request()
            case "data":
                return self.handle_data_request()
            case _:
                return self.handle_http_request()

