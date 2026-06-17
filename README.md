# s8sskills.com

Marketing site for **s8s skills** — an open catalog of *serverless* skills for AI
coding agents. Install a provider's skill pack into your project with one command:

```sh
npx skills add s8sskills/gcp
```

Each cloud lives in its own repo under [github.com/s8sskills](https://github.com/s8sskills)
(`gcp`, `aws`, `vercel`, `netlify`, `cloudflare`, `azure`, …) and is installed by its
`s8sskills/<vendor>` path. This repo is just the website.

> **s8s** = **s**erverles**s** — the `s`, 8 letters, and a final `s` (à la `k8s`).

## Develop

Requires [Hugo extended](https://gohugo.io/) (≥ 0.163).

```sh
hugo server        # http://localhost:1313
hugo --minify      # production build into ./public
```

The landing page is a single template (`layouts/index.html`) driven entirely by
`[params]` in `hugo.toml` — edit copy, the install command, the step list, and the
provider grid there. No content files needed.

## Brand assets

The logo is the *hachidori* (hummingbird) carrying a faceted **skill medallion**.
Everything in `static/` (logo, favicons, social card) is generated — don't hand-edit
the PNGs. To regenerate after changing the source art or the badge:

```sh
python3 tools/make_badge.py   # assets/brand/badge.svg  (the medallion, vector)
python3 tools/make_logo.py    # static/logo.png + favicon/app-icon set
python3 tools/make_og.py      # static/og-image.png     (1200x630 social card)
```

Requires Python with Pillow and `rsvg-convert` on PATH (`brew install librsvg`).

| File | What |
| --- | --- |
| `assets/brand/hachidori-1.png` | Source hummingbird art (4167², transparent) |
| `tools/make_badge.py` | Generates the skill-medallion SVG from the shared palette |
| `tools/make_logo.py` | Composites bird + medallion, emits favicons/app icons |
| `tools/og.svg` / `tools/make_og.py` | Social card (mark embedded as data URI) |

## Deploy

Pushes to `main` build and publish to GitHub Pages via
`.github/workflows/deploy.yml`. The custom domain `s8sskills.com` is set through
`static/CNAME`.
