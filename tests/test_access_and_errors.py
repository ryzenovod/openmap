from __future__ import annotations


def test_import_role_forbidden(client):
    payload = (
        "nrec,addr,razdel,fio,godr,dreg,gdu,cv,mbt,work,diagnoz,found,address,shirota,dolgota\n"
    )
    response = client.post(
        "/api/v1/imports/cases",
        files={"file": ("sample.csv", payload.encode("utf-8"), "text/csv")},
        headers={"X-Role": "viewer"},
    )
    assert response.status_code == 403
    assert response.json()["error"]["code"] == "forbidden"


def test_unknown_role_error(client):
    response = client.get("/api/v1/territories", headers={"X-Role": "stranger"})
    assert response.status_code == 403
    assert response.json()["error"]["code"] == "forbidden"


def test_import_validation_error_envelope(client):
    response = client.post(
        "/api/v1/imports/cases",
        files={"file": ("sample.txt", b"hello", "text/plain")},
        headers={"X-Role": "doctor"},
    )
    assert response.status_code == 400
    assert response.json()["error"]["code"] == "import_error"


def test_pagination_query_validation(client):
    response = client.get("/api/v1/dictionaries/mkb10?limit=0")
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "request_validation_error"
