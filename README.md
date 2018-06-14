## Saned Scanner Host
Simple web app that permit the user to take pictures from a saned scanner and automatically generate pdf.

## Requirements (pip)
- flask
- flask-socketio

## Requirements (system)
- A scanner available from saned over the network (see https://wiki.debian.org/SaneOverNetwork)
- `scanimage` utility (apt-get install sane-utils on debian) to interact with scanner
- `convert` utility (apt-get install imagemagick) to generate `pdf` from images
