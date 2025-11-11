from fastapi.testclient import TestClient
from psybook.main import app

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}

def test_slots_and_booking_flow():
    # 1) получаем слоты на конкретный день
    r = client.get("/api/v1/slots", params={"day": "2025-11-11"})
    assert r.status_code == 200
    slots = r.json()
    assert len(slots) >= 1
    first_slot = next(s for s in slots if s["available"])

    # 2) бронируем первый доступный
    r = client.post("/api/v1/bookings", json={
        "slot_id": first_slot["slot_id"],
        "name": "Alice",
        "email": "alice@example.com",
    })
    assert r.status_code == 201
    booking = r.json()
    assert booking["slot_id"] == first_slot["slot_id"]

    # 3) повторная бронь того же слота — конфликт
    r = client.post("/api/v1/bookings", json={
        "slot_id": first_slot["slot_id"],
        "name": "Bob",
        "email": "bob@example.com",
    })
    assert r.status_code == 409

    # 4) отменяем бронь
    r = client.post("/api/v1/bookings/cancel", json={
        "booking_id": booking["booking_id"],
        "email": "alice@example.com",
    })
    assert r.status_code == 204