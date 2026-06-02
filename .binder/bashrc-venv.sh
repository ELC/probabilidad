# Rocker sets VIRTUAL_ENV=/opt/conda; drop it so we use the uv .venv below.
unset VIRTUAL_ENV

# Deactivate any conda environment (e.g. base)
conda deactivate &>/dev/null

# Then activate our uv-created venv
if [ -f "$HOME/.venv/bin/activate" ]; then
    . "$HOME/.venv/bin/activate"
fi
