from __future__ import annotations

from app.db.models.core import DictMkb10, Territory


def test_health(client) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_territories_and_tree(client, db_session) -> None:
    db_session.add_all(
        [
            Territory(id=1, name="RF", parent_id=None, territory_type_code="country"),
            Territory(id=2, name="PK", parent_id=1, territory_type_code="region"),
            Territory(id=3, name="City", parent_id=2, territory_type_code="municipality"),
        ]
    )
    db_session.commit()

    flat = client.get("/api/v1/territories")
    tree = client.get("/api/v1/territories/tree")

    assert flat.status_code == 200
    assert len(flat.json()) == 3
    assert tree.status_code == 200
    assert tree.json()[0]["children"][0]["children"][0]["name"] == "City"


def test_imports_endpoint(client) -> None:
    payload = "nrec,addr,razdel,fio,godr,dreg,gdu,cv,mbt,work,diagnoz,found,address,shirota,dolgota\n1001,Addr,A,IVANOV,1985,23.04.2025,IА+,+,-,work,A15.0,1,Addr,,\n"

    response = client.post(
        "/api/v1/imports/cases",
        files={"file": ("sample.csv", payload.encode("utf-8"), "text/csv")},
    )
    assert response.status_code == 200
    assert response.json()["success_rows"] == 1

    imports = client.get("/api/v1/imports")
    assert imports.status_code == 200
    assert len(imports.json()) == 1


def test_mkb10_and_cases_endpoints(client, db_session) -> None:
    db_session.add(DictMkb10(id=1, parent_id=None, code="A00", name="Test"))
    db_session.commit()

    mkb = client.get("/api/v1/dictionaries/mkb10")
    assert mkb.status_code == 200
    assert mkb.json()[0]["code"] == "A00"

    cases = client.get("/api/v1/cases")
    assert cases.status_code == 200
    if cases.json():
        case_id = cases.json()[0]["id"]
        detail = client.get(f"/api/v1/cases/{case_id}")
        assert detail.status_code == 200
