import random
from typing import List, Tuple


def create_random_parking_lot(motorcycle_spots: int, car_spots: int, van_spots: int) -> List[Tuple[str, str]]:
    parking_lot = []
    for i in range(0, motorcycle_spots):
        parking_lot.append(('motorcycle', 'o'))
    for i in range(0, car_spots):
        parking_lot.append(('car', 'o'))
    for i in range(0, van_spots):
        parking_lot.append(('van', 'o'))
    random.shuffle(parking_lot)
    return parking_lot


def initialize(motorcycle_spots: int, car_spots: int, van_spots: int) -> \
        (dict[str, int], dict[str, int], dict[str, str]):
    spots = {'motorcycle': motorcycle_spots, 'car': car_spots,
             'van': van_spots}
    parked_vehicles = {'van': [], 'car': [], 'motorcycle': []}
    parking_lot = create_random_parking_lot(motorcycle_spots, car_spots, van_spots)
    return spots, parked_vehicles, parking_lot
