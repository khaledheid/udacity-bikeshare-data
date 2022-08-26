import time
import pandas as pd
from datetime import timedelta
from calendar import month_name

CITY_DATA = {'chicago': 'chicago.csv',
             'new york': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    month = "All"
    day = "All"
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('Would you like to see data for Chicago, New York, or Washington? ')
    while city.title() not in ['Chicago', 'New York', 'Washington']:
        city = input('Would you like to see data for Chicago, New York, or Washington? ')

    filter_by = input(
        'Would you like to filter the data by month, day, both, or not at all? Type "none" for no time filter. ')
    while filter_by.lower() not in ['month', 'day', 'both', 'none']:
        filter_by = input(
            'Would you like to filter the data by month, day, both, or not at all? Type "none" for no time filter. ')

    if filter_by.lower() in ['month', 'both']:
        # get user input for month (all, january, february, ... , june)
        month = input('Which month? January, February, March, April, May, or June? ').title()
        while month not in ['January', 'February', 'March', 'April', 'May', 'June', 'All']:
            month = input('Which month? January, February, March, April, May, or June? ').title()

    if filter_by.lower() in ['day', 'both']:
        # get user input for day of week (all, monday, tuesday, ... sunday)
        day = input('Which day? Please type a day Mo, Tu, We, Th, Fr, Sa, Su. ').title()
        while day not in ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su', 'All']:
            day = input('Which day? Please type a day Mo, Tu, We, Th, Fr, Sa, Su. ').title()

    print('-' * 40)
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

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city.lower()])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df["Start Time"])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df["Start Time"].dt.month
    df['day_of_week'] = df["Start Time"].dt.day_name()
    # df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by both month and day if applicable
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    days = {'Mo': 'Monday', 'Tu': 'Tuesday', 'We': 'Wednesday', 'Fr': 'Friday', 'Sa': 'Saturday', 'Su': 'Sunday'}
    if month in months and day in days:
        month = months.index(month) + 1
        day = days[day]
        df = df[(df["month"] == month) & (df["day_of_week"] == day)]

    # filter by month if applicable
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    if month in months:
        # use the index of the months list to get the corresponding int
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df["month"] == month]

    # filter by day of week if applicable
    days = {'Mo': 'Monday', 'Tu': 'Tuesday', 'We': 'Wednesday', 'Fr': 'Friday', 'Sa': 'Saturday', 'Su': 'Sunday'}
    if day in days:
        # filter by day of week to create the new dataframe
        day = days[day]
        df = df[df["day_of_week"] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    mon_num = df['month'].mode()[0]
    mon_name = month_name[mon_num]
    print('The most common month: ', mon_name, sep='\n')

    # display the most common day of week
    print('\nThe most common day of week: ', df['day_of_week'].mode()[0], sep='\n')

    # display the most common start hour
    print('\nThe most common start hour: ', df['Start Time'].dt.hour.mode()[0], sep='\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('Most commonly used start station:', df['Start Station'].mode()[0], sep='\n')

    # display most commonly used end station
    print('\nMost commonly used end station:', df['End Station'].mode()[0], sep='\n')

    # display most frequent combination of start station and end station trip
    print('\nTop 10 most frequent trip, order by count:',
          df[['Start Station', 'End Station']].value_counts().head(10).to_string(), sep='\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_s = int(df['Trip Duration'].sum())
    total_t = timedelta(seconds=total_s)
    print('Total travel time is', total_t)

    # display mean travel time
    mean_s = int(df['Trip Duration'].mean())
    mean_t = timedelta(seconds=mean_s)
    print('\nMean travel time is', mean_t)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('Counts of user types:', df['User Type'].value_counts().to_string(), sep='\n')

    # Display counts of gender
    try:
        print('\nCounts of gender:', df['Gender'].value_counts().to_string(), sep='\n')
    except KeyError as e:
        print('\n{} data is not available'.format(e))

    # Display earliest, most recent, and most common year of birth
    try:
        print('\nThe earliest year of birth:', df['Birth Year'].min(), sep='\n')
        print('\nThe most recent year of birth:', df['Birth Year'].max(), sep='\n')
        print('\nThe most common year of birth:', df['Birth Year'].mode()[0], sep='\n')
    except KeyError as e:
        print('\n{} data is not available'.format(e))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_data(df):
    df.rename(columns={"Unnamed: 0": ""}, inplace=True)
    row_iterator = df.iterrows()
    view_data = ''
    while view_data.lower() not in ['yes', 'no']:
        view_data = input("Would you like to view individual trip data? Type 'yes' or 'no': ")
        try:
            if view_data.lower() == 'yes':
                for i in range(5):
                    print(next(row_iterator)[1].dropna().to_string())
                    print('-' * 40)
                    view_data = ''
        except StopIteration:
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        trip_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
