# Wave Simulator (Remastered)

A 2D wave simulator that runs in your browser on the GPU. It is based on
[starrfree/wave-simulator](https://github.com/starrfree/wave-simulator) and
extends it with new mechanics, physics fixes and a security rework. It is
rebuilt as a single folder of plain HTML/CSS/JavaScript: double-click
`index.html` and it runs.

**[What's new](#whats-new) · [Security](SECURITY.md) · [Credits](CREDITS.md)**

## What's new

Everything below is compared with the original project.

### New mechanics

- **Phased array:** up to 16 sources, each with its own phase offset.
  - *Linear array* mode steers the beam to any angle; the phases are computed
    for you.
  - *Custom* mode lets you place each source by hand and set its phase.
- **Procedural shapes:** triangle through decagon, star, circle, ellipse and
  an adjustable N-slit barrier. They replace the uneven bitmap templates.
  Shapes are hollow by default, and you can set their size, rotation, wall
  strength and thickness, or invert them.
- **Grid:** always-square cells laid out from the centre. It has a
  black/white colour option and a snap setting. Hold <kbd>Ctrl</kbd> to snap
  the interactive pulse to the grid.
- **Draggable sources:** drag pulse and spherical sources on the canvas. A
  live coordinate readout shows where you are.
- **Zoom and pan:** scroll to zoom up to 20x, and drag with the middle or
  right mouse button to pan.
- **Full-window simulation:** no black letterbox bars, and nothing is
  stretched.
- **Panel placement:** dock the side panel left or right.
- **Video export:** *Render video* computes an MP4 as fast as your GPU allows,
  at an exact 30 or 60 fps, from the first frame, so you don't have to watch
  it. *Record live* captures what you see, clicks included. Both give MP4 in
  Chrome and Edge, ready to post on X.
- **Sharing:** copy a link to the current scene, save the frame as a PNG, and
  use keyboard shortcuts.
- **No setup:** no Node, no npm, no build. It works offline.

### Fixed

- The Duration and y fields wrote to the same stored value, so editing one
  overwrote the other.
- *Reset parameters to default* changed the defaults themselves, so resetting
  restored your last settings instead.
- GPU textures were never freed. Every resize or detail change leaked memory.
- Shaders were downloaded at start-up, so the app could not run from a file.
- **Right and top edges were off by one cell.** A centred pulse bouncing off
  the walls came back 10–14 % lopsided. The simulation is now mirror-symmetric
  to within float rounding (0.001 %).
- **The Absorb edge reflected about 21 % of a wave.** Its rule assumed waves
  move one cell per step, but this solver moves them 0.7. Edge cells now follow
  the one-way wave equation, so reflection is 1.5–3.5 % and the simulation
  stays stable.

### Security

The original depended on the no-longer-supported Angular 13 and Node 16. This
version has **no dependencies at all**, and the page cannot contact any
server. Details are in [SECURITY.md](SECURITY.md).

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
| `js/video-render.js` | Offline video rendering with WebCodecs |
| `js/mp4.js` | Minimal MP4 writer for the rendered video |
| `js/recorder.js` | Live recording with MediaRecorder |
| `js/app.js` | Ties everything together, keyboard shortcuts |

The scripts are classic `<script src>` tags, not ES modules, and the order in
`index.html` matters. Module scripts are fetched with CORS, which a `file://`
page cannot satisfy, so modules would leave a blank page.

### Changing bundled images

The PNGs in `assets/` are the source. After you change one, run:

```
python tools/generate_assets.py
python tools/embed_assets.py
```

The images have to be embedded as data URLs. An image loaded from a `file://`
path taints the canvas, and WebGL refuses to upload a tainted canvas.

## Controls

| Shortcut | Action |
| -------- | ------ |
| <kbd>Space</kbd> | Pause / resume |
| <kbd>R</kbd> | Restart |
| <kbd>N</kbd> or <kbd>→</kbd> | Step forward |
| <kbd>G</kbd> | Toggle the grid |
| <kbd>0</kbd> | Reset the view |
| <kbd>S</kbd> | Save a PNG |
| <kbd>V</kbd> | Start / stop a live recording |

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
