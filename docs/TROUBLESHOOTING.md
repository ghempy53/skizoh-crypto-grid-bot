# Troubleshooting

[← Back to README](../README.md)

## Troubleshooting

### "Grid spacing too tight"
Bot auto-adjusts. If frequent, increase `grid_spacing_percent`.

### "Grid efficiency < 40"
Market is unsuitable for grid trading. Wait for ranging conditions (ADX < 20).

### "Trend pause active"
Normal behavior. Strong trend detected (ADX > 40). Grid trading doesn't work in strong trends.

### "Exposure too high"
Too much crypto held. Bot will favor sell orders until exposure is back within limits.

### "Circuit OPEN" in logs
The exchange API returned repeated errors. The circuit breaker is protecting the bot from cascading failures. It will auto-recover after 60 seconds of cooldown.

### API errors
```bash
./test_setup.sh --api
```

**`-2015 Invalid API-key, IP, or permissions`** — the key was deleted,
lost permissions, or (most common on home ISPs) your public IP rotated
away from the key's IP whitelist. Rotate the key at Binance.US → API
Management (Read + Spot Trading only, never withdrawals). The bot no longer
crash-loops on this: it alerts your phone and re-checks every 15 minutes,
resuming automatically once the key works. The container will show
`unhealthy` while trading is down — that's the healthcheck doing its job.

### Memory issues on Pi
Check Docker resource limits. Consider:
- Reducing `max_position_percent`
- Using longer `check_interval_seconds`
- Archiving old positions manually

### Docker build fails with IPv6 errors

If you see errors like:
```
dial tcp [2606:4700:...]:443: socket: address family not supported by protocol
failed to copy: httpReadSeeker: failed open: failed to do request
```

This is an IPv6 connectivity issue. Docker is trying to reach registries over
IPv6 but your network (or the Pi's kernel) doesn't route IPv6.

> ⚠️  **A REBOOT IS REQUIRED whenever you hit this error**, even on subsequent
> occurrences. The fix touches the kernel cmdline, sysctl, systemd unit
> environments, and the DNS resolver — these only take effect together after a
> full reboot. Restarting Docker alone is not enough.

**Recommended: use the helper (fixes everything in one step)**
```bash
./docker-helper.sh fix-ipv6
sudo reboot                   # REQUIRED — do not skip, even on re-runs
./docker-helper.sh rebuild
```

The helper applies all of the following. If you prefer to do it manually, here
is exactly what it does — **all seven pieces are usually required** on a fresh
Pi OS Lite install, which is why piecemeal fixes tend to fail:

**1. Prefer IPv4 in glibc's name resolver (`/etc/gai.conf`)**

Without it, the resolver returns AAAA records first and Docker attempts IPv6
connections that fail, even when IPv6 is disabled on your interfaces.
```bash
echo "precedence ::ffff:0:0/96  100" | sudo tee -a /etc/gai.conf
```

**2. Disable IPv6 via sysctl (drop-in, not `/etc/sysctl.conf`)**
```bash
sudo tee /etc/sysctl.d/99-disable-ipv6.conf <<'EOF'
net.ipv6.conf.all.disable_ipv6 = 1
net.ipv6.conf.default.disable_ipv6 = 1
net.ipv6.conf.lo.disable_ipv6 = 1
EOF
sudo sysctl --system
```

**3. Disable IPv6 at the kernel level (`/boot/firmware/cmdline.txt`)**

⚠️  `cmdline.txt` **must remain a single line**. Adding `ipv6.disable=1` on a
new line is a common mistake — the bootloader will ignore it.
```bash
sudo nano /boot/firmware/cmdline.txt
# Append to the END of the existing line (preceded by a single space):
#   ... ipv6.disable=1
sudo reboot                   # kernel changes require a reboot to apply
```

**4. Configure the Docker daemon (`/etc/docker/daemon.json`)**
```json
{
  "ipv6": false,
  "dns": ["8.8.8.8", "1.1.1.1"],
  "dns-opts": ["ndots:0", "single-request"],
  "features": {"buildkit": false}
}
```
Then: `sudo systemctl restart docker`

Why `buildkit: false`? BuildKit runs in its own container with a Go-based
DNS resolver that **ignores `/etc/gai.conf`** and does not fall back cleanly
from IPv6 to IPv4 when the kernel rejects `AF_INET6` sockets. The legacy
builder (used when BuildKit is off) pulls through dockerd directly and handles
IPv6-less networks correctly.

**5. Force dockerd + containerd to use glibc's resolver (systemd drop-ins)**

Even with BuildKit off, dockerd/containerd are Go programs whose default
`netgo` resolver ignores `/etc/gai.conf`. They return AAAA records first and
the `httpReadSeeker` blob-fetch path fails with `EAFNOSUPPORT` instead of
falling back to IPv4. Setting `GODEBUG=netdns=cgo+1` routes DNS through glibc,
which honours the `gai.conf` priority from step 1.
```bash
sudo mkdir -p /etc/systemd/system/docker.service.d
sudo tee /etc/systemd/system/docker.service.d/10-ipv4-resolver.conf <<'EOF'
[Service]
Environment=GODEBUG=netdns=cgo+1
EOF
sudo mkdir -p /etc/systemd/system/containerd.service.d
sudo tee /etc/systemd/system/containerd.service.d/10-ipv4-resolver.conf <<'EOF'
[Service]
Environment=GODEBUG=netdns=cgo+1
EOF
sudo systemctl daemon-reload
```

**6. Drop AAAA records entirely (`/etc/resolv.conf` + dhcpcd hook)**

Belt-and-suspenders: tell glibc's stub resolver to skip AAAA lookups, so
nothing upstream ever sees an IPv6 address for `registry-1.docker.io`. Also
persist the option via `/etc/resolvconf.conf` and a `dhcpcd` hook so a DHCP
lease renewal doesn't wipe it.
```bash
echo 'options single-request no-aaaa' | sudo tee -a /etc/resolv.conf
echo 'resolv_conf_options="single-request no-aaaa"' | sudo tee -a /etc/resolvconf.conf
```

**7. Clear stale buildx state**
```bash
docker buildx prune -af
```

**Reboot, then verify**
```bash
sudo reboot                                    # REQUIRED — apply all changes
# --- after reboot ---
ip -6 addr                                     # no global IPv6 addresses
docker info | grep -i ipv6                     # IPv6: off / false
./docker-helper.sh rebuild                     # build should succeed
```

If the rebuild still fails after a reboot, re-run `./docker-helper.sh fix-ipv6`
— the final step pulls the base image as a live test and will tell you exactly
which piece didn't apply.

---

