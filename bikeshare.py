import time
import pandas as pd
import numpy as np

CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York': 'new_york_city.csv',
              'Washington': 'washington.csv' }

def get_filters():

    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\n Hello! Let\'s explore some US bikeshare data!\n')


    cities = ["Chicago", "New York", "Washington"]
    months = ["January", "February", "March", "April", "May", "June", "All"]
    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday", "All"]

    # TO DO: get user input for city (Chicago, New York, Washington). HINT: Use a while loop to handle invalid inputs

    while True:
        city = input(" Would you like to see data for Chicago, New York or Washington : ").title()
        city = (' '.join(city.split()))
        if city in cities:
            print(" You requsted data for {} city\n".format(city))
            break
        else:
            print("\n You entered wrong city {} !!! please RE-NETER".format(city))

    # TO DO: get user input for month (All, January, February, ... , June)

    while True:
        month = input(" Which Month January, February, March, April, May, June or All : ").title()
        if month in months:
            print(" You requsted data for {} month\n".format(month))
            break
        else:
            print("\n You entered wrong {} month !!! please RE-ENTER".format(month))

    # TO DO: get user input for day of week (All, Monday, Tuesday, ... Sunday)

    while True:
        day = input("\n Enter a day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or All : ").title()

        if day in days_of_week:
            print(" You requested data for {} day.\n".format(day))
            break
        else:
            print("\n you entered wrong {} day !!!  please RE-ENTER\n".format(day))

    #print(city, month, day)
    print('-'*80)
    return city, month, day

def load_data(city, month, day):

    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    cities = ["Chicago", "New York", "Washington"]
    months = ["January", "February", "March", "April", "May", "June"]
    days_of_week = ["Monday", "Tueday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    # load data file into a dataframe for city

    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime to find data by month day_of_week

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month from Start Time to create new columns

    df['month'] = df['Start Time'].dt.month

    # Extract day_of_week from Start TIme to create new column day_fo_week

    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # Extract hour of the day to creat new column hour

    df['Hour'] = df['Start Time'].dt.hour

    # filter by month if applicable

    if month != 'All':

        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'All':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    months = ["January", "February", "March", "April", "May", "June"]
    print('\n * * * Calculating The Most Frequent Times of Travel... * * * \n')
    start_time = time.time()

    # TO DO: display the most common month
    most_common_month = df['month'].value_counts().idxmax(skipna=True)
    most_common_month_count = df['month'].value_counts()

    print('\n The most common month {} and count is {}.'.format(months[most_common_month-1], most_common_month_count[most_common_month]))

    # TO DO: display the most common day of week

    most_common_week = df['day_of_week'].value_counts().idxmax(skipna=True)
    print("\n The most common day of week is {}.".format(most_common_week))
    # TO DO: display the most common start hour
    most_common_hour = df['Hour'].value_counts().idxmax(skipna=True)
    print("\n The most common hour is {}.".format(most_common_hour))

    print("\n Time took to run query is %s seconds." % (time.time() - start_time))
    print()
    print('-'*80)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\n* * * Calculating The Most Popular Stations and Trip... * * *\n')

    start_time = time.time()

    # TO DO: display most commonly used start station

    Start_Station = df.groupby('Start Station').size().sort_values(ascending=False).nlargest(1).reset_index(name="count")
    for index, row in Start_Station.iterrows():
        print("\n Most commonly used Start station is {} & no of times used  {}".format(row['Start Station'], row['count']))

    # TO DO: display most commonly used end station
    End_Station = df.groupby('End Station').size().sort_values(ascending=False).nlargest(1).reset_index(name="count")
    for index, row in End_Station.iterrows():
        print("\n Most commonly used End station is {} & no of times used  {}".format(row['End Station'], row['count']))

        # TO DO: display most frequent combination of start station and end station trip
    df['routes'] = df['Start Station']+ " " + df['End Station']
    Combination = df.groupby('routes').size().sort_values(ascending=False).nlargest(1).reset_index(name="count")
    for index, row in Combination.iterrows():
        print("\n Most combination of Start and End station {} & no of times used  {}".format(row['routes'], row['count']))

    print("\n This took %s seconds." % (time.time() - start_time))
    print()
    print('-'*80)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\n* * * Calculating Trip Duration...* * *\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print(" Total travel time {} seconds".format(total_travel_time))

    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print("\n Mean travel time  {} seconds".format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print()
    print('-'*80)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\n* * * Calculating User Stats...* * * \n')
    start_time = time.time()

    # TO DO: Display counts of user types

    usertypes = df.groupby('User Type').size().reset_index(name="count")
    for index, row in usertypes.iterrows():
        print(" User Type {} are {}\n".format(row['User Type'], row['count']))

    # TO DO: Display counts of gender

    try:
        #user_gender = df['Gender'].value_counts()
        #print("\nCount Gender \n", user_gender)
        gender = df.groupby('Gender').size().reset_index(name="count")
        for index, row in gender.iterrows():
            print("\n Gender Type {} are {}".format(row['Gender'], row['count']))
    except:
        print("\n There is no Gender column information Washington.")

    # TO DO: Display earliest, most recent, and most common year of birth
    #df.groupby['Year'].

    try:
        earliestyear = int(min(df['Birth Year']))
        print("\n Earliest Year {}.\n".format(earliestyear))

        recentyear = int(max(df['Birth Year']))
        print(" Recent Year {}.\n".format(recentyear))

        mostcommonyear = int(df['Birth Year'].mode())
        print(" Most Common Year {}.\n".format(mostcommonyear))
    except:
        print("\n There is no Birth year for Washington.")

    print("\n This took %s seconds." % (time.time() - start_time))
    print()
    print('-'*80)

def display_data(df):
    print('\n* * * Displaying Raw Data ...* * * \n')
    n = 0
    choice = input("Do you want view data --  yes or no ! - ").lower()
    while True:
        if (choice == 'yes'):
            print(df.loc[n:n+4])
            n+=5
            choice = input("Want to view more data --  yes or no ! - ").lower()
            if (choice == 'yes'):
                continue
        elif(choice == 'no'):
            break
        else:
            print("Invalid input {} .".format(choice))
            choice = input("Enter Valid yes or no :- ").lower()
            continue

    print()
    print('-'*80)

#  Here is the main program
def main():
    while True:
        print()
        city, month, day = get_filters()
        print("In main {}, {}, {}".format(city, month, day))
        df = load_data(city, month, day)
        #print("In main")
        #print(df.head())
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()
