#!/usr/bin/env bash
#
# One-shot build: protect ./src with obfy, then bundle it with PyInstaller.
# Re-run from a clean tree any time. Use the SAME Python you ship for, because
# obfy's marshal/bytecode format is interpreter-version specific.
set -euo pipefail

PYTHON="${PYTHON:-python3}"

# 1. Obfuscate + encrypt ./src into ./protected (a drop-in mirror).
rm -rf protected
obfy build --src ./src --out ./protected --python "$PYTHON" --level 5

# 2. Bundle the protected mirror into a single executable.
rm -rf build dist
pyinstaller --noconfirm app.spec

echo
echo "Done. Run it with:  ./dist/app"
