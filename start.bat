@echo off
cd /d %~dp0
echo Open this address in your browser:
echo   http://127.0.0.1:4173/
echo Do not double-click index.html — the 3D book needs a local server.
py -m http.server 4173
