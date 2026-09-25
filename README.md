# Wave Simulator (Remastered)

A 2D wave simulator that runs in your browser on the GPU. This is a
plain HTML/CSS/JavaScript port of
[starrfree/wave-simulator](https://github.com/starrfree/wave-simulator). The
original is an Angular app. See [CREDITS.md](CREDITS.md).

New in the remaster: the **Phased Array** initial condition. It runs up to 16
sources, each with its own phase offset, so the beam can be steered. It also
adds a black/white grid colour option.

## Physics fixes over the original

Both fixes were measured in the running simulation. The numbers below are the
measurements.

- **Right and top edges were off by one cell.** They treated the
  second-to-last cell as the edge, so a centred pulse bouncing off the walls
  came back 10–14 % lopsided. The simulation is now mirror-symmetric to within
  float rounding (0.001 %).
- **The "Absorb" edge reflected about 21 % of a wave.** Its rule only fits
  waves that move one cell per step, and this solver moves them 0.7. Edge
  cells now follow the one-way wave equation (first-order upwind). Reflection
  is 1.5–3.5 %, and the scheme stays stable.

## Validation

These results were measured in the simulation and compared with theory:

| Check | Expected | Measured |
| ----- | -------- | -------- |
| Wavelength, free space | 2π·0.7 / (f·LOD) | within 0.5 % |
| Wave speed where alpha = 0.25 / 0.5 / 0.75 | 0.75 / 0.5 / 0.25 | 0.747 / 0.494 / 0.249 |
| Stability (step 0.7, 2-D limit 1/√2) | stays bounded | 18 000 steps, bounded |
| Phased array steered to 0° / 20° / 45° | same angle | 0° / 20° / 45° |
| Beam pattern vs. superposition theory | correlation 1 | 0.996 – 0.999 |
| Grating lobe at 1 λ spacing, steered 30° | extra beam at −30° | −31° |

The simulation is 2-D, so waves spread like ripples on water. Their
amplitude falls off as 1/√r instead of 1/r.

## Running it

Double-click **`index.html`**. You don't need to install anything, run a build
step or start a server, and it works fully offline. The page makes no network
requests: the fonts are in `fonts/` and the icons are inline SVG.

## Layout

| File | What it does |
| ---- | ------------ |
| `index.html` | Page structure and the whole side panel |
| `css/style.css` | All styling |
| `fonts/` | Roboto and Lato (`.woff2`) with their licenses |
| `js/assets.js` | Bundled images as data URLs (**generated**, see below) |
| `js/shaders.js` | GLSL for the wave equation and colouring |
| `js/params.js` | Defaults, limits, and `sanitizeParameters()` |
| `js/phased-array.js` | Phased-array layout and steering phases |
| `js/shapes.js` | Procedural obstacle maps (polygons, stars, slits, ...) |
| `js/share.js` | Scene links, saved settings, phone detection |
| `js/scene.js` | WebGL simulation loop and canvas overlay |
| `js/menu.js` | Cascading dropdown menu |
| `js/toolbar.js` | Side-panel wiring |
| `js/app.js` | Ties everything together, keyboard shortcuts |

The scripts are classic `<script src>` tags, not ES modules, and the order in
`index.html` matters. Module scripts are fetched with CORS, which a `file://`
page cannot satisfy, so modules would leave a blank page.

### Changing bundled images

The PNGs in `assets/` are the source. After you change one, run:

```
python tools/embed_assets.py
```

The images have to be embedded as data URLs. An image loaded from a `file://`
path taints the canvas, and WebGL refuses to upload a tainted canvas.

## Security

- **Content Security Policy** (in `index.html`) allows scripts, styles and
  fonts only from this folder, and images only from embedded data. It blocks
  every network request, so the page cannot fetch or send anything.
- **Every untrusted input is sanitised.** That covers shared links, saved
  settings and typed values. Each number is range-checked against a limit the
  GPU can handle, and unknown fields are dropped.
- **A shared link cannot reference outside images.** Only bundled assets are
  allowed. Before this, a crafted link could make the recipient's browser
  request an arbitrary URL.
- **No third-party requests.** Fonts, icons and images all ship with the page,
  so opening it does not send the visitor's IP address anywhere.
- **Uploads** must be real PNG/JPEG/GIF/WebP/BMP images, up to 15 MB and
  8192 px on a side. SVG is rejected.
- **User-supplied text** (file names) is only ever set with `textContent`,
  never as HTML.

## Controls

| Shortcut | Action |
| -------- | ------ |
| <kbd>Space</kbd> | Pause / resume |
| <kbd>R</kbd> | Restart |
| <kbd>N</kbd> or <kbd>→</kbd> | Step forward |
| <kbd>G</kbd> | Toggle the grid |
| <kbd>0</kbd> | Reset the view |
| <kbd>S</kbd> | Save a PNG |

On the canvas, scroll to zoom and drag with the middle or right mouse button to
pan. Double-click resets the view. To move a pulse or spherical source, drag its
marker.

### Phased array

- **Linear array**: set the element count, the spacing (in wavelengths), the
  orientation and the steering angle. The phases are computed for you. Drag on
  the canvas to move the whole array. Turn on *Average energy* to see the beam
  pattern clearly.
- **Custom**: switching to Custom keeps the current layout and its phases. You
  can then drag each numbered source, type its phase in degrees, and add or
  remove sources.

## License

[MIT](LICENSE). Wave Simulator Remastered is by Aviressence and is based on
Wave Simulator by Eliott Morgensztern. You may use, copy, modify, share and
sell it, as long as you keep the copyright notice in `LICENSE`. It comes with
no warranty. See [CREDITS.md](CREDITS.md) for everyone involved.
