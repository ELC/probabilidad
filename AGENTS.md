# AGENTS.md

Guidance for AI agents working on **Probabilidad y Estadística** (`probabilidad`) — a Jupyter Book 2 project for MyST notebooks and GitHub Pages deployment, powered by [MyST](https://mystmd.org/). All book configuration lives in a single file: `book/myst.yml`.

## Repository layout

```
src/
  core/             # Settings (BaseSettings), parameter BaseModels, pandera schemas, theme constants
  symbolic/         # sympy.stats expressions; one place for formulas
  distributions/    # scipy.stats numeric counterparts to symbolic
  descriptive/      # location, dispersion, position, outliers
  probability/      # set ops, conditional, Bayes, total probability
  sampling/         # CLT, LLN, Galton, bootstrap, Monte Carlo
  inference/        # confidence intervals, hypothesis tests, sample size
  visualization/    # pure Altair chart factories
  widgets/          # ipywidgets factories wrapping Altair charts
  exercises/        # verify_* helpers for notebook exercises
tests/                  # Pytest suite (mirrors src/ 1:1, 100% coverage)
book/
  myst.yml              # Project + site configuration (TOC, theme, plugins)
  chapters/             # Book content (.ipynb only)
  assets/               # Site branding (favicon, logos)
  plugins/              # Custom MyST plugins
  bibliography.bib      # Citations
pyproject.toml          # Project metadata (probabilidad), deps, Poe tasks
.github/workflows/      # GitHub Pages deploy (main branch)
.binder/Dockerfile      # Binder environment (main branch)
```

Build output goes to `book/_build/` (gitignored). Run book commands from the repo root via Poe; tasks set `cwd = "book"`.

## Project source code

Library code lives under `src/` as installable top-level packages (`core`, `symbolic`, `distributions`,
`descriptive`, `probability`, `sampling`, `inference`, `visualization`, `widgets`, `exercises`). Built
with `uv_build` and installed editable on `uv sync` — chapters import them directly, never via
`sys.path`.

The architecture follows **vertical slices by capability**, not by academic unit. Each unit notebook
imports from several slices.

### Binding conventions for `src/`

- **No primitive obsession**: every public function takes exactly one Pydantic `BaseModel` input
  (or none for factories) and returns one typed result (`BaseModel`, `alt.Chart`,
  `ipywidgets.Widget`, `sympy.Expr`, or `matplotlib.figure.Figure` when the chart is a
  specialized diagram not natively supported by Altair, e.g. `matplotlib_venn`).
- **Pure functions only**. Side effects (display, observe, mutation) live inside widget factory
  callbacks; the surrounding code is referentially transparent.
- **No global state**: no module-level mutables, no implicit theme registration. Theme is applied
  per-chart by passing `Settings` to chart factories.
- **Descriptive names over docstrings**: no docstrings on public APIs; identifiers carry intent
  (`build_confidence_interval_for_mean_with_known_variance`).
- **Symbolic-first**: anything derivable in `sympy.stats` is defined symbolically once in
  `src/symbolic/`; numeric layers reuse those expressions via `sp.lambdify` where useful.
- **Strict typing**: `mypy --strict`, pandera `DataFrame[Schema]` instead of bare `pd.DataFrame`.
- **Random generators take `Settings` explicitly** (carrying `random_seed`) so seeds are visible
  at the call site.
- **Tests mirror `src/` 1:1** under `tests/`; enforce 100% line + branch coverage.

### Notebook conventions

- One notebook per academic unit under `book/chapters/`, numbered 01..05.
- Markdown in Spanish, code identifiers in English.
- Each code cell is ≤6 lines and only composes calls to `src/`.
- Each concept follows the CPA progression (Concrete → Pictorial → Abstract → Intuición → Interactive
  exploration with an ipywidgets + Altair combo).
- Every conceptual `##`/`###` section must include a **Cierre operativo** or an
  equivalent closing paragraph that anchors the concept in the chapter scenario:
  the concrete question it answers, when the protagonist should use it, what can
  go wrong, and what decision or communication follows. Use concrete numbers or
  thresholds from the scenario (for example, "5 minutes", "3 people ahead",
  "2 outliers"), not abstract wording. The closure must use only concepts and
  vocabulary already introduced earlier in the chapter; do not mention a future
  tool (for example IQR, z-score, Tukey, or inference) before the reader has met
  it. If a section is too short to support that closure, merge it with a
  neighboring section or rewrite it as an explicit transition instead of leaving
  an isolated concept.
- Render recurring pedagogical pauses as custom-title MyST admonitions, not as
  bold inline labels. Use `::::{admonition} <Title>` with the corresponding
  `:class:` option: **Idea para retener** → `important`, **Trampa común** →
  `caution`, **Cierre operativo** → `tip`, and **Decisión de ingeniería** →
  `seealso`.
- Exercises end with a `verify_*` call that asserts the student's answer against a symbolically
  derived expected value.

## Initialize the template

Use this checklist when turning the template into a new book project.

### GitHub setup

1. Fork the repository (GitHub only allows using templates you own).
2. Use **`main`** as the default branch (content, CI, and site deployment).
3. Enable **Template repository** under Settings → General.
4. Enable **GitHub Actions** if disabled.
5. Enable **GitHub Pages** with source **GitHub Actions** under Settings → Pages.
6. Clone the fork locally.

When creating a new repo from the template, select it from the template dropdown.

### Local environment

Requires **Python 3.13** (see `.python-version`).

```bash
uv sync --all-groups
```

### Replace placeholder values

Search the repo for `REPLACE WITH` and update every match:

| Placeholder | Where | Example |
|-------------|-------|---------|
| Book Title | `book/myst.yml` → `project.title` | `My Data Science Book` |
| Book Title | `book/plugins/ethicalads.mjs` → `DEFAULT_OPTIONS.book_title` | keep in sync with `project.title` |

Also update manually in `book/myst.yml`:

- `project.copyright`
- `project.authors`
- `project.github`
- `site.options.analytics_google` (or remove the key to disable Google Analytics)

Update README badges and links (project URL, Binder, Colab, GitHub Pages URL). Replace the template README with project-specific documentation when ready.

### Verify the setup

```bash
uv run poe build-book    # build static HTML with executed notebooks
uv run poe serve-book    # build, then preview at http://localhost:8000
uv run poe ci            # pre-commit checks + build (same as CI)
```

CI (`.github/workflows/ci.yml`) runs on pushes to **`main`**, sets `BASE_URL=/<repo-name>` for project Pages, and deploys `book/_build/html`.

### Test a branch before merging a PR

When a change affects Binder, `pyproject.toml` / `uv.lock`, or `project.jupyter`, validate on the **feature branch** before merge:

1. Ensure the branch is **pushed** to GitHub (MyBinder only builds remote refs).
2. Temporarily set in `book/myst.yml`:

   ```yaml
   project:
     jupyter:
       binder:
         ref: <branch-name>
   ```

3. **MyBinder** (not CI) builds from `.binder/Dockerfile` on the pushed ref. Use a commit-SHA launch URL
   (`https://mybinder.org/v2/gh/ELC/probabilidad/<sha>`) after each push; branch URLs can show logs from an older cached build. Stale logs show `RUN uv sync` on Dockerfile line 9—the fixed file uses `UV_PROJECT_ENVIRONMENT` and `rm -rf .venv` instead.
4. For manual checks, align README Binder/Colab URLs and `book/myst.yml` `binder.ref` with the branch.
5. Run **`uv run poe build-docker`** locally (same as the `check-docker` CI job). The image installs deps into **`.venv/`** (see `UV_PROJECT_ENVIRONMENT` in `.binder/Dockerfile`); root **`.hidden`** hides `.venv` and `venv` in JupyterLab.
6. **Before merge**, remove `project.jupyter.binder.ref` (or set `ref: main`), revert README badge URLs, and do not leave a feature branch pinned in `myst.yml`.

Agents must not leave `project.jupyter.binder.ref` set to a non-`main` branch in changes intended for merge unless the user explicitly asks to keep it.

## Add new pages

### 1. Create the content file

Add a new file under `book/chapters/`. Supported formats:

- **`.ipynb`** — traditional Jupyter notebooks (Binder/Colab friendly).
- **`.md`** — MyST markdown notebooks (plain text, git-friendly). Copy the YAML frontmatter block from `book/chapters/01_markdown.md` if the page contains executable code cells.

Use a numeric prefix for ordering (e.g. `03_my_chapter.md`).

### 2. Register the page in the table of contents

Edit `project.toc` in `book/myst.yml`. Paths are relative to `book/`. File extensions are **required**.

Flat entry:

```yaml
project:
  toc:
    - file: chapters/00_how_to_use.ipynb
    - file: chapters/03_my_chapter.md
```

Nested section:

```yaml
    - title: My Section
      children:
        - file: chapters/03_part_a.md
        - file: chapters/04_part_b.ipynb
```

The first TOC entry is the book landing page.

For large books, split the TOC into a separate file and reference it with `extends:` in `myst.yml` (see [MyST TOC docs](https://mystmd.org/guide/table-of-contents)).

To auto-generate a starting TOC from filenames:

```bash
cd book
uv run jupyter book init --write-toc
```

Re-order the generated entries as needed.

### 3. Optional: top navigation bar

Add links under `site.nav` in `book/myst.yml`:

```yaml
site:
  nav:
    - title: My Chapter
      url: /chapters/my-chapter
```

URLs use slugs derived from filenames (extension omitted, numeric prefix stripped). The existing entry `/chapters/markdown` maps to `chapters/01_markdown.md`.

### 4. Citations and assets

- Add BibTeX entries to `book/bibliography.bib` and cite with MyST syntax (`[@key]` or `@key`). Numbered references are enabled via `site.options.numbered_references`.
- Put site-wide branding files in `book/assets/` (favicon, logos).
- Reference images from chapter content with paths relative to the chapter file, or colocate them in `book/chapters/`.

### 5. Build to validate

```bash
uv run poe build-book
```

Notebooks are executed at build time (`--execute`). Fix any execution errors before committing.

## Configure the site

All configuration is in `book/myst.yml` under two top-level keys:

### `project:` — content and metadata

| Field | Purpose |
|-------|---------|
| `title`, `copyright`, `authors` | Book metadata shown on the site |
| `github` | Repository URL (edit-on-GitHub links) |
| `bibliography` | List of `.bib` files |
| `numbering.headings` | Number sections automatically |
| `jupyter` | Enable Jupyter notebook support |
| `plugins` | Local MyST plugins (e.g. `plugins/ethicalads.mjs`) |
| `toc` | Table of contents (page order and nesting) |

### `site:` — theme and publishing

| Field | Purpose |
|-------|---------|
| `template` | Theme (`book-theme`) |
| `parts.banner` | Reusable page regions (Ethical Ads banner) |
| `nav` | Top navigation links |
| `options.folders` | Folder-style sidebar grouping |
| `options.numbered_references` | IEEE-style numbered citations |
| `options.favicon`, `logo`, `logo-dark` | Paths under `book/assets/` |
| `options.analytics_google` | Google Analytics measurement ID |

### Custom plugins

The Ethical Ads plugin lives in `book/plugins/`:

- `ethicalads.mjs` — MyST directive (`:::{ethicalads}:::`)
- `ethicalads-widget.mjs` — anywidget renderer

When changing the book title, update **both** `project.title` in `myst.yml` and `book_title` in `ethicalads.mjs`.

### Dependencies

Python packages for notebook execution are declared in `pyproject.toml` under `[project] dependencies`. Add libraries there when chapters import new packages, then run `uv sync`.

## Commands reference

| Task | Command |
|------|---------|
| Install deps | `uv sync --all-groups` |
| Build book | `uv run poe build-book` |
| Preview locally | `uv run poe serve-book-preview` |
| Build + preview | `uv run poe serve-book` |
| Lint + build (CI) | `uv run poe ci` |
| Build Binder image | `uv run poe build-docker` |
| Pre-commit only | `uv run poe check` |
| Clean build artifacts | `cd book && uv run jupyter book clean` |

## Conventions for agents

- Do **not** edit `book/_build/` — it is generated output.
- Keep changes focused: new pages need both a content file and a `myst.yml` TOC entry.
- Run `uv run poe build-book` after adding or changing executable notebooks.
- Do not commit secrets (analytics IDs are fine; API keys are not).
- Only create git commits when explicitly asked.
- Prefer MyST/Jupyter Book 2 docs over Jupyter Book 1 patterns (`_config.yml`, `_toc.yml` are legacy and not used here).

## Further reading

- [Jupyter Book — Table of contents](https://jupyterbook.org/stable/authoring/table-of-contents)
- [MyST configuration](https://mystmd.org/guide/frontmatter)
- [MyST deployment (BASE_URL)](https://mystmd.org/guide/deployment#deploy-base-url)
- [Template README](README.md) — human-oriented fork/setup instructions
