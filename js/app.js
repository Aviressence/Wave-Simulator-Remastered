// Wires the pieces together and owns the one live parameter object.
'use strict'

const App = {
  params: null,
  scene: null,
  toolbar: null,

  init() {
    this.params = this.loadParameters()

    this.scene = new SceneCanvas(document.getElementById('scene'), () => this.params, {
      // A drag or zoom on the canvas: refresh the panel's boxes and save.
      sourceMoved: () => { this.save(); this.refresh() },
      viewChanged: () => { this.save(); this.refresh() },
      resized: () => this.toolbar?.render()
    })
    this.toolbar = new Toolbar(this)

    document.getElementById('btn-fullscreen').addEventListener('click', () => {
      document.body.classList.toggle('fullscreen')
    })
    window.addEventListener('keydown', e => this.onShortcut(e))

    this.refresh()
    const error = this.scene.start()
    if (error) {
      const box = document.getElementById('error')
      box.textContent = error
      box.hidden = false
    }
  },

  /**
   * A shared link wins over this browser's saved scene, so following someone's
   * URL shows their setup. Both go through the sanitiser; only the local save
   * may reference an uploaded image.
   */
  loadParameters() {
    const shared = Share.readFromLocation()
    Share.clearLocation()
    if (shared) {
      return sanitizeParameters(shared, { isMobile: IS_MOBILE, allowUploads: false })
    }
    return sanitizeParameters(SavedSettings.load(), { isMobile: IS_MOBILE, allowUploads: true })
  },

  save() {
    SavedSettings.save(this.params)
  },

  /** Pushes the current parameters into the panel and the canvas overlay. */
  refresh() {
    document.body.classList.toggle('toolbar-right', this.params.toolbarSide === 'right')
    this.toolbar.render()
    this.scene.refreshOverlay()
  },

  restart() {
    this.scene.restart()
  },

  togglePause() {
    this.params.pause = !this.params.pause
    this.refresh()
  },

  stepForward() {
    this.params.nextFrame += 5
  },

  resetAll() {
    SavedSettings.clear()
    this.params = makeDefaultParameters(IS_MOBILE)
    this.scene.rebuildBackground()
    this.scene.rebuildGradient()
    this.restart()
    this.refresh()
  },

  onShortcut(event) {
    // Never steal keys from a text field or an open menu, and leave browser
    // chords alone.
    const target = event.target
    const tag = target?.tagName
    if (tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT' || target?.isContentEditable || Menu.layer) {
      return
    }
    if (event.ctrlKey || event.metaKey || event.altKey) {
      return
    }
    // Space on a just-clicked button would press it again on keyup; drop the
    // focus so Space means "pause" and nothing else.
    if (event.key === ' ' && tag === 'BUTTON') {
      target.blur()
    }
    switch (event.key) {
      case ' ':
        this.togglePause()
        break
      case 'r':
      case 'R':
        this.params.pause = false
        this.restart()
        this.refresh()
        break
      case 'n':
      case 'N':
      case 'ArrowRight':
        this.stepForward()
        break
      case 'g':
      case 'G':
        this.params.grid.show = !this.params.grid.show
        this.save()
        this.refresh()
        break
      case '0':
        this.scene.resetView()
        break
      case 's':
      case 'S':
        this.scene.requestScreenshot()
        break
      default:
        return
    }
    event.preventDefault()
  }
}

App.init()
