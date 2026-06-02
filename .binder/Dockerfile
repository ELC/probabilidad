# binder-build: 6 — bump when changing this file to bust MyBinder layer cache
FROM ghcr.io/rocker-org/binder:4.4.2

# repo2docker passes NB_USER=jovyan / NB_UID=1000 by default. The rocker-org/binder image
# does not have a user literally named `jovyan` in /etc/passwd, so chown by name fails.
# Numeric UID/GID 1000 always exists and matches the user repo2docker runs the kernel as.
ARG NB_UID=1000
ARG NB_GID=1000

COPY --from=ghcr.io/astral-sh/uv:0.11.18 /uv /uvx /bin/

WORKDIR /home/jovyan/

# Rocker sets VIRTUAL_ENV=/opt/conda. Use a dedicated project venv path (not .venv) so a
# copied host .venv cannot block `uv sync` with permission errors on .venv/.lock.
ENV VIRTUAL_ENV=
ENV UV_PROJECT_ENVIRONMENT=/home/jovyan/venv

# .dockerignore strips local .venv/venv from the context; --chown ensures any leftover
# files are owned by the kernel user so `rm` and `uv sync` work without root.
COPY --chown=${NB_UID}:${NB_GID} . /home/jovyan

USER ${NB_UID}

# uv-managed Python ends up under $HOME/.local/share/uv/python/...; running as the
# kernel user (not root) keeps that directory readable when `uv run` resolves the venv.
RUN rm -rf /home/jovyan/.venv /home/jovyan/venv \
 && env -u VIRTUAL_ENV uv sync --all-groups --locked

# Register the project venv as a Jupyter kernel. --sys-prefix installs into the venv
# (`/home/jovyan/venv/share/jupyter/kernels`), which Jupyter finds automatically and which
# the kernel user can write to. /opt/conda from the base image is root-owned.
RUN uv run -m ipykernel install \
     --sys-prefix                      \
     --name=jupyter-book-template      \
     --display-name="Python 3.13 (uv)"

COPY --chown=${NB_UID}:${NB_GID} .binder/vscode/settings.json .vscode/settings.json

COPY --chown=${NB_UID}:${NB_GID} .binder/bashrc-venv.sh /tmp/bashrc-venv.sh
RUN cat /tmp/bashrc-venv.sh >> .bashrc && rm /tmp/bashrc-venv.sh

EXPOSE 8888
