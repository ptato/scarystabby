#!/usr/bin/env python3
import dd, os
from http.server import BaseHTTPRequestHandler, HTTPServer

class DevilHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        option = os.path.basename(self.path)
        if option.startswith('login_steam'):
            print('Logging in to steam!', flush=True)
            self.login_steam()
        elif option.startswith('get_scores'):
            print('Giving them the scores!', flush=True)
            self.get_scores()
        else:
            print('unknown option ' + option, flush=True)

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=UTF-8')
        # TODO: I think these are on the wireshark packets, but uncommenting it
        # makes dd not connect. Double-check they really are and test one by one.
        # self.send_header('Transfer-Encoding', 'chunked')
        # self.send_header('Connection', 'keep-alive')
        # self.send_header('Access-Control-Allow-Methods', 'GET, POST\r\n')
        # self.send_header('Access-Control-Allow-Origin', '*\r\n')
        self.end_headers()

    def login_steam(self):
        self._set_headers()
        # TODO: Need to figure this out
        with open('login.bin', 'rb') as f:
            self.wfile.write(f.read())

    def get_scores(self):
        self._set_headers()
        self.wfile.write(dd.create_leaderboards('leaderboards.bin'))

def run_server(host, port):
    with HTTPServer((host, port), DevilHandler) as httpd:
        print('Listening on ' + host + ':' + str(port) + ' ...', flush=True)
        httpd.serve_forever()

if __name__ == '__main__':
    run_server('localhost', 8081)
