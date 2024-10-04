import pandas as pd
from datetime import datetime
import hashlib


def split_series_column(df):
    try:
        new_df = df.copy()
        new_df["REP"] = new_df["SERIE"].str.extract(r'R(\d+)')
        new_df["SERIE"] = new_df["SERIE"].str.extract(r'S(\d+)')

        return new_df
    except Exception as e:
        print(f"Exception: {e}") 


def create_hash_id(row, columns):
    """Create a hash ID for a row based on selected columns."""
    values = [str(row[col]) for col in columns]
    combined = '_'.join(values)
    return hashlib.md5(combined.encode()).hexdigest()[:8]


def add_hash_ids(df, columns_to_hash):
    df["hash_id"] = df.apply(lambda row: create_hash_id(row, columns_to_hash), axis = 1)
    return df



def change_columns_type(df, columns, type_list):
    """
    Change the data types of specified columns in a DataFrame.

    Parameters:
    - df (pd.DataFrame): The input DataFrame.
    - columns (list of str): List of column names to be converted.
    - type_list (list): List of target data types corresponding to each column.

    Returns:
    - pd.DataFrame: DataFrame with updated column data types.

    Raises:
    - ValueError: If the lengths of columns and type_list do not match.
    - KeyError: If any of the specified columns do not exist in the DataFrame.
    - TypeError: If an invalid type is provided in type_list.
    """
    # Check if 'columns' and 'type_list' have the same length
    if len(columns) != len(type_list):
        raise ValueError("The length of 'columns' and 'type_list' must be the same.")

    # Check if all specified columns exist in the DataFrame
    missing_columns = [col for col in columns if col not in df.columns]
    if missing_columns:
        raise KeyError(f"The following columns are not in the DataFrame: {missing_columns}")

    # Create a copy to avoid modifying the original DataFrame
    df_converted = df.copy()

    # Iterate over columns and their target types
    for col, target_type in zip(columns, type_list):
        try:
            # Handle specific type conversions if necessary
            if target_type == 'category':
                df_converted[col] = df_converted[col].astype('category')
            elif target_type == 'datetime':
                df_converted[col] = pd.to_datetime(df_converted[col], errors='coerce')
            elif target_type == 'numeric':
                df_converted[col] = pd.to_numeric(df_converted[col], errors='coerce')
            else:
                # For standard types like 'int', 'float', 'str', etc.
                df_converted[col] = df_converted[col].astype(target_type)
        except ValueError as ve:
            print(f"ValueError: Cannot convert column '{col}' to {target_type}. {ve}")
        except TypeError as te:
            print(f"TypeError: Invalid type specified for column '{col}'. {te}")
        except Exception as e:
            print(f"An unexpected error occurred while converting column '{col}': {e}")

    return df_converted



def add_timestamps(df):
    """
    Adds a 'Timestamp' column to the DataFrame with the current datetime in 'dd-mm-YYYY HH:mm' format.

    Parameters:
    - df (pd.DataFrame): The input DataFrame.

    Returns:
    - pd.DataFrame: DataFrame with the new 'Timestamp' column added.

    Raises:
    - TypeError: If 'df' is not a pandas DataFrame.
    - ValueError: If the DataFrame is empty.
    """
    # Validate input type
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame.")

    # Check if DataFrame is empty
    if df.empty:
        raise ValueError("Input DataFrame is empty. Cannot add timestamps to an empty DataFrame.")

    # Create a copy to avoid modifying the original DataFrame
    df_converted = df.copy()

    # Get current datetime formatted as 'dd-mm-YYYY HH:mm'
    current_datetime = datetime.now().strftime('%d-%m-%Y %H:%M')

    # Add 'Timestamp' column
    df_converted['Timestamp'] = current_datetime

    return df_converted




def reorder_columns(df):
    """
    Reorder columns in the specified sequence.
    
    Args:
        df (pd.DataFrame): Input DataFrame with all required columns
        
    Returns:
        pd.DataFrame: DataFrame with reordered columns
    """
    # Define the desired column order
    column_order = [
        'Timestamp',
        'SERIE',
        'REP',
        'KG',
        'D',
        'VM',
        'VMP',
        'RM',
        'P(W)',
        'Perfil',
        'Ejer.',
        'Atleta',
        'Ecuacion',
        'hash_id'
    ]
    
    # Verify all columns exist
    missing_cols = [col for col in column_order if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing columns in DataFrame: {missing_cols}")
    
    # Reorder columns
    df_reordered = df[column_order]
    
    return df_reordered



def preprocess_adr_data(new_data):
    new_data_copy = new_data.copy()
    
    new_data_copy = new_data.drop(columns = "R")
    new_data_copy = split_series_column(new_data_copy)
    
    
    columns_to_hash = ['SERIE', 'REP', 'KG', 'D', 'VM', 'VMP', 'RM', 'P(W)', 'Perfil', 'Ejer.', 'Atleta', 'Ecuacion']

    new_data_copy = add_hash_ids(new_data_copy, columns_to_hash)


    
        # List of columns to change
    columns = ['SERIE', 'REP', 'KG', 'D', 'VM', 'VMP', 'RM', 'P(W)']
    
    # Corresponding list of target types
    type_list = ['int', 'int', 'float', 'float', 'float', 'float', 'float', 'float']
    
    new_data_copy = change_columns_type(new_data_copy, columns, type_list)

    new_data_copy = add_timestamps(new_data_copy)

    new_data_copy = reorder_columns(new_data_copy)

    return new_data_copy






def filter_df_based_on_hash(old_df,new_df):
    try:
        existing_hashes = set(old_df['hash_id'])
    
        # Define the conditions
        new_series_condition = ~new_df['hash_id'].isin(existing_hashes)
        new_series_df = new_df[new_series_condition]
    
        return new_series_df

    except Exception as e:
        print(f'Exception: {e}')
