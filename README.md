# Skizoh Crypto Grid Trading Bot v4.1

A profit-optimized, Raspberry Pi-friendly cryptocurrency grid trading bot for Binance.US.

---

## Setup

End-to-end setup for a fresh **Raspberry Pi OS Lite (Bookworm, 64-bit)** install.
Follow every step in order — skipping any of them is the #1 source of "it doesn't
work" reports. If you're on a regular desktop Linux, every step still applies
except the Pi-specific hardware/IPv6 bits (flagged 🍓 below).

> **TL;DR for returning users:**
> ```bash
> cd ~/skizoh-crypto-grid-bot
> ./docker-helper.sh fix-ipv6 && sudo reboot        # 🍓 Pi OS Lite only
> # after reboot:
> cp src/priv/config.json.template src/priv/config.json
> chmod 600 src/priv/config.json
> nano src/priv/config.json                          # paste your API keys
> ./docker-helper.sh fix-permissions
> ./docker-helper.sh rebuild                         # build + start
> ./docker-helper.sh logs                            # verify
> ```

### 0. Prerequisites

You need, on the Pi:

| Requirement | How to check | How to install |
|---|---|---|
| Raspberry Pi OS Lite (Bookworm, 64-bit recommended) | `cat /etc/os-release` | [raspberrypi.com/software](https://www.raspberrypi.com/software/) |
| A user with `sudo` (default `pi` or your own user) | `id` | Created during Pi OS imaging |
| `git` | `git --version` | `sudo apt update && sudo apt install -y git` |
| Docker Engine **+ Compose v2 plugin** | `docker --version` and `docker compose version` | See step 1 below |
| Internet connectivity (IPv4) | `ping -4 -c 1 registry-1.docker.io` | fix router/DNS if this fails |
| Binance.US account with **trading-enabled API key + secret** | [binance.us API management](https://www.binance.us/en/usercenter/settings/api-management) | Create key with *Enable Reading* + *Enable Spot & Margin Trading*, disable *Enable Withdrawals*, IP-whitelist your Pi |

**Do not use your Binance.US login password anywhere in this project. The bot
only needs the API key/secret.**

### 1. Install Docker on Raspberry Pi OS

The canonical script from Docker works on all Pi models running 64-bit OS:

```bash
curl -fsSL https://get.docker.com | sudo sh
sudo usermod -aG docker "$USER"        # let your user run docker without sudo
sudo apt install -y docker-compose-plugin  # installs `docker compose` v2
```

**Log out and log back in** (or `newgrp docker`) so the group change takes
effect. Then verify:

```bash
docker --version                       # Docker version 2x.x.x
docker compose version                 # Docker Compose version v2.x.x
docker run --rm hello-world            # should print a success message
```

If `hello-world` fails with an IPv6 error, that's expected on Pi OS Lite —
continue to step 3 and the fix-ipv6 helper will resolve it before the first
real build.

### 2. Clone the repository

The bot expects to live at `~/skizoh-crypto-grid-bot` (the `run_bot.sh`,
`monitor_bot.sh`, and `test_setup.sh` scripts hard-code this path). If you
clone elsewhere, the Docker workflow still works, but the native Python
helper scripts won't find themselves.

```bash
cd ~
git clone https://github.com/ghempy53/skizoh-crypto-grid-bot.git
cd skizoh-crypto-grid-bot
```

### 3. 🍓 Fix IPv6 on Pi OS Lite (one-time, **requires a reboot**)

Pi OS Lite ships with IPv6 enabled but often no working IPv6 route, which
makes Docker image pulls fail with:

```
dial tcp [2606:4700:...]:443: socket: address family not supported by protocol
```

Run the helper — it applies kernel, sysctl, systemd, daemon, and resolver-level
fixes in one shot, then reboots:

```bash
./docker-helper.sh fix-ipv6
sudo reboot                             # REQUIRED — do not skip
```

> ⚠️  **A reboot is required every time you hit an IPv6 build error**, not just
> the first time. The fix touches the kernel cmdline, systemd unit environment,
> and resolv.conf — these only take effect together after a full reboot.
> Restarting Docker alone is not enough. See the
> [IPv6 troubleshooting section](docs/TROUBLESHOOTING.md#docker-build-fails-with-ipv6-errors) for the
> 7-step manual breakdown if you want to understand what it's doing.

Skip this step on non-Pi Linux or on Pi networks with working IPv6.

### 4. Create and configure `src/priv/config.json`

This is the **only** place your API credentials live. It is gitignored and
bind-mounted read-only into the container.

```bash
cp src/priv/config.json.template src/priv/config.json
chmod 600 src/priv/config.json          # owner read/write only
nano src/priv/config.json
```

Replace the two placeholders with your Binance.US API credentials and save:

```json
{
    "api_key":    "paste-your-binance-us-api-key-here",
    "api_secret": "paste-your-binance-us-api-secret-here",
    "symbol":     "ETH/USDT"
}
```

Leave everything else in the template at its defaults — v4.1's adaptive
engine tunes the trading parameters live. The top-level keys you may want
to review before going live: `symbol`, `use_bnb_for_fees`, `fee_rate`,
`max_position_percent`, `default_scenario`.

### 5. Set file permissions

The project ships with the right permissions, but `git clone` can flatten
the executable bits depending on your umask and filesystem. Reset them in
one command:

```bash
./docker-helper.sh fix-permissions
```

That sets:

| Path | Mode | Why |
|---|---|---|
| `src/priv/config.json` | `600` | Secrets — only your user may read |
| `docker-helper.sh`, `docker-entrypoint.sh`, `run_bot.sh`, `monitor_bot.sh`, `test_setup.sh` | `+x` (755) | Scripts must be executable |
| `data/` | `755` | Bot writes logs, tax CSVs, position state here |
| `src/priv/config.json.template` | `644` | Template stays world-readable |

If `./docker-helper.sh` itself is not yet executable (so `fix-permissions`
can't run), bootstrap it by hand:

```bash
chmod +x docker-helper.sh
./docker-helper.sh fix-permissions
```

Also verify the `data/` directory is owned by UID **1000** (the container's
`gridbot` user). On a default Pi install the first user `pi` / `hondarhonda`
is already UID 1000, so this is automatic. To confirm:

```bash
id -u                                   # should print 1000
mkdir -p data && ls -ld data            # owner should match your user
```

If your host user is not UID 1000, either create a UID-1000 user and `chown`
the tree to it, or change the container user by editing the `useradd` line
in `Dockerfile` before building.

### 6. Tune Docker resource limits for your Pi model (optional)

The bot targets 180 MB RAM at rest, but the default limits in
`docker-compose.yml` are sized for a Pi 4 (2 GB). Edit the `deploy.resources`
block to match your hardware:

| Pi Model | `memory` | `cpus` |
|---|---|---|
| Pi 3 (1 GB) | `256M` | `0.5` |
| Pi 4 (2 GB) | `384M` *(default)* | `0.75` |
| Pi 4 (4 GB+) | `512M` | `1.0` |
| Pi 5 | `768M` | `1.5` |

```yaml
deploy:
  resources:
    limits:
      cpus: '0.75'
      memory: 384M
```

### 7. Test the API connection before going live

Pull the image once and run the API smoke test without starting the bot:

```bash
./docker-helper.sh build                 # first build, ~5-10 min on Pi 4
docker compose run --rm gridbot test-api
```

A successful run prints your account balances and confirms Binance.US sees
your key. If it fails:

- **`Invalid API-key`** → you pasted the wrong key or the key is disabled.
- **`IP not whitelisted`** → add your Pi's public IP to the key's whitelist
  on Binance.US, or temporarily remove the whitelist while testing.
- **IPv6 error** → re-run step 3, then `sudo reboot`.

### 8. Start the bot and verify

```bash
./docker-helper.sh start
./docker-helper.sh logs                  # live logs, Ctrl+C to detach
```

You should see the startup banner, "Config validated", scenario selection,
and within a minute or two, your first grid being placed. If the container
exits immediately, `./docker-helper.sh diagnose` will point at the cause.

### 9. Daily operation

Routine commands you'll actually use:

```bash
./docker-helper.sh logs                  # follow live logs
./docker-helper.sh logs-tail 200         # last 200 lines
./docker-helper.sh status                # container + resources
./docker-helper.sh stop / start / restart
./docker-helper.sh backup                # snapshot config + data/
./docker-helper.sh update                # git pull + rebuild + start
python3 portfolio.py                     # portfolio dashboard (host-side)
```

### Native (non-Docker) setup — advanced

Only use this if you specifically want to run the bot in a venv on the host
(e.g. for development). Docker is the supported production path.

```bash
cd ~/skizoh-crypto-grid-bot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp src/priv/config.json.template src/priv/config.json
chmod 600 src/priv/config.json
nano src/priv/config.json                # paste API keys

chmod +x run_bot.sh monitor_bot.sh test_setup.sh
./test_setup.sh --all                    # full environment check
./run_bot.sh                             # start the bot
```

---

## Documentation

Detailed docs live in the [`docs/`](docs/) folder:

- **[Release History](docs/CHANGELOG.md)** — what changed in each version and why (v4.1 cycle-economics tuning, v4.0 down-market survival, and earlier).
- **[Architecture & Strategy](docs/ARCHITECTURE.md)** — the adaptive configuration engine, market-regime detection, resilience systems, and technical indicators.
- **[Configuration Reference](docs/CONFIGURATION.md)** — file structure, every config parameter, trading scenarios, and ready-made config profiles.
- **[Risk Management & P&L](docs/RISK.md)** — the exposure controller, trailing stop, stop-loss backstop, and FIFO cost-basis accounting.
- **[Operations & Monitoring](docs/OPERATIONS.md)** — phone alerts, the daily report, the portfolio helper CLI, shell scripts, and performance expectations.
- **[Troubleshooting](docs/TROUBLESHOOTING.md)** — common warnings, API errors, memory issues, and the Pi IPv6 fix.

---

## Security Best Practices

1. **Protect config.json**: `chmod 600 src/priv/config.json`
2. **Disable withdrawals** on your API key
3. **Set IP restrictions** on Binance.US
4. **Never commit** config.json to git (it is gitignored by default)
5. **Use read-only mount** in Docker: `config.json:/app/src/priv/config.json:ro`

---


## License

GNU General Public License v3.0

---

## Disclaimer

This software is for educational purposes. Cryptocurrency trading involves significant risk. Past performance does not guarantee future results. Only trade with funds you can afford to lose.

---

*Skizoh Crypto Grid Trading Bot v4.1 — Profit-Optimized Smart Adaptive Trading*
