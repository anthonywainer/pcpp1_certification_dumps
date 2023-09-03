import requests
import json

Service_URI = 'http://localhost:3000/cars/'
h_close = {'Connection': 'Close'}
h_content = {'Content-Type': 'application/json'}
column_headers = ["id", "brand", "model", "production_year", "convertible"]
column_widths = [10, 15, 10, 20, 15]


def check_server(cid=None):
    uri = Service_URI
    if cid:
        uri += str(cid)
    try:
        res = requests.head(uri, headers=h_close)
    except requests.exceptions.RequestException:
        return False
    return res.status_code == requests.codes.ok


def print_menu():
    print("+-----------------------------------+")
    print("|       Vintage Cars Database       |")
    print("+-----------------------------------+")
    print("M E N U")
    print("=======")
    print("1. List cars")
    print("2. Add new car")
    print("3. Delete car")
    print("4. Update car")
    print("0. Exit")


def read_user_choice():
    ok = False
    while not ok:
        answer = input("Enter your choice (0..4): ")
        ok = answer in ['0', '1', '2', '3', '4']
        if ok:
            return answer
        print("Bad choice!")


def print_header():
    for (head, width) in zip(column_headers, column_widths):
        print(head.ljust(width), end='| ')
    print()


def print_car(car):
    for (name, width) in zip(column_headers, column_widths):
        print(str(car[name]).ljust(width), end='| ')
    print()


def list_cars():
    try:
        res = requests.get(Service_URI)
    except requests.exceptions.RequestException:
        print("Communication error :(")
        return
    cars = res.json()
    if len(cars) == 0:
        print("*** Database is empty ***")
        return
    print_header()
    for car in cars:
        print_car((car))
    print()


def name_is_valid(name):
    for char in name:
        if not (char.isspace() or char.isdigit() or char.isalpha()):
            return False
    return True


def enter_id():
    while True:
        id = input("Car ID (empty string to exit): ")
        if not id or id.isspace():
            return None
        if not id.isdigit():
            print("Invalid ID - re-enter.")
            continue
        return int(id)


def enter_production_year():
    while True:
        prod_year = input("Car production year (empty string to exit): ")
        if not prod_year or prod_year.isspace():
            return None
        if not prod_year.isdigit() or not 1900 <= int(prod_year) <= 2023:
            print("Invalid production year - re-enter.")
            continue
        return int(prod_year)


def enter_name(what):
    while True:
        name = input("Car " + what + " (empty string to exit): ")
        if name == '' or name.isspace():
            return None
        if not name_is_valid(name):
            print(what.title() + ' contains illegal characters - re-enter.')
            continue
        return name.title()


def enter_convertible():
    while True:
        conv = input("Is this car convertible? [y/n] (empty string to exit): ")
        if conv == '':
            return None
        if conv.upper() not in ['Y', 'N']:
            print("Invalid input - re-enter.")
            continue
        return conv in ['y', 'Y']


def delete_car():
    while True:
        id = enter_id()
        if not id:
            return
        try:
            res = requests.delete(Service_URI + str(id))
        except requests.exceptions.RequestException:
            print('Communication error - delete failed.')
            return
        if res.status_code == requests.codes.not_found:
            print("Unknown ID - nothing has been deleted")
            continue
        print("Success!")


def input_car_data(with_id):
    if with_id:
        car_id = enter_id()
        if car_id is None:
            return {}
    else:
        car_id = 0
    brand = enter_name('brand')
    if brand is None:
        return {}
    model = enter_name('model')
    if model is None:
        return {}
    prod_year = enter_production_year()
    if prod_year is None:
        return {}
    conv = enter_convertible()
    if conv is None:
        return {}
    return {'id': car_id, 'brand': brand, 'model': model, 'production_year': prod_year, 'convertible': conv}


def add_car():
    new_car = input_car_data(True)
    if not new_car:
        return
    try:
        res = requests.post(Service_URI, headers=h_content, data=json.dumps(new_car))
    except requests.exceptions.RequestException:
        print('Communication error - adding new car failed')
        return
    if res.status_code != 201:
        print("Duplicated car ID - adding new car failed")


def update_car():
    while True:
        car_id = enter_id()
        if not car_id:
            return
        if not check_server(car_id):
            print("Car ID not found in the database.")
        else:
            break
    car = input_car_data(False)
    if not car:
        return

    car["id"] = car_id
    try:
        res = requests.put(Service_URI + str(car_id), headers=h_content, data=json.dumps(car))
    except requests.exceptions.RequestException:
        print('Communication error - updating car data failed')
        return
    if res.status_code != requests.codes.ok:
        print("Duplicated car ID - adding new car failed")


while True:
    if not check_server():
        print("Server is not responding - quitting!")
        exit(1)
    print_menu()
    choice = read_user_choice()
    if choice == '0':
        print("Bye!")
        exit(0)
    elif choice == '1':
        list_cars()
    elif choice == '2':
        add_car()
    elif choice == '3':
        delete_car()
    elif choice == '4':
        update_car()
