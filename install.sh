#!/usr/bin/env bash
# Minimal installer for the runtime-classifier framework.
#
# What this does:
#   1. Verifies python3 is available.
#   2. Installs the one runtime dep (requests) — only one because the worker
#      is intentionally dependency-light.
#   3. Copies .env.example to .env if .env doesn't already exist.
#   4. Reminds you to set OPENAI_API_KEY in .env.
#
# What this does NOT do:
#   - Set your API key (you'll do that manually in .env)
#   - Run any analysis or generation
#   - Install anything globally
#
# Usage: bash install.sh

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$REPO_ROOT"

echo "==> Checking python3..."
if ! command -v python3 >/dev/null 2>&1; then
  echo "ERROR: python3 not found. Install Python 3.9+ and re-run." >&2
  exit 1
fi
PY_VERSION="$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')"
echo "    found python3 ($PY_VERSION)"

echo "==> Installing runtime dependency (requests)..."
python3 -m pip install --quiet requests
echo "    ok"

echo "==> Setting up .env..."
if [ -f .env ]; then
  echo "    .env already exists — leaving it alone"
else
  cp .env.example .env
  echo "    copied .env.example → .env"
fi

cat <<'NOTES'

==> Done.

Next steps:
  1. Edit .env and set OPENAI_API_KEY=sk-...
  2. (Optional) Try the photography example:
       python3 scripts/photography_agent.py \
         --prompt "Couple at NYC farmer's market, golden hour" \
         --batch-name install-test
     Outputs land in output/generation/install-test/.
  3. Read docs/01-README.md to author your own classifier.

NOTES
