# StackAdapt Universal Pixel GTM Web Tag

**A sandboxed Google Tag Manager template for the StackAdapt Universal Pixel: retargeting page views and conversion tracking, without Custom HTML.**

[![Created by Freek Kampen](https://img.shields.io/badge/Created%20by-Freek%20Kampen-455CE9)](https://freekkampen.com) [![Maintained by New North Digital](https://img.shields.io/badge/Maintained%20by-New%20North%20Digital-455CE9)](https://newnorth.nl/?utm_source=github&utm_medium=gtm-template&utm_campaign=stackadapt-web-tag)

## Features

- Page-view (`saq('ts', id)`) and conversion (`saq('conv', id, data)`) modes from a single tag.
- Builds the native `saq` command queue and loads `events.js` once per page.
- Conversion mode sends optional revenue, order ID and currency.
- Custom-parameter table for extra keys such as `action`, `product_id` or `product_category`.
- Debug logging gated behind a checkbox; nothing sensitive is logged.

## Why this instead of Custom HTML?

StackAdapt's only published GTM artifact is a server-side template. For web containers the alternative is a Custom HTML tag. This sandboxed template runs without the `Custom HTML` permission, validates its inputs, scopes script-injection to `tags.srv.stackadapt.com`, and integrates with GTM Consent Mode.

## Installation

### From the Community Template Gallery
1. In a GTM web container, open **Templates → Tag Templates → Search Gallery**.
2. Search for **StackAdapt Conversion Tracking by New North Digital** and add it.
3. Create a new tag from the template.

### Manual installation
1. Download `template.tpl` from this repo.
2. In GTM: **Templates → New → ⋮ → Import**, select the file, and save.

## Setup guide

1. **Page view** — create a tag, set Event type to **Page view**, enter your **Universal Pixel ID** (the 22-character ID, e.g. `PEpR18E5FJGoHB24wvWU6A`, or a GTM variable), and fire it on **All Pages**. This drives retargeting and lookalike audiences.
2. **Conversion** — create a second tag, set Event type to **Conversion**, enter the **Conversion Event Unique ID** as the Pixel ID, reference your transaction value in **Revenue**, and fire it on your conversion trigger.
3. **Consent** — gate the tags with GTM's tag-level consent settings (require `ad_storage` and `ad_user_data`, plus `ad_personalization` for audience use). StackAdapt has no consent command of its own.

> Before publishing, confirm the live base snippet from your StackAdapt pixel's Installation screen matches the host and command names used here.

---

Created and maintained by [Freek Kampen](https://freekkampen.com) at [New North Digital](https://newnorth.nl/?utm_source=github&utm_medium=gtm-template&utm_campaign=stackadapt-web-tag).
