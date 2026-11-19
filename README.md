# Android Home Server

A self-hosted home server running on an Android smartphone using Termux and Debian PRoot.

## Project Overview

This project turns an Android smartphone into a multifunctional home server.

It provides personal cloud storage, media streaming, web dashboard and remote access.

## Features

- **Web Dashboard** – Central page to access server services.
- **My Cloud** – Personal file storage and file management using File Browser Next.
- **Jellyfin** – Self-hosted media streaming for movies, TV shows and music.
- **Nginx** – Reverse proxy connecting the different services.
- **Cloudflare Tunnel** – Remote access through a custom domain without port forwarding.
- **FastAPI Manager** – Server management API and dashboard integration.
- **Termux:Boot** – Automatic startup scripts after phone reboot.

## Architecture

```text
Android Smartphone
|
+-- Termux
|   |
|   +-- Debian PRoot
|   |   |
|   |   +-- Nginx :8080
|   |   +-- My Cloud :8081
|   |   +-- Jellyfin :8096
|   |   +-- API :8000
|   |   +-- Manager :8001
|   |
|   +-- Cloudflare Tunnel
|   +-- Termux:Boot
|
+-- Remote Access
    |
    +-- Cloudflare
        |
        +-- Web Dashboard
        +-- My Cloud
        +-- Jellyfin




Android-Home-Server/
├── README.md
├── .gitignore
├── docs/
├── scripts/
├── dashboard/
├── nginx/
├── cloudflare/
├── jellyfin/
└── my-cloud/




Kemudian semak:

```bash
cat README.md
//


cat > docs/architecture.md <<'EOF'
# System Architecture

## Overview

The Android Home Server uses an Android smartphone as the main host machine.

Termux provides the Linux-like environment, while Debian PRoot runs the server applications.

## Services

| Service | Port | Purpose |
|---|---:|---|
| Nginx | 8080 | Main web entry point |
| My Cloud | 8081 | Personal file storage |
| Jellyfin | 8096 | Media streaming |
| API | 8000 | Backend API |
| Manager | 8001 | Server management |

## Request Flow

Users access the server through the Cloudflare Tunnel.

Cloudflare forwards requests to the local Nginx server on port 8080.

Nginx routes requests to the appropriate application based on URL paths.

- `/` - Dashboard
- `/cloud/` - My Cloud
- `/jellyfin/` - Jellyfin
- `/api/` - API
- `/manager/` - Manager

## Host Environment

- Android smartphone
- Termux
- Debian PRoot
- Termux:Boot

## Remote Access

Cloudflare Named Tunnel provides remote access without opening inbound router ports.

## Notes

Service availability depends on Android background process restrictions, network connectivity and device power.
