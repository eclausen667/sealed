import json
from data_store import initialize
from flask import Flask, request, jsonify

app = Flask(__name__)

MOTORCYCLE = "motorcycle"
VAN = "van"
CAR = "car"
VEHICLE_TYPE = "vehicle_type"

# can adjust the numbers below to modify the number of spots
NUMBER_OF_MOTORCYCLE_SPOTS = 3
NUMBER_OF_CAR_SPOTS = 1
NUMBER_OF_VAN_SPOTS = 1


def modify_parking_lot_for_van(spot_location, spot_value):
    parking_lot[spot_location - 2] = (CAR, spot_value)
    parking_lot[spot_location - 1] = (CAR, spot_value)
    parking_lot[spot_location] = (CAR, spot_value)


def check_open_car_spots_for_van():
    temp = ""
    for i in range(0, len(parking_lot)):
        if parking_lot[i][0] == MOTORCYCLE or parking_lot[i][0] == VAN or parking_lot[i][1] != 'o':
            temp = ""
        else:
            temp += parking_lot[i][1]
            if 'ooo' in temp:
                modify_parking_lot_for_van(i, VAN)
                return True
    return False


def check_closed_car_spots_for_van():
    temp = ""
    for i in range(0, len(parking_lot)):
        if parking_lot[i][0] == MOTORCYCLE or parking_lot[i][0] == VAN or parking_lot[i][1] == "o":
            temp = ""
        else:
            temp += parking_lot[i][1]
            if "vanvanvan" in temp:
                modify_parking_lot_for_van(i, "o")
                return True
    return False


def park_helper(vehicle_type: str, spot_type: str) -> json:
    """check if the parking lot is full."""
    if vehicle_type == VAN and spot_type == CAR:
        is_spot = check_open_car_spots_for_van()
        if is_spot:
            spots[spot_type] -= 3
        else:
            return jsonify({"Warning": "Not enough adjacent car spots for van"})
    else:
        spots[spot_type] -= 1
        parking_lot[parking_lot.index((spot_type, 'o'))] = (spot_type, vehicle_type)
    pv = parked_vehicles[spot_type]
    pv.append(vehicle_type)
    parked_vehicles[spot_type] = pv
    return jsonify({"Vehicle parked": vehicle_type})


def motorcycle_helper() -> json:
    """help to park a motorcycle."""
    if spots[MOTORCYCLE] == 0 and spots[VAN] == 0 and spots[CAR] == 0:
        return jsonify({"message": "No available motorcycle spots"})
    elif spots[MOTORCYCLE] > 0:
        return park_helper(MOTORCYCLE, MOTORCYCLE)
    elif spots[CAR] > 0:
        return park_helper(MOTORCYCLE, CAR)
    else:
        return park_helper(MOTORCYCLE, VAN)


def car_helper() -> json:
    """help tp park a car."""
    if spots[CAR] == 0 and spots[VAN] == 0:
        return jsonify({"message": "No available car spots"})
    elif spots[CAR] > 0:
        return park_helper(CAR, CAR)
    else:
        return park_helper(CAR, VAN)


def van_helper() -> json:
    """help to park a van."""
    if spots[VAN] == 0 and spots[CAR] < 3:
        return jsonify({"message": "No available van spots"})
    elif spots[VAN] > 0:
        return park_helper(VAN, VAN)
    elif spots[CAR] >= 3:
        return park_helper(VAN, CAR)


@app.route('/parking_lot/remaining_spots', methods=['GET'])
def get_remaining_spots() -> json:
    """get the number of available spots for each vehicle type."""
    response = {
        MOTORCYCLE: spots[MOTORCYCLE],
        CAR: spots[CAR],
        VAN: spots[VAN],
    }
    return jsonify(response)


@app.route('/parking_lot/is_full', methods=['GET'])
def is_full() -> json:
    """check if the parking lot is full."""
    if spots[MOTORCYCLE] == 0 and spots[CAR] == 0 and spots[VAN] == 0:
        return jsonify({"is_full": True})
    else:
        return jsonify({"is_full": False})


@app.route('/parking_lot/park', methods=['POST'])
def park_vehicle() -> json:
    """park a vehicle in the parking lot"""
    data = request.get_json()
    vehicle_type = data[VEHICLE_TYPE]
    if vehicle_type == MOTORCYCLE:
        return motorcycle_helper()
    if vehicle_type == CAR:
        return car_helper()
    if vehicle_type == VAN:
        return van_helper()


def remove_helper(vehicle_type: str) -> json:
    """function to remove a vehicle with preference to opening van spots, then car spots, then motorcycle spots."""
    if vehicle_type in parked_vehicles[VAN]:
        parked_vehicles[VAN].remove(vehicle_type)
        spots[VAN] += 1
        parking_lot[parking_lot.index((VAN, vehicle_type))] = (VAN, 'o')
        return jsonify({"removed": f"a {vehicle_type} was removed from a van spot"})
    elif vehicle_type in parked_vehicles[CAR]:
        parked_vehicles[CAR].remove(vehicle_type)
        if vehicle_type == VAN:
            check_closed_car_spots_for_van()
            spots[CAR] += 3
        else:
            parking_lot[parking_lot.index((CAR, vehicle_type))] = (CAR, 'o')
            spots[CAR] += 1
        return jsonify({"removed": f"a {vehicle_type} was removed from a car spot"})
    elif vehicle_type in parked_vehicles[MOTORCYCLE]:
        parked_vehicles[MOTORCYCLE].remove(vehicle_type)
        spots[MOTORCYCLE] += 1
        parking_lot[parking_lot.index((MOTORCYCLE, vehicle_type))] = (MOTORCYCLE, 'o')
        return jsonify({"removed": f"a {vehicle_type} was removed from a motorcycle spot"})


@app.route('/parking_lot/remove', methods=['DELETE'])
def remove_vehicle() -> json:
    """remove a vehicle from the parking lot."""
    data = request.get_json()
    vehicle_type = data[VEHICLE_TYPE]
    if vehicle_type not in parked_vehicles:
        return jsonify({"Warning": "this type of vehicle is not parked in the lot"})
    return remove_helper(vehicle_type)


@app.route('/parking_lot/van_spots_occupied', methods=['GET'])
def get_van_spots() -> json:
    """get the number of spots occupied by vans."""
    if VAN in parked_vehicles[CAR]:
        van_in_car = 0
        for i in parked_vehicles[CAR]:
            if i == VAN:
                van_in_car += 1
        return jsonify({"van spots:": str(len(parked_vehicles[VAN])), "car spots:": str(van_in_car)})
    else:
        return jsonify({"van spots:": str(len(parked_vehicles[VAN]))})


spots, parked_vehicles, parking_lot = initialize(NUMBER_OF_MOTORCYCLE_SPOTS, NUMBER_OF_CAR_SPOTS, NUMBER_OF_VAN_SPOTS)
