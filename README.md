# sca-lab — учебный проект для практики по SCA

Мини-приложение на Flask (заметки, разбор YAML, проверка URL) для отработки pip-audit, safety, Dependabot и Trivy.

## Структура
- `app/` — приложение; `requirements.txt` (безопасный набор), `requirements.vulnerable.txt` (2 уязвимые + 2 устаревшие версии), `requirements.orig.txt` (копия безопасного)
- `docker/` — Dockerfile для Debian, Alpine, Windows
- `.github/` — `dependabot.yml`, workflows (CI + pip-audit, Dependency Review)
- `scripts/` — `audit.sh`, `swap-versions.sh`; `docs/RESULTS.md` — результаты проверок

## Запуск
```
python -m venv .venv && . .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r app/requirements.txt pytest
pytest -q tests && python app/main.py
```

## Docker (Linux-контейнеры)
```
docker build -f docker/Dockerfile.debian -t sca-debian .
docker build -f docker/Dockerfile.alpine -t sca-alpine .
docker run -it --rm -v "$PWD/reports:/reports" sca-debian
# внутри:  /work/scripts/audit.sh  (скрипты смонтируйте -v "$PWD/scripts:/work/scripts")
```
Windows (режим Windows containers): `docker build -f docker/Dockerfile.windows -t sca-windows .`

## Подмена версий для задания
```
scripts/swap-versions.sh vulnerable   # затем пересобрать образ / pip install -r
scripts/swap-versions.sh restore
```

## Trivy
```
trivy fs ./                                        # или через docker run aquasec/trivy fs /src
trivy fs --format template --template "@contrib/html.tpl" -o reports/trivy.html ./
```
