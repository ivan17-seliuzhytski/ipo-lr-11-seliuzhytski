import uuid
class Vehicle:
    def __init__(person, capacity):
        person.vehicle_id = str(uuid.uuid4())
        person.capacity = capacity
        person.current_load = 0
        person.clients_list = []
    def if_load(person, client):
        return person.current_load + client.cargo_weight <= person.capacity
    def load_cargo(person, client):
        if person.if_load(client):
            person.current_load += client.cargo_weight
            person.clients_list.append(client)
            return True
        return False
    def __str__(person):
        return f"ID транспорта: {person.vehicle_id},грузоподъёмность: {person.capacity},текущая загрузка: {person.current_load}"
class Train(Vehicle):
    def __init__(person, capacity, number_of_cars):
        super().__init__(capacity)
        person.number_of_cars = number_of_cars   
class Airplane(Vehicle):
    def __init__(person, capacity, max_altitude):
        super().__init__(capacity)
        person.max_altitude = max_altitude