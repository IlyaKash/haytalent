import pytest

@pytest.mark.asyncio
async def test_read_empty_questions(client):
    """Тест пустого списка вопросов"""
    response = await client.get("/questions/")
    assert response.status_code == 200
    data = response.json()
    assert data == []

@pytest.mark.asyncio
async def test_create_question_and_list(client):
    payload = {"text": "Че спишь?", "user_id": "11111111-1111-1111-1111-111111111111"}
    resp = await client.post("/questions/", json=payload)
    assert resp.status_code == 201
    created = resp.json()
    assert created["text"] == payload["text"]
    assert "id" in created

    resp = await client.get("/questions/")
    assert resp.status_code == 200
    data = resp.json()
    assert any(q["id"] == created["id"] for q in data)