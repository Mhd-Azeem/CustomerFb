#!/usr/bin/env sh
set -eu
cd "$(dirname "$0")/.."
python3 source/build.py
mkdir -p public
cp index.html privacy.html 404.html site.css site.js logo.webp poster.jpg oman-video.mp4 \
  favicon.png social-preview.jpg CNAME robots.txt sitemap.xml public/
cp -R ne en ta si hi public/
for verification in google*.html; do
  [ -f "$verification" ] || continue
  cp "$verification" public/
done
