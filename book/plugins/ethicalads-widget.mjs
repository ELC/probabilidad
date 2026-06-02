const SCRIPT_SRC = 'https://media.ethicalads.io/media/client/ethicalads.min.js';
const FIXED_HEADER_HEIGHT = '50px';

/** @type {Promise<void> | undefined} */
let scriptPromise;

function ensureScript() {
  if (globalThis.ethicalads) return Promise.resolve();
  if (scriptPromise) return scriptPromise;
  scriptPromise = new Promise((resolve, reject) => {
    const script = document.createElement('script');
    script.async = true;
    script.src = SCRIPT_SRC;
    script.onload = () => resolve();
    script.onerror = () => reject(new Error('Failed to load Ethical Ads client'));
    document.head.appendChild(script);
  });
  return scriptPromise;
}

function refreshAds() {
  const ethicalads = globalThis.ethicalads;
  if (!ethicalads) return;
  if (typeof ethicalads.load === 'function') {
    ethicalads.load();
    return;
  }
  if (typeof ethicalads.reload === 'function') {
    ethicalads.reload();
  }
}

/** @param {HTMLElement} el */
function lightDomHost(el) {
  const root = el.getRootNode();
  return root instanceof ShadowRoot ? root.host : el;
}

/**
 * Ethical Ads scans the light DOM. Mount the placement on a visible ancestor
 * (e.g. site banner) instead of inside the anywidget shadow root.
 *
 * @param {HTMLElement} host
 * @returns {{ placement: HTMLDivElement }}
 */
function mountPlacement(host) {
  const placement = document.createElement('div');
  placement.className = 'ethicalads-placement not-prose';

  const parent = host.parentElement;
  if (parent) {
    host.style.display = 'none';
    parent.appendChild(placement);
    return { placement };
  }

  host.insertAdjacentElement('afterend', placement);
  return { placement };
}

/**
 * @param {HTMLDivElement} placement
 * @param {{ publisher: string; adType: string; eaStyle: string; placementId: string }} config
 */
function configurePlacement(placement, { publisher, adType, eaStyle, placementId }) {
  placement.setAttribute('data-ea-publisher', publisher);
  placement.setAttribute('data-ea-type', adType);
  placement.setAttribute('data-ea-style', eaStyle);
  if (placementId) {
    placement.id = placementId;
  }
  if (eaStyle === 'fixedheader') {
    // Preallocate space before the client loads (see Ethical Ads fixedheader docs).
    placement.style.height = FIXED_HEADER_HEIGHT;
  }
}

/**
 * @param {{ model: { get: (key: string) => unknown }; el: HTMLElement }} ctx
 */
function render({ model, el }) {
  const publisher = String(model.get('publisher') ?? 'elcgithubio');
  const adType = String(model.get('adType') ?? 'text');
  const eaStyle = String(model.get('eaStyle') ?? 'fixedheader');
  const placementId = String(model.get('placementId') ?? '');

  const host = lightDomHost(el);
  const { placement } = mountPlacement(host);

  configurePlacement(placement, { publisher, adType, eaStyle, placementId });

  ensureScript()
    .then(refreshAds)
    .catch(() => {
      placement.remove();
      host.style.display = '';
    });

  return () => {
    placement.remove();
    host.style.display = '';
  };
}

export default { render };
