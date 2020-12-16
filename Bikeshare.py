import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def check(input_str, input_type):
    while True:
        input_r = input(input_str).lower()
        try:
            if input_r in ['chicago', 'new york city', 'washington'] and input_type == 1:
                break
            elif input_r in ['january', 'february', 'march', 'april', 'may', 'june', 'all'] and input_type == 2:
                break
            elif input_r in ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all'] and input_type == 3:
                break
            else:
                if input_type == 1 :
                    print('Please Enter one of the three cities (chicago, new york city, washington)')
                if input_type == 2 :
                    print('Please note that you should months within the first six months of the year! or just Enter (all)')    
                if input_type == 3 :
                    print('Please Enter a valid day or just Enter (all)')
        except ValueError:
            print('Please try another input')   
    return input_r         

def inputs() :
    city = check('Enter city name (chicago, new york city, washington): ', 1)
    month = check('Enter month or just type "all" :', 2)
    day = check('Enter day or just type  "all" :', 3)
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
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def time_s(df):
    print("most common month",df['month'].mode()[0])
    print("most common day",df['day_of_week'].mode()[0])
    print("most common hour",df['hour'].mode()[0])
def station(df):
    print("most common start station", df['Start Station'].mode()[0])
    print("most common end station", df['End Station'].mode()[0])
    start_end = df.groupby(['Start Station','End Station'])
    print("most common trip from start to end", start_end.size().sort_values(ascending = False).head(1))
def trip_time(df):   
    print("total travel time in seconds :",df['Trip Duration'].sum())
    print("average travel time in seconds :",df['Trip Duration'].mean())
def user(df, city):
    print("count of each user type :", df['User Type'].value_counts())
    if city != 'washington' :
        print("gender :", df['Gender'].value_counts())
        print("the most common year of birth :", int(df['Birth Year'].mode()[0]))
        print("the most recent year of birth :", int(df['Birth Year'].max()))
        print("the earliest year of birth :", int(df['Birth Year'].min()))

def main():
    while True:
        city, month, day = inputs()    
        df = load_data(city, month, day)
        time_s(df)
        station(df)
        trip_time(df)
        user(df, city)
        restart = input('do you want to give it another try ? y/n')
        if restart != 'y':
            break
if __name__ == "__main__":
    main()



