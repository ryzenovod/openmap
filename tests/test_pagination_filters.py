from __future__ import annotations

from app.db.models.core import DictMkb10


def test_pagination_and_sorting(client, db_session):
    db_session.add_all(
        [
            DictMkb10(id=1, parent_id=None, code="B00", name="B"),
            DictMkb10(id=2, parent_id=None, code="A00", name="A"),
        ]
    )
    db_session.commit()

    response = client.get("/api/v1/dictionaries/mkb10?limit=1&offset=0&sort_by=code&sort_order=asc")
    assert response.status_code == 200
    body = response.json()
    assert body["meta"]["limit"] == 1
    assert body["meta"]["count"] == 1
    assert body["data"][0]["code"] == "A00"
