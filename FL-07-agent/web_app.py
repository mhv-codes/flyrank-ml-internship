"""Local browser UI for the existing read-only FlyRank notes agent."""
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.error import URLError
from agent import run_agent

ROOT = Path(__file__).resolve().parent
PAGE = ROOT / 'web' / 'index.html'

class Handler(BaseHTTPRequestHandler):
    def respond(self, status, obj):
        data = json.dumps(obj).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type','application/json; charset=utf-8')
        self.send_header('Content-Length',str(len(data)))
        self.send_header('Cache-Control','no-store')
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path in ('/', '/index.html'):
            data=PAGE.read_bytes()
            self.send_response(200)
            self.send_header('Content-Type','text/html; charset=utf-8')
            self.send_header('Content-Length',str(len(data)))
            self.send_header('X-Content-Type-Options','nosniff')
            self.end_headers()
            self.wfile.write(data)
        elif self.path == '/api/status':
            self.respond(200, {'model':'qwen3:4b', 'notes':len(list((ROOT/'notes').glob('*.md'))), 'mode':'local'})
        else: self.respond(404, {'error':'Not found'})

    def do_POST(self):
        if self.path != '/api/ask':
            return self.respond(404,{'error':'Not found'})
        try:
            length=int(self.headers.get('Content-Length','0'))
            if length<=0 or length>8192:
                return self.respond(413,{'error':'Request too large or empty'})
            body=json.loads(self.rfile.read(length))
            question=body.get('question')
            if not isinstance(question,str) or not question.strip() or len(question)>1200:
                return self.respond(400,{'error':'Enter a question (maximum 1200 characters).'})
            answer,sources=run_agent(question.strip(), ROOT/'notes', 'qwen3:4b')
            self.respond(200,{'answer':answer,'sources':sorted(sources)})
        except (URLError,TimeoutError,ConnectionError) as e:
            self.respond(503,{'error':'Ollama is unavailable. Start Ollama and check that qwen3:4b is installed.'})
        except (ValueError,KeyError,json.JSONDecodeError) as e:
            self.respond(400,{'error':'Unable to process request. Check the model and try again.'})

if __name__=='__main__':
    print('FlyRank Study Agent: http://127.0.0.1:8765')
    print('Private local server. Press Ctrl+C to stop.')
    ThreadingHTTPServer(('127.0.0.1',8765),Handler).serve_forever()
