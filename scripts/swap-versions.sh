#!/usr/bin/env sh
# Переключение между безопасными и тестовыми (уязвимыми/устаревшими) зависимостями.
cd "$(dirname "$0")/../app" || exit 1
case "$1" in
  vulnerable) cp requirements.vulnerable.txt requirements.txt ;;
  restore)    cp requirements.orig.txt requirements.txt ;;
  *) echo "usage: $0 vulnerable|restore"; exit 1 ;;
esac
cat requirements.txt
