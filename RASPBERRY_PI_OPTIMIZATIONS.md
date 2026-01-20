# Skizoh Grid Bot - Raspberry Pi Docker Optimizations

## Executive Summary

This document outlines comprehensive optimizations for running the Skizoh Crypto Grid Trading Bot on Raspberry Pi in Docker. The optimizations focus on **memory efficiency**, **CPU usage**, **Docker image size**, and **reliability**.

---

# Disabling IPv6 on Raspberry Pi for Docker

A guide to permanently disable IPv6 for Docker on Raspberry Pi OS, solving connection issues with Docker registries.

## The Problem

Docker may attempt to connect to registries over IPv6, causing errors like:
```
dial tcp [2600:1f18:2148:bc00:...]:443: connect: cannot assign requested address
```

## Solution

### Step 1: Disable IPv6 at Kernel Boot

Edit the kernel command line:
```bash
sudo nano /boot/firmware/cmdline.txt
```

Add to the **end** of the existing line (same line, with a space before):
```
 ipv6.disable=1
```

> ⚠️ **Important:** Do not create a new line. The file must remain a single line.

### Step 2: Configure Docker Daemon

Create or edit the Docker daemon configuration:
```bash
sudo nano /etc/docker/daemon.json
```

Add the following:
```json
{
  "ipv6": false,
  "ip6tables": false
}
```

### Step 3: Clean Up /etc/hosts
```bash
sudo nano /etc/hosts
```

Keep it minimal:
```
127.0.0.1       localhost
127.0.1.1       raspberrypi
```

> 💡 **Tip:** Do not hardcode Docker registry IPs — they change over time and will cause issues.

### Step 4: Reboot
```bash
sudo reboot
```

### Step 5: Verify

After reboot, confirm IPv6 is disabled:
```bash
cat /proc/sys/net/ipv6/conf/all/disable_ipv6
```

Expected output: `No such file or directory` (the IPv6 module is not loaded)

Confirm Docker has IPv6 disabled:
```bash
docker network inspect bridge | grep -i enableipv6
```

Expected output: `"EnableIPv6": false`

### Step 6: Test
```bash
docker pull hello-world
```

Should complete without IPv6 errors.

## Why This Works

The `ipv6.disable=1` kernel parameter prevents the IPv6 module from loading at boot, before any services start. This is more reliable than `sysctl` settings, which can be overridden by services like NetworkManager or dhcpcd.

## Troubleshooting

If you still see IPv6 errors after following these steps:

1. Clear Docker's build cache:
```bash
   docker builder prune -a
```

2. Full Docker cleanup:
```bash
   docker system prune -a --volumes
```

3. Restart Docker:
```bash
   sudo systemctl restart docker
```

## 🔍 Analysis of Current State

### Current Performance Metrics (Estimated)
| Metric | Current | Optimized Target |
|--------|---------|------------------|
| Docker Image Size | ~450MB | ~180MB |
| Runtime Memory | 200-350MB | 120-180MB |
| CPU Usage (Idle) | 5-15% | 2-5% |
| Build Time (Pi 4) | 8-15 min | 4-6 min |
| Startup Time | 15-20s | 8-12s |

### Issues Identified

1. **Dockerfile inefficiencies**
   - Not using multi-stage builds
   - Includes gcc/build tools in final image
   - Not using Alpine or slim base optimally

2. **Python code memory issues**
   - Large numpy arrays not freed
   - No caching TTL causing memory growth
   - Position tracker deque unbounded growth potential
   - OHLCV data fetched repeatedly

3. **Docker configuration gaps**
   - No memory swap limits
   - Missing tmpfs for temporary files
   - No CPU throttling for background operation

4. **Logging/storage issues**
   - Log rotation not in Docker
   - No data cleanup automation
   - Tax CSV can grow unbounded

---

## 🐳 Docker Optimizations

### 1. Multi-Stage Dockerfile (NEW)
Reduces image size by ~60% by separating build and runtime stages.

### 2. Resource Limits Enhancement
```yaml
# Optimized for Pi 3/4/5
deploy:
  resources:
    limits:
      cpus: '0.75'       # Leave 25% for OS
      memory: 384M       # Reduced footprint
    reservations:
      cpus: '0.25'
      memory: 128M
  
# Enable swap for memory spikes
sysctls:
  - vm.swappiness=10
```

### 3. Optimized Logging
```yaml
logging:
  driver: "json-file"
  options:
    max-size: "5m"      # Reduced from 10m
    max-file: "2"       # Reduced from 3
    compress: "true"    # Enable compression
```

### 4. tmpfs for Temporary Data
```yaml
tmpfs:
  - /tmp:size=32m,mode=1777
```

---

## 🐍 Python Code Optimizations

### 1. Memory-Efficient OHLCV Caching

**Problem:** Each indicator call fetches fresh OHLCV data (expensive API call + memory)

**Solution:** Implement TTL-based caching with automatic cleanup

```python
class OHLCVCache:
    """Memory-efficient OHLCV cache with TTL."""
    
    def __init__(self, ttl_seconds: int = 60):
        self._cache = {}
        self._timestamps = {}
        self.ttl = ttl_seconds
    
    def get(self, timeframe: str, limit: int) -> Optional[list]:
        key = f"{timeframe}:{limit}"
        if key in self._cache:
            if time.time() - self._timestamps[key] < self.ttl:
                return self._cache[key]
            else:
                del self._cache[key]
                del self._timestamps[key]
        return None
    
    def set(self, timeframe: str, limit: int, data: list):
        key = f"{timeframe}:{limit}"
        self._cache[key] = data
        self._timestamps[key] = time.time()
    
    def clear_expired(self):
        now = time.time()
        expired = [k for k, t in self._timestamps.items() if now - t > self.ttl]
        for k in expired:
            del self._cache[k]
            del self._timestamps[k]
```

### 2. Bounded Position History

**Problem:** `positions` deque can grow indefinitely

**Solution:** Implement automatic archival of old positions

```python
class PositionTracker:
    MAX_POSITIONS_IN_MEMORY = 1000
    
    def _archive_old_positions(self):
        """Archive old positions to reduce memory."""
        if len(self.positions) > self.MAX_POSITIONS_IN_MEMORY:
            to_archive = []
            while len(self.positions) > self.MAX_POSITIONS_IN_MEMORY * 0.8:
                to_archive.append(self.positions.popleft())
            
            # Archive to CSV
            archive_file = self.data_dir / 'position_archive.csv'
            with open(archive_file, 'a', newline='') as f:
                writer = csv.writer(f)
                for pos in to_archive:
                    writer.writerow([...])
```

### 3. Numpy Memory Optimization

**Problem:** Large numpy arrays allocated frequently

**Solution:** Pre-allocate arrays and reuse

```python
class MarketAnalyzer:
    def __init__(self, ...):
        # Pre-allocate common array sizes
        self._atr_buffer = np.zeros(50, dtype=np.float32)
        self._rsi_buffer = np.zeros(50, dtype=np.float32)
    
    def calculate_rsi_wilder(self, ...):
        # Use float32 instead of float64 (50% memory reduction)
        closes = np.array([x[4] for x in ohlcv], dtype=np.float32)
```

### 4. Connection Pooling

**Problem:** Exchange connection created fresh each cycle

**Solution:** Implement connection keep-alive with retry logic

```python
def initialize_exchange(self) -> ccxt.binanceus:
    exchange = ccxt.binanceus({
        'apiKey': self.api_key,
        'secret': self.api_secret,
        'enableRateLimit': True,
        'timeout': 30000,
        'options': {
            'adjustForTimeDifference': True,
            'recvWindow': 60000,
        },
        # Connection pooling
        'session': requests.Session(),
    })
    return exchange
```

### 5. Lazy Loading of Indicators

**Problem:** All indicators calculated every cycle even if not needed

**Solution:** Calculate only when conditions require

```python
def run(self):
    while True:
        # Only check trend filter if not already paused
        if time.time() >= self.trend_pause_until:
            if not self.check_trend_filter():
                continue
        
        # Only check ADX if volatility check passed
        # Only calculate S/R if repositioning grid
```

---

## 📊 Pi-Specific Optimizations

### 1. CPU Governor (Host-Level)
Run on the Pi host to optimize CPU for consistent performance:

```bash
# Add to /etc/rc.local or crontab
echo "ondemand" > /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor
```

### 2. Reduce SD Card Writes
Move logs to tmpfs or RAM:

```yaml
volumes:
  - type: tmpfs
    target: /app/data/logs
    tmpfs:
      size: 32m
```

### 3. Watchdog Timer
Enable hardware watchdog for automatic recovery:

```bash
# On Pi host
sudo apt install watchdog
sudo systemctl enable watchdog
```

### 4. Network Optimization
Reduce DNS lookups:

```yaml
# docker-compose.yml
dns:
  - 8.8.8.8
  - 1.1.1.1
```

---

## 🎯 Recommended Implementation Priority

### Phase 1: Quick Wins (Immediate)
1. ✅ Multi-stage Dockerfile (saves ~200MB image)
2. ✅ Memory limits in docker-compose
3. ✅ Log compression and rotation
4. ✅ tmpfs for temporary data

### Phase 2: Code Optimizations (Next)
1. OHLCV caching layer
2. Float32 numpy arrays
3. Connection session reuse
4. Position archival

### Phase 3: Advanced (Later)
1. Lazy indicator loading
2. Async operations
3. Metrics endpoint
4. Alert system

---

## 📈 Expected Improvements

After implementing Phase 1 & 2:

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Docker Image | 450MB | 180MB | **60% smaller** |
| Runtime RAM | 300MB | 160MB | **47% reduction** |
| Build Time | 10 min | 5 min | **50% faster** |
| API Calls/hour | ~120 | ~60 | **50% reduction** |
| SD Card Writes | High | Low | **80% reduction** |

---

## 🔧 Monitoring Commands

```bash
# Real-time memory usage
docker stats skizoh-gridbot --no-stream

# Check for memory leaks over time
watch -n 60 'docker stats skizoh-gridbot --no-stream'

# View container resource limits
docker inspect skizoh-gridbot | grep -A 20 "HostConfig"

# Check log size
docker exec skizoh-gridbot du -sh /app/data/

# Pi system health
vcgencmd measure_temp && free -h
```

---

## Files Updated

1. `Dockerfile` - Multi-stage build with ARM optimization
2. `docker-compose.yml` - Resource limits and tmpfs
3. `src/market_analysis.py` - OHLCV caching and float32
4. `src/grid_bot.py` - Memory-efficient position tracking
5. `.dockerignore` - Exclude unnecessary files from build

See individual optimized files in this directory.
