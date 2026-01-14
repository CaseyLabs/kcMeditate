.PHONY: serve serve-sw test

PORT ?= 8000

serve:
	python3 -m http.server $(PORT)

serve-sw:
	python3 -m http.server $(PORT) --bind 127.0.0.1

test:
	python3 scripts/validate_assets.py
