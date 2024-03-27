'''
    Contains some functions to preprocess the data used in the visualisation.
'''
import pandas as pd


def convert_dates(dataframe):
    '''
        Converts the dates in the dataframe to datetime objects.

        Args:
            dataframe: The dataframe to process
        Returns:
            The processed dataframe with datetime-formatted dates.
    '''
    # TODO : Convert dates
    
    # Convert the 'Date_Plantation' column to datetime format
    dataframe['Date_Plantation'] = pd.to_datetime(dataframe['Date_Plantation'])
    
    return dataframe


def filter_years(dataframe, start, end):
    '''
        Filters the elements of the dataframe by date, making sure
        they fall in the desired range.

        Args:
            dataframe: The dataframe to process
            start: The starting year (inclusive)
            end: The ending year (inclusive)
        Returns:
            The dataframe filtered by date.
    '''
    # TODO : Filter by dates
    
    dataframe = dataframe.loc[(dataframe['Date_Plantation'].dt.year >= start) & (dataframe['Date_Plantation'].dt.year <= end)]
    
    return dataframe


def summarize_yearly_counts(dataframe):
    '''
        Groups the data by neighborhood and year,
        summing the number of trees planted in each neighborhood
        each year.

        Args:
            dataframe: The dataframe to process
        Returns:
            The processed dataframe with column 'Counts'
            containing the counts of planted
            trees for each neighborhood each year.
    '''
    # TODO : Summarize df
    
    grouped_data = dataframe.groupby(['Arrond', 'Arrond_Nom', dataframe['Date_Plantation'].dt.year]).size().reset_index(name='Counts')
    
    return grouped_data


def restructure_df(yearly_df):
    '''
        Restructures the dataframe into a format easier
        to be displayed as a heatmap.

        The resulting dataframe should have as index
        the names of the neighborhoods, while the columns
        should be each considered year. The values
        in each cell represent the number of trees
        planted by the given neighborhood the given year.

        Any empty cells are filled with zeros.

        Args:
            yearly_df: The dataframe to process
        Returns:
            The restructured dataframe
    '''
    # TODO : Restructure df and fill empty cells with 0
    
    restructured_df = yearly_df.pivot_table(index='Arrond_Nom', columns='Date_Plantation', values='Counts', fill_value=0)

    return restructured_df


def get_daily_info(dataframe, arrond, year):
    '''
        From the given dataframe, gets
        the daily amount of planted trees
        in the given neighborhood and year.

        Args:
            dataframe: The dataframe to process
            arrond: The desired neighborhood
            year: The desired year
        Returns:
            The daily tree count data for that
            neighborhood and year.
    '''
    # TODO : Get daily tree count data and return
    
    # Filter dataframe for the given neighborhood and year
    filtered_data = dataframe[(dataframe['Arrond_Nom'] == arrond) & (dataframe['Date_Plantation'].dt.year == year)]

    # Group filtered data by date of plantation and aggregate counts
    daily_info = filtered_data.groupby(filtered_data['Date_Plantation']).size()

    # Find indices where counts are non-zero
    non_zero_indices = daily_info[daily_info != 0].index

    # Create a new date range based on non-zero indices
    full_date_range = pd.date_range(start=non_zero_indices.min(), end=non_zero_indices.max(), freq='D')

    # Reindex the daily_info Series with the new date range
    daily_info = daily_info.reindex(full_date_range, fill_value=0).reset_index()

    # Rename the columns as requested
    daily_info.columns = ['Date_Plantation', 'Daily_Counts']
    
    return daily_info
