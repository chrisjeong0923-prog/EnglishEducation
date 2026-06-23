# Developer Guide: Hosting and Managing Your Website on Cloudflare

This guide explains how to use **Cloudflare** to host your static English education website for free using **Cloudflare Pages**, and how to configure Cloudflare's CDN and security services.

---

## Table of Contents
1. [Overview of Cloudflare Services](#1-overview-of-cloudflare-services)
2. [Step-by-Step: Hosting Your Site on Cloudflare Pages (Free & Recommended)](#2-step-by-step-hosting-your-site-on-cloudflare-pages-free--recommended)
3. [Step-by-Step: Pointing a Custom Domain to Cloudflare](#3-step-by-step-pointing-a-custom-domain-to-cloudflare)
4. [Essential Cloudflare Settings to Enable](#4-essential-cloudflare-settings-to-enable)
5. [Troubleshooting & Best Practices](#5-troubleshooting--best-practices)

---

## 1. Overview of Cloudflare Services

For a static educational website, Cloudflare provides two major benefits:
1. **Cloudflare Pages:** A fast, secure hosting platform that connects to GitHub and publishes your website automatically whenever you update your code.
2. **Cloudflare CDN & DNS:** A security and performance proxy layer that sits in front of your domain to protect it from attacks, provide free SSL (HTTPS), and speed up loading times around the world.

---

## 2. Step-by-Step: Hosting Your Site on Cloudflare Pages (Free & Recommended)

If you have a static site, you don't need external hosting. You can host it directly on Cloudflare for free.

### Step 2.1: Prepare Your Code on GitHub
1. Create a free account at [GitHub](https://github.com).
2. Create a new repository (e.g., `english-education`).
3. Push your website files (like `index.html`, `style.css`, and images) to your GitHub repository.

### Step 2.2: Link GitHub to Cloudflare
1. Sign up/Log in to the [Cloudflare Dashboard](https://dash.cloudflare.com/).
2. On the left sidebar, click on **Workers & Pages**.
3. Click the **Create** button, then select the **Pages** tab.
4. Click **Connect to Git**.
5. Log in with your GitHub account and authorize Cloudflare to read your repositories (you can select access to "All repositories" or just your `english-education` repository).

### Step 2.3: Configure and Deploy
1. Select your repository and click **Begin setup**.
2. Configure your build settings:
   * **Project name:** This determines your default URL (e.g., `english-lessons.pages.dev`).
   * **Production branch:** Usually `main` or `master`.
   * **Framework preset:** 
     * If using plain HTML/CSS/JS, choose **None**.
     * If using tools like Vite, Astro, or React, select the matching preset.
   * **Build command & Output directory:** 
     * For plain HTML, leave these blank (output directory defaults to the root `.`).
     * For Astro or Vite, Cloudflare will pre-fill these automatically (e.g., build command: `npm run build`, output directory: `dist`).
3. Click **Save and Deploy**.
4. Cloudflare will build and deploy your site. Once complete, you will receive a unique link (e.g., `https://project-name.pages.dev`).

> [!TIP]
> Every time you update your code and push it to GitHub, Cloudflare Pages will automatically rebuild and update your live website in seconds.

---

## 3. Step-by-Step: Pointing a Custom Domain to Cloudflare

If you buy a custom domain (e.g., `learnenglish.com`) and want to use Cloudflare's security, performance benefits, and free SSL:

### Step 3.1: Add Your Domain to Cloudflare
1. In your Cloudflare Dashboard, click **Add a site** (or **Websites** -> **Add a site**).
2. Enter your domain name (e.g., `learnenglish.com`) and click **Continue**.
3. Choose the **Free Plan** ($0/month) and click **Continue**.

### Step 3.2: Update Your Nameservers
1. Cloudflare will scan your existing DNS records and then display two **Cloudflare Nameservers** (e.g., `dina.ns.cloudflare.com` and `oliver.ns.cloudflare.com`).
2. Log in to the registrar where you bought your domain (e.g., Namecheap, GoDaddy, Porkbun).
3. Find the **DNS Settings** or **Nameservers** section for your domain.
4. Change the nameservers from "Default" or "Custom" to the two nameservers Cloudflare provided.
5. Save your changes. 
   *(Note: Nameserver changes can take anywhere from 5 minutes to 24 hours to update globally, though it usually takes under an hour).*

### Step 3.3: Configure DNS in Cloudflare
1. Go back to Cloudflare and click **Check nameservers**.
2. Once active, go to the **DNS** -> **Records** section in Cloudflare.
3. To point your custom domain to your **Cloudflare Pages** site:
   * Click **Add record**.
   * Select Type: `CNAME`.
   * Name: `@` (represents your main domain, e.g., `learnenglish.com`).
   * Target: `your-project.pages.dev` (your Pages URL).
   * Proxy status: **Proxied (Orange Cloud)**.
   * Click **Save**.
4. Add a second record for `www`:
   * Type: `CNAME`.
   * Name: `www`.
   * Target: `your-project.pages.dev`.
   * Proxy status: **Proxied (Orange Cloud)**.
   * Click **Save**.

---

## 4. Essential Cloudflare Settings to Enable

To get the best performance and security, make sure the following features are enabled in the Cloudflare Dashboard:

### SSL/TLS Encryption
* Go to **SSL/TLS** -> **Overview**.
* Set encryption mode to **Full** or **Flexible** to ensure all traffic to your website is encrypted with HTTPS.
* Go to **SSL/TLS** -> **Edge Certificates** and turn on **Always Use HTTPS**. This redirects all insecure `http://` visits to secure `https://` visits automatically.

### Speed Optimization (Caching & Auto Minify)
* Go to **Speed** -> **Optimization** -> **Content Optimization**.
* **Auto Minify:** Check the boxes for **JavaScript**, **CSS**, and **HTML**. This shrinks your file sizes by removing unnecessary spaces, making your lessons load faster.
* **Brotli:** Ensure Brotli compression is turned **On** to compress data sent to browsers.

### Development Mode (When Making Changes)
* If you make direct changes to your server and they aren't appearing due to Cloudflare caching, go to **Caching** -> **Configuration** and toggle **Development Mode** on. This temporarily bypasses Cloudflare’s cache so you can see changes instantly.

---

## 5. Troubleshooting & Best Practices

> [!WARNING]
> **DNS Propagation Delay:** When you first update nameservers, your site might look down or display SSL errors. This is normal; wait up to 2 hours for the new DNS settings to spread across the internet.

*   **Clearing Cache:** If you updated an image or text file on your site but still see the old version, go to **Caching** -> **Configuration** -> **Purge Everything**. This forces Cloudflare to fetch the newest copy of your site.
*   **SSL Handshake Failed (Error 525):** This usually happens if your origin server doesn't support SSL or has an invalid certificate. If using Cloudflare Pages, this will not happen since Cloudflare handles the SSL certificate automatically.
