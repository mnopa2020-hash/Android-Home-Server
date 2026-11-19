# Cloudflare Tunnel Setup Guide

## Overview
Cloudflare Tunnel provides remote access to the Android Home Server without requiring direct port forwarding.

## Configuration
- Service: cloudflared
- Tunnel name: android-home-server
- Domain: nopalngadimanserver.dpdns.org

## Authentication
The tunnel uses a private authentication token.

The token is stored separately from this repository:
- Termux: ~/.cloudflare-tunnel-token
- Debian: /root/.cloudflare-tunnel-token

## Access
The public domain routes traffic to the home server through Cloudflare Tunnel and Nginx.

## Security
- Never upload the tunnel token.
- Never commit credentials or private configuration files.
- Keep the token file outside the Git repository.
