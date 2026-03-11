#!/bin/bash
# ═══════════════════════════════════════════════════════════════
# PythonQuest — build.sh
# Packages the Flask app into a single standalone executable
# using PyInstaller. Run this once to create the binary.
#
# Requirements:
#   pip install pyinstaller flask
#
# Usage:
#   chmod +x build.sh
#   ./build.sh
#
# Output:
#   dist/PythonQuest          (Linux/macOS)
#   dist/PythonQuest.exe      (Windows — run from Windows)
# ═══════════════════════════════════════════════════════════════

set -e

echo ""
echo "╔══════════════════════════════════════════╗"
echo "║     🐍 PythonQuest — Build Script        ║"
echo "╚══════════════════════════════════════════╝"
echo ""

# Check dependencies
echo "→ Checking dependencies…"
python3 -c "import flask"    2>/dev/null || { echo "❌ Flask not found. Run: pip install flask"; exit 1; }
python3 -c "import PyInstaller" 2>/dev/null || { echo "❌ PyInstaller not found. Run: pip install pyinstaller"; exit 1; }

echo "✅ Dependencies OK"
echo ""
echo "→ Cleaning previous build…"
rm -rf build dist PythonQuest.spec

echo "→ Running PyInstaller…"
pyinstaller \
  --onefile \
  --name PythonQuest \
  --add-data "templates:templates" \
  --add-data "static:static" \
  --hidden-import flask \
  --hidden-import jinja2 \
  --hidden-import werkzeug \
  --hidden-import click \
  --hidden-import itsdangerous \
  app.py

echo ""
echo "╔══════════════════════════════════════════╗"
echo "║  ✅ Build complete!                       ║"
echo "║                                          ║"
echo "║  Run the app:  ./dist/PythonQuest        ║"
echo "║                                          ║"
echo "║  The app opens automatically in your    ║"
echo "║  browser at http://127.0.0.1:5000        ║"
echo "╚══════════════════════════════════════════╝"
echo ""
