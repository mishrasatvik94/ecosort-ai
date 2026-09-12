# Deployment Guide: EcoSort AI

EcoSort AI has been completely upgraded into a modern Next.js Web Application to support instant public deployment.

## Option A: Vercel (Recommended & Easiest)
Vercel is the creator of Next.js and provides zero-configuration deployments.

### Prerequisites
1. A GitHub account
2. A free Vercel account (vercel.com)

### Steps
1. **Push your code to GitHub** (See GitHub instructions below).
2. **Log into Vercel** and click **"Add New Project"**.
3. **Import your GitHub repository**.
4. Set the **Framework Preset** to `Next.js`.
5. Set the **Root Directory** to `web` (since the Next.js app is inside the `web/` folder).
6. **Environment Variables**:
   - Add `OPENAI_API_KEY` and paste your secret key. *(If you leave this blank, the app will automatically use the built-in deterministic fallback generator, which is perfectly safe for a demo).*
7. Click **Deploy**. Vercel will automatically build the app and give you a public URL (e.g., `https://ecosort-ai.vercel.app`).

---

## Option B: Firebase Hosting
Firebase is a Google platform. Next.js can be deployed to Firebase via Firebase App Hosting or Cloud Functions.

### Prerequisites
1. A Firebase project created at [console.firebase.google.com](https://console.firebase.google.com).
2. The Firebase CLI installed (`npm install -g firebase-tools`).

### Steps
1. Open a terminal and run `firebase login`.
2. Run `firebase experiments:enable webframeworks`.
3. Navigate into the web directory: `cd web`.
4. Run `firebase init hosting`.
   - Select your Firebase project.
   - When asked "Do you want to use a web framework? (experimental)", say **Yes**.
   - When asked about the framework, select **Next.js**.
   - Set the public directory (usually left as default).
5. **Environment Variables**:
   - Do NOT put your API key in client code. Firebase App Hosting handles secrets via Google Cloud Secret Manager. You will be prompted to manage these during deployment, or you can set them in the Firebase Console.
6. Run `firebase deploy`.

---

## GitHub Push Instructions

If you haven't initialized Git yet, run these exact commands from the **root** of the project (`C:\Users\mishr\OneDrive\Desktop\Ecosort-AI`):

```bash
git init
git add .
git commit -m "Upgrade to Next.js Web App for final submission"
```

Then, go to [github.com/new](https://github.com/new), create a new blank repository called `ecosort-ai`, and copy the two lines they give you to push an existing repository. It will look like this:

```bash
git remote add origin https://github.com/yourusername/ecosort-ai.git
git branch -M main
git push -u origin main
```
