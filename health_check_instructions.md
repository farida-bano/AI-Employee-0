# AI Employee Health Check Instructions

## Service Status Checks

### 1. PM2 Service Status
```bash
# Check overall status of all processes
pm2 status

# Check logs of specific processes
pm2 logs ai-employee-mcp-server
pm2 logs ai-employee-file-watcher
pm2 logs ai-employee-scheduler
```

### 2. Process Health Check Script
Create a script to check health of all AI Employee services:

```bash
#!/bin/bash
# health_check.sh

echo "=== AI Employee Health Check ==="

# Check if PM2 processes are running
echo "Checking PM2 processes:"
pm2 jlist | jq -r '.[] | "Name: \(.name), Status: \(.pm2_env.status), CPU: \(.monit.cpu)%, Memory: \(.monit.memory) bytes"'

# Check if processes are listening on expected ports
echo "Checking port usage:"
netstat -tuln | grep 8000  # Business MCP Server should be on port 8000

# Check recent log entries for errors
echo "Checking for recent errors in logs:"
if [ -f "logs/pm2-mcp-combined.log" ]; then
  echo "Recent errors in MCP Server logs:"
  tail -50 logs/pm2-mcp-combined.log | grep -i error || echo "No errors found in MCP Server logs"
fi

if [ -f "logs/pm2-file-watcher-combined.log" ]; then
  echo "Recent errors in File Watcher logs:"
  tail -50 logs/pm2-file-watcher-combined.log | grep -i error || echo "No errors found in File Watcher logs"
fi

if [ -f "logs/pm2-scheduler-combined.log" ]; then
  echo "Recent errors in Scheduler logs:"
  tail -50 logs/pm2-scheduler-combined.log | grep -i error || echo "No errors found in Scheduler logs"
fi

# Check file system status
echo "Checking Bronze directory status:"
ls -la Bronze/Inbox/ 2>/dev/null || echo "Inbox directory not found"
ls -la Bronze/Needs_Action/ 2>/dev/null || echo "Needs_Action directory not found"
ls -la Bronze/Done/ 2>/dev/null || echo "Done directory not found"

# Check disk usage
echo "Disk usage:"
df -h

echo "=== Health Check Complete ==="
```

### 3. System Health Monitoring

#### Memory and CPU Usage:
```bash
# Check resource usage
pm2 monit
```

#### Log File Monitoring:
```bash
# Monitor logs in real-time
tail -f logs/pm2-mcp-combined.log
tail -f logs/pm2-file-watcher-combined.log
tail -f logs/pm2-scheduler-combined.log
```

### 4. Auto-healing Commands

If services crash:

```bash
# Restart all services
pm2 restart all

# Restart specific service
pm2 restart ai-employee-mcp-server
pm2 restart ai-employee-file-watcher
pm2 restart ai-employee-scheduler

# If services are stuck, reset them
pm2 reset all

# Reload PM2 configuration if changed
pm2 reload all
```

### 5. Automated Health Checks Setup

Add to crontab for periodic health checks:

```bash
# Edit crontab
crontab -e

# Add this line to check every 5 minutes and log to file
*/5 * * * * /opt/ai-employee/health_check.sh >> /opt/ai-employee/logs/health_check.log 2>&1
```

### 6. Startup Verification

After deployment, verify services are running:

```bash
# Ensure service starts on boot
sudo env PATH=$PATH:/usr/bin /usr/lib/node_modules/pm2/bin/pm2 startup systemd -u ubuntu --hp /home/ubuntu
sudo pm2 save
sudo pm2 startup
```

### 7. Troubleshooting Common Issues

- **Service won't start**: Check logs with `pm2 logs <service-name>`
- **Port already in use**: Check with `sudo netstat -tuln | grep 8000`
- **Python environment issues**: Verify virtual environment activation with `source venv/bin/activate`
- **Permission issues**: Ensure all files have proper permissions with `chmod +x start.sh`
- **PM2 not starting on boot**: Run the startup commands above as root/sudo