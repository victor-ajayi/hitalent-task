from app import schemas


class TestReservations:
    URL = "/reservations"

    def test_get_reservations(self, client, test_reservations):
        response = client.get(self.URL)
        assert response.status_code == 200
        reservations = [schemas.Reservation(**res) for res in response.json()]
        assert len(reservations) == len(test_reservations)

    def test_create_reservation(self, client, test_tables):
        res = {
            "customer_name": "Nikita",
            "phone_number": "+79001234567",
            "table_id": 1,
            "reservation_time": "2025-04-16 12:00:00",
            "duration_minutes": 120,
        }
        response = client.post(self.URL, json=res)
        assert response.status_code == 201

    def test_create_invalid_reservation(self, client, test_reservations):
        res = {
            "customer_name": "Nikita",
            "phone_number": "+79001234567",
            "table_id": 2,
            "reservation_time": "2025-04-15 13:00:00",
            "duration_minutes": 30,
        }
        response = client.post(self.URL, json=res)
        assert response.status_code == 400

    def test_delete_reservation(self, client, test_reservations):
        response = client.delete(f"{self.URL}/1")
        assert response.status_code == 204
