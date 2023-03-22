import json
import unittest
from main import app, parked_vehicles, spots, MOTORCYCLE, CAR, VAN, VEHICLE_TYPE

class ParkingLotTest(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    def test_get_status(self):
        response = self.client.get('/parking_lot/remaining_spots')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data())
        self.assertIn(MOTORCYCLE, data)
        self.assertIn(CAR, data)
        self.assertIn(VAN, data)

    def test_is_full(self):
        response = self.client.get('/parking_lot/is_full')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data())
        self.assertIn('is_full', data)

    def test_van_spots_occupied(self):
        response = self.client.get('/parking_lot/van_spots_occupied')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data())
        self.assertIn("message", data)

    def test_park_motorcycle(self):
        data = {VEHICLE_TYPE: MOTORCYCLE}
        response = self.client.post('/parking_lot/park', json=data)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data())
        self.assertIn('message', data)

    def test_park_van(self):
        data = {VEHICLE_TYPE: VAN}
        response = self.client.post('/parking_lot/park', json=data)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data())
        self.assertIn('message', data)

    def test_park_car(self):
        data = {VEHICLE_TYPE: CAR}
        response = self.client.post('/parking_lot/park', json=data)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data())
        self.assertIn('message', data)

    def test_park_car_in_van_spot(self):
        data = {VEHICLE_TYPE: MOTORCYCLE}
        spots[CAR] = 0
        spots[MOTORCYCLE] = 0
        spots[VAN] = 1
        parked_vans = len(parked_vehicles[VAN])
        van_spots = spots[VAN]
        response = self.client.post('/parking_lot/park', json=data)
        van_spots2 = spots[VAN]
        parked_vans2 = len(parked_vehicles[VAN])
        self.assertEqual(response.status_code, 200)
        self.assertGreater(van_spots, van_spots2)
        self.assertGreater(parked_vans2, parked_vans)

    def test_park_motorcycle_in_van_spot(self):
        data = {VEHICLE_TYPE: MOTORCYCLE}
        spots[CAR] = 0
        spots[MOTORCYCLE] = 0
        spots[VAN] = 1
        parked_vans = len(parked_vehicles[VAN])
        van_spots = spots[VAN]
        response = self.client.post('/parking_lot/park', json=data)
        van_spots2 = spots[VAN]
        parked_vans2 = len(parked_vehicles[VAN])
        self.assertEqual(response.status_code, 200)
        self.assertGreater(van_spots, van_spots2)
        self.assertGreater(parked_vans2, parked_vans)

    def test_motorcycle_uses_car_spot(self):
        data = {VEHICLE_TYPE: MOTORCYCLE}
        spots[CAR] = 1
        spots[MOTORCYCLE] = 0
        spots[VAN] = 0
        parked_cars = len(parked_vehicles[CAR])
        car_spots = spots[CAR]
        response = self.client.post('/parking_lot/park', json=data)
        car_spots2 = spots[CAR]
        parked_cars2 = len(parked_vehicles[CAR])
        self.assertEqual(response.status_code, 200)
        self.assertGreater(car_spots, car_spots2)
        self.assertGreater(parked_cars2, parked_cars)

