import requests
import time

API = "http://localhost:8000"


def test_create_and_track():
    # Create campaign
    r = requests.post(f"{API}/campaigns", params={"name": "test-camp", "description": "desc"})
    assert r.status_code == 200
    cid = r.json().get("id")
    assert cid

    # Simulate click
    r2 = requests.get(f"{API}/r/{cid}?email=test%40example.com")
    assert r2.status_code == 200

    # Allow DB commit
    time.sleep(0.2)

    # Check stats
    r3 = requests.get(f"{API}/campaigns/{cid}/stats")
    assert r3.status_code == 200
    data = r3.json()
    assert data["total"] >= 1
    assert data["clicked"] >= 1


if __name__ == '__main__':
    test_create_and_track()
    print('OK')
