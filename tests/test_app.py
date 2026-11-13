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
    expected = ["Sons", "Oráculo", "Mapa astral", "Tarot"]
    pages = ("/sound/", "/oracle/", "/natal/", "/natal/glossary", "/tarot/")
    for path in pages:
        response = client.get(path)
        assert response.status_code == 200, path
        for label in expected:
            assert label in response.text, (path, label)
    assert "Frequências" in client.get("/sound/").text
    assert "Glossário" in client.get("/natal/").text
    assert "Fraunces" not in client.get("/sound/").text
    assert "Source Serif" not in client.get("/natal/").text


def test_shared_styles_define_consistent_controls():
    css = client.get("/site.css").text
    assert ".btn-primary, .btn-generate, .tarot-container .button" in css
    assert "font-family: var(--font-body)" in css
    assert "min-height: 44px" in css


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
