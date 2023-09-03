import json


class Vehicle:
    def __init__(self, registration_number, year_of_production, passenger, mass):
        self.registration_number = registration_number
        self.year_of_production = year_of_production
        self.passenger = passenger
        self.mass = mass


class MyEncoder(json.JSONEncoder):
    def default(self, veh):
        if isinstance(veh, Vehicle):
            return veh.__dict__
        else:
            return super().default(self, veh)


class MyDecoder(json.JSONDecoder):
    def __init__(self):
        json.JSONDecoder.__init__(self, object_hook=self.decode_vehicle)

    def decode_vehicle(self, veh):
        return Vehicle(**veh)


print("What can I do for you?")
print("1 - produce a JSON string describing a vehicle")
print("2 - decode a JSON string into vehicle data")
answer = ''
while answer not in ['1', '2']:
    answer = input("Your choice: ")
if answer == '1':
    rn = input("Registration number: ")
    yop = int(input("Year of production: "))
    psg = input("Passenger [y/n]: ").upper() == 'Y'
    mss = float(input("Vehicle mass: "))
    vehicle = Vehicle(rn, yop, psg, mss)
    print("Resulting JSON string is:")
    print(json.dumps(vehicle, cls=MyEncoder))
else:
    json_str = input("Enter vehicle JSON string: ")
    try:
        new_car = json.loads(json_str, cls=MyDecoder)
        print(new_car.__dict__)
    except TypeError:
        print("The JSON string doesn't describe a valid vehicle")
print("Done")
