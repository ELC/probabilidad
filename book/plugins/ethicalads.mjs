/**
 * Ethical Ads via MyST anywidget (renders real DOM; `html` nodes are shown as text).
 *
 * Configure defaults in DEFAULT_OPTIONS below.
 *
 * In page content or site.parts.banner (myst.yml):
 *
 *   :::{ethicalads}
 *   :::
 *
 * @see https://mystmd.org/guide/widgets
 * @see https://www.ethicalads.io/advertisers/publisher-guide/
 */

/** Edit publisher, ad type, and book title (keep book_title in sync with project.title in myst.yml). */
const DEFAULT_OPTIONS = {
  publisher: 'elcgithubio',
  ad_type: 'text',
  ea_style: 'fixedheader',
  book_title: '(REPLACE WITH Book Title)',
};

/** Resolved from the book project root (`book/`). */
const WIDGET_MODULE = 'plugins/ethicalads-widget.mjs';

/**
 * HTML id for Ethical Ads placement reporting.
 * @see https://ethical-ad-client.readthedocs.io/en/latest/#ad-placement-reporting
 * @param {string} title
 */
function slugifyBookTitle(title) {
  return title
    .toLowerCase()
    .replace(/[^\w\s-]/g, '')
    .trim()
    .replace(/\s+/g, '-');
}

/**
 * @param {string} publisher
 * @param {string} adType
 */
function widgetId(publisher, adType) {
  return `ea-${publisher}-${adType}-${Math.random().toString(36).slice(2, 10)}`;
}

/** @type {import('myst-common').DirectiveSpec} */
const ethicalAdsDirective = {
  name: 'ethicalads',
  alias: ['ethical-ads'],
  doc: 'Insert an Ethical Ads text placement (via anywidget).',
  options: {
    publisher: {
      type: String,
      doc: 'Ethical Ads publisher slug (data-ea-publisher).',
    },
    'ad-type': {
      type: String,
      doc: 'Ad unit type. Defaults to `text`.',
    },
    'placement-id': {
      type: String,
      doc: 'Placement id for Ethical Ads reporting. Defaults to a slug of the book title.',
    },
    'ea-style': {
      type: String,
      doc: 'Ethical Ads placement style, e.g. `fixedheader`.',
    },
  },
  run(data) {
    const publisher = data.options?.publisher ?? DEFAULT_OPTIONS.publisher;
    const adType = data.options?.['ad-type'] ?? DEFAULT_OPTIONS.ad_type;
    const eaStyle = data.options?.['ea-style'] ?? DEFAULT_OPTIONS.ea_style;
    const placementId =
      data.options?.['placement-id'] ?? slugifyBookTitle(DEFAULT_OPTIONS.book_title);
    return [
      {
        type: 'anywidget',
        esm: WIDGET_MODULE,
        model: { publisher, adType, eaStyle, placementId },
        class: 'ethicalads-widget',
        id: widgetId(publisher, adType),
      },
    ];
  },
};

/** @type {import('myst-common').MystPlugin} */
const plugin = {
  name: 'Ethical Ads',
  directives: [ethicalAdsDirective],
};

export default plugin;
