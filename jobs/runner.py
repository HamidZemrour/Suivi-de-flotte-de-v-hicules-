"""Point de commande interne : Airflow déclenche Spark sans socket Docker."""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import subprocess, threading
lock=threading.Lock()
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200); self.end_headers(); self.wfile.write(b'ready')
    def do_POST(self):
        if self.path!='/run': self.send_error(404); return
        if not lock.acquire(blocking=False): self.send_error(409,'Already running'); return
        try:
            r=subprocess.run(['/opt/spark/bin/spark-submit','--master','local[2]','--driver-memory','1g','--packages','org.apache.hudi:hudi-spark3.5-bundle_2.12:0.15.0,org.apache.hadoop:hadoop-aws:3.3.4','/project/jobs/analytics.py'])
            self.send_response(200 if r.returncode==0 else 500); self.end_headers(); self.wfile.write(str(r.returncode).encode())
        finally: lock.release()
ThreadingHTTPServer(('0.0.0.0',8090),Handler).serve_forever()
