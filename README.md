# SEALED BACKENED CHALLENGE


## Install

    The libraries needed for this project can be found in the requirements file. This file can be run using:
    pip install -r requirements.txt

## Run the tests

    you can run the tests using: python -m unittest tests.py
    
## Run the code
    
    To test the code you can either use the tests I included or you can create a seperate file to write api calls. Just note, that the dicts will not last past runtime. Lastly, the one other thing to note, is that you can change the number of spots available for each vehicle type by changing the constant value associated with each type at the top of the main file.
    
    
   
# API

### GET
- Tell us how many spots are remaining
```
    Status: 200 OK
    route: /parking_lot/remaining_spots
    GET
    example_response: {'car': 1, 'motorcycle': 3, 'van': 1}
```

- Tell us when the parking lot is full
```
    Status: 200 OK
    route: /parking_lot/is_full
    GET
    example_reponse: {'is_full': False}
```

- Tell us how many spots vans are taking up
```
    Status: 200 OK
    route: /parking_lot/van_spots_occupied
    GET
    example_reponse: {'car spots:': '1', 'van spots:': '1'}
````
   
### POST
- Take in a vehicle to park
```
    Status: 200 OK
    route: /parking_lot/park
    GET
    example_response: {'Vehicle parked': 'motorcycle'}
```

### DELETE
- Remove a vehicle from the lot
```
    Status: 200 OK
    route: /parking_lot/remove
    GET
    example_response: {'removed': 'a van was removed from a car spot'}
```

## ASUMPTIONS
```
For this take home project I made the assumption that when there are 3 car spots available that they are adjacent. I also made the assumption that when removing vehicles from the lots the preference to clear spots goes in the order of Van, Car, Motorcycle. 

The data source I decided to use for this project was two simple dictionaries. This could also be converted to a sql table if I wanted this dictionary to exist after runtime. However, for the sake of displaying my technical skills I confirmed with Bryan that this is sufficent.

```
