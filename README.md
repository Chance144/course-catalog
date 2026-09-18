# WSU Carson College Course Catalog

Unofficial, advising-oriented mirror of **International Business (I_BUS)** and **Marketing (MKTG)** listings for **Spring, Summer, and Fall 2026**. Live site: [https://catalog.drandrewperkins.com](https://catalog.drandrewperkins.com).

Course titles, credits, prerequisites, [M] flags, cross-listings, and descriptions are parsed from the Word catalog export in `source/catalog-2026.docx`. Wording is not rewritten.

## Local preview

```bash
python3 scripts/parse_catalog.py
python3 scripts/write_pages.py
python3 scripts/test_catalog.py
python3 -m http.server 8787 --directory site
```

Then open [http://127.0.0.1:8787](http://127.0.0.1:8787).

## Cloudflare Pages

This is a static site. There is **no build command**.

| Setting | Value |
| --- | --- |
| Suggested Pages project name | `course-catalog` |
| Production branch | `main` |
| Build command | *(leave empty)* |
| Publish directory | `site` |
| Root directory | `/` (repository root) |

### Connect the GitHub repo

1. In Cloudflare, go to **Workers & Pages → Create → Pages → Connect to Git**.
2. Select [`Chance144/course-catalog`](https://github.com/Chance144/course-catalog).
3. Set the production branch to `main`.
4. Leave the build command empty.
5. Set the **publish directory** to `site`.
6. Save and deploy. The first preview URL will look like `https://course-catalog.pages.dev`.

Direct upload (without Git) also works:

```bash
npx wrangler pages deploy site --project-name=course-catalog
```

`wrangler.jsonc` already points `pages_build_output_dir` at `site`.

### Custom domain `catalog.drandrewperkins.com`

1. Open the Pages project → **Custom domains** → **Set up a domain**.
2. Add `catalog.drandrewperkins.com`.
3. If the zone `drandrewperkins.com` is already on Cloudflare, accept the suggested CNAME (`catalog` → `course-catalog.pages.dev`, proxied).
4. If DNS is elsewhere, create a CNAME for `catalog` to `course-catalog.pages.dev` and finish SSL in the Pages UI.
5. After the certificate is active, confirm https://catalog.drandrewperkins.com serves this site.

Regenerating JSON after a new Word export:

```bash
cp /path/to/export.docx source/catalog-2026.docx
python3 scripts/parse_catalog.py
python3 scripts/test_catalog.py
```

## Contents

- `site/` — published HTML, CSS, JS, and `assets/courses.json`
- `source/catalog-2026.docx` — catalog export used as the source of truth
- `scripts/parse_catalog.py` — extracts course records from the docx
- `scripts/write_pages.py` — shared home / I_BUS / MKTG page template
