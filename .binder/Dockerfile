FROM ghcr.io/rocker-org/binder:4.4.2

COPY --from=ghcr.io/astral-sh/uv:0.11.18 /uv /uvx /bin/

WORKDIR /home/jovyan/

# Rocker sets VIRTUAL_ENV=/opt/conda; project deps live in .venv (unset per RUN below).
ENV VIRTUAL_ENV=

# See .dockerignore — must not copy a host/CI .venv into the image.
COPY --chown=jovyan . /home/jovyan

USER root
RUN rm -rf /home/jovyan/.venv

USER jovyan
RUN env -u VIRTUAL_ENV uv sync --all-groups --locked

# Register the .venv as a kernel for /opt/conda/bin/jupyter so that it is
# discoverable in JupyterLab interface when the container is started
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
