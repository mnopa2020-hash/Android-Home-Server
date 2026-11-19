# System Architecture

This Android Home Server uses Termux and Debian PRoot.

## Services

- Nginx: Port 8080
- My Cloud: Port 8081
- Jellyfin: Port 8096
- API: Port 8000
- Manager: Port 8001

## Remote Access

Cloudflare Named Tunnel provides remote access.

## Startup

Termux:Boot starts the server services after phone reboot.
