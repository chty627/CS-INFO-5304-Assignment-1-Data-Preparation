import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when
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
    spark_df = spark.read.load(filepath, format=format,header="true" )
    return spark_df



def transform_nhis_data(nhis_df):
    """
    Transform df elements

    :param nhis_df: spark df
    :return: spark df, transformed df
    """

    #add your code here
    
    df = nhis_df
    # change name for 3 similar properties
    # SEX,MRACBPI2,HISPAN_I,AGE_P,DIBEV1
    df = df.withColumnRenamed("MRACBPI2","_IMPRACE").withColumnRenamed("AGE_P","_AGEG5YR")
    df = df.withColumn("_IMPRACE", when(df._IMPRACE == 3 , 4) \
        .when( (df._IMPRACE == 6) | (df._IMPRACE == 7) | (df._IMPRACE == 12) , 3) \
        .when( (df._IMPRACE == 16) | (df._IMPRACE == 17) , 6) \
        .when( (df.HISPAN_I != 12) , 5) \
        .otherwise(df._IMPRACE))
    df = df.withColumn("_AGEG5YR", when( (df._AGEG5YR >= 18) & (df._AGEG5YR <= 24), 1 ) \
        .when( (df._AGEG5YR <= 29), 2 ) \
        .when( (df._AGEG5YR <= 34), 3 ) \
        .when( (df._AGEG5YR <= 39), 4 ) \
        .when( (df._AGEG5YR <= 44), 5 ) \
        .when( (df._AGEG5YR <= 49), 6 ) \
        .when( (df._AGEG5YR <= 54), 7 ) \
        .when( (df._AGEG5YR <= 59), 8 ) \
        .when( (df._AGEG5YR <= 64), 9 ) \
        .when( (df._AGEG5YR <= 69), 10 ) \
        .when( (df._AGEG5YR <= 74), 11 ) \
        .when( (df._AGEG5YR <= 79), 12 ) \
        .when( (df._AGEG5YR <= 99), 13 ) \
        .when( (df._AGEG5YR.isNotNull()), 14 ) \
        .otherwise(df._AGEG5YR))
    transformed_df = df.drop("HISPAN_I")
    return transformed_df


def calculate_statistics(joined_df):
    """
    Calculate prevalence statistics

    :param joined_df: the joined df

    :return: None
    """

    #add your code here
    # Race and ethnic background 
    # Gender 
    # BRFSS categorical age
    # SEX,_LLCPWT,_AGEG5YR,_IMPRACE, DIBEV1
    df = joined_df
    
    with open('output.txt', 'w') as f:
        # Race
        races = {1 : "White, Non-Hispanic", 2 : "Black, Non-Hispanic", 3 : "Asian, Non-Hispanic",
                4 : "American Indian/Alaskan Native, Non-Hispanic", 5 : "Hispanic", 6 : "Other race, Non-Hispanic"}
        print("Prevalance in Race and ethnic background", file = f)
        for key, value in races.items():
            prevalance = df.filter((df._IMPRACE == key) & (df.DIBEV1 == 1)).count() / df.filter(df._IMPRACE == key).count() 
            print(value + " : " + str(prevalance), file = f)

        # Gender
        male = df.filter((df.SEX == 1) & (df.DIBEV1 == 1)).count() / df.filter(df.SEX == 1).count()  
        female = df.filter((df.SEX == 2) & (df.DIBEV1 == 1)).count() / df.filter(df.SEX == 2).count() 
        print("\nPrevalance in Gender:", file = f)
        print("Male: ", male , file = f)
        print("Female: ", female, file = f)
        
        # BRFSS categorical age
        ages = {1:"Age 18 to 24",2:"Age 25 to 29",3:"Age 30 to 34",4:"Age 35 to 39",5:"Age 40 to 44",
                6:"Age 45 to 49",7:"Age 50 to 54",8:"Age 55 to 59",9:"Age 60 to 64",10:"Age 65 to 69",
                11:"Age 70 to 74",12:"Age 75 to 79",13:"Age 80 or older"}
        print("\nPrevalance in BRFSS categorical age", file = f)
        for category, title in ages.items():
            prevalance = df.filter((df._AGEG5YR == category) & (df.DIBEV1 == 1)).count() / df.filter(df._AGEG5YR == category).count() 
            print(title, " : ", prevalance, file = f)
            
    return 
    

def join_data(brfss_df, nhis_df):
    """
    Join dataframes

    :param brfss_df: spark df
    :param nhis_df: spark df after transformation
    :return: the joined df

    """
    #add your code here
    # SEX,_LLCPWT,_AGEG5YR,_IMPRACE, DIBEV1
    # SEX,MRACBPI2,HISPAN_I,AGE_P,DIBEV1
    cond = [brfss_df.SEX == nhis_df.SEX, brfss_df._AGEG5YR == nhis_df._AGEG5YR, brfss_df._IMPRACE == nhis_df._IMPRACE ]
    joined_df = brfss_df.join(nhis_df, cond).select(brfss_df.SEX, brfss_df._LLCPWT, brfss_df._AGEG5YR, brfss_df._IMPRACE, nhis_df.DIBEV1)
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
    # # Perform mapping on nhis dataframe
    nhis_df = transform_nhis_data(nhis_df)
    # # Join brfss and nhis df
    joined_df = join_data(brfss_df, nhis_df)
    # Save
    if save_output == "True":
        joined_df.write.csv(output_filename, mode='overwrite', header=True)
    # # Calculate and print statistics
    calculate_statistics(joined_df)
    
    
    # Stop spark session
    spark.stop()

