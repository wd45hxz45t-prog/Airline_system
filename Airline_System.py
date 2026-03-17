# ============================================================
# Apache Airlines - Seat Booking System
# FC723 - Programming Theory | Part A
# ============================================================

# Import built-in library needed for generating miles calculations
# random: used for any random operations if needed in future
import random


# === CLASS 1: AIRCRAFT ===
# This class is responsible for creating and managing the aircraft seat map.
# It handles all operations related to the physical layout of the aircraft.

class Aircraft:

    def __init__(self):
        # Create the seat map when the Aircraft object is created
        # The plane is a list of lists, each row has 7 positions: A B C X D E F
        self.plane = self.create_aircraft()

    def create_aircraft(self):
        # Start with an empty plane list
        plane = []

        # Loop through all 80 rows and build each row
        for row in range(1, 81):

            # Rows 77-79: columns D, E, F are storage areas (S)
            if row in [77, 78, 79]:
                seat_row = ["F", "F", "F", "X", "S", "S", "S"]
            else:
                # Normal row: all seats free, aisle in the middle
                seat_row = ["F", "F", "F", "X", "F", "F", "F"]

            plane.append(seat_row)

        return plane

    def get_column_index(self, col_letter):
        # Convert column letter to list index
        # A=0, B=1, C=2, X=3 (aisle - skipped), D=4, E=5, F=6
        column_map = {
            "A": 0, "B": 1, "C": 2,
            "D": 4, "E": 5, "F": 6
        }
        return column_map.get(col_letter.upper(), -1)

    def show_seat_map(self):
        # Print a blank line followed by a row of 45 '=' signs as a visual border
        print("\n" + "=" * 45)
        print("       APACHE AIRLINES - SEAT MAP")
        print("=" * 45)
        print("  Row |  A   B   C   |   D   E   F")
        print("-" * 45)

        for i, row in enumerate(self.plane):
            row_num = i + 1

            display = []
            for seat in row:
                if seat == "F":
                    display.append(" F ")
                elif seat == "X":
                    display.append(" | ")
                elif seat == "S":
                    display.append(" S ")
                else:
                    # Any reserved seat gets shown as [R]
                    display.append("[R]")

            print(f"  {row_num:>3} | {'  '.join(display[:3])}  |  {'  '.join(display[4:])}")

        print("=" * 45)
        print("  F=Free  [R]=Reserved  |=Aisle  S=Storage")
        print("=" * 45 + "\n")

    def check_seat(self):
        # Ask the user for a seat and check its current status
        print("\n-- Check Seat Availability --")

        try:
            row = int(input("  Enter row number (1-80): "))
            if row < 1 or row > 80:
                print("  Invalid row! Please enter a number between 1 and 80.")
                return
        except ValueError:
            print("  Invalid input! Please enter a number.")
            return

        col = input("  Enter column letter (A, B, C, D, E, F): ").upper()
        col_index = self.get_column_index(col)

        if col_index == -1:
            print("  Invalid column! Please enter A, B, C, D, E, or F.")
            return

        seat_status = self.plane[row - 1][col_index]

        if seat_status == "F":
            print(f"  Seat {row}{col} is AVAILABLE.")
        elif seat_status == "S":
            print(f"  Seat {row}{col} is a STORAGE area. Cannot be booked.")
        elif seat_status == "X":
            print(f"  Seat {row}{col} is an AISLE. Cannot be booked.")
        else:
            print(f"  Seat {row}{col} is already RESERVED.")
            
            
    

# === CLASS 2: BOOKING ===
# This class handles all booking operations including booking and freeing seats.
# It stores "R" in the seat map when a seat is booked.

class Booking:

    def __init__(self, aircraft):
        # Store a reference to the Aircraft object to access the seat map
        self.aircraft = aircraft

    def book_seat(self):
        # Book a seat by storing "R" in the seat map
        print("\n-- Book a Seat --")

        try:
            row = int(input("  Enter row number (1-80): "))
            if row < 1 or row > 80:
                print("  Invalid row! Please enter a number between 1 and 80.")
                return
        except ValueError:
            print("  Invalid input! Please enter a number.")
            return

        col = input("  Enter column letter (A, B, C, D, E, F): ").upper()
        col_index = self.aircraft.get_column_index(col)

        if col_index == -1:
            print("  Invalid column! Please enter A, B, C, D, E, or F.")
            return

        seat_status = self.aircraft.plane[row - 1][col_index]

        # Only book the seat if it is currently free
        if seat_status == "F":
            self.aircraft.plane[row - 1][col_index] = "R"
            print(f"  Seat {row}{col} has been successfully BOOKED!")
        elif seat_status == "R":
            print(f"  Seat {row}{col} is already reserved. Please choose another seat.")
        elif seat_status == "S":
            print(f"  Seat {row}{col} is a storage area. Cannot be booked.")
        else:
            print(f"  Seat {row}{col} is an aisle. Cannot be booked.")

    def free_seat(self):
        # Free a reserved seat by storing "F" back in the seat map
        print("\n-- Free a Seat --")

        try:
            row = int(input("  Enter row number (1-80): "))
            if row < 1 or row > 80:
                print("  Invalid row! Please enter a number between 1 and 80.")
                return
        except ValueError:
            print("  Invalid input! Please enter a number.")
            return

        col = input("  Enter column letter (A, B, C, D, E, F): ").upper()
        col_index = self.aircraft.get_column_index(col)

        if col_index == -1:
            print("  Invalid column! Please enter A, B, C, D, E, or F.")
            return

        seat_status = self.aircraft.plane[row - 1][col_index]

        # Only free the seat if it is currently reserved
        if seat_status == "R":
            self.aircraft.plane[row - 1][col_index] = "F"
            print(f"  Seat {row}{col} has been successfully FREED!")
        elif seat_status == "F":
            print(f"  Seat {row}{col} is already free. Nothing to cancel.")
        elif seat_status == "S":
            print(f"  Seat {row}{col} is a storage area.")
        else:
            print(f"  Seat {row}{col} is an aisle.")
            
            
            
            

# === CLASS 3: MILES ===
# This class handles the miles balance for each passenger and seat upgrades.
# Economy seats (D, E, F) can be upgraded to Business (A, B, C) for 5000 miles.

class Miles:

    def __init__(self, aircraft):
        # Store a reference to the Aircraft object to access the seat map
        self.aircraft = aircraft

        # Dictionary to store miles balance for each booked seat
        # Key = seat key (e.g. "5D"), Value = miles balance (integer)
        self.miles_balance = {}

    def add_miles(self):
        # Add miles to a booked seat's balance
        print("\n-- Add Miles to Your Account --")

        try:
            row = int(input("  Enter your seat row (1-80): "))
            if row < 1 or row > 80:
                print("  Invalid row!")
                return
        except ValueError:
            print("  Invalid input!")
            return

        col = input("  Enter your seat column (A, B, C, D, E, F): ").upper()
        col_index = self.aircraft.get_column_index(col)

        if col_index == -1:
            print("  Invalid column!")
            return

        # Seat must be reserved before adding miles
        if self.aircraft.plane[row - 1][col_index] != "R":
            print(f"  Seat {row}{col} is not reserved. Please book it first.")
            return

        try:
            miles_to_add = int(input("  Enter miles to add: "))
            if miles_to_add <= 0:
                print("  Miles must be a positive number.")
                return
        except ValueError:
            print("  Invalid input!")
            return

        # Add miles to this seat's balance
        # If seat has no record yet, start from 0
        seat_key = f"{row}{col}"
        if seat_key not in self.miles_balance:
            self.miles_balance[seat_key] = 0

        self.miles_balance[seat_key] += miles_to_add
        print(f"  {miles_to_add} miles added.")
        print(f"  Total miles balance: {self.miles_balance[seat_key]} miles")

    def upgrade_seat(self):
        # Upgrade a seat from Economy (D,E,F) to Business (A,B,C) for 5000 miles
        print("\n-- Seat Upgrade Using Miles --")
        print("  Economy (D,E,F) to Business (A,B,C) costs 5000 miles")

        try:
            current_row = int(input("\n  Enter your current seat row (1-80): "))
            if current_row < 1 or current_row > 80:
                print("  Invalid row!")
                return
        except ValueError:
            print("  Invalid input!")
            return

        current_col = input("  Enter your current seat column (D, E, F): ").upper()

        # Only Economy seats (D, E, F) can be upgraded
        if current_col not in ["D", "E", "F"]:
            print("  Upgrades are only available from Economy seats (D, E, F).")
            return

        current_col_index = self.aircraft.get_column_index(current_col)

        # Make sure the current seat is reserved
        if self.aircraft.plane[current_row - 1][current_col_index] != "R":
            print(f"  Seat {current_row}{current_col} is not reserved.")
            return

        # Check miles balance for this seat
        seat_key = f"{current_row}{current_col}"
        if seat_key not in self.miles_balance:
            self.miles_balance[seat_key] = 0

        current_miles = self.miles_balance[seat_key]
        print(f"\n  Your current miles balance: {current_miles} miles")

        # Check if the user has enough miles
        if current_miles < 5000:
            print(f"  Not enough miles! You need {5000 - current_miles} more miles.")
            return

        try:
            new_row = int(input("\n  Enter preferred Business seat row (1-80): "))
            if new_row < 1 or new_row > 80:
                print("  Invalid row!")
                return
        except ValueError:
            print("  Invalid input!")
            return

        new_col = input("  Enter preferred Business seat column (A, B, C): ").upper()

        # New seat must be Business class (A, B, or C)
        if new_col not in ["A", "B", "C"]:
            print("  Please choose a Business class seat (A, B, or C).")
            return

        new_col_index = self.aircraft.get_column_index(new_col)

        # New Business seat must be free
        if self.aircraft.plane[new_row - 1][new_col_index] != "F":
            print(f"  Seat {new_row}{new_col} is not available.")
            return

        # Free the old Economy seat and book the new Business seat
        self.aircraft.plane[current_row - 1][current_col_index] = "F"
        self.aircraft.plane[new_row - 1][new_col_index] = "R"

        # Deduct 5000 miles and transfer remaining balance to the new seat key
        self.miles_balance[seat_key] = current_miles - 5000
        new_seat_key = f"{new_row}{new_col}"
        self.miles_balance[new_seat_key] = self.miles_balance[seat_key]
        del self.miles_balance[seat_key]

        print("\n  Upgrade successful!")
        print(f"  Moved from Economy {current_row}{current_col} to Business {new_row}{new_col}")
        print(f"  Remaining miles: {self.miles_balance[new_seat_key]}")





# === CLASS 4: BOOKING SYSTEM ===
# This is the main class that ties everything together.
# It creates instances of all other classes and runs the main menu loop.

class BookingSystem:

    def __init__(self):
        # Create instances of all classes
        # Aircraft must be created first as Booking and Miles depend on it
        self.aircraft = Aircraft()
        self.booking  = Booking(self.aircraft)
        self.miles    = Miles(self.aircraft)

    def run(self):
        # Run the main menu loop until the user chooses to exit
        print("\n  Welcome to Apache Airlines Booking System")

        while True:
            print("\n" + "=" * 40)
            print("         MAIN MENU")
            print("=" * 40)
            print("  1. Check seat availability")
            print("  2. Book a seat")
            print("  3. Free a seat")
            print("  4. Show full seat map")
            print("  5. Upgrade seat using miles")
            print("  6. Add miles to your account")
            print("  7. Exit program")
            print("=" * 40)

            choice = input("  Enter your choice (1-7): ")

            if choice == "1":
                self.aircraft.check_seat()
            elif choice == "2":
                self.booking.book_seat()
            elif choice == "3":
                self.booking.free_seat()
            elif choice == "4":
                self.aircraft.show_seat_map()
            elif choice == "5":
                self.miles.upgrade_seat()
            elif choice == "6":
                self.miles.add_miles()
            elif choice == "7":
                print("\n  Thank you for using Apache Airlines. Goodbye!\n")
                break
            else:
                print("  Invalid choice! Please enter a number between 1 and 7.")




