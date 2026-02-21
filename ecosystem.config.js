module.exports = {
  apps: [
    {
      name: 'ai-employee-mcp-server',
      script: 'mcp/business_mcp/server.py',
      interpreter: './venv/bin/python',
      cwd: '.',
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: '1G',
      env: {
        NODE_ENV: 'production',
        PYTHONPATH: '.'
      },
      error_file: 'logs/pm2-mcp-err.log',
      out_file: 'logs/pm2-mcp-out.log',
      log_file: 'logs/pm2-mcp-combined.log'
    },
    {
      name: 'ai-employee-file-watcher',
      script: 'Bronze/file_watcher.py',
      interpreter: './venv/bin/python',
      cwd: '.',
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: '1G',
      env: {
        NODE_ENV: 'production',
        PYTHONPATH: '.'
      },
      error_file: 'logs/pm2-file-watcher-err.log',
      out_file: 'logs/pm2-file-watcher-out.log',
      log_file: 'logs/pm2-file-watcher-combined.log'
    },
    {
      name: 'ai-employee-scheduler',
      script: 'scripts/run_ai_employee',
      interpreter: './venv/bin/python',
      cwd: '.',
      args: 'daemon --interval 300',
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: '1G',
      env: {
        NODE_ENV: 'production',
        PYTHONPATH: '.'
      },
      error_file: 'logs/pm2-scheduler-err.log',
      out_file: 'logs/pm2-scheduler-out.log',
      log_file: 'logs/pm2-scheduler-combined.log'
    },
    {
      name: 'ai-employee-watchdog',
      script: 'watchdog.py',
      interpreter: './venv/bin/python',
      cwd: '.',
      args: 'daemon --interval 300',
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: '1G',
      env: {
        NODE_ENV: 'production',
        PYTHONPATH: '.'
      },
      error_file: 'logs/pm2-watchdog-err.log',
      out_file: 'logs/pm2-watchdog-out.log',
      log_file: 'logs/pm2-watchdog-combined.log'
    }
  ]
};