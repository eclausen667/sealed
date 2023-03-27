import json
import unittest

import main
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
        data = {VEHICLE_TYPE: VAN}
        spots[CAR] = 3
        spots[MOTORCYCLE] = 0
        spots[VAN] = 1
        main.parking_lot = [(VAN, 'o'), (CAR, 'o'), (CAR, 'o'), (CAR, 'o')]
        self.client.post('/parking_lot/park', json=data)
        data2 = {VEHICLE_TYPE: VAN}
        self.client.post('/parking_lot/park', json=data2)
        response = self.client.get('/parking_lot/van_spots_occupied')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data())
        self.assertIn("van spots:", data)
        self.assertIn("car spots:", data)

    def test_park_motorcycle(self):
        data = {VEHICLE_TYPE: MOTORCYCLE}
        spots[CAR] = 3
        spots[MOTORCYCLE] = 1
        spots[VAN] = 1
        main.parking_lot = [(CAR, 'o'), (CAR, 'o'), (CAR, 'o'), (MOTORCYCLE, 'o'), (VAN, 'o')]
        response = self.client.post('/parking_lot/park', json=data)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data())
        self.assertIn('Vehicle parked', data)

    def test_park_van(self):
        data = {VEHICLE_TYPE: VAN}
        spots[VAN] = 1
        main.parking_lot = [(VAN, 'o')]
        response = self.client.post('/parking_lot/park', json=data)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data())
        self.assertIn('Vehicle parked', data)

    def test_park_car(self):
        data = {VEHICLE_TYPE: CAR}
        main.parking_lot = [(CAR, 'o')]
        response = self.client.post('/parking_lot/park', json=data)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data())
        self.assertIn('Vehicle parked', data)

    def test_get_remaining_spots(self):
        data = {VEHICLE_TYPE: CAR}
        response = self.client.get('/parking_lot/remaining_spots', json=data)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data())
        self.assertIn('car', data)
        self.assertIn('motorcycle', data)
        self.assertIn('van', data)

    def test_park_car_in_van_spot(self):
        data = {VEHICLE_TYPE: MOTORCYCLE}
        spots[CAR] = 0
        spots[MOTORCYCLE] = 0
        spots[VAN] = 1
        parked_vans = len(parked_vehicles[VAN])
        van_spots = spots[VAN]
        main.parking_lot = [(VAN, 'o')]

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
        main.parking_lot = [(CAR, 'o')]
        parked_cars = len(parked_vehicles[CAR])
        car_spots = spots[CAR]
        response = self.client.post('/parking_lot/park', json=data)
        car_spots2 = spots[CAR]
        parked_cars2 = len(parked_vehicles[CAR])
        self.assertEqual(response.status_code, 200)
        self.assertGreater(car_spots, car_spots2)
        self.assertGreater(parked_cars2, parked_cars)

    def test_removing_van_from_car_spot(self):
        data = {VEHICLE_TYPE: VAN}
        spots[CAR] = 0
        spots[MOTORCYCLE] = 0
        spots[VAN] = 0
        parked_vehicles[CAR] = [VAN]
        parked_vehicles[VAN] = []
        parked_vehicles[MOTORCYCLE] = []
        car_spots = spots[CAR]
        parked_cars = len(parked_vehicles[CAR])
        main.parking_lot = [(CAR, VAN), (CAR, VAN), (CAR, VAN)]
        response = self.client.delete('/parking_lot/remove', json=data)
        car_spots2 = spots[CAR]
        parked_cars2 = len(parked_vehicles[CAR])
        self.assertEqual(response.status_code, 200)
        self.assertGreater(car_spots2, car_spots)
        self.assertEqual(main.parking_lot[0], (CAR, 'o'))
        self.assertGreater(parked_cars, parked_cars2)

    def test_adjacent_car_spots_for_van(self):
        data = {VEHICLE_TYPE: VAN}
        spots[CAR] = 3
        spots[MOTORCYCLE] = 0
        spots[VAN] = 0
        main.parking_lot = [(CAR, 'o'), (VAN, 'x'), (MOTORCYCLE, 'x'), (CAR, 'o'), (CAR, 'o'), (CAR, 'o')]
        response = self.client.post('/parking_lot/park', json=data)
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual('van', data['Vehicle parked'])

    def test_not_enough_adjacent_car_spots_for_van(self):
        data = {VEHICLE_TYPE: VAN}
        spots[CAR] = 3
        spots[MOTORCYCLE] = 0
        spots[VAN] = 0
        main.parking_lot = [(CAR, 'o'), (VAN, 'x'), (MOTORCYCLE, 'x')]
        response = self.client.post('/parking_lot/park', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Warning', json.loads(response.get_data()))

