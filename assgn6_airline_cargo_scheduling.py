from datetime import datetime
import os
import time

# Base class
class Flight:
    def __init__(self, flight_id, source, destination, departure, arrival, aircraft_id=None):
        self.flight_id = flight_id
        self.source = source
        self.destination = destination
        self.departure = departure  # datetime object
        self.arrival = arrival
        self.aircraft_id = aircraft_id

    def display_schedule(self):
        print(f"[Flight {self.flight_id}] {self.source} ➡ {self.destination}")
        print(f"Departure: {self.departure} | Arrival: {self.arrival}")

    def reschedule(self, new_departure, new_arrival):
        self.departure = new_departure
        self.arrival = new_arrival

class PassengerFlight(Flight):
    def __init__(self, flight_id, source, destination, departure, arrival, aircraft_id, capacity):
        super().__init__(flight_id, source, destination, departure, arrival, aircraft_id)
        self.passenger_capacity = capacity
        self.booked_passengers = 0

    def book_seat(self):
        if self.booked_passengers < self.passenger_capacity:
            self.booked_passengers += 1
            print("Seat booked.")
        else:
            print("No available seats.")

    def available_seats(self):
        return self.passenger_capacity - self.booked_passengers


class Cargo:
    def __init__(self, cargo_id, description, weight, owner_name):
        self.cargo_id = cargo_id
        self.description = description
        self.weight = weight
        self.owner_name = owner_name

    def display_details(self):
        print(f"Cargo ID: {self.cargo_id} | {self.description} | Weight: {self.weight}kg | Owner: {self.owner_name}")


class CargoFlight(Flight):
    def __init__(self, flight_id, source, destination, departure, arrival, aircraft_id, max_cargo_weight):
        super().__init__(flight_id, source, destination, departure, arrival, aircraft_id)
        self.max_cargo_weight = max_cargo_weight
        self.current_cargo_weight = 0
        self.cargo_list = []

    def add_cargo(self, cargo):
        if self.current_cargo_weight + cargo.weight <= self.max_cargo_weight:
            self.cargo_list.append(cargo)
            self.current_cargo_weight += cargo.weight
            print("Cargo added.")
        else:
            print("Not enough space for this cargo.")

    def remove_cargo(self, cargo_id):
        for cargo in self.cargo_list:
            if cargo.cargo_id == cargo_id:
                self.current_cargo_weight -= cargo.weight
                self.cargo_list.remove(cargo)
                print("Cargo removed.")
                return
        print("Cargo not found.")

    def available_cargo_space(self):
        return self.max_cargo_weight - self.current_cargo_weight


class Scheduler:
    def __init__(self):
        self.flights = {}

    def schedule_flight(self, flight):
        self.flights[flight.flight_id] = flight
        print(f"Flight {flight.flight_id} scheduled.")

    def cancel_flight(self, flight_id):
        if flight_id in self.flights:
            del self.flights[flight_id]
            print(f"Flight {flight_id} cancelled.")
        else:
            print("Flight not found.")

    def get_schedule_by_date(self, date, sort=False):
        print(f"Flights on {date.date()}:")
        list=[]
        for flight in self.flights.values():
            if flight.departure.date() == date.date():
                list.append(flight)
        if sort:
            list.sort(key=lambda f: f.departure)
        if not list:
            print("No flights found.")
        for flight in list:
            flight.display_schedule()
    
    def get_schedule_by_source(self, source):
        print(f"\nFlights from {source}:")
        found = False
        for flight in self.flights.values():
            if flight.source.lower() == source.lower():
                flight.display_schedule()
                found = True
        if not found:
            print("No flights found.")

    def get_schedule_by_destination(self, destination):
        print(f"\nFlights to {destination}:")
        found = False
        for flight in self.flights.values():
            if flight.destination.lower() == destination.lower():
                flight.display_schedule()
                found = True
        if not found:
            print("No flights found.")

    def get_schedule_by_aircraft_id(self, aircraft_id):
        print(f"\nFlights with Aircraft ID {aircraft_id}:")
        found = False
        for flight in self.flights.values():
            if flight.aircraft_id and flight.aircraft_id.lower() == aircraft_id.lower():
                flight.display_schedule()
                found = True
        if not found:
            print("No flights found.")

    def total_cargo_handled_by_airport(self, airport_name):
        count = 0
        total_weight = 0
        weight_out = 0
        weight_in = 0

        for flight in self.flights.values():
            if isinstance(flight, CargoFlight):
                count += 1
                total_weight += flight.cargo_weight
                if flight.source.lower() == airport_name.lower():
                    weight_out += flight.cargo_weight
                elif flight.destination.lower() == airport_name.lower():
                    weight_in += flight.cargo_weight

        print(f"\nCargo stats for airport '{airport_name}':")
        print(f"  Total cargo flights: {count}")
        print(f"  Total cargo weight handled: {total_weight} kg")
        print(f"    - Cargo weight flown out: {weight_out} kg")
        print(f"    - Cargo weight flown in:  {weight_in} kg")

    def total_passengers_handled_by_airport(self, airport_name):
        count = 0
        total_passengers = 0
        passengers_out = 0
        passengers_in = 0

        for flight in self.flights.values():
            if isinstance(flight, PassengerFlight):
                count += 1
                total_passengers += flight.passenger_count
                if flight.source.lower() == airport_name.lower():
                    passengers_out += flight.passenger_count
                elif flight.destination.lower() == airport_name.lower():
                    passengers_in += flight.passenger_count

        print(f"\nPassenger stats for airport '{airport_name}':")
        print(f"  Total passenger flights: {count}")
        print(f"  Total passengers handled: {total_passengers}")
        print(f"    - Passengers flown out: {passengers_out}")
        print(f"    - Passengers flown in:  {passengers_in}")


def clear_screen():
    os.system('clear')

def get_valid_date():
    while True:
        try:
            date_str = input("Enter date (YYYY-MM-DD): ")
            date = datetime.strptime(date_str, "%Y-%m-%d")
            # Add a default time of midnight
            return datetime.combine(date.date(), datetime.min.time())
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")

def get_valid_datetime():
    while True:
        try:
            date_str = input("Enter date and time (YYYY-MM-DD HH:MM): ")
            return datetime.strptime(date_str, "%Y-%m-%d %H:%M")
        except ValueError:
            print("Invalid format. Please use YYYY-MM-DD HH:MM.")


def manage_flights(scheduler):
    """Menu for flight management"""
    while True:
        print("\n===== FLIGHT MANAGEMENT =====")
        print("1. Schedule passenger flight")
        print("2. Schedule cargo flight")
        print("3. Cancel flight")
        print("4. Reschedule flight")
        print("6. Back to main menu")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            flight_id = input("Enter flight ID: ")
            source = input("Enter source airport: ")
            destination = input("Enter destination airport: ")
            print("Enter departure time:")
            departure = get_valid_datetime()
            print("Enter arrival time:")
            arrival = get_valid_datetime()
            aircraft_id = input("Enter aircraft ID (or leave blank): ")
            
            try:
                capacity = int(input("Enter passenger capacity: "))
                flight = PassengerFlight(flight_id, source, destination, 
                                        departure, arrival, 
                                        aircraft_id if aircraft_id else None, 
                                        capacity)
                scheduler.schedule_flight(flight)
            except ValueError:
                print("Invalid capacity. Please enter a number.")
        
        elif choice == '2':
            flight_id = input("Enter flight ID: ")
            source = input("Enter source airport: ")
            destination = input("Enter destination airport: ")
            print("Enter departure time:")
            departure = get_valid_datetime()
            print("Enter arrival time:")
            arrival = get_valid_datetime()
            aircraft_id = input("Enter aircraft ID (or leave blank): ")
            
            try:
                max_weight = float(input("Enter maximum cargo weight (kg): "))
                flight = CargoFlight(flight_id, source, destination, 
                                    departure, arrival, 
                                    aircraft_id if aircraft_id else None, 
                                    max_weight)
                scheduler.schedule_flight(flight)
            except ValueError:
                print("Invalid weight. Please enter a number.")
        
        elif choice == '3':
            flight_id = input("Enter flight ID to cancel: ")
            scheduler.cancel_flight(flight_id)
        
        elif choice == '4':
            flight_id = input("Enter flight ID to reschedule: ")
            if flight_id in scheduler.flights:
                print("Enter new departure time:")
                new_departure = get_valid_datetime()
                print("Enter new arrival time:")
                new_arrival = get_valid_datetime()
                scheduler.flights[flight_id].reschedule(new_departure, new_arrival)
                print(f"Flight {flight_id} rescheduled.")
            else:
                print("Flight not found.")
        
        elif choice == '6':
            break

        else:
            print("Invalid choice. Please try again.")
        
        input("\nPress Enter to continue...")
        clear_screen()


def manage_passenger_bookings(scheduler):
    while True:
        print("\n===== PASSENGER BOOKING MANAGEMENT =====")
        print("1. Book a seat")
        print("2. Check available seats")
        print("3. Back to main menu")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            flight_id = input("Enter flight ID: ")
            if flight_id in scheduler.flights and isinstance(scheduler.flights[flight_id], PassengerFlight):
                scheduler.flights[flight_id].book_seat()
            else:
                print("Invalid flight ID or not a passenger flight.")
        elif choice == '2':
            flight_id = input("Enter flight ID: ")
            if flight_id in scheduler.flights and isinstance(scheduler.flights[flight_id], PassengerFlight):
                seats = scheduler.flights[flight_id].available_seats()
                print(f"Available seats: {seats}")
            else:
                print("Invalid flight ID or not a passenger flight.")
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")
        
        input("\nPress Enter to continue...")
        clear_screen()


def manage_cargo(scheduler):
    """Menu for cargo management"""
    while True:
        print("\n===== CARGO MANAGEMENT =====")
        print("1. Add cargo to flight")
        print("2. Remove cargo from flight")
        print("3. Check available cargo space")
        print("4. Back to main menu")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            flight_id = input("Enter cargo flight ID: ")
            if flight_id in scheduler.flights and isinstance(scheduler.flights[flight_id], CargoFlight):
                cargo_id = input("Enter cargo ID: ")
                description = input("Enter cargo description: ")
                
                try:
                    weight = float(input("Enter cargo weight (kg): "))
                    owner = input("Enter cargo owner name: ")
                    
                    cargo = Cargo(cargo_id, description, weight, owner)
                    scheduler.flights[flight_id].add_cargo(cargo)
                except ValueError:
                    print("Invalid weight. Please enter a number.")
            else:
                print("Invalid flight ID or not a cargo flight.")
        elif choice == '2':
            flight_id = input("Enter cargo flight ID: ")
            if flight_id in scheduler.flights and isinstance(scheduler.flights[flight_id], CargoFlight):
                cargo_id = input("Enter cargo ID to remove: ")
                scheduler.flights[flight_id].remove_cargo(cargo_id)
            else:
                print("Invalid flight ID or not a cargo flight.")
        elif choice == '3':
            flight_id = input("Enter cargo flight ID: ")
            if flight_id in scheduler.flights and isinstance(scheduler.flights[flight_id], CargoFlight):
                space = scheduler.flights[flight_id].available_cargo_space()
                print(f"Available cargo space: {space} kg")
            else:
                print("Invalid flight ID or not a cargo flight.")
        elif choice == '4':
            break
        
        else:
            print("Invalid choice. Please try again.")
        
        input("\nPress Enter to continue...")
        clear_screen()


def view_schedules(scheduler):
    """Menu for viewing schedules"""
    while True:
        print("\n===== VIEW SCHEDULES =====")
        print("1. View all flights by date")
        print("2. View flights by source airport")
        print("3. View flights by destination airport")
        print("4. View flights by aircraft ID")
        print("5. Back to main menu")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            date = get_valid_date()
            sort_option = input("Sort by departure time? (y/n): ").lower() == 'y'
            scheduler.get_schedule_by_date(date, sort_option)
        elif choice == '2':
            source = input("Enter source airport: ")
            scheduler.get_schedule_by_source(source)
        elif choice == '3':
            destination = input("Enter destination airport: ")
            scheduler.get_schedule_by_destination(destination)
        elif choice == '4':
            aircraft_id = input("Enter aircraft ID: ")
            scheduler.get_schedule_by_aircraft_id(aircraft_id)
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")
        
        input("\nPress Enter to continue...")
        clear_screen()


def view_statistics(scheduler):
    """Menu for viewing statistics"""
    while True:
        print("\n===== VIEW STATISTICS =====")
        print("1. View cargo statistics by airport")
        print("2. View passenger statistics by airport")
        print("3. Back to main menu")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            airport = input("Enter airport name: ")
            scheduler.total_cargo_handled_by_airport(airport)
        elif choice == '2':
            airport = input("Enter airport name: ")
            scheduler.total_passengers_handled_by_airport(airport)
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")
        input("\nPress Enter to continue...")
        clear_screen()


def main():
    print("===== FLIGHT MANAGEMENT SYSTEM =====")
    print("Initializing system...")
    
    scheduler = Scheduler()
    
    while True:
        clear_screen()
        print("\n===== FLIGHT MANAGEMENT SYSTEM =====")
        print("1. Manage Flights")
        print("2. Manage Passenger Bookings")
        print("3. Manage Cargo")
        print("4. View Schedules")
        print("5. View Statistics")
        print("7. Exit System")
        
        choice = input("\nEnter your choice: ")
        
        if choice == '1':
            manage_flights(scheduler)
        elif choice == '2':
            manage_passenger_bookings(scheduler)
        elif choice == '3':
            manage_cargo(scheduler)
        elif choice == '4':
            view_schedules(scheduler)
        elif choice == '5':
            view_statistics(scheduler)
        elif choice == '7':
            print("Thank you for using the Flight Management System. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
            time.sleep(1)

if __name__ == "__main__":
    main()
