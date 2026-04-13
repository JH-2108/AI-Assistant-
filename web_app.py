import json
import base64
import uuid
import time
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse, parse_qs

from Assistant import (
    ASSISTANT_NAME,
    process_command,
    review_file_content,
    generate_cad_design,
    is_cad_model_query,
    format_cad_reply_short,
    normalize,
    attach_stl_preview,
    get_stl_preview_bytes,
)


ROOT = Path(__file__).resolve().parent
INDEX_FILE = ROOT / "index.html"
HOST = "127.0.0.1"
PORT = 8765
MAX_UPLOAD_CHARS = 50000  # For text-based uploads
MAX_UPLOAD_BYTES = 50 * 1024 * 1024  # 50MB for binary file uploads
TEMP_UPLOAD_DIR = ROOT / "temp_uploads"  # For storing temporary uploaded files

# Ensure temp directory exists
TEMP_UPLOAD_DIR.mkdir(exist_ok=True)


class JarvisHandler(BaseHTTPRequestHandler):
    def _send_json(self, payload, status=200):
        data = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _send_html(self, html, status=200):
        data = html.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path in ["/", "/index.html"]:
            self._send_html(INDEX_FILE.read_text(encoding="utf-8"))
            return

        if self.path == "/api/health":
            self._send_json({"ok": True, "assistant": ASSISTANT_NAME})
            return

        parsed = urlparse(self.path)
        if parsed.path == "/api/cad/stl":
            qs = parse_qs(parsed.query)
            pid = (qs.get("id") or [""])[0].strip()
            blob = get_stl_preview_bytes(pid) if pid else None
            if not blob:
                self.send_response(404)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(b'{"error":"STL preview not found or expired"}')
                return
            self.send_response(200)
            self.send_header("Content-Type", "model/stl")
            self.send_header("Content-Disposition", 'inline; filename="preview.stl"')
            self.send_header("Content-Length", str(len(blob)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(blob)
            return

        self._send_json({"error": "Not found"}, status=404)

    def do_POST(self):
        if self.path not in ["/api/command", "/api/review-file", "/api/create-cad"]:
            self._send_json({"error": "Not found"}, status=404)
            return

        content_length = int(self.headers.get("Content-Length", "0"))
        raw_body = self.rfile.read(content_length).decode("utf-8") if content_length else "{}"

        try:
            payload = json.loads(raw_body or "{}")
            command = str(payload.get("command", "")).strip()
        except json.JSONDecodeError:
            self._send_json({"error": "Invalid JSON"}, status=400)
            return

        if self.path == "/api/command":
            if not command:
                self._send_json({"error": "Command is required"}, status=400)
                return

            if is_cad_model_query(normalize(command)):
                design = attach_stl_preview(generate_cad_design(command))
                self._send_json(
                    {
                        "assistant": ASSISTANT_NAME,
                        "response": format_cad_reply_short(design),
                        "design": design,
                    }
                )
                return

            use_vision = bool(payload.get("use_vision", False))
            response = process_command(command, interactive=False, use_vision=use_vision)
            self._send_json({"assistant": ASSISTANT_NAME, "response": response})
            return

        if self.path == "/api/create-cad":
            request = str(payload.get("request", "")).strip() or command
            if not request:
                self._send_json({"error": "Design request is required"}, status=400)
                return

            design = attach_stl_preview(generate_cad_design(request))
            self._send_json(
                {
                    "assistant": ASSISTANT_NAME,
                    "response": format_cad_reply_short(design),
                    "design": design,
                }
            )
            return

        # File review endpoint - supports text content or base64-encoded binary files
        filename = str(payload.get("filename", "")).strip()
        content = payload.get("content", "")  # Can be string or base64
        file_data_b64 = payload.get("file_data", "")  # Base64-encoded file data
        user_request = str(payload.get("request", "")).strip()

        if not filename:
            self._send_json({"error": "Filename is required"}, status=400)
            return

        # Handle base64-encoded binary file data
        if not file_data_b64 and content:
            # Some upload paths may send binary base64 data in the content field.
            fallback_content = str(content).strip()
            if fallback_content and all(c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=\n\r' for c in fallback_content):
                try:
                    base64.b64decode(fallback_content, validate=True)
                    file_data_b64 = fallback_content
                    content = ""
                except Exception:
                    pass

        if file_data_b64:
            try:
                file_bytes = base64.b64decode(file_data_b64)
                if len(file_bytes) > MAX_UPLOAD_BYTES:
                    self._send_json(
                        {"error": f"File is too large. Keep uploads under {MAX_UPLOAD_BYTES / (1024*1024):.0f}MB."},
                        status=400,
                    )
                    return
                
                # Save to temporary file
                temp_filename = f"upload_{uuid.uuid4().hex}_{filename}"
                temp_path = TEMP_UPLOAD_DIR / temp_filename
                
                # Write file with explicit fsync for safety
                with open(temp_path, 'wb') as f:
                    f.write(file_bytes)
                    f.flush()
                    os.fsync(f.fileno())  # Force write to disk
                
                # Verify file was written with multiple checks
                time.sleep(0.1)  # Brief wait for filesystem sync
                
                if not temp_path.exists():
                    return self._send_json(
                        {"error": f"File upload failed: Temp file not found at {str(temp_path)}"},
                        status=400,
                    )
                
                file_size = temp_path.stat().st_size
                if file_size == 0:
                    return self._send_json(
                        {"error": "File upload failed: Uploaded file is empty (0 bytes)."},
                        status=400,
                    )
                
                if file_size != len(file_bytes):
                    return self._send_json(
                        {"error": f"File upload failed: Size mismatch (expected {len(file_bytes)}, got {file_size})."},
                        status=400,
                    )
                
                temp_file_str = str(temp_path)
                
                try:
                    # Analyze the file - temp file must exist during this call
                    response = review_file_content(filename, temp_file_str, user_request=user_request, is_file_path=True)
                finally:
                    # Clean up temp file AFTER analysis is complete
                    time.sleep(0.05)  # Give OS time to release file handle
                    
                    cleanup_retries = 3
                    for attempt in range(cleanup_retries):
                        try:
                            if Path(temp_file_str).exists():
                                Path(temp_file_str).unlink()
                            break
                        except Exception as e:
                            if attempt == cleanup_retries - 1:
                                pass  # Ignore final cleanup failure
                            else:
                                time.sleep(0.1)
                
                self._send_json({"assistant": ASSISTANT_NAME, "response": response, "filename": filename})
                return
            except Exception as e:
                self._send_json({"error": f"File upload error: {str(e)}"}, status=400)
                return

        # Handle direct text content (legacy support)
        content = str(content)
        if not content.strip():
            self._send_json({"error": f"File content is empty for {filename}. If this is a PDF, DOCX, image, or other binary file, try uploading again. Make sure the file is sent as binary base64 data."}, status=400)
            return

        if len(content) > MAX_UPLOAD_CHARS:
            self._send_json(
                {"error": f"File is too large. Keep text uploads under {MAX_UPLOAD_CHARS} characters."},
                status=400,
            )
            return

        response = review_file_content(filename, content, user_request=user_request)
        self._send_json({"assistant": ASSISTANT_NAME, "response": response, "filename": filename})

    def log_message(self, format, *args):
        return


def run():
    server = ThreadingHTTPServer((HOST, PORT), JarvisHandler)
    print(f"{ASSISTANT_NAME} web app running at http://{HOST}:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    run()
