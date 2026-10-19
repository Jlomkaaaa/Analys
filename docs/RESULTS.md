# Результаты проверок (реально выполнены, pip-audit 2.10.1, 14.10.2026, Python 3.12)

| Сценарий | Результат pip-audit |
|---|---|
| Файл `requirements.txt` (безопасный набор) | No known vulnerabilities found |
| Окружение с безопасным набором | находки только в `pip 24.0` (6 уязвимостей) и `nltk 3.10.3` — это зависимость утилиты safety, попавшая в то же venv |
| Окружение с `requirements.vulnerable.txt` | requests 2.19.0 — 5 (PYSEC-2018-28 = CVE-2018-18074, PYSEC-2023-74 = CVE-2023-32681, …); python-dotenv 0.21.1 — 1 (PYSEC-2026-2270 = CVE-2026-28684); транзитивные urllib3 1.23 — 12, idna 2.7 — 2 |
| Файл `requirements.vulnerable.txt` с резолвингом | 4 пакета с уязвимостями: idna 2.7, python-dotenv 0.21.1, requests 2.19.0, urllib3 1.23 (39 записей с дублями) |
| Старый набор из задания (PyYAML 5.3), `--no-deps` | requests 2.19.0 — 5, PyYAML 5.3 — 2 (PYSEC-2020-96, PYSEC-2021-142 = CVE-2020-14343), python-dotenv 0.21.1 — 1 |

Устаревшие, но без уязвимостей: SQLAlchemy 1.4.54, PyYAML 6.0.1 (pip-audit их не отмечает; видны в `pip list --outdated`).
Не проверено в песочнице (нет доступа к серверам): safety, Trivy, Dependabot, Docker.
