#!/usr/bin/env python3
# Usage:
#   python ng_zarr_demo.py /path/to/volume.zarr [--port 5000] [--host 127.0.0.1] [--name mylayer]
#
# This starts a CORS-enabled local HTTP server for the directory that contains your .zarr,
# then opens a Neuroglancer Demo URL pointing at:  zarr://http://HOST:PORT/<basename>.zarr/
#
# Requirements: Python 3.8+, no extra pip packages needed.

import argparse, json, os, threading, webbrowser
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from urllib.parse import quote

NEUROGLANCER_DEMO = "https://neuroglancer-demo.appspot.com/#!"

class CORSRequestHandler(SimpleHTTPRequestHandler):
    # Serve files from a specific directory (passed via constructor)
    def __init__(self, *args, directory=None, **kwargs):
        super().__init__(*args, directory=directory, **kwargs)
    def end_headers(self):
        # Allow cross-origin requests from any origin (needed for demo site)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Range, Content-Type")
        self.send_header("Access-Control-Expose-Headers", "Content-Length, Content-Range, Accept-Ranges")
        self.send_header("Accept-Ranges", "bytes")
        super().end_headers()
    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Range, Content-Type")
        self.end_headers()

def start_server(root_dir, host, port):
    handler = lambda *a, **kw: CORSRequestHandler(*a, directory=root_dir, **kw)
    httpd = ThreadingHTTPServer((host, port), handler)
    t = threading.Thread(target=httpd.serve_forever, daemon=True)
    t.start()
    return httpd

def build_state(file_http_url, layer_name,file_type='zarr'):
    # Minimal/default state for a single image layer from a Zarr.
    # Neuroglancer infers shape/chunks from Zarr metadata; voxel size defaults to 1x1x1.
    return {
        "layers": [
            {
                "type": "image",
                "source": f"{file_type}://{file_http_url}",
                "name": layer_name
            }
        ]
        # You can add "crossSectionScale", "position", "layout", etc., if desired.
    }

def main():
    ap = argparse.ArgumentParser(description="Open a local Zarr store in Neuroglancer Demo.")
    ap.add_argument("file_path", help="Path to your .zarr directory")
    ap.add_argument("--host", default="127.0.0.1", help="Host to bind local HTTP server (default: 127.0.0.1)")
    ap.add_argument("--port", type=int, default=5000, help="Port for local HTTP server (default: 5000)")
    ap.add_argument("--name", default=None, help="Layer name (default: basename of .zarr)")
    ap.add_argument("--file_type", default=None, help="file type (default: zarr)")
    ap.add_argument("--no-open", action="store_true", help="Do not auto-open the browser")
    args = ap.parse_args()

    file_path = os.path.abspath(args.file_path.rstrip("/"))
    if not os.path.isdir(file_path) or not file_path.endswith(".zarr"):
        raise SystemExit("Please provide a path to a Zarr directory ending in .zarr")

    root_dir = os.path.dirname(file_path)
    base = os.path.basename(file_path)  # e.g., volume.zarr
    layer_name = args.name or base

    # 1) Start a CORS-enabled server for the parent directory
    httpd = start_server(root_dir, args.host, args.port)

    # 2) Build Neuroglancer state pointing to the served Zarr
    file_http_url = f"http://{args.host}:{args.port}/{base}/"
    state = build_state(file_http_url, layer_name,file_type='zarr')

    # 3) Encode the state and construct the demo URL
    state_json = json.dumps(state, separators=(",", ":"))
    encoded = quote(state_json, safe="")
    url = NEUROGLANCER_DEMO + encoded

    print("\nNeuroglancer Demo URL (encoded):")
    print(url, "\n")

    # 4) Open in the default browser
    if not args.no_open:
        webbrowser.open(url)

    # Keep the server alive until Ctrl+C
    try:
        threading.Event().wait()  # sleep forever in main thread
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()