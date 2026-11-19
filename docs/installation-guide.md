# Android Home Server — Installation Guide

This guide explains how to prepare an Android smartphone to run the
Android Home Server project using Termux and Debian PRoot.

> **Important:** This repository contains source code and documentation.
> It is not currently a one-click installer. Some components require
> manual installation and configuration. Follow the component guides
> and adjust settings for your own device.

## 1. Requirements

### Hardware
- Android smartphone with an ARM64 processor.
- Sufficient free storage for applications and personal files.
- Stable Wi-Fi or mobile internet connection.
- A charger is recommended for longer server sessions.

### Software
- Termux.
- Debian PRoot (installed through `proot-distro`).
- Termux:Boot (optional, for startup automation).
- A Cloudflare account and domain (optional, for public access).

Android may stop background applications to save battery. Continuous
24/7 operation is therefore not guaranteed.

## 2. Install Termux and required tools

Install Termux from a trusted source, such as the official Termux
GitHub project or F-Droid. Open Termux and run:

```bash
pkg update && pkg upgrade -y
pkg install git proot-distro tmux curl wget nano -y
```

## 3. Download this project

In Termux, run:

```bash
git clone https://github.com/mnopa2020-hash/Android-Home-Server.git
cd Android-Home-Server
```

You can inspect the project files with:

```bash
ls
```

## 4. Install Debian PRoot

In Termux, run:

```bash
proot-distro install debian
proot-distro login debian
```

Inside Debian, update the package list and install basic tools:

```bash
apt update && apt upgrade -y
apt install git curl wget nano python3 python3-pip nginx -y
```

**Shell reminder:** Commands beginning with `pkg` are for Termux.
Commands beginning with `apt` are for the Debian environment.

## 5. Set up the server components

The repository has separate files and guides for its components:

| Component | Project location |
|---|---|
| Dashboard | `dashboard/` |
| Nginx reverse proxy | `nginx/default.conf` |
| My Cloud | `my-cloud/setup-guide.md` |
| Jellyfin | `jellyfin/setup-guide.md` |
| Cloudflare Tunnel | `cloudflare/setup-guide.md` |
| Backend API and Manager | `backend/` |
| Startup and control scripts | `scripts/` |

Read the relevant guide before configuring each service. The project
configuration may need changes to match your own paths, ports, Android
permissions and installed software.

### My Cloud (optional)

My Cloud provides browser-based file management, including uploading,
downloading and browsing files. Follow `my-cloud/setup-guide.md`.

Choose a storage folder on your own phone and make sure Termux has the
required Android storage permission.

### Jellyfin (optional)

Jellyfin can organize and stream your personal video and media library.
Follow `jellyfin/setup-guide.md` and configure your own media folders.

### Backend API and Manager

The Python source code is in `backend/`. Review
`backend/requirements.txt` and the source files before running them.
Install dependencies in an appropriate Python environment, such as a
virtual environment, and configure the manager's authentication token
separately. Never publish that token.

### Nginx

Nginx routes requests to the services configured on your device.
Review `nginx/default.conf` and check that the upstream addresses,
ports and paths match your actual services.

Before reloading Nginx, test its configuration:

```bash
nginx -t
```

Only restart or reload Nginx after the test succeeds.

## 6. Choose how to access your server

You can use either access method. Cloudflare is optional.

### Option A — Local network

1. Connect your phone and the device you are using to the same Wi-Fi.
2. Find your phone's current local IP address.
3. Make sure the server and Nginx are running.
4. Open the configured Nginx address in a browser.

Example:

```text
http://PHONE_LOCAL_IP:8080
```

Replace `PHONE_LOCAL_IP` with your phone's actual local IP address.
The address may change when your phone reconnects to the network.

### Option B — Public internet (optional)

Cloudflare Tunnel can make your server reachable from outside your
home network without traditional router port forwarding.

Follow `cloudflare/setup-guide.md`. Create your own Cloudflare account,
tunnel and DNS configuration. Use your own domain and tunnel token;
do not copy another person's credentials.

Public access should be protected with strong service passwords and
appropriate access controls. Do not expose administration interfaces
unless you understand and have secured them.

## 7. Automatic startup (optional)

Termux:Boot can run a startup script when Android boots.

1. Install Termux:Boot from the same trusted source as Termux.
2. Open Termux:Boot once.
3. Review the scripts in `scripts/`.
4. Configure a startup script under `~/.termux/boot/` and adjust its
   paths and commands for your own installation.

Android battery settings and background-process restrictions can affect
automatic startup and long-running services.

## 8. Security checklist

- Never commit Cloudflare tunnel tokens, passwords or admin tokens.
- Keep private databases, logs and personal media out of GitHub.
- Use strong, unique passwords for hosted services.
- Protect administrative endpoints.
- Consider Cloudflare Access for an additional layer of protection.
- Check `.gitignore` before committing changes.

## 9. Troubleshooting

If a service does not work:

1. Check whether the service process is running.
2. Confirm that the expected port is listening.
3. Check the service logs for errors.
4. Test the Nginx configuration with `nginx -t`.
5. Check that Android has not stopped Termux in the background.

See `docs/troubleshooting.md` for project troubleshooting notes.

## 10. What a GitHub copy provides

Cloning or downloading this repository gives you the project source
code, configuration examples and documentation. It does **not** give
you access to the original owner's phone, live server, personal files,
media, passwords or Cloudflare account.

Each user must install and configure their own server.
