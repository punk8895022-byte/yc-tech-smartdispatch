"""Real Chromium DOM/layout smoke using local repository HTML and CSS only.
No production navigation, third-party requests, authentication, or real user data.
Does NOT substitute for human visual, keyboard, or VoiceOver approval.
"""
import base64
import json
import os
from pathlib import Path
import shutil
import socket
import struct
import subprocess
import tempfile
import time
from urllib.parse import urlsplit
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]
PAGES = ("index.html", "xy-hd-001.html", "cloudlink.html")
SIZES = ((390, 844, "mobile"), (1280, 800, "desktop"))

def recv(sock, count):
    data = b""
    while len(data) < count:
        part = sock.recv(count - len(data))
        if not part:
            raise ConnectionError("CDP connection closed")
        data += part
    return data

class DevTools:
    def __init__(self, url):
        parts = urlsplit(url)
        self.s = socket.create_connection((parts.hostname, parts.port), timeout=15)
        self.s.settimeout(15)
        key = base64.b64encode(os.urandom(16)).decode()
        headers = (f"GET {parts.path} HTTP/1.1\r\nHost: {parts.hostname}:{parts.port}\r\n"
                   "Upgrade: websocket\r\nConnection: Upgrade\r\n"
                   f"Sec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n"
                   "Origin: http://127.0.0.1\r\n\r\n")
        self.s.sendall(headers.encode())
        buf = b""
        while b"\r\n\r\n" not in buf:
            buf += self.s.recv(4096)
        if b" 101 " not in buf.split(b"\r\n", 1)[0]:
            raise RuntimeError("WebSocket upgrade failed")
        self.buf = buf.split(b"\r\n\r\n", 1)[1]
        self.n = 0

    def read(self, n):
        saved, self.buf = self.buf[:n], self.buf[n:]
        return saved + recv(self.s, n - len(saved))

    def frame(self):
        op, size = self.read(2)
        length = size & 127
        if length == 126:
            length = struct.unpack("!H", self.read(2))[0]
        elif length == 127:
            length = struct.unpack("!Q", self.read(8))[0]
        mask = self.read(4) if size & 128 else None
        payload = self.read(length)
        if mask:
            payload = bytes(b ^ mask[i % 4] for i,b in enumerate(payload))
        if op & 15 != 1:
            return None
        return json.loads(payload.decode())

    def call(self, method, params=None):
        self.n += 1
        ident = self.n
        payload = json.dumps({"id":ident,"method":method,"params":params or {}}).encode()
        mask = os.urandom(4)
        size = len(payload)
        head = bytes([0x81, 0x80 | size]) if size < 126 else (
            bytes([0x81, 0xfe]) + struct.pack("!H",size) if size < 65536
            else bytes([0x81, 0xff]) + struct.pack("!Q",size))
        self.s.sendall(head + mask + bytes(b ^ mask[i % 4] for i,b in enumerate(payload)))
        while True:
            response = self.frame()
            if response is None or response.get("id") != ident:
                continue
            if "error" in response:
                raise RuntimeError(f"{method}: {response['error']}")
            return response.get("result", {})

def main():
    chrome = next((shutil.which(n) for n in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser") if shutil.which(n)), None)
    if not chrome:
        raise RuntimeError("Chromium unavailable: browser test must not silently pass")
    css = (ROOT / "assets/styles.css").read_text(encoding="utf-8")
    for name in PAGES:
        assert (ROOT / name).is_file()
    with tempfile.TemporaryDirectory(prefix="xy-showcase-chrome-", ignore_cleanup_errors=True) as user_dir:
        args = [chrome,"--headless=new","--no-sandbox","--disable-dev-shm-usage",
                "--no-first-run","--disable-gpu","--remote-allow-origins=*",
                "--remote-debugging-port=0",f"--user-data-dir={user_dir}","about:blank"]
        chrome_process = subprocess.Popen(args,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        try:
            active = Path(user_dir) / "DevToolsActivePort"
            for _ in range(100):
                if active.exists():
                    break
                if chrome_process.poll() is not None:
                    raise RuntimeError("Chrome exited before DevTools startup")
                time.sleep(.1)
            if not active.exists():
                raise TimeoutError("No Chrome DevTools port")
            port = int(active.read_text().splitlines()[0])
            tabs = json.load(urlopen(f"http://127.0.0.1:{port}/json/list",timeout=10))
            ws = next(x["webSocketDebuggerUrl"] for x in tabs if x.get("type")=="page")
            cdp = DevTools(ws)
            try:
                cdp.call("Page.enable")
                cdp.call("Runtime.enable")
                shots = ROOT / "browser-screenshots"
                shots.mkdir(exist_ok=True)
                passed = 0
                for width,height,label in SIZES:
                    cdp.call("Emulation.setDeviceMetricsOverride",{"width":width,"height":height,
                             "deviceScaleFactor":1,"mobile":label=="mobile"})
                    for name in PAGES:
                        source = (ROOT / name).read_text(encoding="utf-8")
                        link = '<link rel="stylesheet" href="./assets/styles.css">'
                        if link not in source:
                            raise AssertionError(f"Missing stylesheet link in {name}")
                        document = source.replace(link,"<style>"+css+"</style>")
                        cdp.call("Page.navigate",{"url":"about:blank"})
                        cdp.call("Runtime.evaluate",{"expression":"document.open();document.write("+
                                 json.dumps(document)+");document.close();"})
                        result = cdp.call("Runtime.evaluate",{"returnByValue":True,"expression":"""(() => {
                           const grid=document.querySelector('.grid2');
                           return {
                              ready:document.readyState, width:innerWidth,
                              scroll:document.documentElement.scrollWidth,
                              main:!!document.querySelector('main'),
                              cols:grid ? getComputedStyle(grid).gridTemplateColumns.split(' ').filter(Boolean).length:0,
                              css:document.styleSheets.length
                           };
                        })()"""})["result"].get("value")
                        if not result or result["ready"]!="complete" or result["width"]!=width or (
                            result["scroll"]>width+1 or not result["main"] or
                            result["cols"]!=(1 if label=="mobile" else 2) or result["css"]<1):
                            raise AssertionError(f"Browser viewport failed {name} {label}: {result}")
                        png = cdp.call("Page.captureScreenshot",{"format":"png",
                                         "captureBeyondViewport":False})["data"]
                        path = shots / f"{Path(name).stem}-{label}-{width}.png"
                        path.write_bytes(base64.b64decode(png))
                        passed += 1
                        print(f"BROWSER_PASS {name} {label} width={width} scroll={result['scroll']} columns={result['cols']}")
                assert passed==6
                print("CHROMIUM_VIEWPORT_PASS 6/6; not human visual or VoiceOver review")
            finally:
                cdp.s.close()
        finally:
            chrome_process.terminate()
            try:
                chrome_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                chrome_process.kill()
                chrome_process.wait()

if __name__=="__main__":
    main()
