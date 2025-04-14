class TestTables:
    URL = "/tables"

    def test_create_table(self, client):
        response = client.post(
            self.URL, json={"name": "Table", "seats": 2, "location": "TERRACE"}
        )
        assert response.status_code == 201

    def test_get_tables(self, client):
        response = client.get(self.URL)
        assert response.json() is not None

    def test_delete_table(self, client, test_tables):
        response = client.delete(f"{self.URL}/1")
        assert response.status_code == 204
