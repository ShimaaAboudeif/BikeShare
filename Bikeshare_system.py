import time
import pandas as pd
import numpy as np
import calendar

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
months = ['january', 'february', 'march', 'april', 'may', 'june']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    
    """getting the user inputs and checking if the inputs are within the required values"""
    
    city=input("Enter the city u wish to get the data from:(Chicago,New York city or Washington):").lower()
    
    while city not in CITY_DATA:
        city=input("please check the spelling and re-enter the city name: ").lower() 

    # Get user input for month (all, january, february, ... , june)
    month=input('Enter a month name (eg: January, February, ... , June) or enter "all" if u don\'t wish this filter to apply: ').lower()
    while not(month =='all' or month in months):
        month=input("kindly check the spelling and that the months range from January to June then re-enter the month name: ").lower()
    # Get user input for day of week (all, monday, tuesday, ... sunday)
    
    day = input("Enter the day of the week (eg: Monday, Tuesday,...Sunday) or enter 'all' if u don't wish this filter to apply: ").lower()
    while not( day=='all' or  day.title() in calendar.day_name):
        day=input("kindly check the spelling and re-enter the day name: ").lower()
    print('-'*40)
          
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
    df = pd.read_csv(CITY_DATA[city])
    
    df['Start Time'] =pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['weekday'] = df['Start Time'].dt.weekday_name
    
    if month != 'all':
       
        month_index = months.index(month) + 1
        df = df[df['month'] == month_index]
        
    if day != 'all':
        df= df[df['weekday'] == day.title()]
        
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    # Display the most common month
    df['month'] = df['Start Time'].dt.month
    popular_month = df['month'].mode()[0]
    print("The most popular month is: ",popular_month)
    # Display the most common day of week
    df['weekday'] = df['Start Time'].dt.weekday_name
    popular_weekday = df['weekday'].mode()[0]
    print("The most populart day of the week is: ",popular_weekday)
    
    # Display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print("The most popular hour is: ", popular_hour)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print("The most popular start-station is: ",popular_start_station)
    # Display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print("The most popular end-station is: ",popular_end_station)
    # Display most frequent combination of start station and end station trip
    df['start_end_stations'] = df['Start Station']+" & "+df["End Station"]
    popular_start_end_stations= df['start_end_stations'].mode()[0]
    print("The most popular combination of start&end stations: ",popular_start_end_stations)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    travel_total_time=df['Trip Duration'].sum()
    print("The total time travelled (in sec): ",travel_total_time)

    # Display mean travel time
    travel_avg_time=df['Trip Duration'].mean()
    print("The average duration of a trip is:",travel_avg_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)

    # Display counts of gender
    if city=='chicago' or city =='new york city':
        gender_counts = df['Gender'].value_counts()
        print(gender_counts)

        # Display earliest, most recent, and most common year of birth
        earliest=df['Birth Year'].min()
        print("The eraliest year of birth is: ", earliest)
        most_recent=df['Birth Year'].max()
        print("The most recent year of birth is: ", most_recent)
        most_common_birth_year=df['Birth Year'].mode()[0]
        print("The most common year of birth is: ", most_common_birth_year)
    else:
        print("There is no data for gender or date_of_birth for Washington")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    
    
def check_validity(data):
    
    """checks if the user entered a valid input where only on of the two words: 'yes' or 'no' is allowed.
       
       Args:(str) the data input by the user
       """
    
    choice=['yes', 'no']
    while data not in choice:
        data=input('kindly stick to one of the two words only: "yes" or "no": ').lower()
    return data
    

def display_data(df):
    """checks if the user wants to view few lines of the data.
       
       returns: 
       if the user entered 'yes': dispalys the number of rows the user wishes to.
       
    """
    view_data = input("Would you like to view a number of rows of individual trip data? Enter yes or no? ").lower()
    view_display=check_validity(view_data) 
    start_loc = 0
  
        
    while view_display=='yes':
        while True:
            try:
                n=int(input("Please enter the number of rows u want to show: "))
                break
            except:
                print("That's not a valid number")
            
        end_loc = start_loc + n
        
        if end_loc > len(df):
            print("\n the number of rows you asked for is more than what's left to show \n")
            print(df.iloc[start_loc:,:])
            break;
        else:
            print(df.iloc[start_loc:end_loc,:])
            
        start_loc += n
        view_data = input("Do you wish to continue?: ").lower()
        view_display=check_validity(view_data) 
    
    
def main():
    while True:
        city, month, day = get_filters()
        print("The following program shows the information for {}, month(s): {}, day(s): {}".format(city.title(),month.title(),day.title()))
        df = load_data(city, month, day)
        if df.empty:
            print("no data available")
            continue
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        view_data= display_data(df)
        
        restart = input('\nWould you like to restart? Enter yes or no.\n').lower()
        check_validity(restart)
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
