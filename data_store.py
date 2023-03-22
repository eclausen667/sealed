def initialize(motorcycle_spots: int, car_spots: int, van_spots: int) -> [dict[str, int], dict[str, int]]:
    spots = {'motorcycle': motorcycle_spots, 'car': car_spots,
             'van': van_spots}
    parked_vehicles = {'van': [], 'car': [], 'motorcycle': []}
    return spots, parked_vehicles
