# GulfPath Overseas

Multilingual static recruitment information and referral website at [gulfpathoverseas.online](https://gulfpathoverseas.online). Nepali is the default. The site has no application form, candidate database or required backend.

## Build and deployment

- Edit translations in `source/base.json` and `source/copy.txt`. The latter uses the column order English, Nepali, Tamil, Sinhala, Hindi. Keep pipe delimiters between columns and semicolons between entries in list rows.
- Run `python3 source/build.py` from the repository root and commit the regenerated HTML and sitemap with the source. Preview using `sh source/package.sh` and `python3 -m http.server 8134 --directory public`.
- GitHub Actions packages the same files and publishes them to GitHub Pages from `main`. The existing Cloudflare workflow uses the same package when its credentials are configured. Keep `CNAME` and any existing `google*.html` files. If Google verification uses a new meta tag, add the real owner-provided tag to the shared head in `source/build.py`.
- Verify redirects for old `?lang=` links, the custom 404 and HTTP status, all language paths, `sitemap.xml`, and the promotional video after publishing.
- Roll back by reverting the upgrade commit, pushing the revert to `main` and checking the next Pages deployment.

## Verified content

- `source/settings.json` controls the contact number, privacy review date, contact hours and vacancies. Leave unknown or undocumented items unpublished.
- A vacancy has a `status` of `confirmed`, `pending`, `closed` or `information` and five `translations` entries. Each translation supplies `title`, `destination` and `category`. A confirmed record also requires public `employer` and `agency` names, `verified_on` (YYYY-MM-DD), and localized `eligibility`. Only mark a vacancy confirmed after checking current written details, authorization to advertise, and the agency's current licence.
- Under each confirmed vacancy's localized `terms`, publish verified `pay` (with currency and pay period), `accommodation`, `meals`, `transport`, `medical`, `hours`, `overtime`, `duration` and `leave`. Omitted terms display a contract verification message. Close expired posts promptly. Add JobPosting markup only after confirming Google's current eligibility requirements for dedicated vacancy pages.
- `hours` accepts per-language objects with `schedule` (including working days), `timezone`, `response` and `out_of_hours`. Seed with confirmed public information only.
- Before advertising, review agency authorization, local advertisement approvals and Meta's employment ad category. Verify the landing page and the creative together. The archived video retains older Gulf Cleaner Company branding and is contextualized on the site.
- Have native speakers review the translations, especially agency, privacy and contract language. Confirm enquiry retention, referral data-sharing procedures and the policy date with the owner or legal reviewer before changing the policy.
- In Google Search Console, select the verified `gulfpathoverseas.online` property, open Sitemaps, submit `sitemap.xml`, and inspect the canonical Nepali page and representative language pages. Account access and indexing status must be confirmed in Search Console.
