# Algorithms Visualized

Live site: <https://algorithms-visualized.com>

Install Homebrew, uv and Node.js:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

brew install uv node
```

## Quick start

```bash
git clone https://github.com/gavinkhung/algorithms-visualized.git
cd algorithms-visualized

# install the packages
uv sync

make help
```

Build the website and serve it at <http://localhost:8000>:

```bash
make dev
```

Open a notebook in marimo's editor (at <http://localhost:2720>):

```bash
make notebook NOTEBOOK=notebooks/array_sorting.py
```
