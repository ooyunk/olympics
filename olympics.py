"""
*******************************************
CS 1026A Fall 2025
Assignment 3: Olympics
Created By: Winnie Zhang
Student ID: zzha2456
Student Number: 251508584
File Created: November 04, 2025
*******************************************
This file is created to store all the functions needed to run in the main.py file.
These functions will read/write to the files; collecting all data from each csv file.
"""

"""
This function takes data from the host.csv file and converts it into a dictionary. 
The keys of the dictionary are the years of the from the file (first column) stored as integers.
The corresponding values is a list containing the host city, host country, and type of olympics (summer/winter).
"""
def load_hosts(filename):
    host_dict = {}

    # try...except block to handle file opening and parsing errors
    try:
        # Alternative file reading logic: line-by-line manual parsing
        with open(filename, "r") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue

                parts = line.split(",") # Manual splitting

                # Check for correct number of parts
                if len(parts) != 4:
                    raise ValueError("Invalid host file format")

                # Extract and strip data fields
                year_str = parts[0].strip()
                city = parts[1].strip()
                country = parts[2].strip()
                games_type = parts[3].strip()

                try:
                    year = int(year_str)
                except ValueError:
                    # Raise for non-integer year
                    raise ValueError("Invalid host file format")

                host_dict[year] = [city, country, games_type]

    except FileNotFoundError:
        raise
    except ValueError:
        raise

    return host_dict

"""
This function takes data from any medalsxxxx.csv file and converts it into a dictionary.
The keys of the dictionary are the countries from the file in the first column. 
The corresponding values is a list containing the country's number of medals, including the total number of medals.
"""
def load_medals(filename):
    medals_dict = {}
    # try...except block to check for the formatting of each file line.
    try:
        with open(filename, "r") as f:
            first = True
            for line in f:
                line = line.strip()
                if line != "":
                    if first: # Manual header skipping
                        first = False
                        continue

                    parts = line.split(",")
                    if len(parts) < 4:
                        raise ValueError("Invalid medals file format")
                    # assigns a variable to each striped part.
                    country = parts[0].strip()
                    gold_str = parts[1].strip()
                    silver_str = parts[2].strip()
                    bronze_str = parts[3].strip()
                    # try..except ensures the medals are integer.
                    try:
                        gold = int(gold_str)
                        silver = int(silver_str)
                        bronze = int(bronze_str)
                    except ValueError:
                        raise ValueError("Invalid medals file format")

                    # Alternative logic for calculating/reading total: check for 5th column
                    if len(parts) == 5:
                        total_str = parts[4].strip()
                        try:
                            total_medals = int(total_str)
                        except ValueError:
                            # Raise if 5th column exists but is not an integer
                            raise ValueError("Invalid medals file format")
                    else:
                        # Calculate total if 5th column is missing or file only has 4 columns
                        total_medals = gold + silver + bronze

                    medals_dict[country] = [gold, silver, bronze, total_medals]

    except FileNotFoundError:
        raise
    except ValueError:
        raise

    return medals_dict

"""
This function checks if there is a medalxxxx.csv file with the given year. 
If there is, it will return the dictionary corresponding to the year.
If not, the function will return None.
"""
def try_load_medals(year):
    # Alternative filename string concatenation
    filename = "medals" + str(year) + ".csv"
    try:
        medals_data = load_medals(filename)
        return medals_data
    except FileNotFoundError:
        return None
    except ValueError:
        return None

"""
This function analyzes the inputted country name and writes the results to a new text file.
"""
def output_country_results(filename, host_dict, country):
    try:
        # Alternative file opening
        with open(filename, "w") as f:
            f.write(country + "\n")
            f.write("\n")

            # stores the data in a list.
            hosted_list = []
            for year in sorted(host_dict.keys()):
                city, host_country, o_type = host_dict[year]
                # Case-insensitive check
                if host_country.lower() == country.lower():
                    hosted_list.append((year, o_type, city))
            # checks if there is olympics hosted in the country.
            if len(hosted_list) == 0:
                f.write("No Olympics hosted in this country.\n")
            else:
                f.write("Olympics hosted in this country:\n")
                # Alternative tab-separated header
                f.write("Year\tType\tCity\n")
                for year, o_type, city in hosted_list:
                    # Alternative tab-separated data line
                    f.write(f"{year}\t{o_type}\t{city}\n")

            f.write("\n")

            # stores the appearance in a list.
            appearances = []
            for year in sorted(host_dict.keys()):
                medals = try_load_medals(year)
                if medals is not None:
                    # Alternative nested loop logic to find the country
                    for c_name, medal_list in medals.items():
                        if c_name.lower() == country.lower():
                            g, s, b, t = medal_list
                            appearances.append((year, g, s, b, t))
                            break # Found the country for this year, move to next year

            if len(appearances) == 0:
                f.write("No Olympic appearances by this country.") # Alternative line
            else:
                f.write("Olympic appearances by this country:\n")
                # Alternative tab-separated header
                f.write("Year\tGold\tSilver\tBronze\tTotal\n")

                # Alternative logic to suppress final newline
                for i, (year, g, s, b, t) in enumerate(appearances):
                    line = f"{year}\t{g}\t{s}\t{b}\t{t}"
                    if i < len(appearances) - 1:
                        f.write(line + "\n")
                    else:
                        f.write(line) # Suppress final newline
    except IOError as e:
        raise IOError(f"Failed to write results to {filename}: {e}")

"""
This function analyzes the inputted year and write the results to a new text file.
"""
def output_year_results(filename, host_dict, year):
    # Alternative logic: Check host dict first, return early if not found
    if year not in host_dict:
        with open(filename, "w") as f:
            f.write(f"No Olympics were held in {year}") # Alternative line
        return

    city, country, olymp_type = host_dict[year]

    try:
        # Alternative file opening
        with open(filename, "w") as f:
            f.write(f"Year: {year}\n")
            f.write(f"Host: {city}, {country}\n")
            f.write(f"Type: {olymp_type}\n\n")

            medals = try_load_medals(year)

            if medals is None:
                f.write(f"No medals data file available for {year}") # Alternative line
                return

            # Alternative Analysis Logic
            # Find maximums
            max_gold = max([v[0] for v in medals.values()])
            max_silver = max([v[1] for v in medals.values()])
            max_bronze = max([v[2] for v in medals.values()])
            max_total = max([v[3] for v in medals.values()])

            # Find all tying countries
            gold_countries = [c for c, v in medals.items() if v[0] == max_gold]
            silver_countries = [c for c, v in medals.items() if v[1] == max_silver]
            bronze_countries = [c for c, v in medals.items() if v[2] == max_bronze]
            total_countries = [c for c, v in medals.items() if v[3] == max_total]

            # Write results, suppressing final newline
            f.write(f"Most gold medals: {max_gold} by {' and '.join(gold_countries)}\n")
            f.write(f"Most silver medals: {max_silver} by {' and '.join(silver_countries)}\n")
            f.write(f"Most bronze medals: {max_bronze} by {' and '.join(bronze_countries)}\n")
            f.write(f"Most total medals: {max_total} by {' and '.join(total_countries)}") # Suppress final newline

    except IOError as e:
        raise IOError(f"Failed to write results to {filename}: {e}")