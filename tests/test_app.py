import re
from html import unescape

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_home_links_all_practices():
    response = client.get("/")
    assert response.status_code == 200
    for path in ("/sound/", "/oracle/", "/natal/", "/tarot/"):
        assert path in response.text
    assert client.get("/site.css").status_code == 200


def test_primary_navigation_is_consistent_across_features():
    expected = ["Casa Arcana", "Oráculo", "Mapa astral", "Tarot", "Chakras", "Frequências"]
    pages = ("/", "/sound/", "/sound/frequencies", "/oracle/", "/natal/", "/natal/glossary", "/tarot/")
    for path in pages:
        response = client.get(path)
        assert response.status_code == 200, path
        nav = re.search(r'<nav class="unified-nav" aria-label="Navegação principal">(.*?)</nav>', response.text, re.S)
        assert nav is not None, path
        for label in expected:
            assert label in nav.group(1), (path, label)
    assert "Frequências" in client.get("/sound/").text
    assert "Glossário" in client.get("/natal/").text
    assert "Fraunces" not in client.get("/sound/").text
    assert "Source Serif" not in client.get("/natal/").text


def test_shared_styles_define_consistent_controls():
    css = client.get("/site.css").text
    assert ".btn-primary, .btn-ghost, .btn-generate" in css
    assert "font-family: var(--font-body)" in css
    assert "min-height: 44px" in css


def test_home_has_four_short_module_cards():
    cards = re.findall(r'<a class="practice [^"]+".*?<h2>(.*?)</h2><p>(.*?)</p>', client.get("/").text, re.S)
    assert len(cards) == 4
    assert [unescape(title) for title, _ in cards] == [
        "Sons & frequências",
        "Oráculo astrológico",
        "Mapa natal",
        "Tarot",
    ]
    assert all(len(description.split()) <= 10 for _, description in cards)


def test_sound_tools_are_integrated_into_main_navigation():
    for path, current in (("/sound/", "Chakras"), ("/sound/frequencies", "Frequências")):
        response = client.get(path)
        nav = re.search(r'<nav class="unified-nav" aria-label="Navegação principal">(.*?)</nav>', response.text, re.S)
        assert nav is not None
        assert re.search(rf'<a href="[^"]+" aria-current="page">{current}</a>', nav.group(1))
        assert 'aria-label="Ferramentas de som"' not in response.text


def test_feature_pages_and_scoped_assets_render():
    for path in ("/sound/", "/sound/frequencies", "/oracle/", "/natal/", "/natal/glossary", "/tarot/"):
        response = client.get(path)
        assert response.status_code == 200, path

    assert client.get("/sound/static/css/app.css").status_code == 200
    assert client.get("/oracle/static/styles.css").status_code == 200
    assert client.get("/natal/static/js/index.js").status_code == 200
    assert client.get("/tarot/static/img/card-back.png").status_code == 200
    assert "/site.css" in client.get("/sound/").text
    assert "/site.css" in client.get("/oracle/").text
    assert "/site.css" in client.get("/natal/").text
    assert "/site.css" in client.get("/tarot/").text
    assert "bulma.min.css" not in client.get("/tarot/").text


def test_feature_api_routes_are_scoped():
    assert client.get("/natal/api/glossary").status_code == 200
    response = client.post("/tarot/reading", json={"reading_type": "one-card"})
    assert response.status_code == 200
    payload = response.json()
    assert len(payload["questions_and_cards"]) == 1
    assert payload["questions_and_cards"][0][1]["image_link"].startswith("/tarot/static/")


def test_unknown_tarot_spread_returns_validation_error():
    response = client.post("/tarot/reading", json={"reading_type": "unknown"})
    assert response.status_code == 422
