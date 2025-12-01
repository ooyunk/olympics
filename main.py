"""
*******************************************
CS 1026A Fall 2025
Assignment 3: Olympics
Created By: Winnie Zhang
Student ID: zzha2456
Student Number: 251508584
File Created: November 04, 2025
*******************************************
This file is created to run the Olympic analysis command system.
It handles user input, command parsing, error management, and coordinates
the analysis functions found in olympics.py.
"""

from olympics import *

"""
This function will take the user's input and split into three variables, 
checking for the validity of the command format.
"""
# all raise statements checks for errors.
def parse_command(text, host_dict):
    stripped_text = text.strip()
    parts = stripped_text.split()

    if not parts:
        raise ValueError("Incorrect command parameters")

    command = parts[0].lower()

    # Validate command type (country or year)
    if command not in ["country", "year"]:
        raise ValueError("Unknown command")

    if command == "year":
        # 'year' command must have exactly 3 space sep. parts
        if len(parts) != 3:
            raise ValueError("Incorrect command parameters")

        param = parts[1]
        filename = parts[2]

        if not filename.endswith(".txt"):
            raise ValueError("Invalid filename")

        try:
            year = int(param)
        except ValueError:
            raise ValueError("Incorrect command parameters")

        output_year_results(filename, host_dict, year)

    elif command == "country":
        # Complex parsing logic for country command, requiring exact quote placement
        start_quote = stripped_text.find("'")
        first_space = stripped_text.find(" ")

        # Check if single quote is present and is directly after the first space
        if start_quote == -1 or start_quote != first_space + 1:
            raise ValueError("Incorrect command parameters")

        end_quote = stripped_text.find("'", start_quote + 1)

        if end_quote == -1:
            raise ValueError("Incorrect command parameters")

        country_name = stripped_text[start_quote + 1:end_quote]
        remainder = stripped_text[end_quote + 1:].strip()
        remainder_parts = remainder.split()

        # Check if only the filename remains
        if len(remainder_parts) != 1:
            raise ValueError("Incorrect command parameters")

        filename = remainder_parts[0]

        if not filename.endswith(".txt"):
            raise ValueError("Invalid filename")

        output_country_results(filename, host_dict, country_name)

"""
This function runs the entire system and consistently checks for upcoming errors.
"""
def command_system():
    host_dict = None

    # load host file loop
    while host_dict is None:
        # Alternative prompt
        host_file = input("Enter host data filename: ")
        try:
            host_dict = load_hosts(host_file)
        except FileNotFoundError:
            print("Invalid host filename")
        except: # Catches all non-FileNotFoundError exceptions
            print("Invalid host file format")

    # Command loop
    while True:
        try:
            # Alternative prompt
            command = input("Enter a valid command: ")

            if command.lower() == "quit":
                break

            parse_command(command, host_dict)

        except ValueError as e:
            # Alternative error message formatting
            print(f'"{str(e)}"')
        # Note: No specific IOError or generic Exception catches here

if __name__ == "__main__":
    command_system()