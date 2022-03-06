import sys
from pyspark.sql import SparkSession
#feel free to def new functions if you need

def create_dataframe(filepath, format, spark):
    """
    Create a spark df given a filepath and format.

    :param filepath: <str>, the filepath
    :param format: <str>, the file format (e.g. "csv" or "json")
    :param spark: <str> the spark session

    :return: the spark df uploaded
    """

    #add your code here
    spark_df = None #temporary placeholder

    return spark_df


def transform_nhis_data(nhis_df):
    """
    Transform df elements

    :param nhis_df: spark df
    :return: spark df, transformed df
    """

    #add your code here
    transformed_df = None #temporary placeholder
    
    return transformed_df


def calculate_statistics(joined_df):
    """
    Calculate prevalence statistics

    :param joined_df: the joined df

    :return: None
    """

    #add your code here
    pass

def join_data(brfss_df, nhis_df):
    """
    Join dataframes

    :param brfss_df: spark df
    :param nhis_df: spark df after transformation
    :return: the joined df

    """
    #add your code here
    joined_df = None ##temporary placeholder

    return joined_df

if __name__ == '__main__':

    brfss_filename = sys.argv[1]
    nhis_filename = sys.argv[2]
    save_output = sys.argv[3]
    if save_output == "True":
        output_filename = sys.argv[4]
    else:
        output_filename = None
    

    # Start spark session
    spark = SparkSession.builder.getOrCreate()

    # Load dataframes
    brfss_df = create_dataframe(brfss_filename, 'json', spark)
    nhis_df = create_dataframe(nhis_filename, 'csv', spark)
    # Perform mapping on nhis dataframe
    nhis_df = transform_nhis_data(nhis_df)
    # Join brfss and nhis df
    joined_df = join_data(brfss_df, nhis_df)
    # Save
    if save_output == "True":
        joined_df.write.csv(output_filename, mode='overwrite', header=True)
    # Calculate and print statistics
    calculate_statistics(joined_df)
    
    
    # Stop spark session
    spark.stop()

