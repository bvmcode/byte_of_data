def test_main(client):
    resp = client.get("/")
    html = resp.data.decode()
    assert resp.status_code == 200
    assert "<h1>hello world</h1>" in html
