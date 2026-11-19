# Troubleshooting Guide

## Server Not Running
Check active tmux sessions using:
```bash
tmux ls
```

## Restart Home Server
```bash
bash ~/.termux/boot/start-home-server.sh
```

## Jellyfin Connection Problem
Check port 8096:
```bash
proot-distro login debian -- curl -I http://127.0.0.1:8096
```

## My Cloud Connection Problem
Check port 8081:
```bash
proot-distro login debian -- curl -I http://127.0.0.1:8081
```

## Cloudflare Tunnel Problem
Check tunnel session:
```bash
tmux has-session -t named-cloud
```

## Android Background Restrictions
Android may terminate background processes. Enable background activity and use termux-wake-lock.
