#!/bin/bash

# Deployment commands for AI Employee on Ubuntu Linux VM

# 1. Update system packages
sudo apt update && sudo apt upgrade -y

# 2. Install Python 3 and pip
sudo apt install -y python3 python3-pip python3-venv

# 3. Install Node.js and npm (required for PM2)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# 4. Install PM2 globally
sudo npm install -g pm2

# 5. Install additional dependencies for health monitoring
pip install psutil

# 6. Clone the AI Employee repository (if not already present)
# git clone https://your-repository-url.git /opt/ai-employee
# cd /opt/ai-employee

# 7. Create Python virtual environment and install dependencies
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install fastapi uvicorn mcp-server watchdog psutil

# 8. Create logs directory
mkdir -p logs

# 9. Install PM2 startup script to run on system boot
sudo pm2 startup
sudo pm2 save

# 10. Start the AI Employee services with PM2 (including watchdog)
# This assumes you have start.sh and ecosystem.config.js in place
# pm2 start ecosystem.config.js
# pm2 save

# 11. Optional: Set up cron job for health monitoring (alternative to PM2 watchdog)
# crontab health_cron_jobs.txt