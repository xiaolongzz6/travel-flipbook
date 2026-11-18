#!/bin/sh
cd "$(dirname "$0")"
echo "Open http://127.0.0.1:4173/  (do not open index.html as a file)"
python3 -m http.server 4173
