#!/usr/bin/env python3
"""Combined file server + save endpoint for skill-hub-site."""
import json, subprocess, os, mimetypes
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

ROOT = os.path.dirname(os.path.abspath(__file__))
SKILLS = os.path.join(ROOT, 'skills.json')

def git(*args):
    return subprocess.run(['git'] + list(args), cwd=ROOT, capture_output=True, text=True)

class Handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self._cors()

    def do_GET(self):
        # Serve static files
        path = urlparse(self.path).path.lstrip('/') or 'index.html'
        filepath = os.path.join(ROOT, os.path.normpath(path))
        
        if os.path.commonpath([ROOT, filepath]) != ROOT:
            self.send_error(403); return
        
        if not os.path.isfile(filepath):
            # SPA fallback
            filepath = os.path.join(ROOT, 'index.html')
        
        ct = mimetypes.guess_type(filepath)[0] or 'application/octet-stream'
        with open(filepath, 'rb') as f:
            content = f.read()
        
        self.send_response(200)
        self.send_header('Content-Type', ct)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-cache')
        self.end_headers()
        self.wfile.write(content)

    def do_POST(self):
        if self.path not in ('/save', '/'):
            self.send_error(404); return
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length).decode('utf-8')
        
        try:
            data = json.loads(body)
            skills = data.get('skills', [])
            token = data.get('token', '')
            
            if not token:
                raise ValueError('Missing GitHub token')
            
            # Write skills.json
            payload = {'skills': skills, 'updatedAt': data.get('updatedAt', '')}
            with open(SKILLS, 'w', encoding='utf-8') as f:
                json.dump(payload, f, ensure_ascii=False, indent=2)
            
            remote = f'https://oauth2:{token}@github.com/tbj88/skill-hub-site.git'
            
            # Pull latest
            git('pull', '--rebase', remote, 'main')
            
            # Add & commit
            git('add', 'skills.json')
            r = git('commit', '-m', f'save: {len(skills)} skills')
            
            if 'nothing to commit' in (r.stdout + r.stderr):
                self._json({'ok': True, 'msg': 'no changes'}); return
            
            # Push with rebase fallback
            r = git('push', remote, 'main')
            if r.returncode != 0:
                git('pull', '--rebase', remote, 'main')
                r2 = git('push', remote, 'main')
                if r2.returncode != 0:
                    self._json({'ok': False, 'msg': r2.stderr[:200]}, 500); return
            
            self._json({'ok': True, 'msg': f'Saved {len(skills)} skills'})
            
        except Exception as e:
            self._json({'ok': False, 'msg': str(e)}, 500)

    def _json(self, data, code=200):
        self.send_response(code)
        self._cors()
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))

    def _cors(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def log_message(self, format, *args):
        pass  # quiet

if __name__ == '__main__':
    port = 8765
    print(f'Skill Hub server: http://localhost:{port}')
    HTTPServer(('127.0.0.1', port), Handler).serve_forever()
