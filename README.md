# Jimmy's Landscaping (Pty) LTD — website

A plain static website. No build step, no dependencies. Open `index.html` in a browser
or upload the whole folder to any host (Netlify, Vercel, cPanel, Afrihost, GitHub Pages).

```
index.html      all page content
style.css       all styling, grouped and commented by section
script.js       menu, scroll reveals, gallery filter, enquiry form
assets/
  favicon.svg   browser tab icon
  img/          images (currently placeholders)
gen_images.py   the script that generated the placeholder images (not needed to run the site)
```

## Things to change first

**Phone number** — appears in `index.html` as `tel:+27670033499`, `wa.me/27670033499` and the
visible text `067 003 3499`, and once in `script.js` under `CONFIG.phone`. Search and replace all.

**Logo** — the header currently uses a small inline leaf mark. To use a real logo, replace the
`<svg class="brand-mark">…</svg>` inside `<a class="brand">` with
`<img class="brand-mark" src="assets/logo.png" alt="Jimmy's Landscaping">`.

**Photographs** — the images in `assets/img/` are generic illustrations, not photographs of
work done by Jimmy's Landscaping. Replace them with real project photos using the same
filenames and nothing else needs to change. Keep them under about 300 KB each so the site
stays fast; roughly 1600px wide is plenty.

When real photos are in, delete the disclaimer paragraph in the Projects section
(`<p class="disclaimer">…`) and update the `alt` text on each image to describe the actual job.

**Services** — six cards in the Services section, and the same list again in the form's
`<select>`. Keep the two lists matching.

## Connecting the enquiry form

Right now the form validates and then opens WhatsApp with the enquiry filled in, so nothing
is lost while there is no backend.

To send enquiries to an inbox or server instead, set the endpoint at the top of `script.js`:

```js
var CONFIG = {
  phone: '27670033499',
  formEndpoint: 'https://formspree.io/f/xxxxxxx'   // or your own /api/enquiry
};
```

It posts JSON with `name`, `phone`, `service` and `message`. A plain HTML post also works —
add `action="…" method="post"` to the `<form>` and remove the submit handler.

## Still to add when the business provides it

Business address, email address, trading hours, real testimonials, service area, company
registration number. Nothing of that kind has been invented anywhere on the page — the
`LocalBusiness` block in the `<head>` of `index.html` is where an address and email should go
for search engines once they are known.
