.PHONY: help test notebook build dev clean

# Python commands run through uv, using the versions pinned in uv.lock.

ROOT  := $(CURDIR)
BUILD := $(ROOT)/build

NOTEBOOK  ?= notebooks/array_sorting.py
PORT      ?= 2720
BOOK_PORT ?= 8000
# Path the site is served under, e.g. /algorithms-visualized. Set by CI.
BASE_URL  ?=
# Public address written into sitemap.xml and robots.txt. Set by CI.
SITE_URL  ?= http://localhost:$(BOOK_PORT)$(BASE_URL)

NOTEBOOKS  := array_sorting array_search hashing tree_search tree_insert \
              graph_traversal shortest_path mst
PSEUDOCODE := $(wildcard pseudocode/*.py pseudocode/*/*.py)
ALGOVIZ    := $(wildcard algoviz/*.py algoviz/presets/*.py)

help:
	@echo "make test                       run the test suite"
	@echo "make notebook [NOTEBOOK=...]    edit a notebook (default notebooks/array_sorting.py)"
	@echo "make build                      build the site into book/_build/  (npx)"
	@echo "make dev                        build the site and serve it on :$(BOOK_PORT)"
	@echo "make clean                      delete everything generated"

# ---------------------------------------------------------------------------
# Python
# ---------------------------------------------------------------------------
test:
	uv run pytest -q

# --no-skew-protection keeps open tabs working after a server restart.
notebook:
	uv run marimo edit $(NOTEBOOK) --port $(PORT) --no-skew-protection

# ---------------------------------------------------------------------------
# Website. Each page embeds its notebook, exported to run in the browser.
# ---------------------------------------------------------------------------
BOOK_HTML := book/_build/html
EMBEDS    := $(addprefix book/embed/,$(addsuffix .html,$(NOTEBOOKS)))

# Builds the site with mystmd, copies in the embeds, adds BASE_URL to the
# iframe links (MyST leaves them unprefixed) and writes SITE_URL into
# sitemap.xml and robots.txt. Old output is removed first because mystmd does
# not delete images from earlier builds.
build: $(EMBEDS) book/gifs/.stamp
	rm -rf $(BOOK_HTML) book/_build/site
	cd book && BASE_URL=$(BASE_URL) npx --yes mystmd@1.9.1 build --html
	mkdir -p $(BOOK_HTML)
	cp -R book/embed $(BOOK_HTML)/
	find $(BOOK_HTML) -path '$(BOOK_HTML)/embed' -prune -o \
		\( -name '*.html' -o -name '*.json' \) -type f -print0 \
		| xargs -0 perl -pi -e 's|"/embed/|"$(BASE_URL)/embed/|g'
	perl -pi -e 's|http://localhost:3000|$(SITE_URL)|g' \
		$(BOOK_HTML)/sitemap.xml $(BOOK_HTML)/robots.txt

# Bundle the notebook with algoviz/, export it, and merge the shared marimo
# assets into book/embed/ so all pages use one copy. The page itself becomes
# book/embed/<name>.html; the export's CLAUDE.md is skipped.
# --no-sandbox: use the marimo pinned in uv.lock.
# The export runs in build/standalone/, where it looks for css_file.
book/embed/%.html: notebooks/%.py $(ALGOVIZ) algoviz/notebook.css $(PSEUDOCODE) utils/bundle_wasm.py uv.lock
	uv run python utils/bundle_wasm.py $< -o build/standalone
	cd build/standalone && uv run marimo export html-wasm $*.py \
		-o $(BUILD)/wasm/$* --mode run --no-show-code --no-sandbox -f
	mkdir -p book/embed
	rsync -a --exclude index.html --exclude CLAUDE.md build/wasm/$*/ book/embed/
	cp build/wasm/$*/index.html $@

# Landing-page GIFs.
book/gifs/.stamp: $(ALGOVIZ) $(PSEUDOCODE) utils/make_gifs.py uv.lock
	uv run python utils/make_gifs.py -o book/gifs
	@touch $@

# Port 3000 in mystmd's output is its build server, not the site.
dev: build
	@echo
	@echo "  Site: http://localhost:$(BOOK_PORT)   (ignore mystmd's :3000, that was the build)"
	@echo
	python3 -m http.server $(BOOK_PORT) --directory $(BOOK_HTML)

# ---------------------------------------------------------------------------
clean:
	rm -rf $(BUILD) book/_build book/embed book/gifs
