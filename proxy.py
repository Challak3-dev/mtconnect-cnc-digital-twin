"""
Serves the twin page and forwards /agent/* to the MTConnect agent,
so the browser never makes a cross-origin request (no CORS problems).

Usage:
    python proxy.py                                  # agent = https://demo.metalogi.io
    python proxy.py --agent http://192.168.1.50:5000 --port 8000
Then open: http://localhost:8000/index.html?device=OKUMA
"""
import argparse
import os
import urllib.request
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

parser = argparse.ArgumentParser()
parser.add_argument("--agent", default="https://demo.metalogi.io", help="MTConnect agent base URL")
parser.add_argument("--port", type=int, default=8000)
args = parser.parse_args()
AGENT = args.agent.rstrip("/")


class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if not self.path.startswith("/agent/"):
            return super().do_GET()
        url = AGENT + self.path[len("/agent"):]
        try:
            with urllib.request.urlopen(url, timeout=10) as r:
                body = r.read()
                self.send_response(r.status)
                self.send_header("Content-Type", r.headers.get("Content-Type", "application/xml"))
        except urllib.error.HTTPError as e:
            body = e.read()
            self.send_response(e.code)
        except Exception as e:
            body = str(e).encode()
            self.send_response(502)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *a):
        pass  # keep the console quiet


os.chdir(os.path.dirname(os.path.abspath(__file__)))
print(f"Twin:  http://localhost:{args.port}/index.html")
print(f"Agent: {AGENT}  (proxied at /agent)")
ThreadingHTTPServer(("", args.port), Handler).serve_forever()
