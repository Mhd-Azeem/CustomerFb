# Gulf Cleaner Company Oman — website

Source for the existing website at https://gulf-job-vacancies.pages.dev

- `index.html` — HTML, CSS, language switching, WhatsApp contact
- `logo.webp` — small company header logo
- `poster.jpg` — small video preview image
- `oman-video.mp4` — 30-second landscape video

## One-time setup

1. In **Actions**, run **Import existing website media** once. It downloads the three media assets from the live Pages site and commits them to this repository. Check the files appeared.
2. In the Cloudflare dashboard, under **My Profile → API Tokens**, create a token scoped to your account with **Cloudflare Pages: Edit** permission. Copy the Cloudflare Account ID from your dashboard.
3. In this GitHub repository go to **Settings → Secrets and variables → Actions → New repository secret**. Set **CLOUDFLARE_API_TOKEN** and **CLOUDFLARE_ACCOUNT_ID**. Never commit the values or send tokens in chat.
4. In **Actions**, run **Deploy website to existing Cloudflare Pages** once and check the production URL. Its project name must be exactly `gulf-job-vacancies`.

After setup, changes committed to `main` to the website files automatically deploy via GitHub Actions to the **existing** Cloudflare Pages project, without converting it to native Git integration or deleting the Pages project.

### Notes
- During initial setup, a deploy can fail if media or GitHub secrets are missing. This does **not** replace the existing live deployment.
- Cloudflare Pages Direct Upload projects cannot switch directly to native Git integration; this approach uses GitHub Actions with Wrangler and retains the project.
- The site is an overseas work referral landing page. Make sure agency authorization, recruitment advertising approvals, accurate salary/benefits, and a truthful privacy notice are in place before using it for advertisements.
- Always inspect changes to the website before committing them to `main`. Updates made by direct ZIP upload to Cloudflare will **not** sync back to GitHub.
