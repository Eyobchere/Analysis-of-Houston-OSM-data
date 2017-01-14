#Function to  convert my sql queries to pandas dDataFrame.
def sql_to_df(sql_query):

    # Use pandas to pass sql query using connection form SQLite3
    df = pd.read_sql(sql_query, con)
    #df.index= False
    # Show the resulting DataFrame
    return df