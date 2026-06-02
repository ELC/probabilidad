FROM ghcr.io/rocker-org/binder:4.4.2

COPY --from=ghcr.io/astral-sh/uv:0.11.18 /uv /uvx /bin/

WORKDIR /home/jovyan/

# Rocker sets VIRTUAL_ENV=/opt/conda. Use a dedicated project venv path (not .venv) so a
# copied host .venv cannot block `uv sync` with permission errors on .venv/.lock.
ENV VIRTUAL_ENV=
ENV UV_PROJECT_ENVIRONMENT=/home/jovyan/venv

COPY --chown=jovyan . /home/jovyan

# Root can always remove a stale copied .venv; then create /home/jovyan/venv for jovyan.
USER root
RUN rm -rf /home/jovyan/.venv /home/jovyan/venv \
 && cd /home/jovyan \
 && env -u VIRTUAL_ENV uv sync --all-groups --locked \
 && chown -R jovyan:jovyan /home/jovyan/venv

USER jovyan

# Register the project venv as a Jupyter kernel
RUN uv run -m ipykernel install \
     --prefix=/opt/conda               \
     --name=jupyter-book-template      \
     --display-name="Python 3.13 (uv)"

COPY --chown=jovyan .binder/vscode/settings.json .vscode/settings.json

RUN --mount=type=bind,source=.binder/bashrc-venv.sh,target=/mnt/bashrc-venv.sh,readonly \
    cat /mnt/bashrc-venv.sh >> .bashrc

EXPOSE 8888
