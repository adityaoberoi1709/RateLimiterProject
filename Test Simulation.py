import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from fastapi.testclient import TestClient
client = TestClient(app)
def make_request():
    response = client.get("/data")
    return response.status_code,response.json()
def test_concurrent_requests():
    limiter.set_limits(max_request = 5,window_time = 3)
    num_threads = 10
    result = []
    with ThreadPoolExecutor(max_workers = num_threads) as executor:
        futures = [executor.submit(make_request) for _ in range(num_threads)]
        for future in as_completed(futures):
            result.append(future.result())     
    allowed = [r for r in result if r[0] == 200]
    blocked = [r for r in result if r[0] == 429]
    print(f"Allowed requests: {len(allowed)}")
    print(f"Blocked requests: {len(blocked)}")
    assert len(allowed) == limiter.request
    assert len(blocked) == num_threads - limiter.request
val = test_concurrent_requests()
