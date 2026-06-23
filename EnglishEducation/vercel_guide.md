# Developer Guide: Hosting and Managing Your Website on Vercel

This guide explains how to use **Vercel** to host your static English education website for free, connect it to your GitHub repository, and configure custom domains.

---

## Table of Contents
1. [Overview of Vercel](#1-overview-of-vercel)
2. [Step-by-Step: Hosting Your Site on Vercel (Free & Automated)](#2-step-by-step-hosting-your-site-on-vercel-free--automated)
3. [Step-by-Step: Pointing a Custom Domain to Vercel](#3-step-by-step-pointing-a-custom-domain-to-vercel)
4. [Essential Vercel Features to Know](#4-essential-vercel-features-to-know)
5. [Troubleshooting & Best Practices](#5-troubleshooting--best-practices)

---

## 1. Overview of Vercel

Vercel is a cloud platform built specifically for frontend developers. It is the creator and maintainer of Next.js but supports any static HTML/JS site or frontend framework (React, Vue, Astro, Vite, etc.). 

Key features include:
*   **Git-integrated CI/CD:** Every time you push changes to GitHub, Vercel automatically builds and deploys your updates.
*   **Preview Deployments:** Whenever you make a branch or Pull Request, Vercel builds a temporary "preview" site so you can test changes before they go live.
*   **Global Edge Network:** Your website is cached at the edge, ensuring lightning-fast load times for international learners.

---

## 2. Step-by-Step: Hosting Your Site on Vercel (Free & Automated)

Vercel's hobby tier is completely free and includes automatic SSL, DDoS protection, and global CDN.

### Step 2.1: Prepare Your Code on GitHub
1. Create a repository on [GitHub](https://github.com) (e.g., `english-education`).
2. Add your website files (`index.html`, CSS, JS, etc.) and push them to your repository's `main` branch.

### Step 2.2: Sign Up & Connect to GitHub
1. Go to [Vercel](https://vercel.com/) and click **Sign Up**.
2. Select **Hobby** (Free tier) and sign up using your **GitHub** account.
3. Once logged in, you will be taken to your dashboard.

### Step 2.3: Import Your Project
1. From your Vercel Dashboard, click **Add New...** -> **Project**.
2. Under "Import Git Repository", find your `english-education` repository and click **Import**.
   *(If you don't see it, click "Adjust GitHub App Permissions" to give Vercel permission to read that repository).*

### Step 2.4: Configure Build Settings & Deploy
1. Vercel will automatically analyze your code and suggest configuration settings:
   * **Framework Preset:** Vercel automatically detects if you are using Next.js, Vite, Astro, or standard HTML. If it is a simple static site, it will select **Other**.
   * **Root Directory:** Keep this as `./` unless your website lives in a subfolder.
   * **Build and Output Settings:** Vercel pre-configures these for you. For plain static HTML, leave these untouched.
   * **Environment Variables:** If you have secret API keys, you can add them here.
2. Click **Deploy**.
3. In a few seconds, you will see a preview of your website and receive two default domains ending in `.vercel.app` (e.g., `english-education.vercel.app`).

---

## 3. Step-by-Step: Pointing a Custom Domain to Vercel

If you own a custom domain (e.g., `learnenglish.com`) and want to use it with your Vercel site:

### Step 3.1: Add Your Domain in Vercel
1. Go to your project dashboard on Vercel.
2. Click on the **Settings** tab at the top.
3. Click on **Domains** in the left-hand sidebar.
4. Enter your custom domain (e.g., `learnenglish.com`) and click **Add**.
5. Select whether you want to redirect the raw domain to the `www` version or vice versa (e.g., redirect `learnenglish.com` to `www.learnenglish.com`), then click **Add**.

### Step 3.2: Configure DNS Records
Vercel will show that your domain is "Invalid" and provide the DNS records you need to add at your domain registrar (e.g., GoDaddy, Namecheap, Porkbun):

#### **Case A: For the Root Domain (e.g., `learnenglish.com`)**
Go to your registrar's DNS settings and add an **A record**:
*   **Type:** `A`
*   **Name (Host):** `@` (or leave blank depending on the registrar)
*   **Value (Points to):** `76.76.21.21` (This is Vercel's global IP address)
*   **TTL:** Automatic / Default

#### **Case B: For a Subdomain (e.g., `www.learnenglish.com` or `lessons.learnenglish.com`)**
Add a **CNAME record**:
*   **Type:** `CNAME`
*   **Name (Host):** `www` (or `lessons`)
*   **Value (Points to):** `cname.vercel-dns.com`
*   **TTL:** Automatic / Default

### Step 3.3: Verification
1. Once you save the DNS records at your registrar, go back to Vercel's **Settings** -> **Domains** page.
2. Click **Refresh**.
3. Once Vercel detects the DNS records, it will automatically generate a free SSL certificate (Let's Encrypt) for your site. Your custom domain is now live!

---

## 4. Essential Vercel Features to Know

### Preview Deployments
Every time you push to a branch that is *not* `main`, Vercel creates a separate URL just for that branch. This is perfect for trying out a new lesson format or feature without breaking the live website.

### Serverless Functions
If your static site needs a backend action later on (e.g., checking user quiz scores, sending an email, or calling an AI API), you can create an `api` directory in your project root. Vercel automatically deploy files in this directory as Node.js, Python, or Go serverless endpoints.

### Speed Insights & Analytics
Vercel offers built-in, privacy-focused web analytics. You can enable them directly from your project's dashboard to see how many people are visiting your English website, which lessons are most popular, and how fast pages load.

---

## 5. Troubleshooting & Best Practices

> [!NOTE]
> **Production vs. Preview:** Always remember that pushing to your main branch updates your live site immediately. Work in a separate branch (like `draft-lessons`) if you want to experiment before updating.

*   **Build Failures:** If your deployment fails, check the **Deployments** tab on Vercel and look at the build log. It will show you exactly what file or script caused the build error.
*   **Ignoring Files:** If you have files in your GitHub repository that you don't want Vercel to host (like design mockups or local scripts), create a `.vercelignore` file in your root folder and list them there.
