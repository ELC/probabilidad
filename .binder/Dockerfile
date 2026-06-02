# binder-build: 4 — bump when changing this file to bust MyBinder layer cache
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

COPY --chown=${NB_UID}:${NB_GID} . /home/jovyan

USER root
RUN rm -rf /home/jovyan/.venv /home/jovyan/venv \
 && cd /home/jovyan \
 && env -u VIRTUAL_ENV uv sync --all-groups --locked \
 && chown -R ${NB_UID}:${NB_GID} /home/jovyan/venv

USER ${NB_UID}

# Register the project venv as a Jupyter kernel
RUN uv run -m ipykernel install \
     --prefix=/opt/conda               \
     --name=jupyter-book-template      \
     --display-name="Python 3.13 (uv)"

COPY --chown=${NB_UID}:${NB_GID} .binder/vscode/settings.json .vscode/settings.json

COPY --chown=${NB_UID}:${NB_GID} .binder/bashrc-venv.sh /tmp/bashrc-venv.sh
RUN cat /tmp/bashrc-venv.sh >> .bashrc && rm /tmp/bashrc-venv.sh

EXPOSE 8888
