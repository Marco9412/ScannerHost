#!/bin/bash

cd ..

# Generate service description

echo -e "[Unit]
Description=ScannerHost instance
After=network.target

[Service]
User=$(whoami)
Group=$(whoami)
WorkingDirectory=$(pwd)
Environment=\"PATH=/usr/bin\"
ExecStart=\"/usr/bin/python3 ScannerHost.py &> scannerHost.log\"

[Install]
WantedBy=multi-user.target
" > systemd/ScannerHost.service

# Enable and start service
sudo cp systemd/ScannerHost.service /etc/systemd/system/
sudo systemctl start ScannerHost
sudo systemctl enable ScannerHost
