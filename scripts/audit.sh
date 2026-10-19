#!/usr/bin/env sh
# Использование: scripts/audit.sh [requirements-файл]  (запускать внутри контейнера)
REQ="${1:-/work/app/requirements.txt}"
mkdir -p /reports
echo "### pip-audit: окружение приложения"
pip-audit --path "$(/opt/appenv/bin/python -c 'import sysconfig;print(sysconfig.get_paths()["purelib"])')" -f json -o /reports/pip-audit-env.json; pip-audit --path "$(/opt/appenv/bin/python -c 'import sysconfig;print(sysconfig.get_paths()["purelib"])')"
echo "### pip-audit: файл $REQ"
pip-audit -r "$REQ" -f json -o /reports/pip-audit-file.json; pip-audit -r "$REQ"
echo "### safety: файл $REQ (нужен интернет; в новых версиях — safety scan после auth login)"
safety check -r "$REQ" --json --output /reports/safety-file.json; safety check -r "$REQ"
