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

