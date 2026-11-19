# Turn Your Old Android Phone Into a Personal Server! 📱☁️

**Don't let your old smartphone collect dust. Turn it into your own personal cloud and media server!**

Android Home Server transforms an unused Android smartphone into a personal server where you can upload files, store documents, organize photos, upload movies, and stream your videos whenever you want.

Instead of leaving your old phone unused, give it a second life as your own mini server — accessible from your laptop, tablet, or another smartphone.

**Your phone. Your files. Your own server.**

---

## What Can You Do With It?

Imagine turning your old Android phone into your own private cloud server.

<grid columns={2} gap={3}>
  <grid-item>
    <AsyncImage query="modern cloud file manager web interface file upload folders desktop" aspectRatio="5:4" width="100%"/>
    **Upload & Store Files**

    Upload documents, PDFs, assignments and other files to your own server.
  </grid-item>
  <grid-item>
    <AsyncImage query="Jellyfin media server movie library interface television" aspectRatio="5:4" width="100%"/>
    **Watch Your Movies**

    Upload your movies and videos, organize your media library and stream them using Jellyfin.
  </grid-item>
  <grid-item>
    <AsyncImage query="personal cloud storage photo gallery interface" aspectRatio="5:4" width="100%"/>
    **Manage Your Files**

    Browse, download, upload and organize your personal files through a web browser.
  </grid-item>
  <grid-item>
    <AsyncImage query="smartphone home server dashboard dark web interface" aspectRatio="5:4" width="100%"/>
    **Manage Your Server**

    Access a central dashboard to reach your server services.
  </grid-item>
</grid>

## Access Your Server From Anywhere

Choose how you want to connect to your Android server.

### 1. Local Network (Wi-Fi)

Access your server when your phone and other devices are connected to the same Wi-Fi network.

### 2. Cloudflare Tunnel

Access your server remotely through your own public domain, without traditional router port forwarding.

### 3. Tailscale VPN

Create a private network between your devices and access your server remotely without making it publicly accessible.

You can choose one method or configure multiple methods depending on your needs.

---

## How Does It Work?

Your old Android phone becomes the server host.

```text
       YOUR DEVICES
    Laptop / Tablet / Phone
              |
       Choose Access Method
       /        |        \
      LAN   Cloudflare  Tailscale
       \        |        /
              Nginx
                |
        Android Home Server
                |
        Android Smartphone
                |
       +--------+--------+
       |        |        |
    My Cloud Jellyfin Dashboard
       |        |
    Upload    Watch
    Documents Movies
    Photos    Videos
```

## What You Need

- An old Android smartphone (ARM64 recommended).
- Termux to run server tools.
- Debian Linux through PRoot.
- A Wi-Fi or internet connection.
- Storage space for your files and media.

Optional:
- Cloudflare account and domain for public access.
- Tailscale account for private remote access.
- Termux:Boot for startup automation.

## Getting Started

1. Download or clone this GitHub repository.
2. Read the installation guide.
3. Prepare Termux and Debian on your Android phone.
4. Install and configure the server components.
5. Choose your preferred access method.
6. Start uploading your files and organizing your media!

**Installation Guide:** `docs/installation-guide.md`

> This repository provides the source code, configuration examples and setup documentation. It is not yet a one-click installer. Some components require manual configuration.

## Project Components

| Component | What It Does |
|---|---|
| My Cloud | Upload, download and manage files |
| Jellyfin | Organize and stream movies and videos |
| Dashboard | Central access to server services |
| Nginx | Routes requests to the different services |
| Backend API | Provides server-related functionality |
| Server Manager | Provides server monitoring and management |
| Cloudflare Tunnel | Public remote access |
| Tailscale | Private remote access |

## Important: Your Own Personal Server

This project is designed to help you build your own server using your own Android smartphone.

Cloning this repository does not give you access to the original project's phone, files, movies, accounts or live server.

You will configure your own storage, services, credentials and network access.

For security, use strong passwords and protect administrative services. Public access should never be left unprotected.

## Project Goal

The goal is simple:

**Reuse an old smartphone and turn it into a useful personal cloud and media server.**

No need to buy a dedicated server just to start learning and experimenting with self-hosting.

Give your old phone a new purpose!

---

**Built by Nopal**

GitHub: [@mnopa2020-hash](https://github.com/mnopa2020-hash)

[View Android Home Server Repository](https://github.com/mnopa2020-hash/Android-Home-Server)
