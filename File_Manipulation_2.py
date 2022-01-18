#######################################################################################
#
#   CS programming project #7
#
#       Algorithm
#
#           Function definitions
#           Loop until user wants to exit program, reject incorrect input
#           Select user choice
#               Loop while input incorrect
#               Call relevant functions
#                   Compute data
#                   Display data
#                   prompt to plot data
#
########################################################################################

import pylab as py
import csv

MONTHS = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']


def open_file():
    ''' This function repeatedly prompts the user for a filename until the file is
opened successfully. '''

    file_valid = False

    file_name = input("Enter filename: ")

    while file_valid == False:

        try:
            with open(file_name, 'r') as file:
                file_valid = True
                file_name = open(file_name, 'r')
        except FileNotFoundError:
            print("\nFile is not found! Please Try Again!")
            file_valid = False
            file_name = input("Enter filename: ")

    return file_name


def is_numerical(item):
    ''' Checks if number is numerical '''

    try:
        float(item)
        return True
    except:
        return False


def read_file(fp):
    ''' This function read a file pointer and returns a sorted list of tuples. '''

    data = []

    with fp as file:

        reader = csv.reader(file)

        # Skip header line
        next(reader, None)

        for line in reader:

            # Extract data
            year = line[2]
            month = line[3]
            magnitude = line[9]
            location = line[19]
            latitude = line[20]
            longitude = line[21]
            deaths = line[23]
            missing = line[25]
            injuries = line[27]
            damages = line[29]

            if deaths == '':
                deaths = 0
            if missing == '':
                missing = 0
            if injuries == '':
                injuries = 0
            if damages == '':
                damages = 0

            # Check if data is numerical
            if is_numerical(year) and is_numerical(month) and is_numerical(magnitude) and is_numerical(latitude) \
                and is_numerical(deaths) and is_numerical(missing) and is_numerical(injuries) \
                    and is_numerical(damages) and is_numerical(longitude):

                # Convert data to correct data types
                year = int(year)
                month = int(month)
                magnitude = float(magnitude)
                location = location
                latitude = float(latitude)
                longitude = float(longitude)
                deaths = int(deaths)
                missing = int(missing)
                injuries = int(injuries)
                damages = float(damages)

                tup = (year, month, magnitude, location, latitude, longitude, \
                       deaths, missing, injuries, damages)

                data.append(tup)

            else:
                continue

    # Sort data
    data.sort()

    return data


def get_damage_data(data, year):
    '''' This function iterates through the list of earthquake tuples
and returns a list of the earthquakes that occurred in the given year. '''

    earthquakes_in_year = []

    for line in data:

        if line[0] == int(year):

            # Extract data
            month = line[1]
            location = line[3]
            location = location[:40]
            deaths = line[6]
            missing = line[7]
            injuries = line[8]
            damages = line[9]

            # Generate tuple
            tup = (month, location, deaths, missing, injuries, damages)

            earthquakes_in_year.append(tup)

        else:
            continue

    return earthquakes_in_year


def get_quake_data(data, year):
    ''' This function iterates through the list of earthquake tuples
and returns a list of the month, magnitude, location and coordinates from each
earthquake that occurred in the given year. '''

    earthquakes_in_year = []

    for line in data:

        if line[0] == int(year):

            # Extract data
            month = line[1]
            magnitude = line[2]
            location = line[3]
            latitude = line[4]
            longitude = line[5]

            # Generate tuple
            tup = (month, magnitude, location, latitude, longitude)

            earthquakes_in_year.append(tup)

        else:
            continue

    return earthquakes_in_year


def summary_statistics(data, year_start, year_end):
    ''' This function returns a list of three
lists: total number of earthquakes, the damage costs caused by an earthquake, and the total casualties '''

    # Initialization
    year_start = int(year_start)
    year_end = int(year_end)
    summary = []
    earthquake_count_by_year = []
    total_damages_by_year = []
    casualties_by_year = []
    specified_data =[]
    earthquake_count = 0
    total_damages = 0
    total_deaths = 0
    total_missing = 0
    total_injured = 0
    current_year = int(year_start)
    i = 0
    j = 0

    if year_end >= year_start:

        check_year = year_start
        year_range = year_end - year_start
        list_of_years = []

        for line in data:
            list_of_years.append(line[0])

        for i in range(year_range):
            if check_year not in list_of_years:
                earthquake_count_by_year.append((check_year, 0))
                check_year += 1

        print(summary)

        if year_start not in list_of_years:
            current_year = data[0][0]
            j = 0
            pass
        else:
            for line in data:
                if line[0] == year_start:
                    break
                j += 1

        # Find starting index
        '''for line in data:
            if line[0] == year_start:
                break
            j += 1'''

        while data[j][0] <= year_end:

            if current_year != data[j][0]:

                # Append data to lists
                earthquake_count_by_year.append((current_year, earthquake_count))
                total_damages_by_year.append((current_year, total_damages))
                casualties_tup = (current_year, (total_deaths, total_missing, total_injured))
                casualties_by_year.append(casualties_tup)

                # Reset data
                earthquake_count = 0
                total_damages = 0
                total_deaths = 0
                total_missing = 0
                total_injured = 0

                # Add data for first change in year
                current_year = data[j][0]
                earthquake_count += 1
                total_damages += data[j][9]
                total_deaths += data[j][6]
                total_missing += data[j][7]
                total_injured += data[j][8]

            else:

                # Add data for current year
                earthquake_count += 1
                total_damages += data[j][9]
                total_deaths += data[j][6]
                total_missing += data[j][7]
                total_injured += data[j][8]

            # Go to next line
            j += 1

            # Exit loop when end of file
            try:
                data[j][0]
                continue
            except IndexError:
                break

        # Append last set of data
        earthquake_count_by_year.append((current_year, earthquake_count))
        total_damages_by_year.append((current_year, total_damages))
        casualties_tup = (current_year, (total_deaths, total_missing, total_injured))
        casualties_by_year.append(casualties_tup)

        # Generate list of list of tuples
        summary.append(earthquake_count_by_year)
        summary.append(total_damages_by_year)
        summary.append(casualties_by_year)

    else:
        return summary

    return summary


def display_damage_data(L, year):
    ''' This function displays the damage costs of each earthquake '''

    # Initialization
    total_deaths = 0
    total_missing = 0
    total_injuries = 0
    total_damage = 0

    print('                                 Earthquake damage costs in {}                                \
           '.format(year))
    print("{:8s}{:40s}{:>12s}{:>12s}{:>12s}{:>14s}".format("Month", "Location", "Deaths", "Missing", "Injuries"\
                                                           , "Damage"))
    print("{:8s}{:40s}{:>12s}{:>12s}{:>12s}{:>14s}".format("", "", "", "", "", "(Millions)"))
    for line in L:

        # Running totals
        total_deaths += line[2]
        total_missing += line[3]
        total_injuries += line[4]
        total_damage += line[5]
        month = MONTHS[line[0] - 1]

        print("{:<8s}{:40s}{:12,d}{:12,d}{:12,d}{:14,.2f}".format(month, line[1], line[2], line[3], line[4], line[5]))
    print()
    print("{:<8s}{:40s}{:12,d}{:12,d}{:12,d}{:14,.2f}".format("Total", "", total_deaths, total_missing, total_injuries\
                                                              , total_damage))

    return ''


def display_quake_data(L, year):
    ''' This function prints the magnitude of each
earthquake and is quite similar to the display_damage_data. '''

    print('       Earthquake magnitudes and locations in {} '.format(year))
    print("{:8s}{:10s}{:40s}".format("Month", "Magnitude", "Location"))
    for line in L:
        month = MONTHS[line[0] - 1]
        print("{:<8s}{:<10.2f}{:40s}".format(month, line[1], line[2]))

    return ''


def display_summary(quakes, costs, casualties):
    ''' This function first prints a table of
damage by year for each year in the year range with a row of totals for the two
data columns. After that, the total casualty data is displayed with a line for deaths, a line for
missing, and a line for injuries. '''

    i = 0
    total_quakes = 0
    total_cost = 0
    total_deaths = 0
    total_missing = 0
    total_injured = 0

    print("\nNumber of earthquakes and costs per year")
    print("{:5s}{:>10s}{:>12s}".format('Year', 'Quakes', 'Cost'))

    for line in quakes:
        i += 1

    for j in range(i):

        if quakes[j][1] == 0:
            print("{:<5d}{:10,d}{:12,.2f}".format(quakes[j][0], 0, 0))

    for k in range(i-j):
        # Running totals
        total_deaths += casualties[k+j][1][0]
        total_missing += casualties[k+j][1][1]
        total_injured += casualties[k+j][1][2]
        total_cost += costs[k+j][1]
        total_quakes += quakes[k+j][1]
        print("{:<5d}{:10,d}{:12,.2f}".format(quakes[k+j][0], quakes[k+j][1], costs[k+j][1]))


    total_casualties = total_injured + total_missing + total_deaths

    print()

    print("{:5s}{:10,d}{:12,.2f}".format('Total', total_quakes, total_cost))

    print()

    print('Total Casualties')
    print("{:10s}{:>10s}{:>11s}".format('Casualties', 'Total', 'Percent'))
    print("{:10s}{:10d}{:10,.2f}%".format('Deaths', total_deaths, total_deaths/total_casualties*100))
    print("{:10s}{:10d}{:10,.2f}%".format('Missing', total_missing, total_missing/total_casualties*100))
    print("{:10s}{:10d}{:10,.2f}%".format('Injured', total_injured, total_injured/total_casualties*100))

    return ''

def plot_intensity_map(year, quake_data):
    '''
        This function plots the map of the earthquake locations for the
        selected year. This function is provided in the skeleton code.

        Parameters:
            year (string): The year key for the data to plot
            size (int): Number of earthquakes that occured in the selected year

            coordinates (list): List of (latitude,longitude) coordinates for
                                the trajectory of each earthquake that occured
                                in the selected year.

        Returns: None
    '''

    # The the RGB list of the background image.
    img = py.imread("world-map.jpg")

    # Set the max values for the latitude and longitude of the map
    max_longitude, max_latitude = 180, 90

    # Set the background image on the plot
    py.imshow(img, extent=[-max_longitude, max_longitude, \
                           -max_latitude, max_latitude])

    # Show the atlantic ocean region
    py.xlim((-max_longitude, max_longitude))
    py.ylim((-max_latitude, max_latitude))

    # build the x,y coordinates map
    lst = list(zip(*quake_data))
    lat, lon, mag = lst[3], lst[4], lst[1]

    area = ([(1.0 * p) ** 2 for p in mag])

    # plot the scatter plot
    scatter = py.scatter(lon, lat, s=area, c=mag, cmap='seismic')
    py.colorbar(scatter)

    # Set the labels and titles of the plot
    py.xlabel("Longitude (degrees)")
    py.ylabel("Latitude (degrees)")
    py.title("Earthquake Magnitude points for {}".format(year))
    py.show()  # show the full map


def plot_bar(L, title, x_label, y_label):
    '''
        This function receives a list of x,y values.

        Parameters
            L (list):
            title (str):
            x_label (str):
            y_label (str):

        Returns
            None
    '''

    # count the earthquakes per month
    total = [0] * 12
    for i in L:
        total[i[0] - 1] += 1

    py.title(title)
    py.xlabel(x_label)
    py.ylabel(y_label)
    py.xticks(range(12), MONTHS)
    py.bar(range(12), total)
    py.show()


def plot_line(L, title, x_label, y_label):
    '''
        This function receives a list of x,y values.

        Parameters
            L (list):
            title (str):
            x_label (str):
            y_label (str):

        Returns
            None
    '''
    res = list(zip(*L))

    py.title(title)
    py.xlabel(x_label)
    py.ylabel(y_label)
    py.xticks(range(len(res[0])), [str(r) for r in res[0]], rotation=90)
    py.plot(range(len(res[0])), res[1], marker="o")

    py.show()


def plot_pie(L, title):
    '''
        This function receives a list of x,y values.

        Parameters
            L (list):
            title (str):

        Returns
            None
    '''
    #            L[2].append((y,(deaths,missing,injured)))
    deaths = sum([t[0] for y, t in L])
    missing = sum([t[1] for y, t in L])
    injured = sum([t[2] for y, t in L])
    total = deaths + missing + injured
    d = deaths / total
    m = missing / total
    i = injured / total
    L = [["deaths", d], ["missing", m], ["injuries", i]]

    res = list(zip(*L))

    py.title(title)
    py.pie(res[1], labels=res[0], autopct='%.1f%%')
    py.show()


def main():
    '''
        This program will show damages caused by an earthquakes in a year.
        Also, it will plot the intensity of all earthquakes observed in a year.

    '''

    MENU = '''\nEarthquake data software

        1) Visualize damage data for a single year
        2) Visualize earthquakes magnitudes for a single year
        3) Visualize number of earthquake and their damages within a range of years
        4) Exit the program '''

        # Enter a command:

    # Get file pointer, generate data list
    fp = open_file()
    data = read_file(fp)

    valid_options = ['1', '2', '3', '4']

    while True:

        print(MENU)
        print()
        command = input('        Enter a command: ')

        if command not in valid_options:
            print("\nOption '{}' is invalid! Please Try Again!".format(command))
        elif command == '1':

            while True:
                print()

                # Check for valid year
                year = input("Enter a year: ")
                for line in data:
                    if year == str(line[0]):
                        year_valid = True
                        break
                    else:
                        year_valid = False
                if year_valid:
                    break
                else:
                    print("\nYear input '{}' is incorrect!".format(year))
                    break
            print()

            if year_valid == False:
                continue
            else:
                damage_data = get_damage_data(data, year)
                display_damage_data(damage_data, year)

                print()
                plot = input("Do you want to plot (y/n)? ")
                if plot.lower() == 'y':
                    plot_bar(damage_data, "Monthly earthquakes in {}".format(year), 'months', 'earthquakes')

        elif command == '2':

            while True:
                print()

                # Check for valid year
                year = input("Enter year: ")
                for line in data:
                    if year == str(line[0]):
                        year_valid = True
                        break
                    else:
                        year_valid = False
                if year_valid:
                    break
                else:
                    print("\nYear input '{}' is incorrect!".format(year))
                    break
            print()

            if year_valid == False:
                continue
            else:

                quake_data = get_quake_data(data, year)
                display_quake_data(quake_data, year)

                print()
                plot = input("Do you want to plot (y/n)? ")
                if plot.lower() == 'y':
                    plot_intensity_map(year, quake_data)

        elif command == '3':

            print()

            year_start = input("Enter start year: ")
            year_end = input("Enter end year: ")

            try:
                int(year_end)
                int(year_start)
                summary = summary_statistics(data, year_start, year_end)
                display_summary(summary[0], summary[1], summary[2])
                print()
                plot = input('Do you want to plot (y/n)? ')
                if plot.lower() == 'y':
                    plot_line(summary[0], 'Total earthquakes between {} and {}'.format(year_start, year_end), \
                              'Year', 'Earthquakes')
                    plot_pie(summary[2], 'Total casualties by earthquakes between {} and {}'.format(year_start\
                                                                                                    , year_end))
                    plot_line(summary[1], \
                              'Total costs caused by earthquakes between {} and {}'.format(year_start, year_end)\
                              , 'Year', 'Costs')

            except:
                if int(year_end) < int(year_start):
                    print("\nYear range [{},{}] is invalid!".format(year_start, year_end))
                    continue
                else:
                    pass

        elif command == '4':

            break

    print("\nThank you for using this program!")


if __name__ == "__main__":
    main()
