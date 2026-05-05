(function () {
  const STORAGE_KEY = 'ideate_visual_mode';
  const MODES = new Set(['cinematic', 'minimal', 'boardroom']);

  function resolveMode(mode) {
    return MODES.has(mode) ? mode : 'minimal';
  }

  function getStoredMode() {
    try {
      return window.localStorage.getItem(STORAGE_KEY);
    } catch {
      return null;
    }
  }

  function persistMode(mode) {
    try {
      window.localStorage.setItem(STORAGE_KEY, mode);
    } catch {
      // Ignore storage failures (private browsing or blocked storage).
    }
  }

  function setButtonState(buttons, activeMode) {
    buttons.forEach((button) => {
      const isActive = button.dataset.mode === activeMode;
      button.classList.toggle('is-active', isActive);
      button.setAttribute('aria-pressed', String(isActive));
    });
  }

  function applyMode(mode, buttons) {
    const safeMode = resolveMode(mode);
    document.body.dataset.mode = safeMode;
    setButtonState(buttons, safeMode);
    persistMode(safeMode);
  }

  function init() {
    const buttons = Array.from(document.querySelectorAll('.mode-btn[data-mode]'));
    const initialMode = resolveMode(getStoredMode());
    applyMode(initialMode, buttons);

    buttons.forEach((button) => {
      button.addEventListener('click', () => {
        const mode = button.dataset.mode;
        applyMode(mode, buttons);
      });
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init, { once: true });
    return;
  }

  init();
})();
