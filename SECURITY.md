# Security

Wave Simulator Remastered is a static page. It has no server, no accounts, no
dependencies and no build step, so there is little to attack. The measures
below keep it that way.

## What changed from the original

### Supply chain: removed entirely

- The original ran on **Angular 13**, which no longer gets security updates,
  and only built on **Node 16**, which is also end-of-life.
- Moving to Angular 22 during development still left **3 moderate
  `npm audit` advisories**, plus packages that run install scripts during
  `npm install`.
- This version has **no npm, no `node_modules` and no third-party code**. Every
  file in the repository is served as-is, so nothing can be swapped in through
  a dependency.
- The original registered a **service worker** that stayed installed in the
  browser. This version does not use one.

### In the page

- **Content Security Policy.** Scripts, styles and fonts can load only from
  the app's own folder, and images only from embedded data. Every network
  request (`fetch`, remote images, and so on) is blocked.
- **No third-party requests.** Fonts, icons and images ship with the page, so
  opening it does not send the visitor's IP address anywhere.
- **Shared links are treated as untrusted.** A `#s=` link is size-limited,
  parsed as JSON, and rebuilt field by field. Unknown fields are dropped.
  Every number is clamped to a range the GPU can handle, so a crafted link
  cannot freeze the tab with huge values. Images in a link must be bundled
  assets, so a link cannot make the recipient's browser request an outside
  URL.
- **Saved settings** from `localStorage` go through the same checks.
- **Uploads** must be real PNG, JPEG, GIF, WebP or BMP images: at most 15 MB
  and 8192 px on a side, and they must decode successfully. SVG is rejected.
- **No HTML injection.** User-supplied text, such as file names, is only ever
  set with `textContent`. The code never uses `innerHTML` or `eval`.
- **External links** open with `rel="noopener noreferrer"`, and the page sends
  no referrer.
- **Bundled images carry no metadata.** Text, EXIF and date chunks were
  stripped from every PNG.

## Reporting a problem

If you find a security issue, please
[open an issue](https://github.com/Aviressence/Wave-Simulator-Remastered/issues)
describing it. Don't include working exploit code in a public issue; describe
the problem and we will follow up.
