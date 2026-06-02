# binder-build: 11 — bump when changing this file to bust MyBinder layer cache
FROM ghcr.io/rocker-org/binder:4.4.2

# repo2docker passes NB_USER=jovyan / NB_UID=1000 by default. The rocker-org/binder image
# does not have a user literally named `jovyan` in /etc/passwd, so chown by name fails.
# Numeric UID/GID 1000 always exists and matches the user repo2docker runs the kernel as.
ARG NB_UID=1000
ARG NB_GID=1000

COPY --from=ghcr.io/astral-sh/uv:0.11.18 /uv /uvx /bin/

WORKDIR /home/jovyan/

# Rocker sets VIRTUAL_ENV=/opt/conda; shells clear it in .binder/bashrc-venv.sh. uv uses UV_PROJECT_ENVIRONMENT.
# Use .venv (dot-dir) so JupyterLab hides it; .dockerignore keeps any host .venv out of the build context.
ENV UV_PROJECT_ENVIRONMENT=/home/jovyan/.venv
ENV UV_CACHE_DIR=/home/jovyan/.cache/uv
# Required when using cache mounts so packages are copied into the image layer.
ENV UV_LINK_MODE=copy

USER ${NB_UID}

# Dependency layer: lockfiles are bind-mounted (not COPY'd) so this layer invalidates only
# when pyproject.toml / uv.lock / .python-version change. See https://docs.astral.sh/uv/guides/integration/docker/
RUN --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    uv sync --all-groups --locked --no-install-project

# Application layer: book content and Binder config (reuses cached .venv when deps are unchanged).
COPY --chown=${NB_UID}:${NB_GID} . /home/jovyan

RUN --mount=type=cache,target=/home/jovyan/.cache/uv,uid=${NB_UID},gid=${NB_GID} \
    rm -rf /home/jovyan/venv \
 && uv sync --all-groups --locked

# Register the project venv as a Jupyter kernel. --sys-prefix installs into the venv
# (`/home/jovyan/.venv/share/jupyter/kernels`), which Jupyter finds automatically and which
# the kernel user can write to. /opt/conda from the base image is root-owned.
RUN uv run -m ipykernel install \
     --sys-prefix                      \
     --name=jupyter-book-template      \
     --display-name="Python 3.13 (uv)"

COPY --chown=${NB_UID}:${NB_GID} .binder/vscode/settings.json .vscode/settings.json

COPY --chown=${NB_UID}:${NB_GID} .binder/bashrc-venv.sh /tmp/bashrc-venv.sh
RUN cat /tmp/bashrc-venv.sh >> .bashrc && rm /tmp/bashrc-venv.sh

EXPOSE 8888
