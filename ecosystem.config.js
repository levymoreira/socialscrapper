module.exports = {
  apps: [{
    name: 'linkedin-api',
    script: 'api.py',
    interpreter: 'python3',
    instances: 1,
    autorestart: true,
    watch: false,
    max_memory_restart: '1G',
    env: {
      AZURE_API_TOKEN: '7X36bPbHvy6muxdJvkCfxLXvaFNzKfp2Eg4NmPx15L2quvA3W1QYJQQJ99BHACYeBjFXJ3w3AAAAACOGVkXk',
      PYTHONUNBUFFERED: '1'
    },
    error_file: './logs/linkedin-api-err.log',
    out_file: './logs/linkedin-api-out.log',
    log_file: './logs/linkedin-api-combined.log',
    time: true,
    merge_logs: true,
    log_date_format: 'YYYY-MM-DD HH:mm:ss',
    
    // Restart settings
    min_uptime: '10s',
    max_restarts: 10,
    restart_delay: 4000,
    
    // Graceful shutdown
    kill_timeout: 3000,
    wait_ready: true,
    
    // Auto-restart on file changes (optional, disabled by default)
    // watch: ['api.py', '*.py'],
    // ignore_watch: ['node_modules', 'logs', 'results', '.git', '__pycache__', '*.pyc'],
    
    // Cron-like restart (optional)
    // cron_restart: '0 0 * * *', // Restart daily at midnight
  }]
};