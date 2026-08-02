#!/usr/bin/env python3
"""Local save server for skill-hub-site. Handles git push atomically."""
import json, subprocess, sys, os
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs

REPO_DIR = os.path.dirname(os.path.abspath(__file__))
SKILLS_PATH = os.path.join(REPO_DIR, 'skills.json')

class Handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'OK')

    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length).decode('utf-8')
        
        try:
            data = json.loads(body)
            skills = data.get('skills', [])
            token = data.get('token', '')
            
            if not skills or not token:
                raise ValueError('Missing skills or token')
            
            # Write skills.json
            payload = {'skills': skills, 'updatedAt': data.get('updatedAt', '')}
            with open(SKILLS_PATH, 'w', encoding='utf-8') as f:
                json.dump(payload, f, ensure_ascii=False, indent=2)
            
            # Git operations
            def git(*args):
                return subprocess.run(['git'] + list(args), cwd=REPO_DIR, capture_output=True, text=True)
            
            # Pull latest
            git('pull', '--rebase', 
                f'https://oauth2:{token}@github.com/tbj88/skill-hub-site.git', 'main')
            
            # Add, commit, push
            git('add', 'skills.json')
            r = git('commit', '-m', f'update: {len(skills)} skills')
            
            # If nothing to commit, skip push
            if 'nothing to commit' in (r.stdout + r.stderr):
                self.send_json({'ok': True, 'msg': 'no changes'})
                return
            
            r = git('push', 
                     f'https://oauth2:{token}@github.com/tbj88/skill-hub-site.git', 'main')
            
            if r.returncode != 0:
                # Try rebase and push again
                git('pull', '--rebase',
                    f'https://oauth2:{token}@github.com/tbj88/skill-hub-site.git', 'main')
                r = git('push',
                         f'https://oauth2:{token}@github.com/tbj88/skill-hub-site.git', 'main')
            
            if r.returncode == 0:
                self.send_json({'ok': True, 'msg': f'saved {len(skills)} skills'})
            else:
                self.send_json({'ok': False, 'msg': r.stderr[:200]}, 500)
                
        except Exception as e:
            self.send_json({'ok': False, 'msg': str(e)}, 500)

    def send_json(self, data, code=200):
        self.send_response(code)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))

if __name__ == '__main__':
    port = 8766
    print(f'Save server running on http://localhost:{port}')
    HTTPServer(('127.0.0.1', port), Handler).serve_forever()
