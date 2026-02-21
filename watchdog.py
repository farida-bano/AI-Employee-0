#!/usr/bin/env python3

"""
System Health Monitoring Watchdog
Monitors AI Employee processes and restarts them if stopped
"""

import os
import sys
import time
import datetime
import subprocess
import psutil
import logging
from pathlib import Path
from logging.handlers import RotatingFileHandler


class SystemHealthMonitor:
    def __init__(self, vault_path="AI_Employee_Vault"):
        self.vault_path = Path(vault_path)
        self.logs_path = self.vault_path / "logs"
        self.health_log_path = self.logs_path / "system_health.md"
        self.status_log_path = self.logs_path / "system_status.log"

        # Create logs directory if it doesn't exist
        self.logs_path.mkdir(parents=True, exist_ok=True)

        # Define the processes to monitor
        self.processes = {
            "ai_employee_mcp_server": {
                "command": [sys.executable, "mcp/business_mcp/server.py"],
                "pattern": "server.py",
                "name": "Business MCP Server"
            },
            "ai_employee_file_watcher": {
                "command": [sys.executable, "Bronze/file_watcher.py"],
                "pattern": "file_watcher.py",
                "name": "File Watcher"
            },
            "ai_employee_scheduler": {
                "command": [sys.executable, "scripts/run_ai_employee", "daemon", "--interval", "300"],
                "pattern": "run_ai_employee",
                "name": "AI Employee Scheduler"
            }
        }

        # Set up logging
        self.setup_logging()

    def setup_logging(self):
        """Set up logging for the monitor"""
        # Create a custom logger
        self.logger = logging.getLogger('SystemHealthMonitor')
        self.logger.setLevel(logging.INFO)

        # Create handlers
        handler = RotatingFileHandler(
            self.status_log_path,
            maxBytes=5*1024*1024,  # 5MB
            backupCount=5
        )

        # Create formatters and add it to handlers
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        # Add handlers to the logger
        self.logger.addHandler(handler)

        # Prevent duplicate logs
        self.logger.propagate = False

    def find_process_by_pattern(self, pattern):
        """Find a process by command pattern"""
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if pattern in ' '.join(proc.info['cmdline']):
                    return proc
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return None

    def is_process_running(self, process_name):
        """Check if a process is running"""
        process_info = self.processes[process_name]
        pattern = process_info["pattern"]
        return self.find_process_by_pattern(pattern) is not None

    def start_process(self, process_name):
        """Start a process"""
        process_info = self.processes[process_name]
        command = process_info["command"]

        try:
            # Start the process in the background
            subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            self.logger.info(f"Started {process_info['name']} (Process: {command})")
            return True
        except Exception as e:
            self.logger.error(f"Failed to start {process_info['name']}: {e}")
            return False

    def restart_process(self, process_name):
        """Restart a process"""
        process_info = self.processes[process_name]
        self.logger.info(f"Restarting {process_info['name']}")

        # Try to start the process
        return self.start_process(process_name)

    def get_system_stats(self):
        """Get system statistics"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')

            return {
                "cpu_percent": cpu_percent,
                "memory_percent": memory.percent,
                "disk_percent": (disk.used / disk.total) * 100,
                "timestamp": datetime.datetime.now().isoformat()
            }
        except Exception as e:
            self.logger.error(f"Error getting system stats: {e}")
            return None

    def check_all_processes(self):
        """Check the status of all monitored processes"""
        status_report = {
            "timestamp": datetime.datetime.now(),
            "processes": {},
            "system_stats": self.get_system_stats(),
            "actions_taken": []
        }

        for process_name, process_info in self.processes.items():
            is_running = self.is_process_running(process_name)
            status_report["processes"][process_name] = {
                "name": process_info["name"],
                "running": is_running
            }

            if not is_running:
                self.logger.warning(f"{process_info['name']} is not running. Attempting to restart...")
                success = self.restart_process(process_name)
                if success:
                    status_report["actions_taken"].append(f"Restarted {process_info['name']}")
                    self.logger.info(f"Successfully restarted {process_info['name']}")
                else:
                    status_report["actions_taken"].append(f"Failed to restart {process_info['name']}")
                    self.logger.error(f"Failed to restart {process_info['name']}")
            else:
                self.logger.info(f"{process_info['name']} is running")

        return status_report

    def write_health_report(self, status_report):
        """Write health report to system_health.md"""
        try:
            # Read existing content if it exists
            if self.health_log_path.exists():
                existing_content = self.health_log_path.read_text()
            else:
                existing_content = "# System Health Report\n\n"

            # Create new report section
            timestamp = status_report["timestamp"].strftime("%Y-%m-%d %H:%M:%S")

            new_report = f"\n## Health Check - {timestamp}\n\n"

            # Add process status
            new_report += "### Process Status\n\n"
            for process_name, info in status_report["processes"].items():
                status = "✅ Running" if info["running"] else "❌ Stopped"
                new_report += f"- **{info['name']}**: {status}\n"

            # Add system stats if available
            if status_report["system_stats"]:
                stats = status_report["system_stats"]
                new_report += f"\n### System Stats\n\n"
                new_report += f"- CPU Usage: {stats['cpu_percent']:.1f}%\n"
                new_report += f"- Memory Usage: {stats['memory_percent']:.1f}%\n"
                new_report += f"- Disk Usage: {stats['disk_percent']:.1f}%\n"

            # Add actions taken
            if status_report["actions_taken"]:
                new_report += f"\n### Actions Taken\n\n"
                for action in status_report["actions_taken"]:
                    new_report += f"- {action}\n"

            new_report += "\n" + "-"*50 + "\n"  # Separator

            # Write combined content (keep recent entries, limit size)
            combined_content = existing_content + new_report

            # Keep only recent entries to prevent file from growing too large
            lines = combined_content.split('\n')
            if len(lines) > 200:  # Keep only last ~200 lines
                # Find the last 5 health check sections
                check_indices = []
                for i, line in enumerate(lines):
                    if line.startswith('## Health Check -'):
                        check_indices.append(i)

                if len(check_indices) > 10:  # Keep last 10 checks
                    start_idx = check_indices[-10]
                    combined_content = '# System Health Report\n\n' + '\n'.join(lines[start_idx:])

            self.health_log_path.write_text(combined_content)
            self.logger.info("Health report written to system_health.md")

        except Exception as e:
            self.logger.error(f"Error writing health report: {e}")

    def run_once(self):
        """Run a single health check"""
        self.logger.info("Starting health check...")

        # Check all processes
        status_report = self.check_all_processes()

        # Write report
        self.write_health_report(status_report)

        self.logger.info("Health check completed")
        return status_report

    def run_daemon(self, interval=300):  # 5 minutes = 300 seconds
        """Run the health check in daemon mode"""
        self.logger.info(f"Starting system health monitoring daemon (interval: {interval}s)")

        while True:
            try:
                self.run_once()
                time.sleep(interval)
            except KeyboardInterrupt:
                self.logger.info("Health monitoring stopped by user")
                break
            except Exception as e:
                self.logger.error(f"Error in monitoring loop: {e}")
                time.sleep(60)  # Wait a minute before retrying


def main():
    import argparse

    parser = argparse.ArgumentParser(description='System Health Monitor for AI Employee')
    parser.add_argument('mode', choices=['once', 'daemon'], help='Run mode: once or daemon')
    parser.add_argument('--interval', type=int, default=300, help='Interval in seconds for daemon mode (default: 300)')

    args = parser.parse_args()

    monitor = SystemHealthMonitor()

    if args.mode == 'once':
        monitor.run_once()
    elif args.mode == 'daemon':
        monitor.run_daemon(args.interval)


if __name__ == "__main__":
    main()