# Skizoh Grid Bot - Docker Deployment for Raspberry Pi

Complete guide to running the Skizoh Crypto Grid Trading Bot in Docker on your Raspberry Pi.

## 📋 Prerequisites

- Raspberry Pi 3, 4, or 5 (ARM64 recommended)
- Raspberry Pi OS (64-bit recommended) or Ubuntu
- Docker and Docker Compose installed
- At least 1GB free RAM
- Stable internet connection

### Installing Docker on Raspberry Pi

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add your user to docker group (logout/login required)
sudo usermod -aG docker $USER

# Install Docker Compose
sudo apt install -y docker-compose-plugin

# Verify installation
docker --version
docker compose version
```

## 🚀 Quick Start

### 1. Clone or Copy Files

```bash
# Create directory
mkdir -p ~/skizoh-grid-bot
cd ~/skizoh-grid-bot

# Copy all Docker files and source code here
# Your directory should look like:
# ~/skizoh-grid-bot/
# ├── Dockerfile
# ├── docker-compose.yml
# ├── docker-entrypoint.sh
# ├── requirements.txt
# ├── Makefile
# ├── .dockerignore
# ├── config.json          # Your configuration
# ├── data/                 # Data persistence
# └── src/                  # Source code
#     ├── main.py
#     ├── grid_bot.py
#     ├── market_analysis.py
#     ├── config_manager.py
#     ├── tax_summary.py
#     ├── test_api.py
#     └── priv/
#         └── config.json.template
```

### 2. Configure Your Bot

```bash
# Copy template to create your config
cp src/priv/config.json.template config.json

# Edit with your API credentials
nano config.json
```

Update these fields in `config.json`:
```json
{
    "api_key": "YOUR_ACTUAL_BINANCE_US_API_KEY",
    "api_secret": "YOUR_ACTUAL_BINANCE_US_API_SECRET",
    "symbol": "ETH/USDT",
    ...
}
```

### 3. Build and Run

```bash
# Build the Docker image (takes 5-10 minutes on Pi)
make build

# Test your API connection first
make test-api

# Start the bot
make run

# View logs
make logs
```

## 📁 Directory Structure

```
~/skizoh-grid-bot/
├── Dockerfile              # Container build instructions
├── docker-compose.yml      # Service configuration
├── docker-entrypoint.sh    # Container startup script
├── requirements.txt        # Python dependencies
├── Makefile               # Convenience commands
├── .dockerignore          # Build exclusions
├── config.json            # YOUR CONFIG (not in git!)
├── data/                  # Persistent data (auto-created)
│   ├── grid_bot.log       # Runtime logs
│   ├── position_state.json # Position tracking
│   └── tax_transactions.csv # Tax records
└── src/                   # Source code
    ├── main.py
    ├── grid_bot.py
    ├── market_analysis.py
    ├── config_manager.py
    ├── tax_summary.py
    └── test_api.py
```

## 🛠️ Commands Reference

### Using Make (Recommended)

| Command | Description |
|---------|-------------|
| `make build` | Build Docker image |
| `make run` | Start bot in background |
| `make stop` | Stop the bot |
| `make restart` | Restart the bot |
| `make logs` | View live logs |
| `make shell` | Open shell in container |
| `make test-api` | Test API connection |
| `make tax-summary` | Generate tax report |
| `make status` | Show container status |
| `make clean` | Remove container & image |

### Using Docker Compose Directly

```bash
# Build
docker-compose build

# Start (detached)
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down

# Restart
docker-compose restart

# Shell access
docker-compose exec gridbot /bin/bash
```

### Using Docker Run

```bash
# Run bot
docker run -d --name skizoh-gridbot \
  -v $(pwd)/config.json:/app/src/priv/config.json:ro \
  -v $(pwd)/data:/app/data \
  --restart unless-stopped \
  skizoh-grid-bot

# Test API
docker run --rm \
  -v $(pwd)/config.json:/app/src/priv/config.json:ro \
  skizoh-grid-bot test-api

# Generate tax summary
docker run --rm \
  -v $(pwd)/data:/app/data \
  skizoh-grid-bot tax-summary 2025
```

## 🔧 Configuration

### Environment Variables

Set in `docker-compose.yml` or pass with `-e`:

| Variable | Default | Description |
|----------|---------|-------------|
| `TZ` | `America/Denver` | Timezone for logs |
| `PYTHONUNBUFFERED` | `1` | Real-time log output |

### Resource Limits

Default limits in `docker-compose.yml`:
- Memory: 512MB max, 256MB reserved
- Adjust based on your Pi model

For Pi 3 (1GB RAM):
```yaml
deploy:
  resources:
    limits:
      memory: 384M
    reservations:
      memory: 192M
```

For Pi 4/5 (4GB+ RAM):
```yaml
deploy:
  resources:
    limits:
      memory: 1G
    reservations:
      memory: 512M
```

## 📊 Monitoring

### View Logs

```bash
# Live logs
make logs

# Last 100 lines
docker-compose logs --tail=100

# Search for errors
docker-compose logs | grep -i error
```

### Check Status

```bash
# Container status
make status

# Detailed stats
docker stats skizoh-gridbot

# Health check
docker inspect skizoh-gridbot | grep -A 10 Health
```

### View Data Files

```bash
# Check position state
cat data/position_state.json | python3 -m json.tool

# View recent trades
tail -20 data/tax_transactions.csv

# Check log size
ls -lh data/grid_bot.log
```

## 🔄 Updating the Bot

```bash
# Pull latest code changes
git pull  # or copy new files

# Rebuild image
make build

# Restart with new version
make restart
```

## 🔒 Security Best Practices

1. **Protect your config.json**
   ```bash
   chmod 600 config.json
   ```

2. **Use read-only mount for config**
   - Already configured in docker-compose.yml with `:ro`

3. **API Key Permissions on Binance.US**
   - ✅ Enable: Spot Trading
   - ❌ Disable: Withdrawals
   - ✅ Restrict to your Pi's IP address

4. **Keep Docker updated**
   ```bash
   sudo apt update && sudo apt upgrade docker-ce docker-compose-plugin
   ```

## 🐛 Troubleshooting

### Container won't start

```bash
# Check logs
docker-compose logs

# Verify config
docker-compose run --rm gridbot test-api
```

### "Config file not found" error

Ensure `config.json` exists in the project root:
```bash
ls -la config.json
```

### API connection failed

1. Check internet: `ping api.binance.us`
2. Verify API keys in config.json
3. Check IP whitelist on Binance.US

### Out of memory

Reduce memory limits or close other containers:
```bash
docker system prune -a
```

### Permission denied on data directory

```bash
sudo chown -R $USER:$USER data/
```

### Container keeps restarting

Check for crashes:
```bash
docker-compose logs --tail=50
```

## 📈 Performance on Raspberry Pi

| Pi Model | Build Time | Memory Usage | Recommended |
|----------|------------|--------------|-------------|
| Pi 3B+ | ~15 min | 200-300MB | ⚠️ Marginal |
| Pi 4 (2GB) | ~8 min | 200-350MB | ✅ Good |
| Pi 4 (4GB) | ~8 min | 200-350MB | ✅ Great |
| Pi 5 | ~4 min | 200-350MB | ✅ Excellent |

## 🔌 Running at Startup

The `restart: unless-stopped` policy ensures the bot starts on boot.

To manually enable:
```bash
# Enable Docker to start on boot
sudo systemctl enable docker

# Your container will auto-start with Docker
```

## 📝 Backup

```bash
# Backup data directory
tar -czvf gridbot-backup-$(date +%Y%m%d).tar.gz data/

# Backup config (store securely!)
cp config.json config.json.backup
```

## ❓ FAQ

**Q: Can I run multiple bots for different trading pairs?**
A: Yes! Create separate directories with different config files and use different container names.

**Q: Does the bot survive Pi reboots?**
A: Yes, with `restart: unless-stopped` it auto-starts. Position state is persisted in `data/position_state.json`.

**Q: How do I change trading scenarios?**
A: The bot prompts for scenario selection at startup. To change, restart the container and select a new scenario when it prompts.

**Q: Can I access the bot's interactive menu in Docker?**
A: The bot starts with the configured scenario. For interactive mode, use `docker-compose run gridbot run` instead of `docker-compose up`.

---

**Happy Trading! 🚀💰**
