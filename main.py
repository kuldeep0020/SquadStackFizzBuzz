import json

PARKING_LOT = [0]


class SlotVehicleDriverMapping:
    def __init__(self, driver_age=None, vehicle_registration_number=None):
        """Reserved method which is called  when object is created to assign values to members.
        Args:
            driver_age (int): Age of the driver of the vehicle.
            vehicle_registration_number (str): Registration number of the vehicle.
        """
        self.slot_status = 0  # 0 Means the slot is free
        self.vehicle_driver_age = driver_age
        self.vehicle_registration_number = vehicle_registration_number


def command_parser(command):
    """Method to parse the commands and return the supporting data for the command in a dictionary format.
    Args:
        command (str): Command given to the parking maager system.

    Return:
        dict: Dictionary containing command as a value of key 'task' and other keys-values for supporting data for
        that command.
    """
    command_arg_list = command.split()
    if ('Create_parking_lot' in command_arg_list) and (len(command_arg_list) == 2):
        return {
            'task': command_arg_list[0],
            'size': command_arg_list[1]
        }
    if ('Leave' in command_arg_list) and (len(command_arg_list) == 2):
        return {
            'task': command_arg_list[0],
            'slot': command_arg_list[1],
        }
    if ('Park' in command_arg_list) and ('driver_age' in command_arg_list) and (len(command_arg_list) == 4):
        return {
            'task': command_arg_list[0],
            'vehicle_number': command_arg_list[1],
            'driver_age': command_arg_list[3],

        }
    if ('Slot_numbers_for_driver_of_age' in command_arg_list) and (len(command_arg_list) == 2):
        return {
            'task': command_arg_list[0],
            'driver_age': command_arg_list[1]
        }
    if ('Slot_number_for_car_with_number' in command_arg_list) and (len(command_arg_list) == 2):
        return {
            'task': command_arg_list[0],
            'vehicle_number': command_arg_list[1],
        }
    if ('Vehicle_registration_number_for_driver_of_age' in command_arg_list) and (len(command_arg_list) == 2):
        return {
            'task': command_arg_list[0],
            'driver_age': command_arg_list[1]
        }
    else:
        return {
            'task': 'Unknown_command',
            'command': command
        }


def create_parking_lot(data):
    """Method to handle create_parking_lot command with given number of slots in the parking lot.
    Args:
        data: Dictionary containing following key-value pair:
            size (int): Number of slots in the parking.
    """
    size = int(data['size'])
    PARKING_LOT[0] = size
    for i in range(1, size + 1):
        PARKING_LOT.append(SlotVehicleDriverMapping())
    return 'Created parking of {} slots'.format(size)


def leave(data):
    """Method to vacate a slot of parking lot.
    Args:
        data: Dictionary containing following key-value pair:
            slot (int): Number of slot in the parking.
    """
    slot_number = int(data['slot'])
    if 0 < slot_number < PARKING_LOT[0] + 1:
        slot = PARKING_LOT[slot_number]
        if slot.slot_status:
            driver_age = slot.vehicle_driver_age
            vehicle_registration_number = slot.vehicle_registration_number
            slot.slot_status = 0
            slot.vehicle_registration_number = None
            slot.vehicle_driver_age = None
            return 'Slot number {} vacated, the car with vehicle registration number “{}” left the space, the driver ' \
                   'of the car was of age {}'.format(slot_number, vehicle_registration_number, driver_age)
        if not slot.slot_status:
            return 'Slot already vacant'.format(slot_number)
    return 'null'


def park(data):
    """Method to park the vehicle for a given age user and vehicle number in slot available nearest to the entry point.
    Args:
        data: Dictionary containing the following key-value pairs:
            driver_age (int/str): Age of the driver of the vehicle.
            vehicle_number (str): Registration number of the vehicle.
    """
    nearest_free_slot = _get_nearest_free_slot()
    if not nearest_free_slot:
        return 'Not possible to park, lot is out of space.'
    driver_age = int(data['driver_age'])
    vehicle_number = data['vehicle_number']
    slot = PARKING_LOT[nearest_free_slot]
    slot.slot_status = 1
    slot.vehicle_driver_age = driver_age
    slot.vehicle_registration_number = vehicle_number
    return 'Car with vehicle registration number “{}” has been parked at slot number {}'.format(
        vehicle_number, nearest_free_slot
    )


def slot_numbers_for_driver_of_age(data):
    """Method to find the slot numbers where drivers of a given age have parked the vehicle.
    Args:
        data: Dictionary containing the following key-value pair:
            driver_age (int/str): Age of driver.
    """
    age = int(data['driver_age'])
    slot_numbers = []
    for i in range(1, PARKING_LOT[0] + 1):
        if PARKING_LOT[i].vehicle_driver_age == age:
            slot_numbers.append(i)
    return str(slot_numbers).strip('[]').replace(' ', '') if slot_numbers else 'null'


def slot_number_for_car_with_number(data):
    """Method to find slot number where a vehicle with a given registration number is parked.
    Args:
        data: Dictionary containing the following key-value pair:
            vehicle_number (str): Registration number of the vehicle.
    """
    vehicle_number = data['vehicle_number']
    for i in range(1, PARKING_LOT[0] + 1):
        if PARKING_LOT[i].vehicle_registration_number == vehicle_number:
            return str(i)
    return 'null'


def vehicle_registration_number_for_driver_of_age(data):
    """Method to find the vehicle registration numbers of the drivers of a given age.
    Args:
        data: Dictionary containing the following key-value pair:
            driver_age (int/str): Age of driver.
    """
    age = int(data['driver_age'])
    vehicle_numbers = []
    for i in range(1, PARKING_LOT[0] + 1):
        if PARKING_LOT[i].vehicle_driver_age == age:
            vehicle_numbers.append(PARKING_LOT[i].vehicle_registration_number)
    return str(vehicle_numbers).strip('[]').replace(' ', '') if vehicle_numbers else 'null'


def unknown_command(data):
    """Method to handle the commands which are not recognised by the parking manager system.
    Args:
        data: Dictionary containing the following key-value pair:
            command (int/str): The command which was not recognised by the system.
    """
    command = data['command']
    return 'unknown_command: {}'.format(command)


def _get_nearest_free_slot():
    for i in range(1, PARKING_LOT[0] + 1):
        if not PARKING_LOT[i].slot_status:
            return i
    return None


if __name__ == '__main__':
    choice = input('1. Press 1 if you want to give commands from a file.\n'
                   '2. Press 2 if you want to give commands through terminal.\n')
    if int(choice) == 1:
        filename = input("Input the filename which contains the commands(there should be no spaces in file name: ")
        command_file = open(filename, 'r')
        commands = command_file.readlines()
        for command in commands:
            parsed_command = command_parser(command)
            print(eval(parsed_command['task'].lower() + '({})'.format(json.dumps(parsed_command))))
    else:
        while 1:
            command = input('Enter the command and press Enter/Return (Press ctrl+c to exit): ')
            parsed_command = command_parser(command)
            print(eval(parsed_command['task'].lower() + '({})'.format(json.dumps(parsed_command))))
