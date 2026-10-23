#!/usr/bin/env bash
# Sobe o servidor MCP do Google Ads (stdio).
# Na 1ª vez cria um ambiente Python com as dependências em ~/.cache/google-ads-claude.
# Uso: run.sh            → inicia o servidor
#      run.sh --instalar → só prepara o ambiente (rode uma vez antes de abrir o Claude)
set -euo pipefail

DIR="$(cd "$(dirname "$0")" && pwd)"
REQ="$DIR/requirements.txt"
PY="${GOOGLE_ADS_PYTHON:-python3}"

if ! "$PY" -c 'import sys; sys.exit(sys.version_info < (3, 10))' 2>/dev/null; then
  echo "google-ads-claude: precisa de Python 3.10 ou mais novo (defina GOOGLE_ADS_PYTHON)." >&2
  exit 1
fi

HASH="$("$PY" -c 'import hashlib, sys; print(hashlib.sha256(open(sys.argv[1], "rb").read()).hexdigest()[:12])' "$REQ")"
VENV="${XDG_CACHE_HOME:-$HOME/.cache}/google-ads-claude/venv-$HASH"

if [ ! -x "$VENV/bin/python" ]; then
  echo "google-ads-claude: instalando dependências em $VENV (só na 1ª vez)..." >&2
  "$PY" -m venv "$VENV" >&2
  if ! "$VENV/bin/pip" install -q --disable-pip-version-check -r "$REQ" >&2; then
    rm -rf "$VENV"
    exit 1
  fi
fi

if [ "${1:-}" = "--instalar" ]; then
  echo "google-ads-claude: ambiente pronto em $VENV" >&2
  exit 0
fi

exec "$VENV/bin/python" -I "$DIR/server.py"
