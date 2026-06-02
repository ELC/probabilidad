FROM ghcr.io/rocker-org/binder:4.4.2

COPY --from=ghcr.io/astral-sh/uv:0.11.18 /uv /uvx /bin/

WORKDIR /home/jovyan/

# Base image sets VIRTUAL_ENV=/opt/conda; use the project .venv from uv sync instead.
ENV VIRTUAL_ENV=

# Copy project (see .dockerignore). Strip any .venv from the build context — CI runs
# `uv sync` before `docker build`, and a copied host venv breaks uv with permission errors.
COPY --chown=jovyan . /home/jovyan
RUN rm -rf /home/jovyan/.venv

USER jovyan
RUN uv sync --all-groups --locked

# Register the .venv as a kernel for /opt/conda/bin/jupyter so that it is
#discoverable in JupyterLab interface when the container is started
RUN uv run -m ipykernel install \
     --prefix=/opt/conda               \
     --name=jupyter-book-template      \
     --display-name="Python 3.13 (uv)"

# Pre-register the environment for VS Code (code-server) in the container
COPY --chown=jovyan .binder/vscode/settings.json .vscode/settings.json

# Use the uv-created venv by default in interactive shells
RUN --mount=type=bind,source=.binder/bashrc-venv.sh,target=/mnt/bashrc-venv.sh,readonly \
    cat /mnt/bashrc-venv.sh >> .bashrc

EXPOSE 8888
