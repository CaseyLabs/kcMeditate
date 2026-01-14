import json
import os
import re
import sys


ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def fail(message):
    print(f"ERROR: {message}")
    sys.exit(1)


def read_file(path):
    with open(path, "r", encoding="utf-8") as handle:
        return handle.read()


def ensure_exists(path, label=None):
    if not os.path.exists(path):
        suffix = f" ({label})" if label else ""
        fail(f"Missing required file: {path}{suffix}")


def resolve_asset(asset):
    if asset in (".", "./"):
        return ROOT
    if asset.startswith("./"):
        asset = asset[2:]
    return os.path.join(ROOT, asset)


def validate_core_assets():
    sw_path = os.path.join(ROOT, "service-worker.js")
    ensure_exists(sw_path, "service worker")
    content = read_file(sw_path)

    match = re.search(r"CORE_ASSETS\s*=\s*\[(.*?)\];", content, re.S)
    if not match:
        fail("Could not locate CORE_ASSETS array in service-worker.js")

    assets = re.findall(r"'([^']+)'", match.group(1))
    if not assets:
        fail("CORE_ASSETS list appears empty in service-worker.js")

    for asset in assets:
        asset_path = resolve_asset(asset)
        ensure_exists(asset_path, f"CORE_ASSETS entry: {asset}")


def validate_manifest_icons():
    manifest_path = os.path.join(ROOT, "manifest.webmanifest")
    ensure_exists(manifest_path, "manifest")

    data = json.loads(read_file(manifest_path))
    icons = data.get("icons", [])
    if not icons:
        fail("Manifest does not define any icons")

    for icon in icons:
        src = icon.get("src")
        if not src:
            fail("Manifest icon entry missing src")
        icon_path = os.path.join(ROOT, src)
        ensure_exists(icon_path, f"manifest icon: {src}")


def main():
    required = [
        "index.html",
        "offline.html",
        "service-worker.js",
        "manifest.webmanifest",
    ]
    for filename in required:
        ensure_exists(os.path.join(ROOT, filename))

    validate_core_assets()
    validate_manifest_icons()
    print("OK: asset validation passed")


if __name__ == "__main__":
    main()
