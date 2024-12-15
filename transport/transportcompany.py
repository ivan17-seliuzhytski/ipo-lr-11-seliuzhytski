from .vehicle import Vehicle
from .client import Client
class TransportCompany:
    def __init__(person, name):
        person.name = name
        person.vehicles = []
        person.clients = []
    def add_vehicle(person, vehicle):
        if isinstance(vehicle, Vehicle):
            person.vehicles.append(vehicle)
    def list_vehicles(person):
        return [str(vehicle) for vehicle in person.vehicles]
    def add_client(person, client):
        if isinstance(client, Client):
            person.clients.append(client)
    def optimize_cargo_distribution(person):
        vip_clients = sorted([client for client in person.clients if client.is_vip], key=lambda client: client.cargo_weight, reverse=True)
        regular_clients = sorted([client for client in person.clients if not client.is_vip], key=lambda client: client.cargo_weight, reverse=True)
        all_clients = vip_clients + regular_clients
        for client in all_clients:
            for vehicle in sorted(person.vehicles, key=lambda vehicle: vehicle.current_load):
                if vehicle.load_cargo(client):
                    break