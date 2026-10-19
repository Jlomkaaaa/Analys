"""Небольшое учебное приложение: API заметок + проверка внешнего URL."""
import os
import yaml
import requests
from dotenv import load_dotenv
from flask import Flask, jsonify, request, render_template_string
from sqlalchemy import create_engine, text

load_dotenv()
app = Flask(__name__)
engine = create_engine(os.getenv("DATABASE_URL", "sqlite:///notes.db"))

with engine.begin() as conn:
    conn.execute(text("CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY, title TEXT, body TEXT)"))

PAGE = "<h1>Notes ({{ n }})</h1><ul>{% for t in titles %}<li>{{ t }}</li>{% endfor %}</ul>"


@app.get("/")
def index():
    with engine.connect() as conn:
        titles = [r[0] for r in conn.execute(text("SELECT title FROM notes"))]
    return render_template_string(PAGE, n=len(titles), titles=titles)


@app.get("/health")
def health():
    return jsonify(status="ok", requests=requests.__version__, pyyaml=yaml.__version__)


@app.post("/notes")
def add_note():
    data = request.get_json(force=True)
    with engine.begin() as conn:
        conn.execute(text("INSERT INTO notes(title, body) VALUES (:t, :b)"),
                     {"t": data.get("title", ""), "b": data.get("body", "")})
    return jsonify(created=True), 201


@app.get("/notes")
def list_notes():
    with engine.connect() as conn:
        rows = conn.execute(text("SELECT id, title, body FROM notes")).mappings().all()
    return jsonify([dict(r) for r in rows])


@app.post("/config/parse")
def parse_config():
    """Разбор YAML-конфига (безопасный загрузчик)."""
    return jsonify(yaml.safe_load(request.data.decode()))


@app.get("/ping")
def ping():
    url = request.args.get("url", "https://example.com")
    return jsonify(status=requests.head(url, timeout=5).status_code)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")))
